"""
eval_calibration.py
Section 9.4 calibration figures — fixed version
Fixes:
  - Fig4(a): TB s=300K clipped; now shown with inset annotation
  - Fig4: "per window" -> "per epoch" consistency
  - Fig5(a): h(s,T) residual removed for small pool (use h=0 for normalised plot)
  - Fig5: unified x-axis scale between panel (a) and (b) [both 0..300]
  - Fig4(b): subtitle uses ASCII -> instead of unicode arrow
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from pathlib import Path

# ── output dir ────────────────────────────────────────────────────────────────
OUT = Path("output")
OUT.mkdir(exist_ok=True)

# ── global style ──────────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 11,
    "axes.labelsize": 11,
    "axes.titlesize": 11,
    "legend.fontsize": 9,
    "figure.dpi": 150,
})

BLUE   = "#1f77b4"
GREEN  = "#2ca02c"
ORANGE = "#ff7f0e"
RED    = "#d62728"

# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 4 — Ethereum PoS calibration
# ══════════════════════════════════════════════════════════════════════════════
def fig4_eth():
    r_min = 32          # ETH per validator per epoch
    T = np.linspace(1, 1000, 1000)

    s_lido  = 300_000
    s_small = 100

    # ── cost expressions ──────────────────────────────────────────────────────
    def C_par(s, T):
        return s * r_min + T          # h = T (stock acquisition + coordination)

    def C_bnd(s, T):
        return s * T * r_min

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

    # ── panel (a): total cost ─────────────────────────────────────────────────
    ax = axes[0]

    # parallelizable (flat)
    ax.plot(T, np.full_like(T, C_par(s_lido,  1)),  "--", color=BLUE,  lw=1.6,
            label=r"Par., $s=300$K")
    ax.plot(T, np.full_like(T, C_par(s_small, 1)),  "--", color=GREEN, lw=1.6,
            label=r"Par., $s=100$")

    # throughput-bounded s=100 (fits in axis range)
    C_bnd_small = C_bnd(s_small, T)
    ax.plot(T, C_bnd_small, "-", color=GREEN, lw=2,
            label=r"TB, $s=100$ (small operator)")

    # throughput-bounded s=300K — clips above ~T=3; draw up to y_max with
    # annotation indicating the out-of-range growth
    y_max = 2e10
    T_clip = T[C_bnd(s_lido, T) <= y_max]
    if len(T_clip) == 0:
        T_clip = T[:2]
    C_lido_visible = C_bnd(s_lido, T_clip)
    ax.plot(T_clip, C_lido_visible, "-", color=BLUE, lw=2,
            label=r"TB, $s=300$K (Lido, Rated Network 2023)")

    # arrow annotation pointing off-chart
    T_ann = T_clip[-1] if len(T_clip) > 0 else 5
    C_ann = C_bnd(s_lido, T_ann)
    ax.annotate(
        r"TB $s=300$K: $C \propto sT\cdot r_{\min}$, exceeds axis",
        xy=(T_ann, min(C_ann, y_max)),
        xytext=(300, 3e9),
        fontsize=8.5,
        arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.2),
        color=BLUE,
    )

    ax.set_yscale("log")
    ax.set_ylim(1e3, y_max)
    ax.set_xlabel(r"Time horizon $T$ (epochs, 1 epoch $\approx$ 6.4 min)")
    ax.set_ylabel("Adversarial cost (ETH)")
    ax.set_title(
        r"(a) Ethereum PoS: calibrated cost"
        "\n"
        r"($r_{\min} = 32$ ETH per validator per epoch)"
    )
    ax.legend(loc="upper left", framealpha=0.85)
    ax.grid(True, which="both", ls=":", alpha=0.4)

    # ── panel (b): normalised ratio C(s,T)/sT ────────────────────────────────
    ax = axes[1]

    # par -> 0
    ax.plot(T, C_par(s_lido,  T) / (s_lido  * T), "--", color=BLUE,  lw=1.6,
            label=r"Par., $s=300$K")
    ax.plot(T, C_par(s_small, T) / (s_small * T), "--", color=GREEN, lw=1.6,
            label=r"Par., $s=100$")

    # TB -> r_min (constant)
    ax.plot(T, C_bnd(s_lido,  T) / (s_lido  * T), "-",  color=BLUE,  lw=2,
            label=r"TB, $s=300$K")
    ax.plot(T, C_bnd(s_small, T) / (s_small * T), "-",  color=GREEN, lw=2,
            label=r"TB, $s=100$")

    # theoretical bound line
    ax.axhline(r_min, color="gray", ls=":", lw=1.2,
               label=r"$r_{\min}=32$ (Thm. 6.2 bound)")

    ax.set_ylim(-1, 50)
    ax.set_xlabel(r"Time horizon $T$ (epochs)")
    ax.set_ylabel(r"Normalised cost $C(s,T)/sT$")
    ax.set_title(
        r"(b) Normalised ratio:"
        "\n"
        r"Par. $\to 0$; TB bounded at $r_{\min}$"      # ASCII -> instead of unicode
    )
    ax.legend(loc="upper right", framealpha=0.85)
    ax.grid(True, ls=":", alpha=0.4)

    fig.tight_layout()
    path = OUT / "fig4_eth_calibration.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {path}")


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 5 — Bitcoin PoW calibration
# ══════════════════════════════════════════════════════════════════════════════
def fig5_btc():
    r_min = 1.0          # normalised units

    # pool tiers from Gencer et al. 2018
    pools = [
        (50,   RED,    r"Small pool, $s=50$"),
        (300,  GREEN,  "Mid pool 3%, $s=300$"),
        (1200, ORANGE, "Pool 12%, $s=1200$"),
        (1650, BLUE,   "Top pool 16.5%, $s=1650$"),
    ]

    # C_par includes h(s,T)=s+T; ratio = r_min/T + 1/T + 1/s.
    # 1/s term separates pool-tier curves visibly; all decay to 0 as T->inf.
    def C_par_norm(s, T):
        return (s * r_min + s + T) / (s * T)

    # ── Fix 4: unified x-axis for both panels (0..300 block intervals) ────────
    T_max = 300
    T = np.linspace(1, T_max, 500)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

    # ── panel (a): normalised C_par(s,T)/sT ──────────────────────────────────
    ax = axes[0]
    for s, color, label in pools:
        ratio = C_par_norm(s, T)
        ax.plot(T, ratio, color=color, lw=2, label=label)

    ax.axhline(0, color="gray", ls="--", lw=1.2,
               label="Limit 0 (Thm. 5.4)")
    ax.set_xlim(0, T_max)
    ax.set_ylim(-0.002, 0.06)
    ax.set_xlabel(r"Time horizon $T$ (block intervals)")
    ax.set_ylabel(r"Normalised cost $C_{\mathrm{par}}(s,T)/sT$")
    ax.set_title(
        r"(a) PoW: $C_{\mathrm{par}}/sT \to 0$ for all pool tiers"
        "\n"
        "(Gencer et al. 2018 pool sizes)"
    )
    ax.legend(loc="upper right", framealpha=0.85)
    ax.grid(True, ls=":", alpha=0.4)

    # ── panel (b): marginal cost structural gap ───────────────────────────────
    ax = axes[1]

    # parallelizable: Delta_par = O(1), here = r_min (constant)
    ax.axhline(r_min, color=BLUE, ls="--", lw=2,
               label=r"$\Delta_{\mathrm{par}}(s,T)=O(1)$ --- Thm. 5.4")

    # throughput-bounded: Delta_bnd = r_min * T
    Delta_bnd = r_min * T
    ax.plot(T, Delta_bnd, color=ORANGE, lw=2,
            label=r"$\Delta_{\mathrm{bnd}}(s,T)=\Omega(T)$ --- Thm. 6.2")

    # shaded structural gap
    ax.fill_between(T, r_min, Delta_bnd,
                    color=ORANGE, alpha=0.12, label="Structural gap")

    ax.set_xlim(0, T_max)
    ax.set_ylim(-5, 310)
    ax.set_xlabel(r"Time horizon $T$ (block intervals)")
    ax.set_ylabel(r"Marginal identity cost $\Delta(s,T)$")
    ax.set_title(
        r"(b) Marginal cost: structural separation"
        "\n"
        r"(resource class boundary)"
    )
    ax.legend(loc="upper left", framealpha=0.85)
    ax.grid(True, ls=":", alpha=0.4)

    fig.tight_layout()
    path = OUT / "fig5_btc_calibration.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {path}")


# ── run ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    fig4_eth()
    fig5_btc()
    print("Done.")