"""pyplots.ai
pie-exploded: Exploded Pie Chart
Library: altair | Python 3.13
Quality: pending | Created: 2025-12-25
"""

import altair as alt
import pandas as pd


# Data - Market share analysis with highlighted leader
categories = ["Enterprise", "Consumer", "Government", "SMB", "Education"]
values = [38, 25, 18, 12, 7]

# Colors - Python palette first, then colorblind-safe
colors = ["#306998", "#FFD43B", "#4ECDC4", "#FF6B6B", "#95E1D3"]

# Calculate percentages
total = sum(values)
percentages = [v / total * 100 for v in values]

# Create dataframe
df = pd.DataFrame(
    {
        "category": categories,
        "value": values,
        "percentage": percentages,
        "explode": [1, 0, 0, 0, 0],
        "order": range(len(categories)),
    }
)
df["label"] = df["percentage"].apply(lambda x: f"{x:.1f}%")

# Base encoding for pie with all data
base = alt.Chart(df).encode(
    theta=alt.Theta("value:Q", stack=True),
    color=alt.Color(
        "category:N",
        scale=alt.Scale(domain=categories, range=colors),
        legend=alt.Legend(
            title="Segment", titleFontSize=22, labelFontSize=18, symbolSize=350, orient="right", offset=20
        ),
    ),
    order=alt.Order("order:O"),
)

# Main pie slices
pie = base.mark_arc(outerRadius=350, innerRadius=0, stroke="white", strokeWidth=3)

# Exploded overlay for Enterprise
exploded = (
    alt.Chart(df[df["explode"] == 1])
    .mark_arc(outerRadius=390, innerRadius=40, stroke="white", strokeWidth=3)
    .encode(
        theta=alt.Theta("value:Q"),
        color=alt.Color("category:N", scale=alt.Scale(domain=categories, range=colors), legend=None),
    )
)

# Labels - ensure they render on top
labels = base.mark_text(radius=220, fontSize=24, fontWeight="bold", fill="white").encode(text="label:N")

# Layer order: pie first, exploded overlay, labels last (on top)
chart = (
    alt.layer(pie, exploded, labels)
    .properties(
        width=1200,
        height=1200,
        title=alt.Title("pie-exploded \u00b7 altair \u00b7 pyplots.ai", fontSize=28, anchor="middle"),
    )
    .configure_view(strokeWidth=0)
)

# Save outputs
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
