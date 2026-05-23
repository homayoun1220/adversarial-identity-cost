# Adversarial Identity Cost Simulations

A research-oriented simulation framework for evaluating adversarial identity cost under different governance and throughput models.

This repository accompanies a theoretical study on identity-bounded participation systems and adversarial coordination economics.

---

## Overview

The project investigates how adversarial participation cost scales under different governance assumptions.

We compare:

- Parallelizable identity acquisition models
- Throughput-bounded governance systems
- Coordination overhead formulations
- Marginal identity cost growth
- Time-horizon scaling behavior

The experiments numerically validate the theoretical asymptotic properties derived in the paper.

---

## Repository Structure

```text
.
├── experiments/
│   └── simulation.py
│
├── figures/
│   ├── fig_e1_identity_scaling.pdf
│   ├── fig_e2_time_scaling.pdf
│   ├── fig_e3_marginal_cost.pdf
│   ├── fig_e4_coordination.pdf
│   └── fig2_theorem_validation.pdf
│
└── paper/
    ├── document.tex
    ├── document.pdf
    └── references.bib
```

---

## Experiments

### E1 — Identity Scaling

Evaluates adversarial cost growth as the number of identities increases.

### E2 — Time Horizon Scaling

Analyzes cost behavior as governance participation extends over time.

### E3 — Marginal Identity Cost

Measures the incremental cost of adding new adversarial identities.

### E4 — Coordination Robustness

Compares different coordination-overhead models under bounded throughput assumptions.

---

## Running the Simulation

Install dependencies:

```bash
pip install -r requirements.txt
```

Run experiments:

```bash
python experiments/simulation.py
```

Generated figures are saved automatically.

---

## Research Context

This project explores governance systems in which participation cost cannot be perfectly amortized across time windows.

The simulations illustrate the asymptotic distinction between:

- Parallelizable adversarial models
- Throughput-bounded participation systems

---

## Figures

The repository includes generated evaluation figures in:

```text
figures/
```

These figures reproduce the experimental results discussed in the paper.

---

## License

MIT License.
