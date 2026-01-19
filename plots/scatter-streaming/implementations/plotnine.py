"""pyplots.ai
scatter-streaming: Streaming Scatter Plot
Library: plotnine | Python 3.13
Quality: pending | Created: 2026-01-19
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_blank,
    element_text,
    geom_point,
    ggplot,
    guides,
    labs,
    scale_alpha_continuous,
    scale_color_gradient,
    theme,
    theme_minimal,
)


# Data - Simulated streaming sensor data (temperature vs humidity)
np.random.seed(42)
n_points = 200

# Simulate streaming data arriving over time
timestamps = pd.date_range("2026-01-19 10:00:00", periods=n_points, freq="500ms")

# Generate correlated sensor readings with some drift over time
base_temp = 22 + np.cumsum(np.random.randn(n_points) * 0.1)  # Temperature baseline drifts
base_humidity = 55 + np.cumsum(np.random.randn(n_points) * 0.15)  # Humidity baseline drifts

# Add measurement noise
temperature = base_temp + np.random.randn(n_points) * 0.5
humidity = base_humidity + np.random.randn(n_points) * 1.0

# Calculate point age (0 = oldest, 1 = newest) for opacity encoding
point_age = np.linspace(0, 1, n_points)

df = pd.DataFrame(
    {
        "temperature": temperature,
        "humidity": humidity,
        "timestamp": timestamps,
        "age": point_age,
        "alpha_value": 0.2 + point_age * 0.8,  # Opacity: 0.2 (oldest) to 1.0 (newest)
    }
)

# Create streaming scatter plot with age-based opacity
plot = (
    ggplot(df, aes(x="temperature", y="humidity", alpha="alpha_value", color="age"))
    + geom_point(size=4)
    + scale_alpha_continuous(range=(0.15, 1.0))
    + scale_color_gradient(low="#306998", high="#FFD43B")
    + guides(alpha=False, color=False)
    + labs(x="Temperature (C)", y="Humidity (%)", title="scatter-streaming \u00b7 plotnine \u00b7 pyplots.ai")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24),
        legend_position="none",
        panel_grid_minor=element_blank(),
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
