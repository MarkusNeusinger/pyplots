"""pyplots.ai
bubble-basic: Basic Bubble Chart
Library: letsplot 4.8.2 | Python 3.14.3
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

# Data - market analysis: companies by revenue, growth rate, and market share
np.random.seed(42)

# (sector, count, rev_low, rev_high, growth_base, growth_slope, share_mean)
# Distinct sector profiles: Tech = high-growth startups, Energy = large stable firms
sector_specs = [
    ("Technology", 10, 15, 120, 28, -0.10, 10),
    ("Healthcare", 10, 20, 140, 18, -0.04, 14),
    ("Finance", 9, 50, 200, 10, -0.02, 20),
    ("Energy", 8, 60, 195, 7, -0.01, 22),
    ("Consumer Goods", 8, 10, 130, 15, -0.05, 12),
]

rows = []
for sector, count, r_lo, r_hi, g_base, g_slope, s_mean in sector_specs:
    rev = np.random.uniform(r_lo, r_hi, count)
    growth = g_base + g_slope * rev + np.random.randn(count) * 2.5
    share = np.clip(np.random.randn(count) * 5 + s_mean, 2, 30)
    for r, g, s in zip(rev, growth, share, strict=True):
        rows.append({"revenue": r, "growth_rate": g, "market_share": s, "sector": sector})

df = pd.DataFrame(rows)

# Palette: Python Blue first, colorblind-safe complementary colors
palette = ["#306998", "#E5883E", "#2A9D8F", "#8B5CF6", "#E63946"]

# Plot
plot = (
    ggplot(df, aes(x="revenue", y="growth_rate", size="market_share", color="sector"))
    + geom_point(
        alpha=0.7,
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
        color="#444444",
        size=1.5,
        alpha=0.12,
        inherit_aes=False,
        show_legend=False,
    )
    + scale_size_area(max_size=24, name="Market Share (%)", breaks=[5, 10, 15, 20, 25])
    + scale_color_manual(values=palette, name="Sector")
    + guides(
        color=guide_legend(override_aes={"size": 7}), size=guide_legend(override_aes={"color": "#306998", "alpha": 0.7})
    )
    + labs(x="Revenue (Million USD)", y="Growth Rate (%)", title="bubble-basic · letsplot · pyplots.ai")
    + theme_minimal()
    + theme(
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24),
        legend_title=element_text(size=16),
        legend_text=element_text(size=14),
        panel_grid_major=element_line(size=0.3, color="#E0E0E0"),
        panel_grid_minor=element_blank(),
        legend_position="bottom",
        legend_direction="horizontal",
        legend_box="horizontal",
        legend_box_spacing=5,
    )
    + ggsize(1600, 900)
)

# Save
ggsave(plot, "plot.png", path=".", scale=3)
plot.to_html("plot.html")
