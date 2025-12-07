"""
line-basic: Basic Line Plot
Library: matplotlib
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - simulating time series data (e.g., monthly values)
np.random.seed(42)
time = np.arange(1, 13)  # 12 months
base_trend = np.linspace(10, 30, 12)
noise = np.random.randn(12) * 2
value = base_trend + noise

# Create plot
fig, ax = plt.subplots(figsize=(16, 9))
ax.plot(time, value, linewidth=2, color="#306998", marker="o", markersize=6)

# Labels and styling
ax.set_xlabel("Month", fontsize=20)
ax.set_ylabel("Value", fontsize=20)
ax.set_title("Basic Line Plot", fontsize=20)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
