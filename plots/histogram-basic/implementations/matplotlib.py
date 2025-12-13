"""
histogram-basic: Basic Histogram
Library: matplotlib
"""

import matplotlib.pyplot as plt
import numpy as np


# Data
np.random.seed(42)
# Simulate exam scores with a roughly normal distribution centered around 72
values = np.random.normal(loc=72, scale=12, size=500)
# Clip to realistic exam score range (0-100)
values = np.clip(values, 0, 100)

# Plot
fig, ax = plt.subplots(figsize=(16, 9))
ax.hist(values, bins=20, color="#306998", edgecolor="white", linewidth=1.5, alpha=0.85)

# Labels and styling
ax.set_xlabel("Exam Score", fontsize=20)
ax.set_ylabel("Frequency", fontsize=20)
ax.set_title("histogram-basic · matplotlib · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, alpha=0.3, linestyle="--", axis="y")

# Ensure y-axis starts at zero
ax.set_ylim(bottom=0)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
