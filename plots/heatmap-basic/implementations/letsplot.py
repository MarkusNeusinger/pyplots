"""pyplots.ai
heatmap-basic: Basic Heatmap
Library: letsplot 4.8.2 | Python 3.14.3
Quality: /100 | Updated: 2026-02-15
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
    scale_fill_gradient2,
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

# Build long-form data as dict lists
zone_col, month_col, kwh_col = [], [], []
for i, month in enumerate(months):
    for j, zone in enumerate(zones):
        zone_col.append(zone)
        month_col.append(month)
        kwh_col.append(int(values[i, j]))

data = {"Zone": zone_col, "Month": month_col, "kWh": kwh_col}

# Split for adaptive text color (dark on light cells, white on dark)
median_val = int(np.median(kwh_col))
light_data = {"Zone": [], "Month": [], "kWh": []}
dark_data = {"Zone": [], "Month": [], "kWh": []}
for z, m, v in zip(zone_col, month_col, kwh_col, strict=True):
    target = dark_data if v > median_val else light_data
    target["Zone"].append(z)
    target["Month"].append(m)
    target["kWh"].append(v)

# Heatmap with interactive tooltips
plot = (
    ggplot(data, aes(x="Zone", y="Month", fill="kWh"))
    + geom_tile(width=0.92, height=0.92, tooltips=layer_tooltips().line("@Zone | @Month").line("Energy: @kWh kWh"))
    + geom_text(aes(label="kWh"), data=light_data, size=12, fontface="bold", color="#1a1a2e")
    + geom_text(aes(label="kWh"), data=dark_data, size=12, fontface="bold", color="white")
    + scale_fill_gradient2(low="#f0f4ff", mid="#4a90d9", high="#1a1a2e", midpoint=median_val, name="Energy\n(kWh)")
    + scale_x_discrete(limits=zones)
    + scale_y_discrete(limits=months[::-1])
    + labs(x="Building Zone", y="", title="heatmap-basic · letsplot · pyplots.ai")
    + theme_minimal()
    + theme(
        plot_title=element_text(size=24, face="bold"),
        axis_title_x=element_text(size=20),
        axis_title_y=element_blank(),
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
