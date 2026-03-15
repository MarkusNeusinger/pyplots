""" pyplots.ai
funnel-meta-analysis: Meta-Analysis Funnel Plot for Publication Bias
Library: matplotlib 3.10.8 | Python 3.14.3
Quality: 86/100 | Created: 2026-03-15
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - 15 RCTs comparing drug vs placebo (log odds ratios)
np.random.seed(42)
n_studies = 15
true_effect = -0.4

std_errors = np.concatenate(
    [np.random.uniform(0.05, 0.15, 4), np.random.uniform(0.15, 0.30, 5), np.random.uniform(0.30, 0.55, 6)]
)

effect_sizes = true_effect + np.random.normal(0, std_errors)

# Introduce mild asymmetry (publication bias): shift small studies toward significance
small_study_mask = std_errors > 0.35
effect_sizes[small_study_mask] -= np.random.uniform(0.05, 0.20, small_study_mask.sum())

summary_effect = np.average(effect_sizes, weights=1 / std_errors**2)

# Funnel boundaries
se_range = np.linspace(0, 0.60, 200)
upper_ci = summary_effect + 1.96 * se_range
lower_ci = summary_effect - 1.96 * se_range

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

ax.fill_betweenx(se_range, lower_ci, upper_ci, color="#306998", alpha=0.06)
ax.plot(upper_ci, se_range, color="#306998", linewidth=1.5, alpha=0.5, linestyle="--")
ax.plot(lower_ci, se_range, color="#306998", linewidth=1.5, alpha=0.5, linestyle="--")

ax.axvline(x=summary_effect, color="#306998", linewidth=2, alpha=0.7, label="Summary effect")
ax.axvline(x=0, color="#888888", linewidth=1.5, linestyle=":", alpha=0.5, label="Null effect")

ax.scatter(effect_sizes, std_errors, s=220, color="#306998", edgecolors="white", linewidth=0.8, zorder=5, alpha=0.85)

# Style
ax.set_xlabel("Log Odds Ratio", fontsize=20)
ax.set_ylabel("Standard Error", fontsize=20)
ax.set_title("funnel-meta-analysis · matplotlib · pyplots.ai", fontsize=24, fontweight="medium")
ax.tick_params(axis="both", labelsize=16)

ax.invert_yaxis()
ax.set_ylim(0.65, 0)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.legend(fontsize=16, frameon=False, loc="upper right")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
