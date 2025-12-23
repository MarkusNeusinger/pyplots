""" pyplots.ai
histogram-basic: Basic Histogram
Library: matplotlib 3.10.8 | Python 3.13.11
Quality: 93/100 | Created: 2025-12-23
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - Simulate exam scores with a roughly normal distribution
np.random.seed(42)
scores = np.random.normal(loc=72, scale=12, size=500)
scores = np.clip(scores, 0, 100)  # Realistic exam score range

# Plot
fig, ax = plt.subplots(figsize=(16, 9))
ax.hist(scores, bins=20, color="#306998", edgecolor="white", linewidth=1.5, alpha=0.85)

# Labels and styling
ax.set_xlabel("Exam Score (points)", fontsize=20)
ax.set_ylabel("Frequency (count)", fontsize=20)
ax.set_title("histogram-basic · matplotlib · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, alpha=0.3, linestyle="--", axis="y")

# Ensure y-axis starts at zero
ax.set_ylim(bottom=0)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
