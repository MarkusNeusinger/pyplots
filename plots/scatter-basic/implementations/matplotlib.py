"""pyplots.ai
scatter-basic: Basic Scatter Plot
Library: matplotlib | Python 3.13
Quality: pending | Created: 2025-12-22
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - study hours vs exam scores (realistic educational context)
np.random.seed(42)
study_hours = np.random.uniform(1, 12, 120)
exam_scores = 45 + study_hours * 4.5 + np.random.randn(120) * 8
exam_scores = np.clip(exam_scores, 0, 100)

# Create plot
fig, ax = plt.subplots(figsize=(16, 9))
ax.scatter(study_hours, exam_scores, alpha=0.7, s=180, color="#306998", edgecolors="white", linewidths=0.5)

# Labels and styling
ax.set_xlabel("Study Hours (per week)", fontsize=20)
ax.set_ylabel("Exam Score (%)", fontsize=20)
ax.set_title("scatter-basic · matplotlib · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, alpha=0.3, linestyle="--")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
