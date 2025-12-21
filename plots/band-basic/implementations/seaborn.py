""" pyplots.ai
band-basic: Basic Band Plot
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 96/100 | Created: 2025-12-17
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Data - Time series with 95% confidence interval
np.random.seed(42)
x = np.linspace(0, 10, 100)

# Central trend line (sinusoidal with linear trend)
y_center = 2 * np.sin(x) + 0.3 * x + 5

# Confidence interval bounds (widening uncertainty over time)
uncertainty = 0.3 + 0.15 * x
y_lower = y_center - uncertainty
y_upper = y_center + uncertainty

# Create figure
sns.set_style("whitegrid")
fig, ax = plt.subplots(figsize=(16, 9))

# Plot the confidence band
ax.fill_between(x, y_lower, y_upper, alpha=0.3, color="#306998", label="95% Confidence Interval")

# Plot the central trend line
ax.plot(x, y_center, color="#FFD43B", linewidth=3, label="Mean Trend")

# Styling
ax.set_xlabel("Time (seconds)", fontsize=20)
ax.set_ylabel("Measurement Value", fontsize=20)
ax.set_title("band-basic · seaborn · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.legend(fontsize=16, loc="upper left")
ax.grid(True, alpha=0.3, linestyle="--")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
