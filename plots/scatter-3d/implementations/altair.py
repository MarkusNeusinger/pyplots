"""pyplots.ai
scatter-3d: 3D Scatter Plot
Library: altair 6.0.0 | Python 3.13.11
Quality: 88/100 | Created: 2025-12-25
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - create 3D clusters to demonstrate spatial relationships
np.random.seed(42)

n_points = 150

# Create three distinct clusters in 3D space (well-separated for clear visualization)
clusters = []
centers = [
    (3, 1, 3),  # Cluster 1 - front-right, high
    (-3, 2, 2),  # Cluster 2 - back-left, mid-high
    (0, -2, -2),  # Cluster 3 - front, low
]

for i, (cx, cy, cz) in enumerate(centers):
    n_cluster = n_points // 3
    x = np.random.randn(n_cluster) * 0.7 + cx
    y = np.random.randn(n_cluster) * 0.7 + cy
    z = np.random.randn(n_cluster) * 0.7 + cz
    clusters.append(pd.DataFrame({"x": x, "y": y, "z": z, "cluster": f"Cluster {i + 1}"}))

df = pd.concat(clusters, ignore_index=True)

# 3D to 2D projection (elevation=25, azimuth=35) for better depth perception
elev_rad = np.radians(25)
azim_rad = np.radians(35)

# Rotation around z-axis (azimuth)
df["x_rot"] = df["x"] * np.cos(azim_rad) - df["y"] * np.sin(azim_rad)
df["y_rot"] = df["x"] * np.sin(azim_rad) + df["y"] * np.cos(azim_rad)

# Rotation around x-axis (elevation) and project to 2D
df["x_proj"] = df["x_rot"]
df["z_proj"] = df["y_rot"] * np.sin(elev_rad) + df["z"] * np.cos(elev_rad)

# Calculate depth for point ordering (painters algorithm)
df["depth"] = df["y_rot"] * np.cos(elev_rad) - df["z"] * np.sin(elev_rad)

# Normalize depth for opacity (further points slightly more transparent)
depth_min = df["depth"].min()
depth_max = df["depth"].max()
df["opacity"] = 0.65 + 0.35 * (df["depth"] - depth_min) / (depth_max - depth_min + 1e-6)

# Scatter chart with clusters
scatter = (
    alt.Chart(df)
    .mark_circle(size=280, strokeWidth=1.5, stroke="white")
    .encode(
        x=alt.X("x_proj:Q", axis=alt.Axis(title="X-axis (isometric projection)", labelFontSize=18, titleFontSize=22)),
        y=alt.Y(
            "z_proj:Q", axis=alt.Axis(title="Z-axis (Y encodes depth via opacity)", labelFontSize=18, titleFontSize=22)
        ),
        color=alt.Color(
            "cluster:N",
            scale=alt.Scale(domain=["Cluster 1", "Cluster 2", "Cluster 3"], range=["#306998", "#FFD43B", "#E07B39"]),
            legend=alt.Legend(
                title="Cluster",
                titleFontSize=20,
                labelFontSize=16,
                orient="none",
                legendX=1300,
                legendY=100,
                direction="vertical",
            ),
        ),
        opacity=alt.Opacity("opacity:Q", legend=None),
        order=alt.Order("depth:Q", sort="ascending"),
        tooltip=[
            alt.Tooltip("x:Q", title="X", format=".2f"),
            alt.Tooltip("y:Q", title="Y", format=".2f"),
            alt.Tooltip("z:Q", title="Z", format=".2f"),
            alt.Tooltip("cluster:N", title="Cluster"),
        ],
    )
)

# Add pan and zoom interactivity
pan_zoom = alt.selection_interval(bind="scales", encodings=["x", "y"])

# Final chart
chart = (
    scatter.add_params(pan_zoom)
    .properties(
        width=1600,
        height=900,
        title=alt.Title(
            text="scatter-3d · altair · pyplots.ai",
            subtitle="Isometric 3D projection: X/Z shown on axes, Y mapped to depth (opacity)",
            fontSize=28,
            subtitleFontSize=18,
            subtitleColor="#666666",
        ),
    )
    .configure_axis(grid=True, gridOpacity=0.3, gridDash=[6, 4])
    .configure_view(strokeWidth=0)
)

# Save outputs
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
