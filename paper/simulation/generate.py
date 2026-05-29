"""
Evaluation figures for:
"Scarcity Is Not Enough: An Impossibility Result for
 Linear Sybil Cost Under Parallelizable Resources"

Run:  python evaluation_figures_v3.py
Output: ./output/fig1_cost_vs_s.png
        ./output/fig2_cost_vs_T.png
        ./output/fig3_influence_share.png
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# ── Output directory ─────────────────────────────────────────────
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
os.makedirs(OUT, exist_ok=True)

# ── Global style ─────────────────────────────────────────────────
plt.rcParams.update({
    "font.family":     "serif",
    "font.size":       11,
    "axes.labelsize":  12,
    "axes.titlesize":  11,
    "legend.fontsize": 9,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "lines.linewidth": 2.0,
    "figure.dpi":      150,
    "text.usetex":     False,
})

R_MIN   = 1.0
T_FIXED = 100
S_FIXED = 10

def C_par(s, T, r=R_MIN):
    return s * r + (s + T)

def C_bnd(s, T, r=R_MIN):
    return s * T * r

def crossover(T, r=R_MIN):
    denom = T * r - r - 1
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(denom > 0, T / denom, np.nan)


# ════════════════════════════════════════════════════════════════
# FIGURE 1 — Cost vs s  (log-log)
# ════════════════════════════════════════════════════════════════
s_vals = np.logspace(0, 4, 500)
cp = C_par(s_vals, T_FIXED)
cb = C_bnd(s_vals, T_FIXED)
sc = float(crossover(T_FIXED))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))

ax1.loglog(s_vals, cp, color="#2166ac",
           label=r"$C_{\rm par}(s,T)$  [parallelizable]")
ax1.loglog(s_vals, cb, color="#d6604d",
           label=r"$C_{\rm bnd}(s,T)$  [throughput-bounded]")
ax1.loglog(s_vals, s_vals * T_FIXED * R_MIN,
           "k--", lw=1.2, alpha=0.45, label=r"$sT r_{\min}$  (reference)")
ax1.axvline(sc, color="gray", ls=":", lw=1.3,
            label=rf"crossover $s^*\approx{sc:.1f}$")
ax1.set_xlabel(r"Sustained influence units $s$")
ax1.set_ylabel(r"Total cost $C(s,T)$")
ax1.set_title(rf"(a) Total cost  ($T={T_FIXED}$,  $r_{{\min}}={R_MIN}$)")
ax1.legend()
ax1.grid(True, which="both", alpha=0.25)

ax2.semilogx(s_vals, cp / (s_vals * T_FIXED),
             color="#2166ac", label=r"$C_{\rm par}/(sT)\to 0$")
ax2.semilogx(s_vals, cb / (s_vals * T_FIXED),
             color="#d6604d", label=r"$C_{\rm bnd}/(sT)=r_{\min}$")
ax2.axhline(R_MIN, color="#d6604d", ls="--", lw=1.2, alpha=0.6)
ax2.set_xlabel(r"Sustained influence units $s$")
ax2.set_ylabel(r"Normalised cost $C(s,T)\,/\,sT$")
ax2.set_title(r"(b) Amortised cost per influence-unit-window")
ax2.set_ylim(-0.1, 2.5)
ax2.legend()
ax2.grid(True, which="both", alpha=0.25)

fig.tight_layout()
path = os.path.join(OUT, "fig1_cost_vs_s.png")
fig.savefig(path, bbox_inches="tight")
plt.close(fig)
print(f"Saved: {path}")


# ════════════════════════════════════════════════════════════════
# FIGURE 2 — Cost vs T
# ════════════════════════════════════════════════════════════════
T_vals  = np.arange(1, 301)
rm_list = [0.5, 1.0, 2.0]
colors  = ["#4dac26", "#2166ac", "#d6604d"]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))

for rm, col in zip(rm_list, colors):
    ax1.plot(T_vals, C_bnd(S_FIXED, T_vals, rm),
             color=col, label=rf"$r_{{\min}}={rm}$  [throughput-bounded]")
ax1.plot(T_vals, C_par(S_FIXED, T_vals),
         "k-.", lw=1.8, label="parallelizable")
ax1.set_xlabel(r"Time horizon $T$")
ax1.set_ylabel(r"Total cost $C(s,T)$")
ax1.set_title(rf"(a) Total cost  ($s={S_FIXED}$)")
ax1.legend()
ax1.grid(True, alpha=0.25)

for rm, col in zip(rm_list, colors):
    ax2.plot(T_vals,
             C_bnd(S_FIXED, T_vals, rm) / (S_FIXED * T_vals * rm),
             color=col, label=rf"$r_{{\min}}={rm}$  [throughput-bounded]")
ax2.plot(T_vals, C_par(S_FIXED, T_vals) / (S_FIXED * T_vals),
         "k-.", lw=1.8, label="parallelizable")
ax2.set_xlabel(r"Time horizon $T$")
ax2.set_ylabel(r"Normalised cost $C(s,T)\,/\,sT$")
ax2.set_title(rf"(b) Normalised cost  ($s={S_FIXED}$)")
ax2.legend()
ax2.grid(True, alpha=0.25)

fig.tight_layout()
path = os.path.join(OUT, "fig2_cost_vs_T.png")
fig.savefig(path, bbox_inches="tight")
plt.close(fig)
print(f"Saved: {path}")


# ════════════════════════════════════════════════════════════════
# FIGURE 3 — Adversarial influence share vs channel capacity m
#
# Key message: influence share = m / (m + n_honest)
# This is INDEPENDENT of s (identity count).
# We show three values of s, all larger than m_max=350,
# so min(m, s) = m throughout --- all curves are identical.
# This makes the non-amplification result visually undeniable.
# ════════════════════════════════════════════════════════════════
N_HONEST = 200
M_VALS   = np.arange(0, 351)

# s values all larger than max(M_VALS)=350 so min(m,s)=m always
S_VALS      = [400, 700, 1000]
LINE_STYLES = ["-",  "--",  ":"]
LINE_WIDTHS = [3.0,  2.5,   2.0]
LINE_COLORS = ["#d6604d", "#2166ac", "#4dac26"]

fig, ax = plt.subplots(figsize=(7.5, 5.0))

for s_adv, ls, lw, col in zip(S_VALS, LINE_STYLES, LINE_WIDTHS, LINE_COLORS):
    share = np.minimum(M_VALS, s_adv) / (np.minimum(M_VALS, s_adv) + N_HONEST)
    ax.plot(M_VALS, share, ls=ls, lw=lw, color=col,
            label=rf"$s={s_adv}$ adversarial identities")

ax.axhline(0.5, color="k", ls="--", lw=1.3,
           label="majority threshold (0.5)")
ax.axvline(N_HONEST, color="gray", ls=":", lw=1.3,
           label=rf"$m = n_{{\rm honest}} = {N_HONEST}$")

ax.set_xlabel(r"Adversarial channel capacity $m$")
ax.set_ylabel(r"Adversarial influence share  $W_{\mathcal{A}}\,/\,W_{\rm tot}$")
ax.set_title(
    r"Adversarial influence share vs channel capacity" "\n"
    r"(all three curves overlap: share is independent of $s$)"
)
ax.legend()
ax.set_xlim(0, 350)
ax.set_ylim(0, 0.75)
ax.grid(True, alpha=0.25)
fig.tight_layout()

path = os.path.join(OUT, "fig3_influence_share.png")
fig.savefig(path, bbox_inches="tight")
plt.close(fig)
print(f"Saved: {path}")


# ════════════════════════════════════════════════════════════════
# TABLE — crossover s*
# ════════════════════════════════════════════════════════════════
T_tbl  = [10, 25, 50, 100, 200]
rm_tbl = [0.5, 1.0, 2.0]
print("\nCrossover s* table:")
header = f"{'T':>6}" + "".join(f"  r_min={r:.1f}" for r in rm_tbl)
print(header)
print("-" * len(header))
for T in T_tbl:
    row = f"{T:>6}"
    for r in rm_tbl:
        v = crossover(float(T), r)
        row += f"  {float(v):>9.1f}" if not np.isnan(v) else f"  {'---':>9}"
    print(row)

print(f"\nAll figures saved to: {OUT}/")