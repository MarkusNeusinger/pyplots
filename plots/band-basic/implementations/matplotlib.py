"""
band-basic: Basic Band Plot
Library: matplotlib
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - Simulating a time series with 95% confidence interval
np.random.seed(42)
x = np.linspace(0, 10, 100)

# Central trend line (sinusoidal pattern with slight upward trend)
y_center = 2 * np.sin(x) + 0.3 * x + 5

# Confidence interval that widens over time (common in forecasting)
uncertainty = 0.5 + 0.15 * x
y_lower = y_center - uncertainty
y_upper = y_center + uncertainty

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

# Filled band (semi-transparent)
ax.fill_between(x, y_lower, y_upper, alpha=0.3, color="#306998", label="95% Confidence Interval")

# Central trend line
ax.plot(x, y_center, color="#306998", linewidth=3, label="Mean Trend")

# Boundary lines (subtle)
ax.plot(x, y_lower, color="#306998", linewidth=1.5, linestyle="--", alpha=0.7)
ax.plot(x, y_upper, color="#306998", linewidth=1.5, linestyle="--", alpha=0.7)

# Styling
ax.set_xlabel("Time (s)", fontsize=20)
ax.set_ylabel("Value", fontsize=20)
ax.set_title("band-basic · matplotlib · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.legend(fontsize=16, loc="upper left")
ax.grid(True, alpha=0.3, linestyle="--")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
