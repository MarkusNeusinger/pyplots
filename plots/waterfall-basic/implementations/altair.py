"""
waterfall-basic: Basic Waterfall Chart
Library: altair
"""

import altair as alt
import pandas as pd


# Data - Quarterly financial breakdown from revenue to net income
categories = [
    "Starting Revenue",
    "Product Sales",
    "Service Revenue",
    "Cost of Goods",
    "Operating Expenses",
    "Marketing",
    "Taxes",
    "Net Income",
]

# Values: first is total, middle are changes, last is calculated total
base_values = [100000, 65000, 35000, -50000, -30000, -15000, -10000, 0]

# Calculate waterfall positions
starts = []
ends = []
types = []
running_total = 0

for i, (_cat, val) in enumerate(zip(categories, base_values, strict=True)):
    if i == 0:
        # First bar: starting total (from 0 to value)
        starts.append(0)
        ends.append(val)
        running_total = val
        types.append("total")
    elif i == len(categories) - 1:
        # Last bar: ending total (from 0 to running_total)
        starts.append(0)
        ends.append(running_total)
        types.append("total")
    else:
        # Change bars: start from running total, end at new total
        starts.append(running_total)
        running_total += val
        ends.append(running_total)
        if val >= 0:
            types.append("positive")
        else:
            types.append("negative")

# Create DataFrame for waterfall chart
data = pd.DataFrame(
    {
        "category": categories,
        "value": base_values,
        "type": types,
        "start": starts,
        "end": ends,
        "order": list(range(len(categories))),
    }
)

# Create labels for display
data["label"] = data.apply(
    lambda row: f"${row['end']:,.0f}"
    if row["type"] == "total"
    else f"{'+' if row['value'] > 0 else ''}{row['value']:,}",
    axis=1,
)

# Label positions (at top of bar for positive/total, at bottom for negative)
data["label_y"] = data.apply(lambda row: max(row["start"], row["end"]) + 3000, axis=1)

# Color mapping
color_scale = alt.Scale(
    domain=["total", "positive", "negative"],
    range=["#306998", "#2E8B57", "#DC3545"],  # Blue for totals, green for positive, red for negative
)

# Explicit x-axis scale with category sort order
x_scale = alt.Scale(domain=categories)

# Create bars
bars = (
    alt.Chart(data)
    .mark_bar(
        cornerRadiusTopLeft=3, cornerRadiusTopRight=3, cornerRadiusBottomLeft=3, cornerRadiusBottomRight=3, size=60
    )
    .encode(
        x=alt.X(
            "category:N",
            title="Category",
            scale=x_scale,
            axis=alt.Axis(labelAngle=-30, labelFontSize=16, titleFontSize=20),
        ),
        y=alt.Y("start:Q", title="Amount ($)", axis=alt.Axis(labelFontSize=16, titleFontSize=20)),
        y2=alt.Y2("end:Q"),
        color=alt.Color(
            "type:N", scale=color_scale, legend=alt.Legend(title="Type", labelFontSize=16, titleFontSize=18)
        ),
        tooltip=[
            alt.Tooltip("category:N", title="Category"),
            alt.Tooltip("end:Q", title="Cumulative", format="$,.0f"),
            alt.Tooltip("value:Q", title="Change", format="+,.0f"),
            alt.Tooltip("type:N", title="Type"),
        ],
    )
)

# Value labels on bars
labels = (
    alt.Chart(data)
    .mark_text(fontSize=14, fontWeight="bold")
    .encode(
        x=alt.X("category:N", scale=x_scale), y=alt.Y("label_y:Q"), text=alt.Text("label:N"), color=alt.value("#333333")
    )
)

# Connecting lines between bars (horizontal lines at the end value of each bar)
# Create data for connector lines
connector_data = []
for i in range(len(data) - 1):
    if data.iloc[i]["type"] != "total" or i == 0:
        connector_data.append({"x_start": i, "x_end": i + 1, "y": data.iloc[i]["end"]})

connector_df = pd.DataFrame(connector_data)

# Map order back to category names for connectors
connector_df["cat_start"] = connector_df["x_start"].map(dict(zip(data["order"], data["category"], strict=True)))
connector_df["cat_end"] = connector_df["x_end"].map(dict(zip(data["order"], data["category"], strict=True)))

# Draw connector lines as rules
connectors = (
    alt.Chart(connector_df)
    .mark_rule(color="#666666", strokeWidth=1.5, strokeDash=[4, 4])
    .encode(x=alt.X("cat_start:N", scale=x_scale), x2=alt.X2("cat_end:N"), y=alt.Y("y:Q"))
)

# Combine chart layers (bars, connectors for cumulative flow, and labels)
chart = (
    alt.layer(bars, connectors, labels)
    .properties(
        width=1600,
        height=900,
        title=alt.Title(text="Quarterly P&L Breakdown · waterfall-basic · altair · pyplots.ai", fontSize=28),
    )
    .configure_view(strokeWidth=0)
    .configure_axis(grid=True, gridOpacity=0.3, gridDash=[4, 4], labelFontSize=16, titleFontSize=20)
    .configure_legend(labelFontSize=16, titleFontSize=18)
)

# Save as PNG (scaled to 4800 x 2700)
chart.save("plot.png", scale_factor=3.0)

# Save interactive HTML
chart.save("plot.html")
