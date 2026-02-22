"""pyplots.ai
bump-basic: Basic Bump Chart
Library: plotnine 0.15.3 | Python 3.14.3
Quality: /100 | Updated: 2026-02-22
"""

import pandas as pd
from plotnine import (
    aes,
    element_blank,
    element_line,
    element_rect,
    element_text,
    geom_line,
    geom_point,
    geom_text,
    ggplot,
    labs,
    scale_color_manual,
    scale_x_continuous,
    scale_y_reverse,
    theme,
    theme_minimal,
)


# Data - Streaming platform market share rankings over 8 quarters
platforms = ["StreamVue", "WavePlay", "CloudCast", "PixelFlix", "SonicNet", "EchoTV"]
quarters = ["Q1'24", "Q2'24", "Q3'24", "Q4'24", "Q1'25", "Q2'25", "Q3'25", "Q4'25"]
n_periods = len(quarters)

rankings = {
    "StreamVue": [1, 1, 1, 2, 2, 3, 3, 4],
    "WavePlay": [2, 3, 3, 1, 1, 1, 1, 1],
    "CloudCast": [4, 2, 2, 3, 3, 2, 2, 2],
    "PixelFlix": [3, 4, 4, 4, 5, 5, 4, 3],
    "SonicNet": [5, 5, 5, 5, 4, 4, 5, 5],
    "EchoTV": [6, 6, 6, 6, 6, 6, 6, 6],
}

rows = []
for platform, ranks in rankings.items():
    for i, rank in enumerate(ranks):
        rows.append({"platform": platform, "quarter": quarters[i], "qnum": i + 1, "rank": rank})
df = pd.DataFrame(rows)

# Subset for end labels
df_end = df[df["qnum"] == n_periods].copy()

# Colors - Python Blue first, then colorblind-safe complements
palette = {
    "StreamVue": "#306998",
    "WavePlay": "#e8963e",
    "CloudCast": "#2ca02c",
    "PixelFlix": "#d62728",
    "SonicNet": "#8c564b",
    "EchoTV": "#7f7f7f",
}

# Plot
plot = (
    ggplot(df, aes(x="qnum", y="rank", color="platform", group="platform"))
    + geom_line(size=2.8, alpha=0.85)
    + geom_point(size=6, stroke=0.8, fill="white")
    + geom_point(size=4)
    + geom_text(aes(label="platform"), data=df_end, nudge_x=0.35, ha="left", size=12, fontstyle="italic")
    + scale_y_reverse(breaks=range(1, len(platforms) + 1))
    + scale_x_continuous(breaks=range(1, n_periods + 1), labels=quarters, limits=(0.5, n_periods + 2))
    + scale_color_manual(values=palette)
    + labs(x="Quarter", y="Market Share Ranking", title="bump-basic · plotnine · pyplots.ai")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        axis_text_x=element_text(rotation=0),
        plot_title=element_text(size=24, weight="bold"),
        panel_grid_major_x=element_blank(),
        panel_grid_minor=element_blank(),
        panel_grid_major_y=element_line(alpha=0.2, size=0.5),
        panel_background=element_rect(fill="white", color="none"),
        legend_position="none",
    )
)

plot.save("plot.png", dpi=300)
