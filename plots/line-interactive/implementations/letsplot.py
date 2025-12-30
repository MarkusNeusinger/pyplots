"""pyplots.ai
line-interactive: Interactive Line Chart with Hover and Zoom
Library: lets-plot | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import os

import numpy as np
import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_text,
    geom_line,
    geom_point,
    ggplot,
    ggsave,
    ggsize,
    labs,
    layer_tooltips,
    scale_x_datetime,
    theme,
    theme_minimal,
)


LetsPlot.setup_html()

# Data - Server response time metrics (hourly over ~2 weeks)
np.random.seed(42)
n_points = 350

# Generate timestamps (hourly data for ~2 weeks)
dates = pd.date_range(start="2024-06-01", periods=n_points, freq="h")

# Create realistic server response pattern with daily cycles and trends
hours = np.arange(n_points)
daily_pattern = 15 * np.sin(2 * np.pi * hours / 24 - np.pi / 2)  # Daily cycle
weekly_pattern = 8 * np.sin(2 * np.pi * hours / 168)  # Weekly cycle
trend = 0.02 * hours  # Slight upward trend
noise = np.random.normal(0, 5, n_points)

# Add some anomaly spikes
anomalies = np.zeros(n_points)
anomaly_indices = [50, 120, 200, 280]
for idx in anomaly_indices:
    if idx < n_points:
        anomalies[idx : idx + 3] = np.array([30, 45, 20])[: min(3, n_points - idx)]

response_time = 85 + daily_pattern + weekly_pattern + trend + noise + anomalies
response_time = np.clip(response_time, 20, 200)  # Keep values realistic

df = pd.DataFrame({"datetime": dates, "response_time": response_time})

# Create interactive plot with tooltips
tooltips = layer_tooltips().line("@datetime").line("Response Time: @response_time ms")

plot = (
    ggplot(df, aes(x="datetime", y="response_time"))
    + geom_line(color="#306998", size=1.2, alpha=0.8)
    + geom_point(color="#FFD43B", size=2, alpha=0.6, tooltips=tooltips)
    + scale_x_datetime()
    + labs(title="line-interactive · lets-plot · pyplots.ai", x="Date/Time", y="Response Time (ms)")
    + theme_minimal()
    + theme(
        plot_title=element_text(size=24),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        legend_text=element_text(size=16),
    )
    + ggsize(1600, 900)  # 1600x900 * scale=3 = 4800x2700 px
)

# Save as PNG (static preview) and HTML (interactive with zoom/pan/hover)
script_dir = os.path.dirname(os.path.abspath(__file__))
ggsave(plot, os.path.join(script_dir, "plot.png"), scale=3)
ggsave(plot, os.path.join(script_dir, "plot.html"))
