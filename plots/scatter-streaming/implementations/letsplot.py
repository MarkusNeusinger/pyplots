"""pyplots.ai
scatter-streaming: Streaming Scatter Plot
Library: lets-plot | Python 3.13
Quality: pending | Created: 2025-01-19
"""

import numpy as np
import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_text,
    geom_point,
    ggplot,
    ggsave,
    ggsize,
    labs,
    scale_alpha,
    scale_color_gradient,
    theme,
    theme_minimal,
)


LetsPlot.setup_html()

# Data - Simulated streaming sensor readings
np.random.seed(42)
n_points = 200

# Simulate arrival times over ~20 seconds
timestamps = pd.date_range("2025-01-19 10:00:00", periods=n_points, freq="100ms")

# Sensor readings with some correlation and drift
base_x = np.cumsum(np.random.randn(n_points) * 0.3) + 25  # Temperature-like
base_y = base_x * 0.6 + np.random.randn(n_points) * 3 + 40  # Humidity-like

# Create age values for opacity (0 = oldest, 1 = newest)
age = np.linspace(0, 1, n_points)

df = pd.DataFrame({"x": base_x, "y": base_y, "timestamp": timestamps, "age": age, "alpha_value": 0.2 + age * 0.7})

# Create plot - scatter with opacity encoding for point age
plot = (
    ggplot(df, aes(x="x", y="y", color="age", alpha="alpha_value"))
    + geom_point(size=5)
    + scale_color_gradient(low="#1a365d", high="#306998", name="Recency")
    + scale_alpha(range=[0.15, 0.9], guide="none")
    + labs(x="Temperature (°C)", y="Humidity (%)", title="scatter-streaming · letsplot · pyplots.ai")
    + theme_minimal()
    + theme(
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24),
        legend_title=element_text(size=18),
        legend_text=element_text(size=14),
    )
    + ggsize(1600, 900)
)

# Save with 3x scale for 4800x2700 px output
ggsave(plot, "plot.png", path=".", scale=3)

# Save interactive HTML version
ggsave(plot, "plot.html", path=".")
