""" pyplots.ai
donut-basic: Basic Donut Chart
Library: altair 6.0.0 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-14
"""

import altair as alt
import pandas as pd


# Data
data = pd.DataFrame(
    {"category": ["Marketing", "Development", "Operations", "Sales", "Support"], "value": [28, 35, 18, 12, 7]}
)

# Calculate percentages for labels
total = data["value"].sum()
data["percentage"] = (data["value"] / total * 100).round(1)
data["label"] = data["category"] + " (" + data["percentage"].astype(str) + "%)"

# Create donut chart using arc mark
chart = (
    alt.Chart(data)
    .mark_arc(innerRadius=120, outerRadius=280, stroke="white", strokeWidth=3)
    .encode(
        theta=alt.Theta(field="value", type="quantitative"),
        color=alt.Color(
            field="category",
            type="nominal",
            scale=alt.Scale(
                domain=["Marketing", "Development", "Operations", "Sales", "Support"],
                range=["#306998", "#FFD43B", "#4B8BBE", "#646464", "#8FBC8F"],
            ),
            legend=alt.Legend(title="Category", titleFontSize=20, labelFontSize=16, orient="right", symbolSize=300),
        ),
        tooltip=[
            alt.Tooltip("category:N", title="Category"),
            alt.Tooltip("value:Q", title="Value"),
            alt.Tooltip("percentage:Q", title="Percentage", format=".1f"),
        ],
    )
    .properties(
        width=1600, height=900, title=alt.Title(text="donut-basic · altair · pyplots.ai", fontSize=28, anchor="middle")
    )
)

# Add text labels on segments
text = (
    alt.Chart(data)
    .mark_text(radius=200, fontSize=18, fontWeight="bold")
    .encode(
        theta=alt.Theta(field="value", type="quantitative", stack=True),
        text=alt.Text("percentage:Q", format=".1f"),
        color=alt.value("white"),
    )
)

# Add center text showing total
center_text = (
    alt.Chart(pd.DataFrame({"text": [f"Total: {total}"]}))
    .mark_text(fontSize=32, fontWeight="bold", color="#306998")
    .encode(text="text:N")
)

# Combine layers
final_chart = alt.layer(chart, text, center_text).configure_view(strokeWidth=0)

# Save outputs
final_chart.save("plot.png", scale_factor=3.0)
final_chart.save("plot.html")
