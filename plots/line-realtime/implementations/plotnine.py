""" pyplots.ai
line-realtime: Real-Time Updating Line Chart
Library: plotnine 0.15.2 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-31
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    annotate,
    element_rect,
    element_text,
    geom_line,
    geom_point,
    ggplot,
    guides,
    labs,
    scale_alpha_continuous,
    theme,
    theme_minimal,
)


# Data - Simulated CPU usage with sliding window effect
np.random.seed(42)

# Generate 100 time points, showing last 60 as "visible window"
n_total = 100
n_visible = 60

# Create timestamps for the visible window
end_time = pd.Timestamp("2025-01-15 14:32:45")
timestamps = pd.date_range(end=end_time, periods=n_visible, freq="100ms")

# Generate CPU usage data with realistic fluctuations
base_cpu = 45
trend = np.linspace(0, 10, n_visible)  # Slight upward trend
noise = np.cumsum(np.random.randn(n_visible) * 2)  # Random walk component
spike_idx = [15, 35, 50]  # CPU spikes
spikes = np.zeros(n_visible)
for idx in spike_idx:
    spikes[max(0, idx - 2) : min(n_visible, idx + 3)] += np.array(
        [5, 15, 25, 15, 5][: min(5, n_visible - max(0, idx - 2))]
    )

cpu_values = base_cpu + trend + noise + spikes
cpu_values = np.clip(cpu_values, 5, 95)  # Keep within realistic bounds

# Create alpha values for fade effect (older data fades out)
alpha_values = np.linspace(0.3, 1.0, n_visible)

# Create DataFrame
df = pd.DataFrame(
    {
        "timestamp": timestamps,
        "cpu": cpu_values,
        "alpha": alpha_values,
        "time_seconds": np.arange(n_visible) * 0.1,  # Time in seconds for easier plotting
    }
)

# Current (latest) value for annotation
current_value = cpu_values[-1]
current_time = df["time_seconds"].iloc[-1]

# Create a secondary dataframe for the gradient effect (multiple overlapping lines)
# This simulates the fade effect by drawing lines with decreasing alpha
gradient_segments = []
segment_size = 5
for i in range(0, n_visible - 1, segment_size):
    end_idx = min(i + segment_size + 1, n_visible)
    segment_df = df.iloc[i:end_idx].copy()
    segment_df["segment"] = i
    segment_df["segment_alpha"] = alpha_values[i]
    gradient_segments.append(segment_df)

gradient_df = pd.concat(gradient_segments, ignore_index=True)

# Plot
plot = (
    ggplot()
    # Main line with gradient effect using segments
    + geom_line(
        data=gradient_df,
        mapping=aes(x="time_seconds", y="cpu", group="segment", alpha="segment_alpha"),
        color="#306998",
        size=2,
    )
    # Points at key intervals for visibility
    + geom_point(data=df.iloc[::10], mapping=aes(x="time_seconds", y="cpu"), color="#306998", size=3, alpha=0.7)
    # Highlight the latest point (live indicator)
    + geom_point(data=df.iloc[[-1]], mapping=aes(x="time_seconds", y="cpu"), color="#FFD43B", size=6, stroke=2)
    + geom_point(data=df.iloc[[-1]], mapping=aes(x="time_seconds", y="cpu"), color="#FF4444", size=3)
    # Current value annotation
    + annotate(
        "text",
        x=current_time + 0.3,
        y=current_value,
        label=f"{current_value:.1f}%",
        color="#306998",
        size=14,
        ha="left",
        fontweight="bold",
    )
    # "LIVE" indicator
    + annotate("text", x=current_time, y=92, label="● LIVE", color="#FF4444", size=12, ha="right", fontweight="bold")
    # Scrolling direction indicator (arrow at left edge)
    + annotate("text", x=0.2, y=current_value - 5, label="◀ older data", color="#888888", size=10, ha="left", alpha=0.6)
    # Labels and theme
    + labs(title="line-realtime · plotnine · pyplots.ai", x="Time (seconds)", y="CPU Usage (%)")
    + scale_alpha_continuous(range=(0.3, 1.0))
    + guides(alpha="none")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=24, weight="bold"),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        panel_grid_major=element_text(color="#CCCCCC"),
        panel_background=element_rect(fill="#FAFAFA"),
        plot_background=element_rect(fill="white"),
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
