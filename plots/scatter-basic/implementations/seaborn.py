""" pyplots.ai
scatter-basic: Basic Scatter Plot
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-22
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Data - study hours vs exam scores with realistic correlation
np.random.seed(42)
study_hours = np.random.uniform(1, 10, 150)
exam_scores = study_hours * 8 + np.random.randn(150) * 8 + 25

# Create plot
fig, ax = plt.subplots(figsize=(16, 9))
sns.scatterplot(
    x=study_hours, y=exam_scores, ax=ax, alpha=0.7, s=200, color="#306998", edgecolor="white", linewidth=0.5
)

# Labels and styling
ax.set_xlabel("Study Hours (per week)", fontsize=20)
ax.set_ylabel("Exam Score (points)", fontsize=20)
ax.set_title("scatter-basic · seaborn · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, alpha=0.3, linestyle="--")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
