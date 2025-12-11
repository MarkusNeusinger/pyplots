"""
bar-stacked: Stacked Bar Chart
Library: matplotlib
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - monthly sales by product category
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
np.random.seed(42)

# Generate realistic sales data for 4 product categories
electronics = np.random.randint(40, 80, 12)
clothing = np.random.randint(30, 60, 12)
home_garden = np.random.randint(20, 45, 12)
sports = np.random.randint(15, 35, 12)

# Color palette from style guide
colors = ["#306998", "#FFD43B", "#DC2626", "#059669"]

# Create plot
fig, ax = plt.subplots(figsize=(16, 9))

x = np.arange(len(months))
width = 0.6

# Stack bars from bottom to top
ax.bar(x, electronics, width, label="Electronics", color=colors[0])
ax.bar(x, clothing, width, bottom=electronics, label="Clothing", color=colors[1])
ax.bar(x, home_garden, width, bottom=electronics + clothing, label="Home & Garden", color=colors[2])
ax.bar(x, sports, width, bottom=electronics + clothing + home_garden, label="Sports", color=colors[3])

# Labels and styling
ax.set_xlabel("Month", fontsize=20)
ax.set_ylabel("Sales (thousands $)", fontsize=20)
ax.set_title("Monthly Sales by Product Category", fontsize=20)
ax.set_xticks(x)
ax.set_xticklabels(months, fontsize=16)
ax.tick_params(axis="y", labelsize=16)
ax.legend(fontsize=16, loc="upper left")
ax.grid(True, axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
