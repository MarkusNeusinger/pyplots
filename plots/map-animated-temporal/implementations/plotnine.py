"""pyplots.ai
map-animated-temporal: Animated Map over Time
Library: plotnine | Python 3.13
Quality: pending | Created: 2025-01-20
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    coord_fixed,
    element_rect,
    element_text,
    facet_wrap,
    geom_point,
    ggplot,
    labs,
    scale_color_gradient,
    scale_size_continuous,
    theme,
    theme_minimal,
)


# Data - Simulated earthquake aftershock sequence across California region
np.random.seed(42)

# Time steps (6 days of aftershocks for small multiples grid)
n_timesteps = 6
timestamps = pd.date_range("2024-03-01", periods=n_timesteps, freq="D")

# Generate earthquake aftershock data spreading from epicenter
epicenter_lat, epicenter_lon = 36.0, -118.5
data_rows = []

for i, ts in enumerate(timestamps):
    # Number of points increases then decreases (aftershock pattern)
    n_points = int(30 + 20 * np.sin(np.pi * i / (n_timesteps - 1)))
    # Spread increases over time
    spread = 0.5 + i * 0.3

    for _ in range(n_points):
        lat = epicenter_lat + np.random.normal(0, spread)
        lon = epicenter_lon + np.random.normal(0, spread * 1.2)
        # Magnitude decreases over time (aftershocks get weaker)
        magnitude = max(1.0, 5.5 - i * 0.3 + np.random.exponential(0.8))
        data_rows.append(
            {
                "lat": lat,
                "lon": lon,
                "timestamp": ts,
                "magnitude": magnitude,
                "day": f"Day {i + 1}: {ts.strftime('%b %d')}",
            }
        )

df = pd.DataFrame(data_rows)

# Order factor for facets
day_order = [f"Day {i + 1}: {ts.strftime('%b %d')}" for i, ts in enumerate(timestamps)]
df["day"] = pd.Categorical(df["day"], categories=day_order, ordered=True)

# Create small multiples visualization
plot = (
    ggplot(df, aes(x="lon", y="lat", color="magnitude", size="magnitude"))
    + geom_point(alpha=0.7)
    + facet_wrap("~day", ncol=3)
    + scale_color_gradient(low="#FFD43B", high="#C73E1D", name="Magnitude")
    + scale_size_continuous(range=(2, 8), name="Magnitude")
    + coord_fixed(ratio=1.0)
    + labs(
        title="Earthquake Aftershock Sequence · map-animated-temporal · plotnine · pyplots.ai",
        subtitle="Small multiples showing spatial spread of aftershocks over 6 days",
        x="Longitude",
        y="Latitude",
    )
    + theme_minimal()
    + theme(
        figure_size=(16, 10),
        plot_title=element_text(size=22, weight="bold"),
        plot_subtitle=element_text(size=16),
        axis_title=element_text(size=16),
        axis_text=element_text(size=12),
        strip_text=element_text(size=14, weight="bold"),
        legend_title=element_text(size=14),
        legend_text=element_text(size=12),
        panel_background=element_rect(fill="#E8F4F8"),
        plot_background=element_rect(fill="white"),
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
