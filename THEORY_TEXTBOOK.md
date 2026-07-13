# F1 Strategy Simulator: Theoretical Foundations & Project Script

This document serves as the "human-readable textbook" and the primary script for explaining the project. It breaks down the mathematics, theory, and all finalized decisions made during development, organized chronologically from Phase 1 to Phase 5. This document only contains elements that are 100% committed to the project.

---

## Phase 1: Data Ingestion & Formatting

Before we can simulate the chaos of a real race, we must build the environment using a high-speed, localized data structure.
*   **Data Source:** We use the FastF1 Python library to pull data from the 2022-2024 (Ground Effect Regulation) era. This timeframe ensures our aerodynamic and tire structure priors remain stable. We are currently pulling pure lap times.
*   **Storage Architecture:** We store everything locally using **Parquet (Columnar Storage)**. This allows the engine to bypass slow CSV row-reads and instantly load specific data arrays directly into RAM, maximizing CPU cache efficiency.
*   **API Rate Limiting:** FastF1 hits the Ergast API which has strict rate limits. We do not use complex workarounds; we simply run the scraper in batches and wait out the 1-hour reset.

---

## Phase 2: The Deterministic Physics Model

We must mathematically define a "perfect lap." The deterministic model calculates the theoretical, unperturbed lap time (\(T_{det}\)) for any given lap \(n\) on tire age \(x\).

**The Equation:** 
\[ T_{det}(n, x) = T_{base} + \alpha(M_{start} - c_f \cdot n) + (\beta_1 x + \beta_2 x^2) \]

*   **Base Pace (\(T_{base}\)):** The absolute limit of the car/driver on new tires with qualifying fuel.
*   **The Fuel Penalty:** Modeled as a *linear* time penalty. \(\alpha\) is the track-specific weight penalty (e.g., losing 0.035s per kg of fuel).
*   **Tire Degradation:** Modeled as a *quadratic* equation (a curve). \(\beta_1\) is initial linear wear, and \(\beta_2\) is the exponential drop-off representing the sudden tire "cliff."

---

## Phase 3: The Monte Carlo Engine (Stochastic Chaos)

Real races aren't perfect. We simulate 10,000 alternate realities of the race simultaneously using vectorized matrices, injecting random mathematical "noise" to represent real-world events.

*   **Driver Error:** Modeled using a Gaussian (Normal) bell curve centered around \(T_{det}\).
*   **Traffic & Dirty Air:** Modeled as an asymmetric Exponential distribution. Being stuck behind a slower car can only *lose* you time, never magically make you faster.
*   **Utility Theory (Expected Points):** The engine maximizes *Expected Points*. Finishing P1 (10% chance) and P11 (90% chance) yields more average points than finishing consistently in P8.

---

## Phase 4: Live Bayesian Inference (Kalman Filters)

Pre-race plans rarely survive the first lap. We use a **Kalman Filter** to update our \(\beta\) (tire deg) equations live.

*   **The Bayesian Update:** The filter takes the "Prior" (historical data) and the "Measurement" (live lap times). It calculates a "Gain" (\(K\)) to update the tire model. 
*   **Dynamic Measurement Noise (\(R\)):** If the engine detects the car was stuck in traffic, it intelligently recognizes a "corrupted" lap time, spikes the mathematical noise (\(R\)), and throws the data point away so it doesn't accidentally assume tire degradation is massive.

---

## Phase 5: Constructor-Level Game Theory (Multi-Agent Dynamics)

Strategy optimized for one car in a vacuum fails when opponents react. F1 is a cooperative game played by teams of two. We are specifically building this from the perspective of **McLaren**.

*   **Joint Utility & Nash Equilibrium:** We maximize \(Points(Driver A) + Points(Driver B)\) against the best responses of the grid. This allows the math to justify "sacrificing" one driver if it secures the win for the team.
*   **Core Tactics Modeled:**
    *   *The "Clean Air" Paradox:* The mathematical evaluation of whether the mechanical grip gained from pitting for fresh tires outweighs the aerodynamic penalty of merging into dirty traffic. The engine must often decide that staying out on heavily degraded tires in pure clean air yields a faster overall race time than having brand new tires but being stuck in a DRS train.
    *   *The "Sacrificial" Undercut:* Pitting a trailing driver early to force opponents into a suboptimal response.
    *   *The DRS Defense:* The lead driver slows down to give the defending teammate DRS.
    *   *Split Strategies & Double Stacking.*
*   **Recursive Shadow Modeling:** We assume all opponent teams are also running our math to optimize their strategy. 
*   **State Space Clamping:** Because calculating joint actions against opponent reactions creates massive branching probability trees, we strictly limit the depth of the sequence we look into to prevent the simulation from freezing (state space explosion).
