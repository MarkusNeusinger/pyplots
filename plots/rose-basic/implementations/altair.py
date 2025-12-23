"""pyplots.ai
rose-basic: Basic Rose Chart
Library: altair | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import altair as alt
import pandas as pd


# Data - Monthly rainfall in mm (cyclical 12-month pattern)
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
rainfall = [78, 52, 68, 45, 35, 28, 22, 30, 55, 85, 92, 88]

n = len(months)

# Create DataFrame with month order for proper sorting
df = pd.DataFrame({"month": months, "value": rainfall, "order": range(n)})

# Color palette - Python Blue first, then Python Yellow, then colorblind-safe colors
colors = [
    "#306998",  # Python Blue
    "#FFD43B",  # Python Yellow
    "#4ECDC4",  # Teal
    "#FF6B6B",  # Coral
    "#95E1D3",  # Mint
    "#F38181",  # Salmon
    "#A8D5BA",  # Sage
    "#FFC93C",  # Gold
    "#5D9CEC",  # Sky Blue
    "#AC92EB",  # Lavender
    "#EC87C0",  # Pink
    "#48CFAD",  # Seafoam
]

# Rose chart using mark_arc with theta for equal angles and radius for values
# In a rose chart: theta (angle) is equal per category, radius varies by value
rose = (
    alt.Chart(df)
    .mark_arc(stroke="#ffffff", strokeWidth=2)
    .encode(
        # Use theta as nominal to create equal-width segments
        theta=alt.Theta("order:O", stack=True),
        # Radius proportional to value (the key characteristic of rose charts)
        radius=alt.Radius("value:Q", scale=alt.Scale(type="sqrt", zero=True, rangeMin=20)),
        color=alt.Color(
            "month:N",
            scale=alt.Scale(domain=months, range=colors),
            legend=alt.Legend(
                title="Month", titleFontSize=22, labelFontSize=20, symbolSize=400, orient="right", titlePadding=10
            ),
        ),
        tooltip=[alt.Tooltip("month:N", title="Month"), alt.Tooltip("value:Q", title="Rainfall (mm)")],
    )
)

# Text labels showing values on each segment
text = (
    alt.Chart(df)
    .mark_text(radiusOffset=30, fontSize=22, fontWeight="bold")
    .encode(
        theta=alt.Theta("order:O", stack=True),
        radius=alt.Radius("value:Q", scale=alt.Scale(type="sqrt", zero=True, rangeMin=20)),
        text=alt.Text("value:Q"),
        color=alt.value("#333333"),
    )
)

# Combine layers - 16:9 landscape format (1600x900 * 3 = 4800x2700)
chart = (
    alt.layer(rose, text)
    .properties(
        width=1600,
        height=900,
        title=alt.Title(text="Monthly Rainfall · rose-basic · altair · pyplots.ai", fontSize=32, anchor="middle"),
    )
    .configure_view(strokeWidth=0)
)

# Save at scale_factor=3 for 4800x2700 landscape format
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
