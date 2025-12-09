"""
area-basic: Basic Area Chart
Library: plotnine
"""

import pandas as pd
from plotnine import aes, element_line, element_text, geom_area, geom_line, ggplot, labs, theme, theme_minimal


# Data - monthly sales example from spec
data = pd.DataFrame(
    {
        "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        "sales": [120, 135, 148, 162, 175, 195, 210, 198, 185, 170, 158, 190],
    }
)

# Convert month to ordered categorical for proper x-axis ordering
data["month"] = pd.Categorical(
    data["month"],
    categories=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    ordered=True,
)

# Plot
plot = (
    ggplot(data, aes(x="month", y="sales", group=1))
    + geom_area(fill="#306998", alpha=0.6)
    + geom_line(color="#306998", size=2)
    + labs(title="Monthly Sales Trend", x="Month", y="Sales")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=20, weight="bold", ha="center"),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        panel_grid_major=element_line(alpha=0.3),
        panel_grid_minor=element_line(alpha=0),
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
