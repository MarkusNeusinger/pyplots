"""
slope-basic: Basic Slope Chart (Slopegraph)
Library: letsplot
"""

import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_blank,
    element_text,
    geom_point,
    geom_segment,
    geom_text,
    ggplot,
    ggsave,
    ggsize,
    labs,
    scale_color_manual,
    scale_x_continuous,
    theme,
    theme_minimal,
)


LetsPlot.setup_html()

# Data - Sales figures for 10 products comparing Q1 vs Q4
data = {
    "entity": [
        "Product A",
        "Product B",
        "Product C",
        "Product D",
        "Product E",
        "Product F",
        "Product G",
        "Product H",
        "Product I",
        "Product J",
    ],
    "Q1": [120, 85, 200, 150, 95, 180, 110, 140, 75, 165],
    "Q4": [155, 70, 210, 130, 145, 175, 160, 135, 105, 180],
}
df = pd.DataFrame(data)

# Calculate change direction for color coding
df["change"] = df["Q4"] - df["Q1"]
df["direction"] = df["change"].apply(lambda x: "Increase" if x > 0 else "Decrease")

# Prepare data for segment plot
df_long = pd.DataFrame(
    {
        "entity": df["entity"].tolist() * 2,
        "period": ["Q1"] * 10 + ["Q4"] * 10,
        "value": df["Q1"].tolist() + df["Q4"].tolist(),
        "x": [0] * 10 + [1] * 10,
    }
)

# Create segment data for lines
df_segments = pd.DataFrame(
    {
        "entity": df["entity"],
        "x_start": [0] * 10,
        "x_end": [1] * 10,
        "y_start": df["Q1"],
        "y_end": df["Q4"],
        "direction": df["direction"],
    }
)

# Merge direction info for points
df_long = df_long.merge(df[["entity", "direction"]], on="entity")

# Plot
plot = (
    ggplot()
    + geom_segment(
        data=df_segments,
        mapping=aes(x="x_start", y="y_start", xend="x_end", yend="y_end", color="direction"),
        size=2,
        alpha=0.8,
    )
    + geom_point(data=df_long, mapping=aes(x="x", y="value", color="direction"), size=6)
    # Labels on left side (Q1)
    + geom_text(
        data=df_long[df_long["x"] == 0],
        mapping=aes(x="x", y="value", label="entity"),
        hjust=1.1,
        size=12,
        color="#333333",
    )
    # Labels on right side (Q4)
    + geom_text(
        data=df_long[df_long["x"] == 1],
        mapping=aes(x="x", y="value", label="entity"),
        hjust=-0.1,
        size=12,
        color="#333333",
    )
    + scale_color_manual(values={"Increase": "#306998", "Decrease": "#DC2626"})
    + scale_x_continuous(breaks=[0, 1], labels=["Q1 Sales ($K)", "Q4 Sales ($K)"], limits=[-0.5, 1.5])
    + labs(title="slope-basic · letsplot · pyplots.ai", x="", y="Sales ($K)", color="Change")
    + theme_minimal()
    + theme(
        plot_title=element_text(size=24),
        axis_title_y=element_text(size=20),
        axis_title_x=element_blank(),
        axis_text_x=element_text(size=18),
        axis_text_y=element_text(size=16),
        legend_title=element_text(size=18),
        legend_text=element_text(size=16),
        panel_grid_major_x=element_blank(),
        panel_grid_minor=element_blank(),
    )
    + ggsize(1600, 900)
)

# Save PNG (scale 3x to get 4800 x 2700 px)
ggsave(plot, "plot.png", path=".", scale=3)

# Save HTML for interactivity
ggsave(plot, "plot.html", path=".")
