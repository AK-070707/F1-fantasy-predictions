# F1 Optimal Stopping Simulator: Architecture Overview

## Mission Objective
Build a production-level, high-speed F1 race strategy predictive engine in Python. The system utilizes stochastic modeling, vectorization, and Bayesian frameworks to calculate the mathematically optimal pit stop windows under high uncertainty.

## System Architecture

### Phase 1: Data Ingestion & Formatting
*   **Data Source:** FastF1 library. Pulling all sessions (including all historical Sprint Shootouts and Qualifying formats) using lap times and sector-session times.
*   **Timeframe:** 2022-2025 (Ground Effect Regulation Era). 100% Complete.
*   **Storage Architecture:** **Parquet (Columnar Storage)** for RAM efficiency and microsecond read times.
*   **Track Profiles:** Data grouped by track to isolate local variables.

### Phase 2: The Deterministic Baseline (Physics Model)
Calculates the theoretical, unperturbed lap time (\(T_{det}\)).
*   **Equation:** \(T_{det}(n, x) = T_{base} + \alpha(M_{start} - c_f \cdot n) + (\beta_1 x + \beta_2 x^2)\)
*   **Variables:** Base Pace, Fuel Penalty, Tire Degradation.

### Phase 3: The Monte Carlo Engine (Stochastic Chaos)
Simulates 10,000 possible futures simultaneously using vectorized NumPy operations.
*   **Variance Injections:** Driver Error, Traffic/Dirty Air, DRS advantage, Safety Cars (VSC/SC).
*   **Optimization Target:** Expected Points (Utility Theory) using a Risk Multiplier.

### Phase 4: Live Bayesian Inference (Kalman Filter)
Updates tire degradation curves on the fly during a race.
*   **Core Mechanism:** Pure linear algebra Kalman updates.
*   **Dynamic Measurement Noise:** Ignores lap times corrupted by traffic or errors.

### Phase 5: Constructor-Level Optimization (Two-Car Game Theory)
Optimizes strategy at the team level (specifically acting as **McLaren**), maximizing joint expected points of both drivers against grid reactions.
*   **The "Clean Air" Paradox:** Evaluating if the time gained from fresh tires outweighs the aerodynamic penalty of pitting into dirty air/traffic, versus staying out on old tires in clean air.
*   **Recursive Shadow Modeling:** We assume all opponent teams are also running our math to optimize their strategy. 
*   **Computation Depth:** We will limit the depth of sequence look-aheads to prevent state space explosion.

### Phase 6: Final Validation (The 2025 Test)
Backtesting the model tick-by-tick against the 2025 season to verify real-world efficacy.

### Phase 7: Educational Content & Video Production
Translating the extreme mathematics of the simulator into a highly educational, entertaining video that breaks down the concepts (Monte Carlo, Bayesian filters, Game Theory) and critiques McLaren's 2025 "Papaya Rules" strategy.

---

## The Quant Interview Syllabus
I have extracted the detailed mathematical and architectural concepts you must learn into a dedicated study guide. 
Please refer to: **[MATH_AND_CODE_SYLLABUS.md](MATH_AND_CODE_SYLLABUS.md)**

---

## Master Task List
- [/] Implement FastF1 historical data scraper and Parquet pipeline. *(Waiting on 1-hour Ergast API reset)*
- [ ] Build the deterministic lap time mathematical model.
- [ ] Develop the vectorized Monte Carlo simulation engine.
- [ ] Integrate Bayesian Kalman filters for live parameter updating.
- [ ] Construct the multi-agent Game Theory module for Constructor-level strategy.
  - [ ] Implement joint utility function (`Maximize(Points(Driver A) + Points(Driver B))`).
  - [ ] Model the "Clean Air Paradox" (Fresh Tires + Traffic vs Old Tires + Clean Air).
  - [ ] Model the "Sacrificial Undercut" chain reaction.
  - [ ] Implement the "DRS Defense" (rolling roadblock) logic.
  - [ ] Build split-strategy logic for Safety Car hedging.
  - [ ] Add pit-box spacing and double-stack coordination logic.
  - [ ] Implement Qualifying Strategy (Tire Allocation Optimization across Q1/Q2/Q3).
- [ ] Set up the 2025 backtesting framework.
- [ ] Produce the final highly educational video explaining the project's math and McLaren's strategy.
