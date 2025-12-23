"""pyplots.ai
density-basic: Basic Density Plot
Library: matplotlib | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


# Data - Simulating test scores with realistic distribution characteristics
np.random.seed(42)
# Create a slightly left-skewed distribution typical of test scores
values = np.concatenate(
    [
        np.random.normal(72, 12, 400),  # Main group of students
        np.random.normal(45, 8, 100),  # Lower performing group (creates slight bimodality)
    ]
)
values = np.clip(values, 0, 100)  # Clip to valid test score range

# Calculate kernel density estimation
kde = stats.gaussian_kde(values)
x_range = np.linspace(values.min() - 5, values.max() + 5, 500)
density = kde(x_range)

# Create plot (4800x2700 px)
fig, ax = plt.subplots(figsize=(16, 9))

# Plot density curve with fill
ax.fill_between(x_range, density, alpha=0.4, color="#306998")
ax.plot(x_range, density, linewidth=3, color="#306998")

# Add rug plot showing individual observations
rug_height = -0.0015
ax.plot(values, np.full_like(values, rug_height), "|", color="#306998", alpha=0.4, markersize=12)

# Labels and styling (scaled font sizes for 4800x2700)
ax.set_xlabel("Test Score", fontsize=20)
ax.set_ylabel("Density", fontsize=20)
ax.set_title("density-basic · matplotlib · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, alpha=0.3, linestyle="--")

# Remove top and right spines for cleaner look
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Set y-axis to show rug plot
ax.set_ylim(bottom=-0.003)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
