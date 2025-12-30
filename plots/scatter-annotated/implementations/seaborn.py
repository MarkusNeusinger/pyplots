"""pyplots.ai
scatter-annotated: Annotated Scatter Plot with Text Labels
Library: seaborn | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Data: Technology companies with revenue vs market cap
np.random.seed(42)
companies = [
    "TechCorp",
    "DataSys",
    "CloudNet",
    "AILabs",
    "CyberSec",
    "NetFlow",
    "AppWorks",
    "CodeBase",
    "DevOps",
    "QuantumX",
    "ByteLogic",
    "StreamIO",
    "VirtualAI",
    "SecureIT",
    "SmartHub",
]
n_points = len(companies)

# Revenue (billions) and Market Cap (billions) - realistic tech company scale
revenue = np.random.uniform(5, 80, n_points)
market_cap = revenue * np.random.uniform(2, 8, n_points) + np.random.randn(n_points) * 10

# Create plot
fig, ax = plt.subplots(figsize=(16, 9))

# Scatter plot with seaborn
sns.scatterplot(x=revenue, y=market_cap, s=200, alpha=0.7, color="#306998", edgecolor="white", linewidth=1.5, ax=ax)

# Add text annotations with offset to avoid overlap
for i, company in enumerate(companies):
    # Offset labels slightly above and to the right
    offset_x = 1.5
    offset_y = market_cap[i] * 0.03 + 5

    ax.annotate(
        company,
        xy=(revenue[i], market_cap[i]),
        xytext=(revenue[i] + offset_x, market_cap[i] + offset_y),
        fontsize=14,
        color="#333333",
        ha="left",
        va="bottom",
        arrowprops={"arrowstyle": "-", "color": "#999999", "alpha": 0.5, "lw": 1},
    )

# Labels and styling
ax.set_xlabel("Annual Revenue ($ Billion)", fontsize=20)
ax.set_ylabel("Market Capitalization ($ Billion)", fontsize=20)
ax.set_title("scatter-annotated · seaborn · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, alpha=0.3, linestyle="--")

# Adjust axis limits to accommodate labels
ax.set_xlim(0, max(revenue) + 15)
ax.set_ylim(min(market_cap) - 20, max(market_cap) + 50)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
