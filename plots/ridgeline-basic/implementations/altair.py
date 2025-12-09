"""
ridgeline-basic: Ridgeline Plot
Library: altair
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Monthly temperature distributions
np.random.seed(42)
months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

# Generate temperature data with seasonal patterns
data = []
for i, month in enumerate(months):
    # Seasonal temperature pattern (Northern Hemisphere)
    base_temp = 5 + 20 * np.sin(np.pi * (i - 3) / 6)  # Peak in July
    temps = np.random.normal(base_temp, 5, 150)
    for temp in temps:
        data.append({"month": month, "temperature": temp})

df = pd.DataFrame(data)

# Create a step value for vertical positioning
month_order = {month: i for i, month in enumerate(months)}
df["month_num"] = df["month"].map(month_order)

# Define colors - seasonal gradient (blue=cold, orange=warm)
# Colors match temperature patterns: cold winters (blue) to warm summers (orange)
colors = [
    "#306998",  # January - Python Blue (cold)
    "#3b7ba8",  # February
    "#59a0c4",  # March
    "#8cc4d4",  # April
    "#b4d4d8",  # May
    "#f0b070",  # June
    "#f97316",  # July - Orange (peak summer)
    "#f99548",  # August
    "#e0c9a8",  # September
    "#8cc4d4",  # October
    "#59a0c4",  # November
    "#306998",  # December - Python Blue (cold)
]

# Create ridgeline using faceted area charts
# Each row is a separate density chart, vertically offset
chart = (
    alt.Chart(df)
    .transform_density(density="temperature", as_=["temperature", "density"], groupby=["month"], extent=[-15, 45])
    .mark_area(fillOpacity=0.7, stroke="white", strokeWidth=1)
    .encode(
        x=alt.X("temperature:Q", title="Temperature (°C)", scale=alt.Scale(domain=[-15, 45])),
        y=alt.Y("density:Q", title=None, scale=alt.Scale(range=[80, 0]), axis=None),
        fill=alt.Fill("month:N", scale=alt.Scale(domain=months, range=colors), legend=None),
        row=alt.Row(
            "month:N",
            title=None,
            header=alt.Header(labelAngle=0, labelAlign="right", labelFontSize=14, labelPadding=10),
            sort=months,
            spacing=-30,  # Negative spacing creates overlap
        ),
    )
    .properties(width=1400, height=60, title="Monthly Temperature Distributions")
    .configure_view(stroke=None)
    .configure_facet(spacing=0)
    .configure_title(fontSize=24, anchor="middle")
)

# Save outputs
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
