"""pyplots.ai
pie-exploded: Exploded Pie Chart
Library: altair 6.0.0 | Python 3.13.11
Quality: 82/100 | Created: 2025-12-25
"""

import altair as alt
import pandas as pd


# Data - Market share analysis with exploded segments for emphasis
categories = ["Enterprise", "Consumer", "Government", "SMB", "Education"]
values = [38, 25, 18, 12, 7]

# Explode distances: Enterprise (leader) and Government (government contracts) emphasized
# Values represent offset distance from center (0 = no explode, 0.1 = typical)
explode = [0.12, 0, 0.08, 0, 0]

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

# Separate exploded and non-exploded slices
exploded_df = df[df["explode"] > 0]

# Base radius for pie chart (large to fill canvas)
base_radius = 450

# Base pie with all slices (centered)
base_pie = (
    alt.Chart(df)
    .mark_arc(outerRadius=base_radius, innerRadius=0, stroke="white", strokeWidth=4)
    .encode(
        theta=alt.Theta("value:Q", stack=True),
        color=alt.Color(
            "category:N",
            scale=alt.Scale(domain=categories, range=colors),
            legend=alt.Legend(
                title="Segment", titleFontSize=24, labelFontSize=20, symbolSize=400, orient="right", offset=40
            ),
        ),
        order=alt.Order("order:O"),
    )
)

# Create exploded slice overlays with larger radius to create visual separation
exploded_layers = []
for _, row in exploded_df.iterrows():
    slice_df = df[df["category"] == row["category"]]
    explosion_amount = row["explode"]

    # Larger outer radius and inner gap creates dramatic explosion effect
    outer_r = base_radius + int(explosion_amount * 250)
    inner_r = int(explosion_amount * 120)

    exploded_arc = (
        alt.Chart(slice_df)
        .mark_arc(outerRadius=outer_r, innerRadius=inner_r, stroke="white", strokeWidth=5)
        .encode(
            theta=alt.Theta("value:Q"),
            color=alt.Color("category:N", scale=alt.Scale(domain=categories, range=colors), legend=None),
        )
    )
    exploded_layers.append(exploded_arc)

# Labels positioned at appropriate radius for visibility
labels = (
    alt.Chart(df)
    .mark_text(radius=310, fontSize=28, fontWeight="bold", fill="white")
    .encode(theta=alt.Theta("value:Q", stack=True), text="label:N", order=alt.Order("order:O"))
)

# Combine all layers: base pie, exploded overlays, then labels on top
all_layers = [base_pie] + exploded_layers + [labels]

chart = (
    alt.layer(*all_layers)
    .properties(
        width=1200,
        height=1200,
        title=alt.Title("pie-exploded · altair · pyplots.ai", fontSize=32, anchor="middle", dy=-20),
    )
    .configure_view(strokeWidth=0)
)

# Save outputs
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
