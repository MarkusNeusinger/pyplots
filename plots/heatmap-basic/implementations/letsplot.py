""" pyplots.ai
heatmap-basic: Basic Heatmap
Library: letsplot 4.8.2 | Python 3.14.3
Quality: 86/100 | Updated: 2026-02-15
"""

import numpy as np
from lets_plot import (
    LetsPlot,
    aes,
    element_blank,
    element_text,
    geom_text,
    geom_tile,
    ggplot,
    ggsize,
    labs,
    layer_tooltips,
    scale_color_identity,
    scale_fill_gradient,
    scale_x_discrete,
    scale_y_discrete,
    theme,
    theme_minimal,
)
from lets_plot.export import ggsave


LetsPlot.setup_html()

# Data - Monthly energy consumption (kWh) by building zone
np.random.seed(42)
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
zones = ["Lobby", "Offices", "Lab", "Server Room", "Cafeteria", "Warehouse"]

# Realistic patterns: seasonal variation + zone-specific baselines
baselines = np.array([120, 280, 350, 520, 180, 90])
seasonal = np.array([1.3, 1.2, 1.0, 0.8, 0.7, 0.75, 0.85, 0.9, 0.8, 0.9, 1.1, 1.25])

values = np.outer(seasonal, baselines)
noise = np.random.normal(0, 15, (len(months), len(zones)))
values = np.round(values + noise, 0).astype(int)

# Build long-form data with adaptive text color computed per cell
zone_col, month_col, kwh_col = [], [], []
for i, month in enumerate(months):
    for j, zone in enumerate(zones):
        zone_col.append(zone)
        month_col.append(month)
        kwh_col.append(int(values[i, j]))

median_val = int(np.median(kwh_col))
text_color = ["white" if v > median_val else "#1a1a2e" for v in kwh_col]

data = {"Zone": zone_col, "Month": month_col, "kWh": kwh_col, "label_color": text_color}

# Heatmap with interactive tooltips and adaptive annotations
plot = (
    ggplot(data, aes(x="Zone", y="Month", fill="kWh"))
    + geom_tile(
        width=0.92,
        height=0.92,
        tooltips=layer_tooltips()
        .line("@Zone | @Month")
        .line("Energy: @kWh kWh")
        .line("Median: " + str(median_val) + " kWh"),
    )
    + geom_text(aes(label="kWh", color="label_color"), size=12, fontface="bold")
    + scale_color_identity()
    + scale_fill_gradient(low="#e8f0fe", high="#0d1b3e", name="Energy (kWh)")
    + scale_x_discrete(limits=zones)
    + scale_y_discrete(limits=months[::-1])
    + labs(x="Building Zone", y="Month", title="heatmap-basic · letsplot · pyplots.ai")
    + theme_minimal()
    + theme(
        plot_title=element_text(size=24, face="bold"),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        legend_text=element_text(size=14),
        legend_title=element_text(size=16),
        panel_grid=element_blank(),
    )
    + ggsize(1600, 900)
)

# Save PNG (scale=3 gives 4800x2700)
ggsave(plot, "plot.png", path=".", scale=3)

# Save HTML for interactivity
ggsave(plot, "plot.html", path=".")
