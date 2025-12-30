"""pyplots.ai
bar-sorted: Sorted Bar Chart
Library: seaborn | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Data - Product sales data sorted by revenue
np.random.seed(42)
products = [
    "Electronics",
    "Clothing",
    "Home & Garden",
    "Sports",
    "Books",
    "Toys",
    "Beauty",
    "Automotive",
    "Food & Grocery",
    "Pet Supplies",
]
sales = np.array([450, 380, 320, 275, 240, 210, 185, 150, 120, 95])

# Create DataFrame and sort by value (descending)
df = pd.DataFrame({"Product Category": products, "Sales (thousands $)": sales})
df = df.sort_values("Sales (thousands $)", ascending=False)

# Create plot (4800x2700 px = 16x9 at 300 dpi)
fig, ax = plt.subplots(figsize=(16, 9))

# Horizontal bar chart for better label readability
sns.barplot(
    data=df,
    y="Product Category",
    x="Sales (thousands $)",
    hue="Product Category",
    palette=["#306998"] * len(df),
    legend=False,
    ax=ax,
    orient="h",
)

# Add value labels on bars
for i, value in enumerate(df["Sales (thousands $)"]):
    ax.text(value + 5, i, f"${value}k", va="center", fontsize=14, color="#333333")

# Styling
ax.set_xlabel("Sales (thousands $)", fontsize=20)
ax.set_ylabel("Product Category", fontsize=20)
ax.set_title("bar-sorted · seaborn · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, axis="x", alpha=0.3, linestyle="--")

# Extend x-axis slightly to fit labels
ax.set_xlim(0, max(sales) * 1.15)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
