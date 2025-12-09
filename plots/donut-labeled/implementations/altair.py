"""
donut-labeled: Donut Chart with Percentage Labels
Library: altair
"""

import altair as alt
import pandas as pd


# Data - Department budget allocation
data = pd.DataFrame(
    {"category": ["Engineering", "Marketing", "Operations", "Sales", "HR"], "value": [35, 22, 18, 15, 10]}
)

# Calculate percentages for labels
total = data["value"].sum()
data["percentage"] = data["value"] / total

# PyPlots.ai default color palette
PYPLOTS_COLORS = ["#306998", "#FFD43B", "#DC2626", "#059669", "#8B5CF6", "#F97316"]

# Define explicit order for categories
category_order = data["category"].tolist()

# Create donut chart using arc mark
# Altair uses theta encoding for pie/arc charts
base = alt.Chart(data).encode(
    theta=alt.Theta("value:Q", stack=True),
    color=alt.Color(
        "category:N",
        scale=alt.Scale(domain=category_order, range=PYPLOTS_COLORS),
        legend=alt.Legend(title="Department", orient="right", labelFontSize=16, titleFontSize=16),
        sort=category_order,
    ),
    order=alt.Order("category:N", sort="ascending"),
    tooltip=[
        alt.Tooltip("category:N", title="Department"),
        alt.Tooltip("value:Q", title="Budget (%)"),
        alt.Tooltip("percentage:Q", title="Share", format=".1%"),
    ],
)

# Create the donut with arc mark
# Inner radius at ~55% of outer radius for classic donut appearance
outer_radius = 300
inner_radius = 165
donut = base.mark_arc(innerRadius=inner_radius, outerRadius=outer_radius, stroke="#ffffff", strokeWidth=2)

# Add percentage labels positioned in the middle of each arc segment
# Radius for labels should be at the center of the ring
label_radius = (inner_radius + outer_radius) / 2
text = base.mark_text(radius=label_radius, fontSize=24, fontWeight="bold").encode(
    text=alt.Text("percentage:Q", format=".1%"), color=alt.value("#FFFFFF")
)

# Combine donut and labels
chart = alt.layer(donut, text).properties(
    width=800,
    height=800,
    title=alt.TitleParams(text="Department Budget Allocation", fontSize=20, anchor="middle", fontWeight="bold"),
)

# Configure chart appearance
chart = chart.configure_view(strokeWidth=0).configure_legend(
    labelFontSize=16, titleFontSize=16, symbolSize=200, padding=20
)

# Save - scale_factor=3 gives 2400x2400 from 800x800 base
# For donut charts, square aspect ratio is more appropriate
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
