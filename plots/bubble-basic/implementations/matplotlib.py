""" pyplots.ai
bubble-basic: Basic Bubble Chart
Library: matplotlib 3.10.8 | Python 3.14.3
Quality: 86/100 | Updated: 2026-02-15
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - tech company metrics: revenue vs growth with market cap as bubble size
np.random.seed(42)
n_companies = 35

revenue = np.random.uniform(5, 120, n_companies)  # billions USD
growth_rate = 0.4 * (100 - revenue) / 100 + np.random.randn(n_companies) * 0.08 + 0.05
growth_rate = np.clip(growth_rate, -0.10, 0.55)
market_cap = revenue * (1 + growth_rate * 3) * np.random.uniform(0.6, 1.8, n_companies)
market_cap = np.clip(market_cap, 5, 400)

# Add a few distinctive outlier companies for visual interest
# High-growth unicorn: modest revenue but explosive growth
revenue = np.append(revenue, [18, 12])
growth_rate = np.append(growth_rate, [0.48, 0.44])
market_cap = np.append(market_cap, [280, 220])

# Mature giant: massive revenue, low growth, huge market cap
revenue = np.append(revenue, [118])
growth_rate = np.append(growth_rate, [0.02])
market_cap = np.append(market_cap, [380])

# Mid-tier standout
revenue = np.append(revenue, [55])
growth_rate = np.append(growth_rate, [0.30])
market_cap = np.append(market_cap, [260])

n_total = len(revenue)

# Sector assignment for color encoding (4th variable)
sectors = np.array(
    ["Cloud/SaaS"] * 12
    + ["E-Commerce"] * 8
    + ["Semiconductors"] * 8
    + ["Social Media"] * 7
    + ["Cloud/SaaS", "Cloud/SaaS", "Semiconductors", "E-Commerce"]
)
sector_names = ["Cloud/SaaS", "E-Commerce", "Semiconductors", "Social Media"]
sector_colors = ["#306998", "#E07B39", "#5BA58B", "#8B6BAE"]

# Scale bubble sizes by area for accurate visual perception
size_scaled = (market_cap / market_cap.max()) * 2200 + 120

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

# Plot each sector separately for legend
for sector, color in zip(sector_names, sector_colors, strict=True):
    mask = sectors == sector
    ax.scatter(
        revenue[mask],
        growth_rate[mask] * 100,
        s=size_scaled[mask],
        alpha=0.6,
        color=color,
        edgecolors="white",
        linewidths=1.2,
        label=sector,
        zorder=3,
    )

# Annotate notable outliers to guide the viewer
annotations = [
    (n_companies, "High-Growth\nUnicorn", (0, 20)),  # first added unicorn
    (n_companies + 2, "Market\nLeader", (-55, 30)),  # mature giant — offset left+up to clear legend
    (n_companies + 3, "Breakout\nPerformer", (0, 20)),  # mid-tier standout
]
for idx, label, offset in annotations:
    ax.annotate(
        label,
        (revenue[idx], growth_rate[idx] * 100),
        fontsize=13,
        fontweight="bold",
        color="#333333",
        ha="center",
        va="bottom",
        xytext=offset,
        textcoords="offset points",
        arrowprops={"arrowstyle": "-", "color": "#999999", "lw": 0.8},
    )

# Size legend with representative bubble sizes — placed upper left to balance layout
legend_caps = [25, 100, 300]
legend_handles = [
    ax.scatter(
        [], [], s=(v / market_cap.max()) * 2200 + 120, c="#888888", alpha=0.5, edgecolors="white", linewidths=1.2
    )
    for v in legend_caps
]
size_legend = ax.legend(
    legend_handles,
    [f"${v}B" for v in legend_caps],
    title="Market Cap",
    title_fontsize=16,
    fontsize=14,
    loc="upper left",
    framealpha=0.9,
    scatterpoints=1,
    labelspacing=1.8,
    borderpad=1.2,
)
ax.add_artist(size_legend)

# Sector color legend — placed center right where there is open space
sector_legend = ax.legend(
    fontsize=14, loc="center right", framealpha=0.9, title="Sector", title_fontsize=16, markerscale=0.5
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
