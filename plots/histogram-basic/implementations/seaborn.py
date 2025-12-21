""" pyplots.ai
histogram-basic: Basic Histogram
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 95/100 | Created: 2025-12-13
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Data - simulated test scores with realistic distribution
np.random.seed(42)
values = np.random.normal(loc=75, scale=12, size=500)

# Create figure (4800x2700 px)
fig, ax = plt.subplots(figsize=(16, 9))

# Plot histogram
sns.histplot(values, bins=25, color="#306998", edgecolor="white", linewidth=1.5, alpha=0.85, ax=ax)

# Labels and styling (scaled for 4800x2700)
ax.set_xlabel("Test Score", fontsize=20)
ax.set_ylabel("Frequency", fontsize=20)
ax.set_title("histogram-basic · seaborn · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, alpha=0.3, linestyle="--", axis="y")

# Ensure y-axis starts at zero
ax.set_ylim(bottom=0)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
