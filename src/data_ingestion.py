import fastf1
import pandas as pd
import time
from pathlib import Path
from tqdm import tqdm
import warnings

# Suppress SettingWithCopyWarning from Pandas which FastF1 sometimes triggers
warnings.simplefilter(action='ignore', category=FutureWarning)
pd.options.mode.chained_assignment = None

# Enable FastF1 caching
cache_dir = Path("data/cache")
cache_dir.mkdir(parents=True, exist_ok=True)
fastf1.Cache.enable_cache(str(cache_dir))

from fastf1.exceptions import RateLimitExceededError

def main():
    years = [2022, 2023, 2024, 2025]
    target_sessions = ['FP1', 'FP2', 'FP3', 'Sprint Qualifying', 'Sprint', 'Qualifying', 'Race']
    
    for year in years:
        schedule_loaded = False
        while not schedule_loaded:
            try:
                print(f"\nFetching schedule for {year}...")
                schedule = fastf1.get_event_schedule(year)
                schedule_loaded = True
            except RateLimitExceededError:
                print(f"Rate limit hit while fetching schedule for {year}. Sleeping for 60 minutes...")
                time.sleep(3605)
            except Exception as e:
                if '500 calls/h' in str(e):
                    print(f"Rate limit hit. Sleeping for 60 minutes...")
                    time.sleep(3605)
                else:
                    print(f"Could not load schedule for {year}: {e}")
                    break

        if not schedule_loaded:
            continue
            
        # Filter out pre-season testing
        events = schedule[schedule['EventFormat'] != 'testing']
        
        # Loop through races
        for _, event in tqdm(events.iterrows(), total=len(events), desc=f"Year {year}"):
            round_num = event['RoundNumber']
            if pd.isna(round_num) or round_num == 0:
                continue
                
            round_num = int(round_num)
            event_name = event['EventName'].replace(' ', '_').replace('/', '_')
            
            # Create rigid nested directory structure
            base_path = Path(f"data/laps/{year}/Round_{round_num:02d}_{event_name}")
            base_path.mkdir(parents=True, exist_ok=True)
            
            for session_name in target_sessions:
                # Skip fetching if the parquet file already exists (idempotent design)
                file_path = base_path / f"{session_name.replace(' ', '_')}.parquet"
                if file_path.exists():
                    continue
                
                session_downloaded = False
                while not session_downloaded:
                    try:
                        session = fastf1.get_session(year, round_num, session_name)
                        session.load(telemetry=False, weather=True)
                        if session.laps is not None and len(session.laps) > 0:
                            laps_df = session.laps.astype(str).copy()
                            laps_df.to_parquet(file_path, engine='pyarrow')
                        session_downloaded = True
                    except RateLimitExceededError:
                        print(f"\nRate limit hit during {year} {event_name} {session_name}. Sleeping for 60 mins...")
                        time.sleep(3605)
                    except Exception as e:
                        if '500 calls/h' in str(e):
                            print(f"\nRate limit hit. Sleeping for 60 mins...")
                            time.sleep(3605)
                        else:
                            # If it's a different error (e.g., no Sprint on this weekend), just skip and move on
                            session_downloaded = True
                    
                time.sleep(1)
            time.sleep(3)

if __name__ == "__main__":
    main()
