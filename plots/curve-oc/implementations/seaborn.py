""" pyplots.ai
curve-oc: Operating Characteristic (OC) Curve
Library: seaborn 0.13.2 | Python 3.14.3
Quality: 89/100 | Created: 2026-03-19
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.stats import binom


# Data - OC curves for different acceptance sampling plans
fraction_defective = np.linspace(0, 0.20, 200)

plans = [
    {"n": 50, "c": 1, "label": "n=50, c=1"},
    {"n": 80, "c": 2, "label": "n=80, c=2"},
    {"n": 100, "c": 2, "label": "n=100, c=2"},
]

oc_curves = {}
for plan in plans:
    prob_accept = binom.cdf(plan["c"], plan["n"], fraction_defective)
    oc_curves[plan["label"]] = prob_accept

# Quality levels
aql = 0.02
ltpd = 0.10

# Plot
palette = ["#306998", "#E6894A", "#5BA67D"]
fig, ax = plt.subplots(figsize=(16, 9))

for i, plan in enumerate(plans):
    sns.lineplot(
        x=fraction_defective, y=oc_curves[plan["label"]], label=plan["label"], color=palette[i], linewidth=3, ax=ax
    )

# AQL and LTPD reference lines with labels at top
ax.axvline(x=aql, color="#888888", linestyle="--", linewidth=1.5, alpha=0.6)
ax.axvline(x=ltpd, color="#888888", linestyle="--", linewidth=1.5, alpha=0.6)
ax.text(aql + 0.002, 1.02, f"AQL = {aql}", fontsize=13, color="#555555", fontweight="medium", va="bottom")
ax.text(ltpd + 0.002, 1.02, f"LTPD = {ltpd}", fontsize=13, color="#555555", fontweight="medium", va="bottom")

# Risk annotations for the middle plan (n=80, c=2)
alpha_risk = 1 - binom.cdf(plans[1]["c"], plans[1]["n"], aql)
beta_risk = binom.cdf(plans[1]["c"], plans[1]["n"], ltpd)
prob_at_aql = binom.cdf(plans[1]["c"], plans[1]["n"], aql)

ax.plot(aql, prob_at_aql, "o", color=palette[1], markersize=10, zorder=5)
ax.plot(ltpd, beta_risk, "o", color=palette[1], markersize=10, zorder=5)

ax.annotate(
    f"Producer's risk\n\u03b1 = {alpha_risk:.3f}",
    xy=(aql, prob_at_aql),
    xytext=(aql + 0.018, prob_at_aql + 0.02),
    fontsize=14,
    color="#444444",
    arrowprops={"arrowstyle": "->", "color": "#888888", "lw": 1.2},
)

ax.annotate(
    f"Consumer's risk\n\u03b2 = {beta_risk:.3f}",
    xy=(ltpd, beta_risk),
    xytext=(ltpd + 0.018, beta_risk + 0.12),
    fontsize=14,
    color="#444444",
    arrowprops={"arrowstyle": "->", "color": "#888888", "lw": 1.2},
)

# Style
ax.set_xlabel("Fraction Defective (p)", fontsize=20)
ax.set_ylabel("Probability of Acceptance P(a)", fontsize=20)
ax.set_title("curve-oc \u00b7 seaborn \u00b7 pyplots.ai", fontsize=24, fontweight="medium")
ax.tick_params(axis="both", labelsize=16)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.yaxis.grid(True, alpha=0.2, linewidth=0.8)
ax.set_xlim(0, 0.20)
ax.set_ylim(0, 1.05)
ax.legend(fontsize=16, frameon=False, title="Sampling Plan", title_fontsize=17)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
