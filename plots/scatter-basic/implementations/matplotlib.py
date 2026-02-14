""" pyplots.ai
scatter-basic: Basic Scatter Plot
Library: matplotlib 3.10.8 | Python 3.14
Quality: 85/100 | Created: 2025-12-22
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - study hours vs exam scores (realistic educational context)
np.random.seed(42)
study_hours = np.random.uniform(1, 12, 120)
exam_scores = 45 + study_hours * 4.5 + np.random.randn(120) * 8
exam_scores = np.clip(exam_scores, 0, 100)

# Plot
fig, ax = plt.subplots(figsize=(16, 9))
scatter = ax.scatter(
    study_hours,
    exam_scores,
    c=exam_scores,
    cmap="viridis",
    alpha=0.7,
    s=80,
    edgecolors="white",
    linewidths=0.5,
    vmin=40,
    vmax=100,
)

# Colorbar - distinctive matplotlib feature
cbar = fig.colorbar(scatter, ax=ax, pad=0.02, shrink=0.85)
cbar.set_label("Exam Score (%)", fontsize=18)
cbar.ax.tick_params(labelsize=14)

# Style
ax.set_xlabel("Study Hours (per week)", fontsize=20)
ax.set_ylabel("Exam Score (%)", fontsize=20)
ax.set_title("scatter-basic · matplotlib · pyplots.ai", fontsize=24, fontweight="medium")
ax.tick_params(axis="both", labelsize=16)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(True, alpha=0.2, linewidth=0.8, linestyle="--")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
