# Quant Interview Syllabus: Math & Code to Learn

This document serves as your definitive study guide while the data pipeline downloads and we wait for the next development phase. To pass a Quantitative Researcher (QR) or Quantitative Developer (QD) interview, you must be able to whiteboard and defend these concepts from scratch.

*The AI will write the boilerplate; you must master the math.*

---

## 1. High-Performance Computing & Python (The Code)

You must prove you understand *why* code is fast or slow at the hardware level. Quants care about microseconds.

### Core Concepts to Master:
*   **Vectorization & SIMD:** Understand why `NumPy` is orders of magnitude faster than a Python `for` loop. Learn how Single Instruction, Multiple Data (SIMD) works at the CPU level to execute math on entire arrays simultaneously.
*   **Memory Contiguity & Cache Lines:** Learn the difference between C-contiguous and Fortran-contiguous arrays. Understand why CPU Cache (L1/L2/L3) spatial locality makes `.parquet` (columnar data) infinitely faster for this simulator than `.csv` (row-based data).
*   **Algorithmic Complexity:** Be able to calculate the Big-O time and space complexity for our Monte Carlo matrix operations.

### What to Code Yourself (Practice):
*   Write a pure Python `for` loop to multiply two lists of 10,000 numbers. Then write the `NumPy` equivalent. Use the `timeit` module to prove the speed difference.

---

## 2. Probability & Stochastic Modeling (The Math)

You must understand how to inject realistic chaos into a deterministic model.

### Core Concepts to Master:
*   **Probability Distributions:** You must know the PDF (Probability Density Function) and CDF of these distributions, and exactly *why* we use them:
    *   *Gaussian (Normal):* Used for natural driver pace variance.
    *   *Exponential / Log-Normal:* Used for Traffic and Dirty Air (because lap time can only be *lost*, creating a long right-tail).
    *   *Poisson / Binomial:* Used for discrete, rare events like Safety Cars.
*   **Monte Carlo Convergence:** Understand the Law of Large Numbers. Be able to prove mathematically that the Standard Error of the Mean scales by \(\frac{\sigma}{\sqrt{N}}\) (which is why we need \(N=10,000\) simulations for confidence).

### What to Code Yourself (Practice):
*   Generate 10,000 random variables using `numpy.random.exponential`. Plot them using a histogram to visualize the asymmetric tail.

---

## 3. Linear Algebra & Bayesian Inference (The Math)

This is the hardest and most important section. You must prove you understand dynamic updating.

### Core Concepts to Master:
*   **The Kalman Filter Equations:** You must be able to write these on a whiteboard:
    1.  *State Update Equation:* \(\hat{x}_k = \hat{x}_{k-1} + K_k (z_k - H \hat{x}_{k-1})\)
    2.  *Covariance Update:* \(P_k = (I - K_k H) P_{k-1}\)
*   **The Kalman Gain (\(K\)):** This is the magic ratio. Explain exactly what happens to the math when the measurement uncertainty (\(R\)) spikes (e.g., the driver hits traffic, so we shouldn't trust the lap time). Prove that as \(R \rightarrow \infty\), the Gain \(K \rightarrow 0\), meaning the filter ignores the bad data.
*   **Matrix Multiplication:** Understand dot products, identity matrices, and matrix inversion.

### What to Code Yourself (Practice):
*   Write a 1-dimensional Kalman Filter from scratch in raw Python/NumPy (without using a library) that tracks a noisy sine wave.

---

## 4. Game Theory & Optimization (The Math)

You must prove you understand how to optimize against an opponent who is also optimizing.

### Core Concepts to Master:
*   **Utility Theory:** Understand why maximizing "Expected Points" leads to different decisions than maximizing "Average Finish Position." Learn how asymmetric payoff structures (e.g., 1st place gets 25 pts, 2nd gets 18) dictate risk tolerance (\(\gamma\)).
*   **Nash Equilibriums:** Understand basic 2-player zero-sum and non-zero-sum games (e.g., the undercut vs. overcut dynamic).
*   **State Space Complexity (The Curse of Dimensionality):** Explain why evaluating every possible pit-stop permutation for 20 cars over 50 laps causes the number of states to explode beyond the number of atoms in the universe. Explain "Branch Pruning" (how we cut off mathematical branches that are statistically irrelevant).

---

## 5. Extension Topics (To impress interviewers)

If you want to go above and beyond for a tier-1 firm, look into these concepts that extend our project:

*   **MCMC vs. Kalman:** Be able to explain why we chose Kalman Filters instead of Markov Chain Monte Carlo (MCMC/PyMC). (Answer: MCMC provides better non-linear posteriors, but is far too slow for real-time, microsecond race execution).
*   **Reinforcement Learning (Q-Learning):** Instead of using static probabilities for opponent pit stops, research how a Q-Learning agent could be trained to dynamically mimic Ferrari or Red Bull's pit wall tendencies.
*   **GPU Compute (CUDA/CuPy):** Research how moving our NumPy Monte Carlo matrices from the CPU to the GPU (using CuPy) allows for massive parallelization (e.g., running 1,000,000 futures instead of 10,000).
