# F1 Optimal Stopping Simulator: Architecture Overview

## Mission Objective
Build a production-level, high-speed F1 race strategy predictive engine in Python. The system utilizes stochastic modeling, vectorization, and Bayesian frameworks to calculate the mathematically optimal pit stop windows under high uncertainty.

## Phase 1: Data Ingestion & Formatting
*   **Data Source:** FastF1 library.
*   **Timeframe:** 2022-2024 (Ground Effect Regulation Era) to ensure stable aerodynamic and tire structural priors.
*   **Storage Architecture:** **Parquet (Columnar Storage)**. Parquet replaces row-based CSVs to allow the engine to instantly load specific data arrays (e.g., only lap times) directly into RAM, maximizing CPU Cache efficiency via spatial locality and providing massive file compression.
*   **Track Profiles:** Data is grouped by track to calculate track-specific coefficients (abrasiveness, pit loss time, weight penalty).

## Phase 2: The Deterministic Baseline (Physics Model)
Calculates the theoretical, unperturbed lap time (\(T_{det}\)) for any given lap.
*   **Base Pace (\(T_{base}\)):** The absolute limit of the car/driver on new tires and qualifying fuel. This is a latent variable updated via Exponential Smoothing/Kalman Filtering to track car upgrades across the season.
*   **Fuel Penalty (\(F\)):** A linear time penalty based on weight. Decreases as the race goes on. \(\alpha\) defines the track-specific time penalty per kg.
*   **Tire Degradation (\(D\)):** A non-linear quadratic model (\(D(x) = \beta_1 x + \beta_2 x^2\)) to model the sudden performance "cliff" of aging tires.
*   **Equation:** \(T_{det}(n, x) = T_{base} + \alpha(M_{start} - c_f \cdot n) + (\beta_1 x + \beta_2 x^2)\)

## Phase 3: The Monte Carlo Engine (Stochastic Chaos)
Instead of predicting *the* future, the engine simulates 10,000 *possible* futures simultaneously.
*   **Vectorization (NumPy):** Standard Python loops are bypassed. The simulation runs entirely in RAM using C-level SIMD operations on contiguous memory blocks (10,000 x 50 matrices) for microsecond execution.
*   **Variance Injections:**
    *   *Driver Error:* Modeled as a Normal (Gaussian) distribution around \(T_{det}\).
    *   *Traffic & Dirty Air:* Modeled as an asymmetric (Exponential) distribution. Time can only be lost, not gained.
    *   *Safety Cars (SC/VSC):* Modeled as a Poisson/Binomial discrete probability based on historical track data.
*   **Game Theory (Opponent Modeling):** Opponent pit stops are triggered dynamically in the simulation to discover Nash Equilibriums (e.g., boxing to cover an undercut).
*   **Utility Theory (Optimization):** The engine does not optimize for "Average Finish Position". It optimizes for **Expected Points**, using a Risk Multiplier (\(\gamma\)) to dictate when to take massive gambles from outside the top 10.

## Phase 4: Live Bayesian Inference (Kalman Filter)
Updates the tire degradation curves (\(\beta_1, \beta_2\)) on the fly as live lap times come in.
*   **Prior Generation:** Historical data creates the initial distributions. FP1/FP2 practice data provides the first Bayesian update to create the "Race Start Prior."
*   **Real-Time Kalman Update:** Avoids slow MCMC libraries (PyMC) in favor of pure linear algebra matrix multiplication.
*   **Dynamic Measurement Noise (\(R\)):** The filter intelligently decides whether to trust a live lap time. If telemetry shows the car was in dirty air or the driver made an error, the measurement uncertainty (\(R\)) is spiked, driving the Kalman Gain (\(K\)) to 0, and the engine ignores the corrupted lap.

## Backtesting Strategy (The 2025 Test)
The ultimate proof of the algorithm. The model's memory is frozen at the end of 2024. The 2025 season is fed into the engine tick-by-tick as a "Time Machine" to verify if the engine successfully calls winning strategies against real-world F1 pit walls.

---

## 🚀 Open Questions & Strategic Decisions Moving Forward

As we transition from theory to coding, we need to answer the following architectural questions:

1.  **FastF1 Rate Limiting:** FastF1 hits the Ergast API and F1 live timing. How do we structure our historical data scraper to avoid API rate limits when downloading 3 years of telemetry?
2.  **Telemetry Density:** Do we pull full 10Hz telemetry (throttle, brake, steering) for every lap of every race to calculate the dynamic noise (\(R\)) for the Kalman filter? 10Hz telemetry for 3 years will result in massive datasets. Should we stick to micro-sectors instead?
3.  **Opponent Shadow Modeling:** For Phase 3 Game Theory, do we hardcode historical pit-stop tendencies for specific teams (e.g., "Ferrari pits early 60% of the time"), or do we run a recursive Monte Carlo where the opponents are also running our math? (The latter is computationally heavy).
4.  **Weather Modeling:** How do we ingest and represent track temperature and rain? Do we add a \(\Delta T\) modifier to the \(\beta\) coefficients for track temp, or create entirely separate Bayesian profiles for different weather bands?
5.  **Compute Tech Stack:** We are using Python, NumPy, and Parquet. Should we introduce `Numba` (JIT compilation) or `CuPy` (GPU acceleration via CUDA) for the Monte Carlo matrix calculations to push execution time from milliseconds down to microseconds?
