""" pyplots.ai
scatter-basic: Basic Scatter Plot
Library: plotnine 0.15.3 | Python 3.14.2
Quality: /100 | Updated: 2026-02-10
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_blank,
    element_line,
    element_rect,
    element_text,
    geom_point,
    ggplot,
    guides,
    labs,
    scale_color_manual,
    scale_size_continuous,
    theme,
    theme_minimal,
)


# Data: Coffee growing regions - altitude vs flavor score by variety
np.random.seed(42)
n_points = 180

varieties = np.random.choice(["Arabica", "Robusta", "Liberica"], n_points, p=[0.5, 0.35, 0.15])
altitude = np.where(
    varieties == "Arabica",
    np.random.normal(1600, 300, n_points),
    np.where(varieties == "Robusta", np.random.normal(900, 250, n_points), np.random.normal(500, 150, n_points)),
)
altitude = np.clip(altitude, 200, 2400)

flavor_score = np.where(
    varieties == "Arabica",
    70 + (altitude - 800) * 0.012 + np.random.normal(0, 4, n_points),
    np.where(
        varieties == "Robusta",
        60 + (altitude - 400) * 0.008 + np.random.normal(0, 5, n_points),
        55 + (altitude - 200) * 0.006 + np.random.normal(0, 4.5, n_points),
    ),
)
flavor_score = np.clip(flavor_score, 45, 95)

bean_weight = np.where(
    varieties == "Arabica",
    np.random.uniform(12, 18, n_points),
    np.where(varieties == "Robusta", np.random.uniform(10, 16, n_points), np.random.uniform(14, 22, n_points)),
)

df = pd.DataFrame(
    {
        "altitude": altitude,
        "flavor_score": flavor_score,
        "variety": pd.Categorical(varieties, categories=["Arabica", "Robusta", "Liberica"]),
        "bean_weight": bean_weight,
    }
)

# Plot
palette = {"Arabica": "#306998", "Robusta": "#E8873D", "Liberica": "#5BA37E"}

plot = (
    ggplot(df, aes(x="altitude", y="flavor_score", color="variety", size="bean_weight"))
    + geom_point(alpha=0.65)
    + scale_color_manual(values=palette)
    + scale_size_continuous(range=(2, 7))
    + guides(size=False)
    + labs(
        x="Growing Altitude (meters)",
        y="Flavor Score (0-100)",
        color="Variety",
        title="scatter-basic \u00b7 plotnine \u00b7 pyplots.ai",
    )
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14, color="#2D2D2D"),
        axis_title=element_text(size=20, weight="bold"),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24, weight="bold", color="#1A1A1A"),
        legend_title=element_text(size=18, weight="bold"),
        legend_text=element_text(size=16),
        legend_position="right",
        legend_background=element_rect(fill="white", alpha=0.8),
        panel_grid_major=element_line(color="#E0E0E0", size=0.5),
        panel_grid_minor=element_blank(),
        panel_background=element_rect(fill="#FAFAFA"),
        plot_background=element_rect(fill="white"),
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
