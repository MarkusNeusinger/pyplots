"""anyplot.ai
line-multi: Multi-Line Comparison Plot
Library: letsplot | Python 3.13
Quality: pending | Created: 2026-05-06
"""

import os

import numpy as np
import pandas as pd
from lets_plot import *


LetsPlot.setup_html()

# Theme tokens
THEME = os.getenv("ANYPLOT_THEME", "light")
PAGE_BG = "#FAF8F1" if THEME == "light" else "#1A1A17"
ELEVATED_BG = "#FFFDF6" if THEME == "light" else "#242420"
INK = "#1A1A17" if THEME == "light" else "#F0EFE8"
INK_SOFT = "#4A4A44" if THEME == "light" else "#B8B7B0"
RULE = "rgba(26,26,23,0.10)" if THEME == "light" else "rgba(240,239,232,0.10)"

# Okabe-Ito palette
OKABE_ITO = ["#009E73", "#D55E00", "#0072B2"]

# Data: Monthly sales for 3 product lines over 12 months
np.random.seed(42)
months = np.arange(1, 13)
month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Generate realistic sales data with distinct trends
electronics = 150 + np.cumsum(np.random.randn(12) * 8) + np.linspace(0, 40, 12)
clothing = 120 + np.cumsum(np.random.randn(12) * 6) + np.sin(np.linspace(0, 2 * np.pi, 12)) * 20
home_goods = 90 + np.cumsum(np.random.randn(12) * 5) + np.linspace(0, 25, 12)

# Create long-format DataFrame for ggplot
df = pd.DataFrame(
    {
        "Month": np.tile(months, 3),
        "MonthLabel": np.tile(month_labels, 3),
        "Sales": np.concatenate([electronics, clothing, home_goods]),
        "Product Line": np.repeat(["Electronics", "Clothing", "Home Goods"], 12),
    }
)

# Plot
plot = (
    ggplot(df, aes(x="Month", y="Sales", color="Product Line"))
    + geom_line(size=2.5)
    + geom_point(size=5, alpha=0.9)
    + scale_color_manual(values=OKABE_ITO)
    + scale_x_continuous(breaks=months.tolist(), labels=month_labels)
    + labs(title="line-multi · letsplot · anyplot.ai", x="Month", y="Sales (thousands USD)")
    + theme(
        plot_background=element_rect(fill=PAGE_BG, color=PAGE_BG),
        panel_background=element_rect(fill=PAGE_BG, color=PAGE_BG),
        panel_grid_major=element_line(color=RULE, size=0.3),
        panel_grid_minor=element_blank(),
        axis_title=element_text(size=20, color=INK),
        axis_text=element_text(size=16, color=INK_SOFT),
        plot_title=element_text(size=24, color=INK),
        legend_title=element_text(size=16, color=INK),
        legend_text=element_text(size=16, color=INK_SOFT),
        legend_background=element_rect(fill=ELEVATED_BG, color=INK_SOFT),
        legend_position="right",
    )
    + ggsize(1600, 900)
)

# Save PNG (scale 3x for 4800 × 2700 px)
ggsave(plot, f"plot-{THEME}.png", scale=3, path=".")

# Save HTML for interactivity
ggsave(plot, f"plot-{THEME}.html", path=".")
