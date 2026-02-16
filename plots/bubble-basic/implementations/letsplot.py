"""pyplots.ai
bubble-basic: Basic Bubble Chart
Library: letsplot 4.8.2 | Python 3.14.3
Quality: 80/100 | Updated: 2026-02-15
"""

import numpy as np
import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_blank,
    element_line,
    element_text,
    geom_point,
    geom_smooth,
    ggplot,
    ggsave,
    ggsize,
    guide_legend,
    guides,
    labs,
    layer_tooltips,
    scale_color_manual,
    scale_size_area,
    theme,
    theme_minimal,
)


LetsPlot.setup_html()

# Data - market analysis: companies across sectors by revenue, growth, and market share
np.random.seed(42)
n = 45

sectors = ["Technology", "Healthcare", "Finance", "Energy", "Consumer Goods"]
sector_props = {
    "Technology": {"rev_range": (20, 180), "growth_base": 22, "growth_slope": -0.06},
    "Healthcare": {"rev_range": (15, 150), "growth_base": 18, "growth_slope": -0.05},
    "Finance": {"rev_range": (30, 200), "growth_base": 12, "growth_slope": -0.03},
    "Energy": {"rev_range": (25, 190), "growth_base": 10, "growth_slope": -0.02},
    "Consumer Goods": {"rev_range": (10, 160), "growth_base": 15, "growth_slope": -0.04},
}

data = {"revenue": [], "growth_rate": [], "market_share": [], "sector": []}
counts = [10, 10, 9, 8, 8]

for sector, count in zip(sectors, counts, strict=True):
    props = sector_props[sector]
    rev = np.random.uniform(*props["rev_range"], count)
    growth = props["growth_base"] + props["growth_slope"] * rev + np.random.randn(count) * 4
    share = np.abs(np.random.randn(count) * 7 + 13)
    data["revenue"].extend(rev)
    data["growth_rate"].extend(growth)
    data["market_share"].extend(share)
    data["sector"].extend([sector] * count)

df = pd.DataFrame(data)

# Palette: Python Blue first, then cohesive complementary colors (colorblind-safe)
palette = ["#306998", "#E5883E", "#2A9D8F", "#8B5CF6", "#E63946"]

# Plot
plot = (
    ggplot(df, aes(x="revenue", y="growth_rate", size="market_share", color="sector"))
    + geom_point(
        alpha=0.65,
        tooltips=layer_tooltips()
        .format("revenue", "${.1f}M")
        .format("growth_rate", "{.1f}%")
        .format("market_share", "{.1f}%")
        .line("@sector")
        .line("Revenue|@revenue")
        .line("Growth|@growth_rate")
        .line("Market Share|@market_share"),
    )
    + geom_smooth(
        aes(x="revenue", y="growth_rate"),
        method="loess",
        color="#555555",
        size=1.2,
        alpha=0.15,
        inherit_aes=False,
        show_legend=False,
    )
    + scale_size_area(max_size=22, name="Market Share (%)", breaks=[5, 10, 15, 20, 25])
    + scale_color_manual(values=palette, name="Sector")
    + guides(
        color=guide_legend(override_aes={"size": 8}), size=guide_legend(override_aes={"color": "#306998", "alpha": 0.7})
    )
    + labs(x="Revenue (Million USD)", y="Growth Rate (%)", title="bubble-basic · letsplot · pyplots.ai")
    + theme_minimal()
    + theme(
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24),
        legend_title=element_text(size=18),
        legend_text=element_text(size=14),
        panel_grid_major=element_line(size=0.4, color="#E8E8E8"),
        panel_grid_minor=element_blank(),
        legend_position="right",
    )
    + ggsize(1600, 900)
)

# Save
ggsave(plot, "plot.png", path=".", scale=3)
plot.to_html("plot.html")
