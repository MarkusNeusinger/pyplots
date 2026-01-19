"""pyplots.ai
map-route-path: Route Path Map
Library: lets-plot | Python 3.13
Quality: pending | Created: 2026-01-19
"""

import numpy as np
import pandas as pd
from lets_plot import *


LetsPlot.setup_html()

# Generate a realistic hiking trail route (simulated GPS track)
np.random.seed(42)

# Starting point (approximate coordinates for a scenic trail area)
start_lat, start_lon = 46.85, 9.85  # Near Swiss Alps area

# Generate 150 waypoints for a hiking trail
n_points = 150

# Create a winding path with natural-looking movement
t = np.linspace(0, 4 * np.pi, n_points)

# Path with curves and some elevation-driven meandering
lat_offset = np.cumsum(np.sin(t) * 0.002 + np.random.randn(n_points) * 0.0003)
lon_offset = np.cumsum(np.cos(t * 0.7) * 0.003 + np.random.randn(n_points) * 0.0004)

lat = start_lat + lat_offset
lon = start_lon + lon_offset

# Sequence numbers and timestamps
sequence = np.arange(n_points)
base_time = pd.Timestamp("2026-01-19 08:00:00")
timestamps = [base_time + pd.Timedelta(minutes=i * 2) for i in range(n_points)]

# Create DataFrame
df = pd.DataFrame(
    {
        "lat": lat,
        "lon": lon,
        "sequence": sequence,
        "timestamp": timestamps,
        "progress": sequence / (n_points - 1) * 100,  # 0-100% progress
    }
)

# Start and end points for markers
start_point = df.iloc[[0]].copy()
end_point = df.iloc[[-1]].copy()

# Create the plot with path and markers
plot = (
    ggplot()
    # Main route path with color gradient showing progress
    + geom_path(aes(x="lon", y="lat", color="progress"), data=df, size=2.5, alpha=0.9)
    # Start marker (green circle)
    + geom_point(aes(x="lon", y="lat"), data=start_point, color="#22C55E", size=8, shape=21, fill="#22C55E", stroke=2)
    # End marker (red square)
    + geom_point(aes(x="lon", y="lat"), data=end_point, color="#DC2626", size=8, shape=22, fill="#DC2626", stroke=2)
    # Color scale for progress (blue to yellow - Python colors)
    + scale_color_gradient(low="#306998", high="#FFD43B", name="Progress (%)")
    # Labels
    + labs(x="Longitude", y="Latitude", title="map-route-path · letsplot · pyplots.ai")
    # Theme with larger text
    + theme_minimal()
    + theme(
        plot_title=element_text(size=24, face="bold"),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        legend_title=element_text(size=18),
        legend_text=element_text(size=14),
        legend_position="right",
    )
    # Figure size (will be 4800x2700 with scale=3)
    + ggsize(1600, 900)
    # Fixed aspect ratio for geographic data
    + coord_fixed(ratio=1.0)
)

# Save as PNG (scale 3x for 4800x2700 px)
ggsave(plot, "plot.png", path=".", scale=3)

# Save interactive HTML version
ggsave(plot, "plot.html", path=".")
