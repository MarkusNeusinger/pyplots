""" pyplots.ai
pictogram-basic: Pictogram Chart (Isotype Visualization)
Library: altair 6.0.0 | Python 3.14.3
Quality: 79/100 | Created: 2026-03-10
"""

import altair as alt
import pandas as pd


# Data - Fruit production (thousands of tonnes)
categories = ["Apples", "Oranges", "Bananas", "Grapes", "Mangoes"]
values = [35, 22, 18, 12, 8]
colors = ["#306998", "#E8A838", "#5BA65B", "#9B59B6", "#E74C3C"]
unit_value = 5
max_icons = max(v // unit_value + (1 if v % unit_value else 0) for v in values)
x_max = max_icons + 1.5

# Build row data: one row per icon position using quantitative x for tight spacing
rows = []
for cat, val, color in zip(categories, values, colors, strict=True):
    full_icons = val // unit_value
    remainder = (val % unit_value) / unit_value

    for i in range(full_icons):
        rows.append({"category": cat, "col": i, "opacity": 1.0, "color": color, "value": val})

    if remainder > 0:
        rows.append({"category": cat, "col": full_icons, "opacity": round(remainder, 2), "color": color, "value": val})

df = pd.DataFrame(rows)

# Category sort order (by value descending)
sort_order = [c for _, c in sorted(zip(values, categories, strict=True), reverse=True)]

# Plot - circles arranged in a grid
chart = (
    alt.Chart(df)
    .mark_point(size=1200, filled=True)
    .encode(
        x=alt.X(
            "col:Q",
            title=None,
            scale=alt.Scale(domain=[-0.5, x_max]),
            axis=alt.Axis(labels=False, ticks=False, domain=False, grid=False),
        ),
        y=alt.Y(
            "category:N",
            title=None,
            sort=sort_order,
            axis=alt.Axis(
                labelFontSize=20, labelFontWeight="bold", ticks=False, domain=False, grid=False, labelPadding=16
            ),
        ),
        color=alt.Color("color:N", scale=None),
        opacity=alt.Opacity("opacity:Q", scale=alt.Scale(domain=[0, 1]), legend=None),
        tooltip=[alt.Tooltip("category:N", title="Category"), alt.Tooltip("value:Q", title="Production (k tonnes)")],
    )
)

# Value labels at end of each row
label_data = []
for cat, val in zip(categories, values, strict=True):
    icon_count = val // unit_value + (1 if val % unit_value else 0)
    label_data.append({"category": cat, "col": icon_count + 0.2, "label": f"{val}k", "value": val})

label_df = pd.DataFrame(label_data)

labels = (
    alt.Chart(label_df)
    .mark_text(align="left", baseline="middle", fontSize=18, fontWeight="bold", color="#555555")
    .encode(x=alt.X("col:Q"), y=alt.Y("category:N", sort=sort_order), text=alt.Text("label:N"))
)

# Subtitle legend text
subtitle_df = pd.DataFrame([{"text": f"\u25cf = {unit_value}k tonnes    (partial circle = fractional amount)"}])

subtitle = (
    alt.Chart(subtitle_df)
    .mark_text(align="left", baseline="top", fontSize=16, color="#888888")
    .encode(x=alt.value(0), y=alt.value(16), text=alt.Text("text:N"))
)

# Combine layers
combined = (
    (chart + labels + subtitle)
    .properties(
        width=1600,
        height=900,
        title=alt.Title(text="pictogram-basic \u00b7 altair \u00b7 pyplots.ai", fontSize=28, anchor="start", offset=20),
    )
    .configure_view(strokeWidth=0)
)

# Save
combined.save("plot.png", scale_factor=3.0)
combined.save("plot.html")
