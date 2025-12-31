"""pyplots.ai
line-realtime: Real-Time Updating Line Chart
Library: lets-plot | Python 3.13
Quality: pending | Created: 2025-12-31
"""

import numpy as np
import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_blank,
    element_line,
    element_text,
    geom_area,
    geom_hline,
    geom_line,
    geom_point,
    geom_text,
    ggplot,
    ggsize,
    labs,
    scale_alpha_identity,
    scale_y_continuous,
    theme,
    theme_minimal,
)
from lets_plot.export import ggsave


LetsPlot.setup_html()

# Data - Simulated CPU usage with real-time streaming effect
np.random.seed(42)
n_points = 100

# Generate realistic CPU usage with some noise and occasional spikes
base_usage = 35 + 15 * np.sin(np.linspace(0, 4 * np.pi, n_points))  # Oscillating base
noise = np.random.normal(0, 5, n_points)
spikes = np.zeros(n_points)
spike_indices = [25, 48, 72, 88]
for idx in spike_indices:
    spikes[idx : idx + 3] = np.array([15, 25, 10])[: min(3, n_points - idx)]
cpu_usage = np.clip(base_usage + noise + spikes, 0, 100)

# Create alpha gradient for fade effect (older points fade out)
alpha_values = np.linspace(0.2, 1.0, n_points)

# Use numeric index for x-axis
df = pd.DataFrame({"x_idx": range(n_points), "cpu_usage": cpu_usage, "alpha": alpha_values})

# Get latest value for annotation
latest_value = cpu_usage[-1]

# Create annotation dataframes
annotation_current = pd.DataFrame(
    {"x_idx": [n_points - 1], "cpu_usage": [latest_value + 8], "label": [f"Current: {latest_value:.1f}%"]}
)
annotation_fade = pd.DataFrame({"x_idx": [5], "cpu_usage": [10], "label": ["← older data fades"]})
annotation_threshold = pd.DataFrame({"x_idx": [n_points - 1], "cpu_usage": [83], "label": ["Warning threshold"]})

# Create the plot with streaming visualization effect
plot = (
    ggplot(df, aes(x="x_idx", y="cpu_usage"))
    # Main line
    + geom_line(color="#306998", size=2.5, alpha=0.9)
    # Add area fill for visual depth
    + geom_area(fill="#306998", alpha=0.15)
    # Add points with size/alpha gradient to show streaming direction
    + geom_point(aes(alpha="alpha"), color="#306998", size=3, show_legend=False)
    # Highlight the latest point prominently
    + geom_point(
        data=df.tail(1),
        mapping=aes(x="x_idx", y="cpu_usage"),
        color="#FFD43B",
        size=8,
        shape=21,
        fill="#FFD43B",
        stroke=2,
    )
    # Add horizontal reference lines for CPU thresholds
    + geom_hline(yintercept=80, linetype="dashed", color="#DC2626", alpha=0.6, size=1)
    + geom_hline(yintercept=50, linetype="dotted", color="#888888", alpha=0.4, size=0.8)
    # Add text annotations using geom_text
    + geom_text(
        data=annotation_current,
        mapping=aes(x="x_idx", y="cpu_usage", label="label"),
        color="#FFD43B",
        size=16,
        fontface="bold",
        hjust=1,
    )
    + geom_text(
        data=annotation_fade, mapping=aes(x="x_idx", y="cpu_usage", label="label"), color="#888888", size=12, hjust=0
    )
    + geom_text(
        data=annotation_threshold,
        mapping=aes(x="x_idx", y="cpu_usage", label="label"),
        color="#DC2626",
        size=11,
        hjust=1,
    )
    # Labels and title
    + labs(title="line-realtime · letsplot · pyplots.ai", x="Time (samples at 100ms interval)", y="CPU Usage (%)")
    # Scale configuration
    + scale_y_continuous(limits=[0, 100], breaks=[0, 25, 50, 75, 100])
    + scale_alpha_identity()
    # Theme for large canvas
    + theme_minimal()
    + theme(
        plot_title=element_text(size=28, face="bold"),
        axis_title=element_text(size=22),
        axis_text=element_text(size=16),
        panel_grid_major=element_line(color="#cccccc", size=0.5),
        panel_grid_minor=element_blank(),
    )
    # Set figure size (will be scaled 3x to 4800x2700)
    + ggsize(1600, 900)
)

# Save PNG (scale=3 gives 4800x2700)
ggsave(plot, "plot.png", path=".", scale=3)

# Save HTML for interactivity
ggsave(plot, "plot.html", path=".")
