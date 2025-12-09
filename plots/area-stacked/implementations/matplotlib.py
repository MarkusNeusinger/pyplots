"""
area-stacked: Stacked Area Chart
Library: matplotlib
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Color palette from style guide
colors = ["#306998", "#FFD43B", "#DC2626", "#059669"]

# Data - monthly revenue by product line over 2 years
np.random.seed(42)
dates = pd.date_range(start="2022-01-01", periods=24, freq="ME")

# Generate realistic revenue data with some trends
base = np.linspace(100, 150, 24)
y1 = base + np.random.randn(24) * 10  # Product A - steady growth
y2 = base * 0.8 + np.random.randn(24) * 8  # Product B
y3 = base * 0.6 + np.random.randn(24) * 6  # Product C
y4 = base * 0.4 + np.random.randn(24) * 5  # Product D

# Ensure no negative values
y1 = np.maximum(y1, 10)
y2 = np.maximum(y2, 10)
y3 = np.maximum(y3, 10)
y4 = np.maximum(y4, 10)

# Create plot
fig, ax = plt.subplots(figsize=(16, 9))

# Stacked area chart - order by magnitude (largest at bottom)
ax.stackplot(
    dates, y1, y2, y3, y4, labels=["Product A", "Product B", "Product C", "Product D"], colors=colors, alpha=0.75
)

# Labels and styling
ax.set_xlabel("Date", fontsize=20)
ax.set_ylabel("Revenue ($ thousands)", fontsize=20)
ax.set_title("Monthly Revenue by Product Line", fontsize=20)

# Tick label sizes
ax.tick_params(axis="both", labelsize=16)

# Legend
ax.legend(loc="upper left", fontsize=16)

# Subtle grid
ax.grid(True, alpha=0.3, linestyle="-", linewidth=0.5)

# Format x-axis dates
fig.autofmt_xdate(rotation=45)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
