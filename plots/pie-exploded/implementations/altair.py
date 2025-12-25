"""pyplots.ai
pie-exploded: Exploded Pie Chart
Library: altair 6.0.0 | Python 3.13.11
Quality: 84/100 | Created: 2025-12-25
"""

import altair as alt
import pandas as pd


# Data - Market share analysis with exploded segments for emphasis
categories = ["Enterprise", "Consumer", "Government", "SMB", "Education"]
values = [38, 25, 18, 12, 7]

# Explode distances: Enterprise (leader) and Government (government contracts) emphasized
# Altair achieves explosion via padAngle (gap between slices) and radius variation
explode = [0.15, 0, 0.10, 0, 0]

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
        "explode": explode,
        "order": range(len(categories)),
    }
)
df["label"] = df["percentage"].apply(lambda x: f"{x:.1f}%")

# Chart dimensions - larger radius to fill more canvas
base_radius = 480

# Base pie chart with all slices
base_pie = (
    alt.Chart(df)
    .mark_arc(outerRadius=base_radius, innerRadius=0, stroke="white", strokeWidth=5, padAngle=0.03)
    .encode(
        theta=alt.Theta("value:Q", stack=True),
        color=alt.Color(
            "category:N",
            scale=alt.Scale(domain=categories, range=colors),
            legend=alt.Legend(
                title="Segment", titleFontSize=26, labelFontSize=22, symbolSize=600, orient="right", offset=20
            ),
        ),
        order=alt.Order("order:O"),
    )
)

# Create explosion effect layers - exploded slices drawn with larger radius and gap
exploded_layers = []
for _, row in df[df["explode"] > 0].iterrows():
    explosion_factor = row["explode"]
    # Explosion creates: larger outer radius + inner gap (donut effect) + wider pad angle
    outer_radius = base_radius + int(explosion_factor * 350)
    inner_gap = int(explosion_factor * 200)

    exploded_arc = (
        alt.Chart(df)
        .transform_filter(alt.datum.category == row["category"])
        .mark_arc(outerRadius=outer_radius, innerRadius=inner_gap, stroke="white", strokeWidth=6, padAngle=0.08)
        .encode(
            theta=alt.Theta("value:Q", stack=True),
            color=alt.Color("category:N", scale=alt.Scale(domain=categories, range=colors), legend=None),
            order=alt.Order("order:O"),
        )
    )
    exploded_layers.append(exploded_arc)

# Labels positioned for visibility on all slices
labels = (
    alt.Chart(df)
    .mark_text(radius=320, fontSize=36, fontWeight="bold", fill="white")
    .encode(theta=alt.Theta("value:Q", stack=True), text="label:N", order=alt.Order("order:O"))
)

# Combine all layers
chart = (
    alt.layer(base_pie, *exploded_layers, labels)
    .properties(
        width=1200,
        height=1200,
        title=alt.Title("pie-exploded · altair · pyplots.ai", fontSize=36, anchor="middle", dy=-15),
    )
    .configure_view(strokeWidth=0)
)

# Save outputs
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
