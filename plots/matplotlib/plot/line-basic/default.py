"""
line-basic: Basic Line Plot
Library: matplotlib
"""

import matplotlib.pyplot as plt
import numpy as np


# Data
np.random.seed(42)
time = np.arange(1, 31)
base_value = 10
trend = 0.5 * time
noise = np.random.randn(30) * 2
value = base_value + trend + noise

# Plot
fig, ax = plt.subplots(figsize=(16, 9))
ax.plot(time, value, color="#306998", linewidth=2, marker="o", markersize=4)

# Labels and styling
ax.set_xlabel("Time (days)", fontsize=20)
ax.set_ylabel("Value", fontsize=20)
ax.set_title("Basic Line Plot", fontsize=20)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
