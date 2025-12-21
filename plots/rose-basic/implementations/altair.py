""" pyplots.ai
rose-basic: Basic Rose Chart
Library: altair 6.0.0 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-17
"""

import altair as alt
import pandas as pd


# Data - Monthly rainfall in mm (cyclical 12-month pattern)
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
rainfall = [78, 52, 68, 45, 35, 28, 22, 30, 55, 85, 92, 88]

n = len(months)
max_val = max(rainfall)

# Create DataFrame with month order for proper sorting
df = pd.DataFrame({"month": months, "value": rainfall, "order": range(n)})

# Color palette - Python Blue first, then colorblind-safe colors
colors = [
    "#306998",
    "#FFD43B",
    "#4ECDC4",
    "#FF6B6B",
    "#95E1D3",
    "#F38181",
    "#A8D5BA",
    "#FFC93C",
    "#5D9CEC",
    "#AC92EB",
    "#EC87C0",
    "#48CFAD",
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
            legend=alt.Legend(title="Month", titleFontSize=20, labelFontSize=18, symbolSize=300, orient="right"),
        ),
        tooltip=[alt.Tooltip("month:N", title="Month"), alt.Tooltip("value:Q", title="Rainfall (mm)")],
    )
)

# Text labels showing values on each segment
text = (
    alt.Chart(df)
    .mark_text(radiusOffset=25, fontSize=20, fontWeight="bold")
    .encode(
        theta=alt.Theta("order:O", stack=True),
        radius=alt.Radius("value:Q", scale=alt.Scale(type="sqrt", zero=True, rangeMin=20)),
        text=alt.Text("value:Q"),
        color=alt.value("#333333"),
    )
)

# Combine layers
chart = (
    alt.layer(rose, text)
    .properties(
        width=1400,
        height=1200,
        title=alt.Title(text="Monthly Rainfall · rose-basic · altair · pyplots.ai", fontSize=28),
    )
    .configure_view(strokeWidth=0)
)

# Save (scale_factor=3 gives ~4200x3600, close to target)
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
