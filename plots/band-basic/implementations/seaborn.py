"""pyplots.ai
band-basic: Basic Band Plot
Library: seaborn | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Data: simulated time series with 95% confidence interval
np.random.seed(42)
x = np.linspace(0, 10, 100)
y_center = 2 * np.sin(x) + 0.5 * x  # Trend with oscillation
noise_scale = 0.3 + 0.1 * x  # Increasing uncertainty over time
y_lower = y_center - 1.96 * noise_scale
y_upper = y_center + 1.96 * noise_scale

# Create figure
sns.set_style("whitegrid")
fig, ax = plt.subplots(figsize=(16, 9))

# Band plot: confidence interval as filled region
ax.fill_between(x, y_lower, y_upper, alpha=0.3, color="#306998", label="95% Confidence Interval")

# Central trend line using seaborn
sns.lineplot(x=x, y=y_center, ax=ax, linewidth=3, color="#FFD43B", label="Mean Trend")

# Styling
ax.set_xlabel("Time (s)", fontsize=20)
ax.set_ylabel("Amplitude", fontsize=20)
ax.set_title("band-basic · seaborn · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.legend(fontsize=16, loc="upper left")
ax.grid(True, alpha=0.3, linestyle="--")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
