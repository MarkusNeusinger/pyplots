"""
pie-basic: Basic Pie Chart
Library: altair
"""

import altair as alt
import pandas as pd


# Data
data = pd.DataFrame(
    {"category": ["Product A", "Product B", "Product C", "Product D", "Other"], "value": [35, 25, 20, 15, 5]}
)

# Calculate percentages for labels
total = data["value"].sum()
data["percentage"] = data["value"] / total

# PyPlots.ai default color palette
PYPLOTS_COLORS = ["#306998", "#FFD43B", "#DC2626", "#059669", "#8B5CF6", "#F97316"]

# Create pie chart using arc mark
# Altair uses theta encoding for pie/arc charts
base = alt.Chart(data).encode(
    theta=alt.Theta("value:Q", stack=True),
    color=alt.Color(
        "category:N",
        scale=alt.Scale(range=PYPLOTS_COLORS),
        legend=alt.Legend(title="Category", orient="right", labelFontSize=16, titleFontSize=16),
    ),
    tooltip=[
        alt.Tooltip("category:N", title="Category"),
        alt.Tooltip("value:Q", title="Value"),
        alt.Tooltip("percentage:Q", title="Share", format=".1%"),
    ],
)

# Create the pie with arc mark
pie = base.mark_arc(innerRadius=0, outerRadius=300, stroke="#ffffff", strokeWidth=2)

# Add percentage labels on slices
text = base.mark_text(radius=200, fontSize=20, fontWeight="bold", color="#FFFFFF").encode(
    text=alt.Text("percentage:Q", format=".1%")
)

# Combine pie and labels
chart = alt.layer(pie, text).properties(
    width=800,
    height=800,
    title=alt.TitleParams(text="Market Share Distribution", fontSize=20, anchor="middle", fontWeight="bold"),
)

# Configure chart appearance
chart = chart.configure_view(strokeWidth=0).configure_legend(
    labelFontSize=16, titleFontSize=16, symbolSize=200, padding=20
)

# Save - scale_factor=3 gives 2400x2400 from 800x800 base
# For pie charts, square aspect ratio is more appropriate
chart.save("plot.png", scale_factor=3.0)
