# Work in Progress: Ideas & Open Questions

This document is your active notepad. It contains work-in-progress ideas, debates, and questions that are **NOT** yet formally committed to the project. Once an idea is refined and decided upon, it will be moved to the Architecture Overview and the Theory Textbook.

---

### 1. Data Granularity for the "Delta Array" (Traffic Mapping)
Currently, the project is committed to pulling full lap times. Do we need to upgrade to pulling **Sector Times** to accurately map where our driver merges into traffic off a pit exit, rather than guessing mid-lap gaps?
*   *Option A (Current Plan):* Lap Times only. Flaw: Pit exits are mid-lap.
*   *Option B (Proposed Idea):* Sector 1, 2, 3 times. Pit exits are in Sector 1.
*   *Option C (Too Heavy):* Full 10Hz Telemetry.

### 2. Weather & Track Evolution
How do we mathematically model track temperature and rain? Do we add a \(\Delta T\) modifier to the tire degradation \(\beta\) coefficients, or do we need completely separate Bayesian profiles for different weather bands?

### 3. The Non-Linear DRS "Wobble" Equation
Currently, the project simply commits to a standard "DRS advantage." However, we are contemplating a specific **Exponential Decay Function** for dirty air that mathematically *inverts* into a lap time advantage at the ~0.5s mark due to slipstream/DRS overpowering cornering loss. We need to figure out how to optimize this specific curve against the historical dataset to find the exact "maximum penalty distance."

### 4. The Compute Tech Stack Accelerator
The project currently assumes standard Python/NumPy execution. We need to evaluate whether to replace NumPy with an accelerator to prevent the simulation from lagging during the complex McLaren Game Theory recursive loops.
*   *NumPy (Current):* CPU-bound, single-threaded.
*   *Numba (JIT Compilation):* Unlocks multi-threading (`prange`), allows fast Python for-loops.
*   *CuPy (GPU/CUDA):* Massive parallelization on thousands of cores, but risks PCIe transfer bottlenecks when moving Parquet data to VRAM.

### 5. Qualifying Strategy & Tire Allocation
Can we extend the Game Theory module to mathematically optimize a driver's Qualifying session? 
*   **The Problem:** Drivers have a limited allocation of Soft tires for the weekend. 
*   **The Trade-off:** Do we burn an extra set of brand new Softs in Q2 to guarantee survival into Q3 (sacrificing our grid potential in Q3 or our race strategy)? Or do we risk running a used set of Softs in Q2, risking elimination (P11), but keeping fresh rubber for the race?
*   **The Math:** We would need to build a predictive model that calculates the "Cut-off Delta" for Q2 based on track evolution, and evaluates the expected utility (points) of starting P9 with old tires vs starting P11 with fresh tires.
