""" pyplots.ai
bubble-basic: Basic Bubble Chart
Library: matplotlib 3.10.8 | Python 3.14.3
Quality: 86/100 | Updated: 2026-02-15
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - tech company metrics: revenue vs growth with market cap as bubble size
np.random.seed(42)
n_companies = 40

revenue = np.random.uniform(5, 120, n_companies)  # billions USD
growth_rate = 0.4 * (100 - revenue) / 100 + np.random.randn(n_companies) * 0.08 + 0.05
growth_rate = np.clip(growth_rate, -0.10, 0.55)
market_cap = revenue * (1 + growth_rate * 3) * np.random.uniform(0.6, 1.8, n_companies)
market_cap = np.clip(market_cap, 5, 400)

# Scale bubble sizes by area for accurate visual perception
size_scaled = (market_cap / market_cap.max()) * 2500 + 150

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

scatter = ax.scatter(
    revenue,
    growth_rate * 100,
    s=size_scaled,
    alpha=0.55,
    c=market_cap,
    cmap="cividis",
    edgecolors="white",
    linewidths=1.2,
    zorder=3,
)

# Colorbar for market cap
cbar = fig.colorbar(scatter, ax=ax, pad=0.02, shrink=0.8)
cbar.set_label("Market Cap ($B)", fontsize=18)
cbar.ax.tick_params(labelsize=14)

# Size legend with representative bubble sizes
legend_caps = [25, 100, 300]
legend_handles = [
    ax.scatter([], [], s=(v / market_cap.max()) * 2500 + 150, c="gray", alpha=0.5, edgecolors="white", linewidths=1.2)
    for v in legend_caps
]
ax.legend(
    legend_handles,
    [f"${v}B" for v in legend_caps],
    title="Market Cap",
    title_fontsize=18,
    fontsize=16,
    loc="upper right",
    framealpha=0.9,
    scatterpoints=1,
    labelspacing=1.8,
    borderpad=1.2,
)

# Style
ax.set_xlabel("Annual Revenue ($B)", fontsize=20)
ax.set_ylabel("Revenue Growth Rate (%)", fontsize=20)
ax.set_title("bubble-basic · matplotlib · pyplots.ai", fontsize=24, fontweight="medium")
ax.tick_params(axis="both", labelsize=16)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(True, alpha=0.2, linewidth=0.8, linestyle="--", zorder=0)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
