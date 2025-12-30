""" pyplots.ai
contour-density: Density Contour Plot
Library: altair 6.0.0 | Python 3.13.11
Quality: 88/100 | Created: 2025-12-30
"""

import altair as alt
import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde


# Data - simulating temperature and humidity measurements showing natural clusters
# e.g., weather patterns from different climate zones or seasons
np.random.seed(42)

# Create three distinct clusters representing different climate conditions
# Cluster 1: Cool and dry (morning/winter measurements)
n1 = 150
temp1 = np.random.normal(25, 5, n1)
humidity1 = np.random.normal(35, 8, n1)

# Cluster 2: Moderate temperature and humidity (typical day conditions)
n2 = 200
temp2 = np.random.normal(50, 7, n2)
humidity2 = np.random.normal(55, 10, n2)

# Cluster 3: Warm and humid (afternoon/summer measurements)
n3 = 150
temp3 = np.random.normal(75, 6, n3)
humidity3 = np.random.normal(72, 8, n3)

# Combine data
temperature = np.concatenate([temp1, temp2, temp3])
humidity = np.concatenate([humidity1, humidity2, humidity3])

# Compute 2D KDE for contour lines
xy = np.vstack([temperature, humidity])
kde = gaussian_kde(xy)

# Create grid for density estimation
x_grid = np.linspace(temperature.min() - 5, temperature.max() + 5, 100)
y_grid = np.linspace(humidity.min() - 5, humidity.max() + 5, 100)
xx, yy = np.meshgrid(x_grid, y_grid)
positions = np.vstack([xx.ravel(), yy.ravel()])
z = kde(positions).reshape(xx.shape)

# Create DataFrame for the density grid (for heatmap visualization)
grid_data = []
for i in range(len(x_grid)):
    for j in range(len(y_grid)):
        grid_data.append({"Temperature": x_grid[i], "Humidity": y_grid[j], "Density": z[j, i]})

grid_df = pd.DataFrame(grid_data)

# Create the density heatmap with rect marks (continuous density visualization)
heatmap = (
    alt.Chart(grid_df)
    .mark_rect()
    .encode(
        x=alt.X(
            "Temperature:Q",
            bin=alt.Bin(maxbins=100),
            title="Temperature (\u00b0C)",
            axis=alt.Axis(labelFontSize=18, titleFontSize=22, grid=True, gridOpacity=0.3, tickCount=10),
        ),
        y=alt.Y(
            "Humidity:Q",
            bin=alt.Bin(maxbins=100),
            title="Humidity (%)",
            axis=alt.Axis(labelFontSize=18, titleFontSize=22, grid=True, gridOpacity=0.3, tickCount=10),
        ),
        color=alt.Color(
            "mean(Density):Q",
            scale=alt.Scale(scheme="blues"),
            legend=alt.Legend(
                title="Density", titleFontSize=20, labelFontSize=16, gradientLength=350, gradientThickness=25
            ),
        ),
    )
)

# Create scatter point overlay (original data points for context)
scatter_df = pd.DataFrame({"Temperature": temperature, "Humidity": humidity})

scatter = (
    alt.Chart(scatter_df)
    .mark_point(size=30, opacity=0.4, color="#306998", filled=True)
    .encode(
        x=alt.X("Temperature:Q"),
        y=alt.Y("Humidity:Q"),
        tooltip=[
            alt.Tooltip("Temperature:Q", title="Temp (\u00b0C)", format=".1f"),
            alt.Tooltip("Humidity:Q", title="Humidity (%)", format=".1f"),
        ],
    )
)

# Layer the charts
chart = (
    alt.layer(heatmap, scatter)
    .properties(
        width=1600,
        height=900,
        title=alt.Title(text="contour-density \u00b7 altair \u00b7 pyplots.ai", fontSize=28, anchor="middle"),
    )
    .configure_view(strokeWidth=0)
    .configure_axis(labelFontSize=16, titleFontSize=22)
)

# Save as PNG (1600 * 3 = 4800, 900 * 3 = 2700)
chart.save("plot.png", scale_factor=3.0)

# Save as interactive HTML
chart.save("plot.html")
