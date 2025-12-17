"""
bump-basic: Basic Bump Chart
Library: letsplot
"""

import pandas as pd
from lets_plot import *  # noqa: F403


LetsPlot.setup_html()  # noqa: F405

# Data - Tech company rankings over quarters
data = {
    "company": ["Alpha", "Beta", "Gamma", "Delta", "Epsilon"] * 6,
    "quarter": ["Q1"] * 5 + ["Q2"] * 5 + ["Q3"] * 5 + ["Q4"] * 5 + ["Q5"] * 5 + ["Q6"] * 5,
    "rank": [
        1,
        2,
        3,
        4,
        5,  # Q1: Initial standings
        2,
        1,
        3,
        5,
        4,  # Q2: Beta overtakes Alpha
        2,
        1,
        4,
        5,
        3,  # Q3: Epsilon rises
        3,
        1,
        4,
        5,
        2,  # Q4: Epsilon continues climbing
        3,
        2,
        4,
        5,
        1,  # Q5: Epsilon takes lead
        2,
        3,
        4,
        5,
        1,  # Q6: Alpha recovers to 2nd
    ],
}
df = pd.DataFrame(data)

# Quarter order for proper x-axis
quarter_order = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6"]
df["quarter"] = pd.Categorical(df["quarter"], categories=quarter_order, ordered=True)

# Colors for 5 companies
colors = ["#306998", "#FFD43B", "#2E8B57", "#DC2626", "#8B5CF6"]

# Plot  # noqa: F405
plot = (
    ggplot(df, aes(x="quarter", y="rank", color="company", group="company"))  # noqa: F405
    + geom_line(size=3, alpha=0.8)  # noqa: F405
    + geom_point(size=8)  # noqa: F405
    + scale_y_reverse(breaks=[1, 2, 3, 4, 5])  # Rank 1 at top, integer breaks only  # noqa: F405
    + scale_color_manual(values=colors)  # noqa: F405
    + labs(x="Quarter", y="Rank", title="bump-basic · letsplot · pyplots.ai", color="Company")  # noqa: F405
    + theme_minimal()  # noqa: F405
    + theme(  # noqa: F405
        plot_title=element_text(size=28, face="bold"),  # noqa: F405
        axis_title=element_text(size=22),  # noqa: F405
        axis_text=element_text(size=18),  # noqa: F405
        legend_title=element_text(size=20),  # noqa: F405
        legend_text=element_text(size=18),  # noqa: F405
        panel_grid_major_x=element_blank(),  # noqa: F405
        panel_grid_minor=element_blank(),  # noqa: F405
    )
    + ggsize(1600, 900)  # noqa: F405
)

# Save PNG (scale 3x = 4800 x 2700 px)
ggsave(plot, "plot.png", path=".", scale=3)  # noqa: F405

# Save HTML for interactive version
ggsave(plot, "plot.html", path=".")  # noqa: F405
