"""pyplots.ai
scatter-basic: Basic Scatter Plot
Library: seaborn 0.13.2 | Python 3.14
Quality: /100 | Updated: 2026-02-14
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Data - study hours vs exam scores with realistic correlation
np.random.seed(42)
study_hours = np.random.uniform(1, 10, 150)
exam_scores = study_hours * 8 + np.random.randn(150) * 8 + 25
df = pd.DataFrame({"Study Hours (per week)": study_hours, "Exam Score (points)": exam_scores})

# Plot
sns.set_theme(style="ticks", context="talk", font_scale=1.1)
fig, ax = plt.subplots(figsize=(16, 9))
sns.scatterplot(
    data=df,
    x="Study Hours (per week)",
    y="Exam Score (points)",
    ax=ax,
    alpha=0.7,
    s=120,
    color="#306998",
    edgecolor="white",
    linewidth=0.5,
)

# Style
ax.set_title("scatter-basic · seaborn · pyplots.ai", fontsize=24, fontweight="medium")
ax.set_xlabel("Study Hours (per week)", fontsize=20)
ax.set_ylabel("Exam Score (points)", fontsize=20)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, alpha=0.2, linestyle="--", linewidth=0.8)
sns.despine(ax=ax)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
