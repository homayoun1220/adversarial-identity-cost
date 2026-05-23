"""
generate_figures.py
────────────────────────────────────────────────────────────
Generates all figures for:

  "The Geometry of Adversarial Identity Cost:
   Structural Limits of Sybil Resistance in Open Systems"

Output files
────────────
  fig2_theorem_validation.pdf   ← Section VIII  (was already in paper)
  fig_e1_identity_scaling.pdf   ─┐
  fig_e2_time_scaling.pdf        │ Section XI
  fig_e3_marginal_cost.pdf       │ (Simulation Study, added)
  fig_e4_coordination.pdf       ─┘

Usage
────────────────────────────────────────────────────────────
  python generate_figures.py

All PDFs are saved to ./outputs/
────────────────────────────────────────────────────────────
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ─────────────────────────────────────────────
# Output directory
# ─────────────────────────────────────────────
OUT = Path(__file__).parent / "outputs"
OUT.mkdir(parents=True, exist_ok=True)

# ─────────────────────────────────────────────
# Style
# ─────────────────────────────────────────────
plt.rcParams.update({
    "font.family":      "serif",
    "font.size":        11,
    "axes.titlesize":   12,
    "axes.labelsize":   11,
    "legend.fontsize":  9,
    "lines.linewidth":  1.8,
    "figure.dpi":       150,
})

COLOR_PAR = "#2166ac"   # blue  — parallelizable
COLOR_BND = "#d6604d"   # red   — throughput-bounded
COLOR_REF = "#888888"   # gray  — reference line


# ═════════════════════════════════════════════
# Core cost functions
# ═════════════════════════════════════════════

def h_sublinear(s, T):
    """Coordination overhead: O(s+T) = o(sT)  [cloud orchestration baseline]"""
    return s + T

def h_log(s, T):
    """Coordination overhead: s·log(T)"""
    return s * np.log(T + 1)

def h_sqrt(s, T):
    """Coordination overhead: s·√T"""
    return s * np.sqrt(T)

def cost_parallelizable(s, T, r_min=1.0, h=h_sublinear):
    """
    Parallelizable resource.
    Adversary acquires s·r_min once (stock), reuses across all T windows.
    C(s,T) = s·r_min + h(s,T)
    """
    return s * r_min + h(s, T)

def cost_bounded(s, T, r_min=1.0):
    """
    Throughput-bounded resource.
    Each identity pays r_min in every window (flow, non-reusable).
    C(s,T) = s · T · r_min
    """
    return s * T * r_min


# ═════════════════════════════════════════════
# fig2_theorem_validation  — Section VIII
# ═════════════════════════════════════════════

def figure_theorem_validation(r_fixed=500.0, T=100, r_min=1.0):
    """
    Section VIII figure.
    Plots C(s,T) and C(s,T)/sT for s in [1, 10 000] on a log scale.
    r_fixed: one-time stock acquisition cost for the parallelizable case.
    """
    s_vals = np.logspace(0, 4, 500)        # 1 to 10 000

    cp = r_fixed + (s_vals + T)            # stock + coordination (h = s+T)
    cb = s_vals * T * r_min                # throughput-bounded

    s_star = r_fixed / (r_min * T)         # crossover point

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

    # Left — raw cost
    ax = axes[0]
    ax.plot(s_vals, cp, color=COLOR_PAR, label="Parallelizable $C(s,T)$")
    ax.plot(s_vals, cb, color=COLOR_BND, label="Throughput-Bounded $C(s,T)$")
    ax.axvline(s_star, linestyle=":", color=COLOR_REF, alpha=0.8,
               label=fr"Crossover $s^* = {int(s_star)}$")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Sustained Identities $s$")
    ax.set_ylabel("Total Adversarial Cost $C(s,T)$")
    ax.set_title(f"Total Cost vs.\\ Identities  ($T={T}$)")
    ax.legend()

    # Right — normalized ratio
    ax = axes[1]
    ax.plot(s_vals, cp / (s_vals * T), color=COLOR_PAR,
            label=r"Parallelizable $C(s,T)/sT \to 0$")
    ax.plot(s_vals, cb / (s_vals * T), color=COLOR_BND,
            label=r"Bounded $C(s,T)/sT = r_{\min}$")
    ax.axhline(r_min, linestyle="--", color=COLOR_REF, alpha=0.7,
               label=r"$r_{\min} = 1.0$ (Theorem~2 bound)")
    ax.set_xscale("log")
    ax.set_xlabel("Sustained Identities $s$")
    ax.set_ylabel(r"Normalized Cost $C(s,T)\,/\,sT$")
    ax.set_title(f"Normalized Cost Ratio  ($T={T}$)")
    ax.legend()

    fig.tight_layout()
    path = OUT / "fig2_theorem_validation.pdf"
    fig.savefig(path)
    plt.close(fig)
    print(f"[fig2] saved → {path}")


# ═════════════════════════════════════════════
# E1 — Identity Scaling   (Section XI)
# ═════════════════════════════════════════════

def experiment_e1(T=100, r_min=1.0):
    s_vals = np.arange(1, 101)
    cp = np.array([cost_parallelizable(s, T, r_min) for s in s_vals])
    cb = np.array([cost_bounded(s, T, r_min)        for s in s_vals])

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    ax = axes[0]
    ax.plot(s_vals, cp, color=COLOR_PAR, label="Parallelizable")
    ax.plot(s_vals, cb, color=COLOR_BND, label="Throughput-Bounded")
    ax.plot(s_vals, s_vals * T * r_min, "--", color=COLOR_REF,
            alpha=0.5, label="Linear reference $sT$")
    ax.set_xlabel("Number of Identities $s$")
    ax.set_ylabel("$C(s,T)$")
    ax.set_title(f"E1a: Raw Cost  ($T={T}$)")
    ax.legend()

    ax = axes[1]
    ax.plot(s_vals, cp / (s_vals * T), color=COLOR_PAR,
            label=r"Parallelizable $\to 0$")
    ax.plot(s_vals, cb / (s_vals * T), color=COLOR_BND,
            label=r"Bounded $= \Omega(1)$")
    ax.axhline(r_min, linestyle="--", color=COLOR_REF,
               alpha=0.7, label=r"$r_{\min}$ (Theorem~2 bound)")
    ax.set_xlabel("Number of Identities $s$")
    ax.set_ylabel(r"$C(s,T)\,/\,sT$")
    ax.set_title(f"E1b: Normalized Ratio  ($T={T}$)")
    ax.legend()

    fig.tight_layout()
    path = OUT / "fig_e1_identity_scaling.pdf"
    fig.savefig(path)
    plt.close(fig)
    print(f"[E1] saved → {path}")


# ═════════════════════════════════════════════
# E2 — Time Horizon Scaling   (Section XI)
# ═════════════════════════════════════════════

def experiment_e2(s=10, r_min=1.0):
    T_vals = np.arange(1, 201)
    cp = np.array([cost_parallelizable(s, T, r_min) for T in T_vals])
    cb = np.array([cost_bounded(s, T, r_min)        for T in T_vals])

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    ax = axes[0]
    ax.plot(T_vals, cp, color=COLOR_PAR, label="Parallelizable")
    ax.plot(T_vals, cb, color=COLOR_BND, label="Throughput-Bounded")
    ax.plot(T_vals, s * T_vals * r_min, "--", color=COLOR_REF,
            alpha=0.5, label="Linear reference $sT$")
    ax.set_xlabel("Time Horizon $T$ (windows)")
    ax.set_ylabel("$C(s,T)$")
    ax.set_title(f"E2a: Raw Cost  ($s={s}$)")
    ax.legend()

    ax = axes[1]
    ax.plot(T_vals, cp / (s * T_vals), color=COLOR_PAR,
            label=r"Parallelizable $\to 0$")
    ax.plot(T_vals, cb / (s * T_vals), color=COLOR_BND,
            label=r"Bounded $= r_{\min}$")
    ax.axhline(r_min, linestyle="--", color=COLOR_REF, alpha=0.7,
               label=r"$r_{\min}$")
    ax.set_xlabel("Time Horizon $T$ (windows)")
    ax.set_ylabel(r"$C(s,T)\,/\,sT$")
    ax.set_title(f"E2b: Normalized Ratio  ($s={s}$)")
    ax.legend()

    fig.tight_layout()
    path = OUT / "fig_e2_time_scaling.pdf"
    fig.savefig(path)
    plt.close(fig)
    print(f"[E2] saved → {path}")


# ═════════════════════════════════════════════
# E3 — Marginal Identity Cost   (Section XI)
# ═════════════════════════════════════════════

def experiment_e3(T=100, r_min=1.0):
    s_vals = np.arange(2, 101)
    delta_p = np.array([
        cost_parallelizable(s, T, r_min) - cost_parallelizable(s-1, T, r_min)
        for s in s_vals
    ])
    delta_b = np.array([
        cost_bounded(s, T, r_min) - cost_bounded(s-1, T, r_min)
        for s in s_vals
    ])

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(s_vals, delta_p, color=COLOR_PAR,
            label=r"Parallelizable: $\Delta(s,T)$")
    ax.plot(s_vals, delta_b, color=COLOR_BND,
            label=r"Throughput-Bounded: $\Delta(s,T) = T \cdot r_{\min}$")
    ax.axhline(T * r_min, linestyle="--", color=COLOR_REF,
               alpha=0.7, label=fr"$T \cdot r_{{\min}} = {T}$ (Theorem~2)")
    ax.set_xlabel("Number of Identities $s$")
    ax.set_ylabel(r"Marginal Cost $\Delta(s,T)$")
    ax.set_title(f"E3: Marginal Identity Cost  ($T={T}$)")
    ax.legend()
    fig.tight_layout()
    path = OUT / "fig_e3_marginal_cost.pdf"
    fig.savefig(path)
    plt.close(fig)
    print(f"[E3] saved → {path}")


# ═════════════════════════════════════════════
# E4 — Coordination Model Robustness   (Section XI)
# ═════════════════════════════════════════════

def experiment_e4(T=100, r_min=1.0):
    s_vals = np.arange(1, 101)

    h_models = {
        r"$h = s + T$  (cloud orchestration)": (h_sublinear, "-",  "#4dac26"),
        r"$h = s \cdot \log T$":               (h_log,       "--", "#7b3294"),
        r"$h = s \cdot \sqrt{T}$":             (h_sqrt,      "-.", "#e66101"),
    }

    fig, ax = plt.subplots(figsize=(7, 4))
    for label, (h_func, ls, col) in h_models.items():
        ratios = np.array([
            cost_parallelizable(s, T, r_min, h_func) / (s * T)
            for s in s_vals
        ])
        ax.plot(s_vals, ratios, linestyle=ls, color=col, label=label)

    ax.axhline(r_min, linestyle="-", color=COLOR_BND, linewidth=2,
               label=r"Throughput-Bounded $= r_{\min}$ (linear)")
    ax.set_xlabel("Number of Identities $s$")
    ax.set_ylabel(r"$C(s,T)\,/\,sT$")
    ax.set_title("E4: Robustness to Coordination Overhead Model")
    ax.legend(fontsize=8)
    fig.tight_layout()
    path = OUT / "fig_e4_coordination.pdf"
    fig.savefig(path)
    plt.close(fig)
    print(f"[E4] saved → {path}")


# ═════════════════════════════════════════════
# Entry point
# ═════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("  Generating all figures")
    print("=" * 60)

    # Section VIII figure (was already referenced in paper)
    figure_theorem_validation()

    # Section XI figures (new Simulation Study section)
    experiment_e1()
    experiment_e2()
    experiment_e3()
    experiment_e4()

    print("\n✓ Done. All 5 figures saved to:", OUT)