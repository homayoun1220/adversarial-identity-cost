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
│   ├── simulation.py
│   └── outputs/
│
├── paper/
│   ├── document.tex
│   ├── document.pdf
│   └── references.bib
│
├── README.md
├── requirements.txt
└── .gitignore