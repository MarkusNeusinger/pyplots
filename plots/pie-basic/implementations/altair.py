"""pyplots.ai
pie-basic: Basic Pie Chart
Library: altair 6.0.0 | Python 3.14.0
Quality: /100 | Updated: 2026-02-14
"""

import altair as alt
import pandas as pd


# Data - Market share of cloud providers
data = pd.DataFrame(
    {"category": ["AWS", "Azure", "Google Cloud", "Alibaba", "Oracle", "Others"], "value": [31, 24, 11, 4, 3, 27]}
)

# Calculate percentages and labels
data["percentage"] = data["value"] / data["value"].sum() * 100
data["label"] = data["percentage"].apply(lambda x: f"{x:.0f}%")

# Color palette - Python Blue first, then cohesive colorblind-safe colors
colors = ["#306998", "#FFD43B", "#4ECDC4", "#FF6B6B", "#95E1D3", "#A8A8A8"]

# Base chart with shared encodings
base = alt.Chart(data).encode(
    theta=alt.Theta("value:Q", stack=True),
    color=alt.Color(
        "category:N",
        scale=alt.Scale(domain=data["category"].tolist(), range=colors),
        legend=alt.Legend(
            title="Provider",
            titleFontSize=20,
            labelFontSize=18,
            symbolSize=300,
            orient="bottom",
            direction="horizontal",
            columns=6,
            titleAnchor="middle",
        ),
    ),
)

# Pie slices with padAngle for separation and cornerRadius for polish
pie = base.mark_arc(
    outerRadius=320, innerRadius=0, stroke="#ffffff", strokeWidth=2.5, padAngle=0.02, cornerRadius=3
).encode(tooltip=[alt.Tooltip("category:N", title="Provider"), alt.Tooltip("value:Q", title="Market Share (%)")])

# Percentage labels outside slices
text = base.mark_text(radius=380, fontSize=21, fontWeight="bold").encode(text="label:N")

# Combine pie and labels
chart = (
    alt.layer(pie, text)
    .properties(
        width=1200,
        height=1200,
        title=alt.Title(
            text="pie-basic · altair · pyplots.ai",
            subtitle="Global Cloud Infrastructure Market Share",
            fontSize=28,
            subtitleFontSize=20,
            subtitleColor="#666666",
            anchor="middle",
        ),
    )
    .configure_view(strokeWidth=0)
)

# Save as PNG (scale_factor=3 gives us 3600x3600 for square format)
chart.save("plot.png", scale_factor=3.0)

# Save interactive HTML
chart.save("plot.html")
