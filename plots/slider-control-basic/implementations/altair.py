"""pyplots.ai
slider-control-basic: Interactive Plot with Slider Control
Library: altair | Python 3.13
Quality: pending | Created: 2025-12-31
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Monthly sales data across multiple years
np.random.seed(42)
years = [2019, 2020, 2021, 2022, 2023]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

data = []
base_sales = 100
for year in years:
    # Different growth patterns per year
    year_factor = 1 + (year - 2019) * 0.15
    for i, month in enumerate(months):
        # Seasonal pattern with noise
        seasonal = np.sin(i * np.pi / 6) * 20 + 10
        sales = base_sales * year_factor + seasonal + np.random.normal(0, 10)
        data.append({"Year": year, "Month": month, "Month_Num": i + 1, "Sales": max(0, sales)})

df = pd.DataFrame(data)

# Create slider binding for year selection
year_slider = alt.binding_range(min=2019, max=2023, step=1, name="Year: ")
year_selection = alt.selection_point(fields=["Year"], bind=year_slider, value=2023)

# Bar chart showing monthly sales for selected year
chart = (
    alt.Chart(df)
    .mark_bar(size=40, color="#306998", opacity=0.8)
    .encode(
        x=alt.X("Month:N", sort=months, axis=alt.Axis(labelFontSize=18, titleFontSize=22, labelAngle=0), title="Month"),
        y=alt.Y(
            "Sales:Q",
            axis=alt.Axis(labelFontSize=18, titleFontSize=22),
            title="Sales (thousands $)",
            scale=alt.Scale(domain=[0, 200]),
        ),
        tooltip=[
            alt.Tooltip("Year:O", title="Year"),
            alt.Tooltip("Month:N", title="Month"),
            alt.Tooltip("Sales:Q", title="Sales", format=".1f"),
        ],
    )
    .add_params(year_selection)
    .transform_filter(year_selection)
    .properties(
        width=1600,
        height=900,
        title=alt.Title(
            "slider-control-basic · altair · pyplots.ai",
            fontSize=28,
            anchor="middle",
            subtitle="Use the Year slider to filter monthly sales data",
            subtitleFontSize=18,
        ),
    )
    .configure_axis(gridColor="#cccccc", gridOpacity=0.3, domainColor="#333333")
    .configure_view(strokeWidth=0)
)

# Save as PNG (static snapshot at default year)
chart.save("plot.png", scale_factor=3.0)

# Save as HTML (interactive version with working slider)
chart.save("plot.html")
