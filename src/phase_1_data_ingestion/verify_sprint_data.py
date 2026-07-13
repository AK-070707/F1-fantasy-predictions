import pandas as pd
from pathlib import Path

def main():
    base_dir = Path("data/laps")
    
    sprint_files = list(base_dir.rglob("Sprint.parquet"))
    
    if not sprint_files:
        print("No Sprint files found yet. Waiting for data ingestion to complete.")
        return
        
    # Grab the first sprint file we find
    sprint_file = sprint_files[0]
    race_file = sprint_file.parent / "Race.parquet"
    
    if not race_file.exists():
        print(f"Found Sprint file at {sprint_file} but no matching Race file yet!")
        return
        
    print(f"--- SPRINT VS RACE SCHEMA VERIFICATION ---")
    print(f"Testing Sprint: {sprint_file}")
    print(f"Testing Race:   {race_file}\n")
    
    sprint_df = pd.read_parquet(sprint_file)
    race_df = pd.read_parquet(race_file)
    
    sprint_cols = set(sprint_df.columns)
    race_cols = set(race_df.columns)
    
    if sprint_cols == race_cols:
        print("✅ SUCCESS: Sprint and Race DataFrames have identical column structures.")
        print(f"Number of columns: {len(sprint_cols)}")
        print(f"Sprint data rows: {len(sprint_df)}")
        print(f"Race data rows: {len(race_df)}")
    else:
        print("❌ ERROR: Column mismatch detected!")
        print("Columns in Sprint but not Race:", sprint_cols - race_cols)
        print("Columns in Race but not Sprint:", race_cols - sprint_cols)

if __name__ == "__main__":
    main()
