"""
pie-basic: Basic Pie Chart
Library: altair
"""

import altair as alt
import pandas as pd


# Data - Budget allocation by department
data = pd.DataFrame(
    {"category": ["Engineering", "Marketing", "Operations", "Sales", "HR", "R&D"], "value": [35, 20, 18, 15, 7, 5]}
)

# Calculate percentages for labels
data["percentage"] = data["value"] / data["value"].sum() * 100
data["label"] = data["percentage"].apply(lambda x: f"{x:.1f}%")

# Color palette - Python Blue first, then colorblind-safe colors
colors = ["#306998", "#FFD43B", "#4ECDC4", "#FF6B6B", "#95E1D3", "#F38181"]

# Base chart
base = alt.Chart(data).encode(
    theta=alt.Theta("value:Q", stack=True),
    color=alt.Color(
        "category:N",
        scale=alt.Scale(range=colors),
        legend=alt.Legend(title="Department", titleFontSize=20, labelFontSize=18, symbolSize=300, orient="right"),
    ),
    tooltip=[
        alt.Tooltip("category:N", title="Department"),
        alt.Tooltip("value:Q", title="Budget Share"),
        alt.Tooltip("label:N", title="Percentage"),
    ],
)

# Pie slices with slight explode effect on largest slice
pie = base.mark_arc(outerRadius=320, innerRadius=0, stroke="#ffffff", strokeWidth=2)

# Percentage labels on slices
text = base.mark_text(radius=380, fontSize=20, fontWeight="bold").encode(text="label:N")

# Combine pie and labels
chart = (
    alt.layer(pie, text)
    .properties(
        width=1400, height=800, title=alt.Title(text="pie-basic · altair · pyplots.ai", fontSize=28, anchor="middle")
    )
    .configure_view(strokeWidth=0)
)

# Save as PNG (scale_factor=3 gives us close to 4800x2700)
chart.save("plot.png", scale_factor=3.0)

# Save interactive HTML
chart.save("plot.html")
