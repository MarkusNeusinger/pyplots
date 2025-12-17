"""
bump-basic: Basic Bump Chart
Library: plotnine
"""

import pandas as pd
from plotnine import (
    aes,
    element_text,
    geom_line,
    geom_point,
    geom_text,
    ggplot,
    labs,
    scale_color_brewer,
    scale_x_continuous,
    scale_y_reverse,
    theme,
    theme_minimal,
)


# Data - Tech company rankings over 6 quarters
data = {
    "entity": ["Alpha Corp"] * 6 + ["Beta Inc"] * 6 + ["Gamma Tech"] * 6 + ["Delta Systems"] * 6 + ["Epsilon Labs"] * 6,
    "period": ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6"] * 5,
    "period_num": [1, 2, 3, 4, 5, 6] * 5,
    "rank": [
        1,
        1,
        2,
        2,
        1,
        1,  # Alpha Corp - starts strong, slight dip, recovers
        2,
        3,
        1,
        1,
        2,
        3,  # Beta Inc - rises to top mid-year, then falls
        3,
        2,
        3,
        4,
        4,
        2,  # Gamma Tech - volatile movement
        4,
        4,
        4,
        3,
        3,
        4,  # Delta Systems - stable middle performer
        5,
        5,
        5,
        5,
        5,
        5,  # Epsilon Labs - consistently last
    ],
}
df = pd.DataFrame(data)

# Plot
plot = (
    ggplot(df, aes(x="period_num", y="rank", color="entity", group="entity"))
    + geom_line(size=2.5, alpha=0.8)
    + geom_point(size=6)
    + geom_text(aes(label="entity"), data=df[df["period_num"] == 6], nudge_x=0.3, ha="left", size=12)
    + scale_y_reverse(breaks=[1, 2, 3, 4, 5])
    + scale_x_continuous(breaks=[1, 2, 3, 4, 5, 6], labels=["Q1", "Q2", "Q3", "Q4", "Q5", "Q6"], limits=(0.5, 7.5))
    + scale_color_brewer(type="qual", palette="Set2")
    + labs(x="Quarter", y="Rank", title="bump-basic · plotnine · pyplots.ai", color="Company")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24),
        legend_text=element_text(size=16),
        legend_title=element_text(size=18),
        legend_position="none",  # Labels on right side instead
    )
)

plot.save("plot.png", dpi=300)
