""" pyplots.ai
rug-basic: Basic Rug Plot
Library: matplotlib 3.10.8 | Python 3.13.11
Quality: 95/100 | Created: 2025-12-17
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - bimodal distribution to show clustering patterns
np.random.seed(42)
values = np.concatenate(
    [
        np.random.normal(25, 5, 60),  # Cluster around 25
        np.random.normal(55, 8, 40),  # Cluster around 55
    ]
)

# Create plot (4800x2700 px)
fig, ax = plt.subplots(figsize=(16, 9))

# Rug plot - vertical tick marks along x-axis
# Height set to 0.8 to make marks prominent
ax.vlines(values, ymin=0, ymax=0.8, color="#306998", alpha=0.6, linewidth=3)

# Set axis limits
ax.set_xlim(0, 80)
ax.set_ylim(0, 1)

# Hide y-axis as rug plots focus on x-distribution
ax.set_yticks([])
ax.set_ylabel("")
ax.spines["left"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Labels and styling
ax.set_xlabel("Value", fontsize=20)
ax.set_title("rug-basic \u00b7 matplotlib \u00b7 pyplots.ai", fontsize=24)
ax.tick_params(axis="x", labelsize=16)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
