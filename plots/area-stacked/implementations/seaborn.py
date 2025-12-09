"""
area-stacked: Stacked Area Chart
Library: seaborn
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Data - monthly revenue by product line over 2 years
np.random.seed(42)
dates = pd.date_range(start="2022-01-01", periods=24, freq="MS")

# Generate realistic revenue data for 4 product lines
base_values = [30, 25, 20, 15]  # Base revenue in millions
growth_factors = [1.05, 1.08, 1.03, 1.12]  # Monthly growth rates
noise_scales = [3, 2.5, 2, 1.5]

y1, y2, y3, y4 = [], [], [], []
for i in range(24):
    seasonal = 1 + 0.15 * np.sin(2 * np.pi * i / 12)  # Seasonal variation
    y1.append(base_values[0] * (growth_factors[0] ** i) * seasonal + np.random.randn() * noise_scales[0])
    y2.append(base_values[1] * (growth_factors[1] ** i) * seasonal + np.random.randn() * noise_scales[1])
    y3.append(base_values[2] * (growth_factors[2] ** i) * seasonal + np.random.randn() * noise_scales[2])
    y4.append(base_values[3] * (growth_factors[3] ** i) * seasonal + np.random.randn() * noise_scales[3])

# Ensure all values are positive
y1 = np.maximum(y1, 1)
y2 = np.maximum(y2, 1)
y3 = np.maximum(y3, 1)
y4 = np.maximum(y4, 1)

# Create DataFrame
df = pd.DataFrame({"Date": dates, "Product A": y1, "Product B": y2, "Product C": y3, "Product D": y4})

# Color palette from style guide
colors = ["#306998", "#FFD43B", "#DC2626", "#059669"]

# Create plot
fig, ax = plt.subplots(figsize=(16, 9))

# Seaborn doesn't have a direct stacked area function, so we use matplotlib's stackplot
# with seaborn styling
sns.set_style("whitegrid")

# Stack the areas (largest at bottom for stability)
# Sort by mean value descending
means = {"Product A": np.mean(y1), "Product B": np.mean(y2), "Product C": np.mean(y3), "Product D": np.mean(y4)}
sorted_products = sorted(means.keys(), key=lambda x: means[x], reverse=True)
sorted_data = [df[p].values for p in sorted_products]
sorted_colors = [colors[["Product A", "Product B", "Product C", "Product D"].index(p)] for p in sorted_products]

ax.stackplot(df["Date"], *sorted_data, labels=sorted_products, colors=sorted_colors, alpha=0.75)

# Labels and styling
ax.set_xlabel("Date", fontsize=20)
ax.set_ylabel("Revenue ($ Million)", fontsize=20)
ax.set_title("Monthly Revenue by Product Line", fontsize=20)
ax.tick_params(axis="both", labelsize=16)

# Legend
ax.legend(loc="upper left", fontsize=16, framealpha=0.9)

# Grid
ax.grid(True, alpha=0.3, linestyle="-", linewidth=0.5)
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
