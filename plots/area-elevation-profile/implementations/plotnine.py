""" pyplots.ai
area-elevation-profile: Terrain Elevation Profile Along Transect
Library: plotnine 0.15.3 | Python 3.14.3
Quality: 82/100 | Created: 2026-03-15
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    annotate,
    element_blank,
    element_line,
    element_rect,
    element_text,
    geom_area,
    geom_line,
    geom_segment,
    ggplot,
    labs,
    scale_x_continuous,
    scale_y_continuous,
    theme,
    theme_minimal,
)


# Data - Alpine hiking trail elevation profile (~120 km)
np.random.seed(42)
n_points = 480
distance = np.linspace(0, 120, n_points)

# Build terrain with controlled peaks at landmark locations
elevation = np.full(n_points, 800.0)
# Major peaks
elevation += 500 * np.exp(-((distance - 18) ** 2) / 50)  # Kleine Scheidegg
elevation += 900 * np.exp(-((distance - 35) ** 2) / 80)  # Jungfraujoch (highest)
elevation += 650 * np.exp(-((distance - 62) ** 2) / 60)  # Mürren
elevation += 750 * np.exp(-((distance - 78) ** 2) / 70)  # Schilthorn
elevation += 400 * np.exp(-((distance - 98) ** 2) / 90)  # Kandersteg
# Broad rolling hills
elevation += 200 * np.sin(distance * np.pi / 20 + 0.8)
elevation += 100 * np.sin(distance * np.pi / 10 + 1.5)
# Small terrain noise
elevation += np.random.normal(0, 15, n_points)
# Smooth
elevation = pd.Series(elevation).rolling(window=8, center=True, min_periods=1).mean().values.copy()
# Valley towns at start and end
elevation[:12] = np.linspace(580, elevation[12], 12)
elevation[-12:] = np.linspace(elevation[-12], 620, 12)

df = pd.DataFrame({"distance": distance, "elevation": elevation})

# Landmarks
landmark_distances = [0, 18, 35, 50, 62, 78, 98, 120]
landmark_names = [
    "Grindelwald",
    "Kleine Scheidegg",
    "Jungfraujoch",
    "Lauterbrunnen",
    "Mürren",
    "Schilthorn",
    "Kandersteg",
    "Adelboden",
]
landmark_elevations = []
for d in landmark_distances:
    idx = np.argmin(np.abs(distance - d))
    landmark_elevations.append(elevation[idx])

landmarks = pd.DataFrame({"name": landmark_names, "distance": landmark_distances, "elevation": landmark_elevations})

# Y-axis
y_min = 300
y_max = int(np.ceil(elevation.max() / 100) * 100) + 250

# Plot
plot = (
    ggplot(df, aes(x="distance", y="elevation"))
    + geom_area(fill="#306998", alpha=0.3)
    + geom_line(color="#1a3d5c", size=1.4)
)

# Landmark marker lines (vertical segments from elevation to label position)
for _, row in landmarks.iterrows():
    plot = plot + geom_segment(
        aes(x="distance", xend="distance", y="elevation", yend="label_y"),
        data=pd.DataFrame(
            {"distance": [row["distance"]], "elevation": [row["elevation"]], "label_y": [row["elevation"] + 160]}
        ),
        color="#888888",
        linetype="dotted",
        size=0.5,
    )

# Landmark points
plot = plot + annotate(
    "point",
    x=landmarks["distance"].values,
    y=landmarks["elevation"].values,
    size=3.5,
    color="#1a3d5c",
    fill="#FFD43B",
    stroke=0.8,
)

# Landmark labels
for _, row in landmarks.iterrows():
    ha = "center"
    if row["distance"] < 5:
        ha = "left"
    elif row["distance"] > 115:
        ha = "right"

    plot = plot + annotate(
        "text",
        x=row["distance"],
        y=row["elevation"] + 180,
        label=f"{row['name']}\n{int(row['elevation']):,} m",
        size=7.5,
        color="#2d2d2d",
        ha=ha,
        va="bottom",
        fontweight="bold",
    )

# Style
plot = (
    plot
    + labs(
        x="Distance (km)",
        y="Elevation (m)",
        title="area-elevation-profile · plotnine · pyplots.ai",
        subtitle="Alpine Trail: Grindelwald to Adelboden (120 km) · Vertical exaggeration ~10×",
    )
    + scale_x_continuous(breaks=range(0, 130, 10))
    + scale_y_continuous(limits=(y_min, y_max))
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14, color="#2d2d2d"),
        axis_title=element_text(size=20, color="#2d2d2d"),
        axis_text=element_text(size=16, color="#555555"),
        plot_title=element_text(size=24, weight="bold", color="#1a1a1a"),
        plot_subtitle=element_text(size=16, color="#555555", style="italic"),
        panel_background=element_rect(fill="#f8f9fa", color="none"),
        plot_background=element_rect(fill="#ffffff", color="none"),
        panel_grid_major_y=element_line(color="#d0d0d0", size=0.4),
        panel_grid_major_x=element_blank(),
        panel_grid_minor=element_blank(),
        axis_line_x=element_line(color="#999999", size=0.6),
        axis_ticks_major_x=element_line(color="#999999", size=0.4),
        axis_ticks_major_y=element_blank(),
        plot_margin=0.04,
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
