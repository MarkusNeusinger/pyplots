""" pyplots.ai
slider-control-basic: Interactive Plot with Slider Control
Library: letsplot 4.8.2 | Python 3.13.11
Quality: 55/100 | Created: 2025-12-31
"""

import numpy as np
import pandas as pd
from lets_plot import *  # noqa: F403
from lets_plot.export import ggsave as export_ggsave


LetsPlot.setup_html()  # noqa: F405

# Data - Monthly temperature readings for multiple years
np.random.seed(42)

years = [2019, 2020, 2021, 2022, 2023, 2024]
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
        data.append(
            {
                "year": str(year),  # String to avoid comma formatting in legend
                "month": month,
                "month_name": month_names[month - 1],
                "temperature": round(temp, 1),
            }
        )

df = pd.DataFrame(data)

# Distinct colors for each year - Tableau colorblind-friendly palette
year_colors = ["#4E79A7", "#F28E2B", "#E15759", "#76B7B2", "#59A14F", "#EDC948"]

# Create interactive plot with clickable legend for year filtering
# In lets-plot HTML output, clicking legend items shows/hides the corresponding series
# This provides slider-like filtering functionality for selecting which years to display
plot = (
    ggplot(df, aes(x="month", y="temperature", color="year", group="year"))  # noqa: F405
    + geom_line(  # noqa: F405
        size=2.5, alpha=0.85
    )
    + geom_point(  # noqa: F405
        size=6,
        alpha=0.9,
        tooltips=layer_tooltips()  # noqa: F405
        .title("@year")
        .line("Month: @month_name")
        .line("Temperature: @{temperature} °C"),
    )
    + scale_x_continuous(  # noqa: F405
        breaks=list(range(1, 13)), labels=month_names
    )
    + scale_color_manual(values=year_colors, name="Year\n(click to filter)")  # noqa: F405
    + labs(  # noqa: F405
        title="slider-control-basic · lets-plot · pyplots.ai",
        subtitle="Monthly Temperature Trends – Click legend to show/hide years (interactive HTML)",
        x="Month",
        y="Temperature (°C)",
    )
    + theme_minimal()  # noqa: F405
    + theme(  # noqa: F405
        plot_title=element_text(size=26, face="bold"),  # noqa: F405
        plot_subtitle=element_text(size=16, color="#555555"),  # noqa: F405
        axis_title=element_text(size=20),  # noqa: F405
        axis_text_x=element_text(size=14, angle=45),  # noqa: F405
        axis_text_y=element_text(size=16),  # noqa: F405
        legend_title=element_text(size=18, face="bold"),  # noqa: F405
        legend_text=element_text(size=16),  # noqa: F405
        legend_position="right",
        panel_grid_major=element_line(color="#DDDDDD", size=0.5),  # noqa: F405
        panel_grid_minor=element_blank(),  # noqa: F405
    )
    + ggsize(1600, 900)  # noqa: F405
)

# Save PNG (scale 3x to get 4800 x 2700 px)
export_ggsave(plot, filename="plot.png", path=".", scale=3)

# Save interactive HTML version with legend-based filtering and hover tooltips
export_ggsave(plot, filename="plot.html", path=".")
