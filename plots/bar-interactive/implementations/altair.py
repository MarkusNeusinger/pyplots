""" pyplots.ai
bar-interactive: Interactive Bar Chart with Hover and Click
Library: altair 6.0.0 | Python 3.13.11
Quality: 92/100 | Created: 2026-01-07
"""

import altair as alt
import pandas as pd


# Data - Quarterly product sales with additional details for tooltips
data = pd.DataFrame(
    {
        "product": ["Laptops", "Monitors", "Keyboards", "Mice", "Headsets", "Webcams", "Speakers", "Tablets"],
        "sales": [245000, 178000, 89000, 67000, 52000, 41000, 38000, 156000],
        "units_sold": [1225, 890, 4450, 6700, 2600, 2050, 1900, 780],
        "growth": [12.5, 8.3, -2.1, 15.7, 22.4, 45.2, -5.8, 18.9],
    }
)

# Calculate percentage of total for tooltips
data["percentage"] = (data["sales"] / data["sales"].sum() * 100).round(1)

# Selection for click interaction - enables highlighting on click
# empty='none' ensures no bars are selected initially (all show unselected state)
selection = alt.selection_point(fields=["product"], on="click", clear="dblclick", empty=False)

# Base chart with interactive features
chart = (
    alt.Chart(data)
    .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4, stroke="#306998", strokeWidth=1)
    .encode(
        x=alt.X(
            "product:N",
            title="Product Category",
            axis=alt.Axis(labelFontSize=16, titleFontSize=20, labelAngle=-30),
            sort="-y",
        ),
        y=alt.Y("sales:Q", title="Sales Revenue ($)", axis=alt.Axis(labelFontSize=16, titleFontSize=20, format=",.0f")),
        # Color changes based on selection (clicked items highlighted)
        color=alt.condition(
            selection,
            alt.value("#306998"),  # Python Blue when selected
            alt.value("#FFD43B"),  # Python Yellow when not selected
        ),
        # Opacity changes based on selection
        opacity=alt.condition(selection, alt.value(1.0), alt.value(0.7)),
        # Comprehensive tooltips with multiple data fields
        tooltip=[
            alt.Tooltip("product:N", title="Product"),
            alt.Tooltip("sales:Q", title="Revenue", format="$,.0f"),
            alt.Tooltip("units_sold:Q", title="Units Sold", format=","),
            alt.Tooltip("percentage:Q", title="% of Total", format=".1f"),
            alt.Tooltip("growth:Q", title="YoY Growth (%)", format="+.1f"),
        ],
    )
    .add_params(selection)
    .properties(
        width=1600,
        height=900,
        title=alt.Title(
            "bar-interactive · altair · pyplots.ai",
            fontSize=28,
            anchor="middle",
            subtitle="Click a bar to highlight, double-click to reset. Hover for details.",
            subtitleFontSize=16,
            subtitleColor="#666666",
        ),
    )
    .configure_axis(labelFontSize=16, titleFontSize=20, grid=True, gridOpacity=0.3, gridDash=[4, 4])
    .configure_view(strokeWidth=0)
)

# Save as PNG (4800x2700 with scale_factor=3)
chart.save("plot.png", scale_factor=3.0)

# Save interactive HTML version
chart.save("plot.html")
