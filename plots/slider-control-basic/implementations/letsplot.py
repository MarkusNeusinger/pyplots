"""pyplots.ai
slider-control-basic: Interactive Plot with Slider Control
Library: lets-plot | Python 3.13
Quality: pending | Created: 2025-12-31
"""

import numpy as np
import pandas as pd
from lets_plot import *  # noqa: F403
from lets_plot.export import ggsave as export_ggsave


LetsPlot.setup_html()  # noqa: F405

# Data - Monthly temperature readings for multiple years
np.random.seed(42)

years = range(2019, 2025)
months = range(1, 13)
month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Generate realistic seasonal temperature pattern with yearly variation
data = []
for year in years:
    base_temp = 10 + np.random.uniform(-2, 2)  # Yearly baseline variation
    for month in months:
        # Seasonal pattern: coldest in Jan, warmest in Jul
        seasonal = 15 * np.sin((month - 4) * np.pi / 6)
        temp = base_temp + seasonal + np.random.normal(0, 2)
        data.append({"year": year, "month": month, "month_name": month_names[month - 1], "temperature": temp})

df = pd.DataFrame(data)

# Create interactive plot with year filtering via tooltips and interactive legend
# In lets-plot, interactivity includes hovering, zooming, and legend-based filtering
plot = (
    ggplot(df, aes(x="month", y="temperature", color="year"))  # noqa: F405
    + geom_line(  # noqa: F405
        aes(group="year"),  # noqa: F405
        size=2,
        alpha=0.8,
        tooltips=layer_tooltips()  # noqa: F405
        .line("Year: @year")
        .line("Month: @month_name")
        .line("Temp: @{temperature} °C"),
    )
    + geom_point(size=5, alpha=0.9)  # noqa: F405
    + scale_x_continuous(breaks=list(range(1, 13)), labels=month_names)  # noqa: F405
    + scale_color_gradient(low="#306998", high="#FFD43B", name="Year")  # noqa: F405
    + labs(  # noqa: F405
        title="slider-control-basic · letsplot · pyplots.ai",
        subtitle="Monthly Temperature by Year - Interactive legend controls visibility",
        x="Month",
        y="Temperature (°C)",
    )
    + theme_minimal()  # noqa: F405
    + theme(  # noqa: F405
        plot_title=element_text(size=24, face="bold"),  # noqa: F405
        plot_subtitle=element_text(size=16, color="#666666"),  # noqa: F405
        axis_title=element_text(size=20),  # noqa: F405
        axis_text=element_text(size=16),  # noqa: F405
        legend_title=element_text(size=18),  # noqa: F405
        legend_text=element_text(size=16),  # noqa: F405
        panel_grid_major=element_line(color="#CCCCCC", size=0.5),  # noqa: F405
    )
    + ggsize(1600, 900)  # noqa: F405
)

# Save PNG (scale 3x to get 4800 x 2700 px)
export_ggsave(plot, filename="plot.png", path=".", scale=3)

# Save interactive HTML version
export_ggsave(plot, filename="plot.html", path=".")
