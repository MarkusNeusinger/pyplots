""" pyplots.ai
bar-realtime: Real-Time Updating Bar Chart
Library: letsplot 4.8.2 | Python 3.13.11
Quality: 91/100 | Created: 2026-01-19
"""

import numpy as np
import pandas as pd
from lets_plot import *  # noqa: F403
from lets_plot.export import ggsave as export_ggsave


LetsPlot.setup_html()  # noqa: F405

# Data - Simulating live service metrics with current and previous values
np.random.seed(42)
services = ["API Gateway", "Auth Service", "Database", "Cache", "CDN", "Worker"]

# Current values (active requests)
current_values = [342, 287, 198, 425, 156, 231]

# Previous values (for ghosted effect showing change)
previous_values = [318, 295, 210, 398, 162, 245]

# Calculate change indicators
changes = [c - p for c, p in zip(current_values, previous_values, strict=True)]
change_labels = [f"+{c}" if c > 0 else str(c) for c in changes]
change_colors = ["#22C55E" if c > 0 else "#EF4444" if c < 0 else "#306998" for c in changes]

# Create dataframes
df_previous = pd.DataFrame({"service": services, "requests": previous_values})

df_current = pd.DataFrame(
    {"service": services, "requests": current_values, "change_label": change_labels, "bar_color": change_colors}
)

# Preserve service order
df_previous["service"] = pd.Categorical(df_previous["service"], categories=services, ordered=True)
df_current["service"] = pd.Categorical(df_current["service"], categories=services, ordered=True)

# Plot with ghosted previous state and solid current state
plot = (
    ggplot()  # noqa: F405
    # Ghost bars showing previous state (lighter, behind)
    + geom_bar(  # noqa: F405
        data=df_previous,
        mapping=aes(x="service", y="requests"),  # noqa: F405
        stat="identity",
        fill="#306998",
        alpha=0.25,
        width=0.75,
    )
    # Current bars (solid) - color based on change direction
    + geom_bar(  # noqa: F405
        data=df_current,
        mapping=aes(x="service", y="requests", fill="bar_color"),  # noqa: F405
        stat="identity",
        alpha=0.9,
        width=0.55,
    )
    # Value labels on bars
    + geom_text(  # noqa: F405
        data=df_current,
        mapping=aes(x="service", y="requests", label="requests"),  # noqa: F405
        position=position_nudge(y=18),  # noqa: F405
        size=14,
        fontface="bold",
        color="#1F2937",
    )
    # Change indicators above value labels
    + geom_text(  # noqa: F405
        data=df_current,
        mapping=aes(x="service", y="requests", label="change_label", color="bar_color"),  # noqa: F405
        position=position_nudge(y=45),  # noqa: F405
        size=11,
    )
    + scale_fill_identity()  # noqa: F405
    + scale_color_identity()  # noqa: F405
    + scale_y_continuous(limits=[0, 520])  # noqa: F405
    + labs(  # noqa: F405
        title="bar-realtime · letsplot · pyplots.ai", x="Service", y="Active Requests"
    )
    + theme_minimal()  # noqa: F405
    + theme(  # noqa: F405
        plot_title=element_text(size=24, hjust=0.5),  # noqa: F405
        axis_title_x=element_text(size=20),  # noqa: F405
        axis_title_y=element_text(size=20),  # noqa: F405
        axis_text_x=element_text(size=16, angle=25, hjust=1),  # noqa: F405
        axis_text_y=element_text(size=16),  # noqa: F405
        legend_position="none",
        panel_grid_major_x=element_blank(),  # noqa: F405
        panel_grid_minor=element_blank(),  # noqa: F405
    )
    + ggsize(1600, 900)  # noqa: F405
)

# Save PNG and HTML
export_ggsave(plot, filename="plot.png", path=".", scale=3)
export_ggsave(plot, filename="plot.html", path=".")
