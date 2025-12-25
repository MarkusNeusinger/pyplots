""" pyplots.ai
raincloud-basic: Basic Raincloud Plot
Library: plotnine 0.15.2 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-25
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    coord_flip,
    element_blank,
    element_line,
    element_text,
    geom_boxplot,
    geom_point,
    geom_ribbon,
    ggplot,
    labs,
    scale_color_manual,
    scale_fill_manual,
    scale_x_continuous,
    theme,
    theme_minimal,
)
from scipy import stats


# Data - Reaction times (ms) for three experimental conditions
np.random.seed(42)

# Control group: normal distribution centered at 450ms
control = np.random.normal(450, 60, 80)

# Treatment A: faster responses, centered at 380ms
treatment_a = np.random.normal(380, 50, 80)

# Treatment B: bimodal distribution (some fast responders, some slow)
treatment_b = np.concatenate([np.random.normal(350, 40, 50), np.random.normal(500, 45, 30)])

# Build dataframe with numeric x positions
df = pd.DataFrame(
    {
        "condition": ["Control"] * len(control)
        + ["Treatment A"] * len(treatment_a)
        + ["Treatment B"] * len(treatment_b),
        "reaction_time": np.concatenate([control, treatment_a, treatment_b]),
    }
)

# Map conditions to numeric positions (for coord_flip: higher = top)
condition_map = {"Control": 2, "Treatment A": 1, "Treatment B": 0}
df["x_pos"] = df["condition"].map(condition_map).astype(float)

# Add jitter for rain points (below center, after coord_flip)
np.random.seed(123)
df["x_rain"] = df["x_pos"] - 0.22 + np.random.uniform(-0.06, 0.06, len(df))

# Colors - dictionary mapping for condition names
colors = {"Control": "#306998", "Treatment A": "#FFD43B", "Treatment B": "#5BA85B"}

# Create half-violin (cloud) data using KDE
# The cloud should be on TOP only (positive direction after coord_flip)
cloud_dfs = []
for cond, x_base in condition_map.items():
    data = df[df["condition"] == cond]["reaction_time"].values
    kde = stats.gaussian_kde(data)
    y_range = np.linspace(data.min() - 10, data.max() + 10, 200)
    density = kde(y_range)
    # Normalize density and scale for visual width (half-violin on TOP only)
    density_scaled = density / density.max() * 0.35
    cloud_df = pd.DataFrame(
        {
            "reaction_time": y_range,
            "ymin": x_base,  # Base position (center line)
            "ymax": x_base + density_scaled,  # Extend upward only (becomes top after flip)
            "condition": cond,
        }
    )
    cloud_dfs.append(cloud_df)

cloud_data = pd.concat(cloud_dfs, ignore_index=True)

# Create raincloud plot with horizontal orientation (coord_flip)
# After flip: Cloud (half-violin) on TOP, boxplot centered, rain points BELOW
plot = (
    ggplot()
    # Half-violin (cloud) using geom_ribbon - extends from center to one side only
    + geom_ribbon(
        data=cloud_data,
        mapping=aes(x="reaction_time", ymin="ymin", ymax="ymax", fill="condition"),
        alpha=0.85,
        show_legend=False,
    )
    # Box plot - centered, narrow, white fill
    + geom_boxplot(
        data=df,
        mapping=aes(x="x_pos", y="reaction_time", group="condition"),
        width=0.08,
        outlier_shape="",
        fill="white",
        color="#333333",
        size=0.6,
        alpha=0.95,
        show_legend=False,
    )
    # Jittered points (rain) - below the center line (after flip)
    + geom_point(
        data=df, mapping=aes(x="x_rain", y="reaction_time", color="condition"), size=2, alpha=0.6, show_legend=False
    )
    + scale_fill_manual(values=colors)
    + scale_color_manual(values=colors)
    + scale_x_continuous(breaks=[0, 1, 2], labels=["Treatment B", "Treatment A", "Control"])
    + coord_flip()
    + labs(x="Experimental Condition", y="Reaction Time (ms)", title="raincloud-basic · plotnine · pyplots.ai")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24),
        panel_grid_major_y=element_blank(),
        panel_grid_minor=element_blank(),
        panel_grid_major_x=element_line(color="#cccccc", size=0.5),
        legend_position="none",
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
