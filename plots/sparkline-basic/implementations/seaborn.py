""" pyplots.ai
sparkline-basic: Basic Sparkline
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 93/100 | Created: 2025-12-16
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Data - simulated monthly revenue trend (24 months)
np.random.seed(42)
values = 100 + np.cumsum(np.random.randn(24) * 5)

# Create figure with compact sparkline aspect ratio
fig, ax = plt.subplots(figsize=(16, 4))

# Plot sparkline using seaborn lineplot
x = np.arange(len(values))
sns.lineplot(x=x, y=values, ax=ax, color="#306998", linewidth=2.5)

# Highlight min and max points
min_idx = np.argmin(values)
max_idx = np.argmax(values)
ax.scatter([min_idx], [values[min_idx]], color="#d62728", s=150, zorder=5)
ax.scatter([max_idx], [values[max_idx]], color="#2ca02c", s=150, zorder=5)

# Highlight first and last points
ax.scatter([0], [values[0]], color="#306998", s=100, zorder=5)
ax.scatter([len(values) - 1], [values[-1]], color="#306998", s=100, zorder=5)

# Remove all chart chrome for sparkline aesthetic
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlabel("")
ax.set_ylabel("")
for spine in ax.spines.values():
    spine.set_visible(False)

# Title placed above the sparkline
ax.set_title("sparkline-basic · seaborn · pyplots.ai", fontsize=24, pad=20)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
