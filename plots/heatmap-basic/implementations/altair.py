"""pyplots.ai
heatmap-basic: Basic Heatmap
Library: altair | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - create a matrix with patterns
np.random.seed(42)
rows = ["Row A", "Row B", "Row C", "Row D", "Row E", "Row F", "Row G", "Row H"]
cols = ["Col 1", "Col 2", "Col 3", "Col 4", "Col 5", "Col 6", "Col 7", "Col 8"]

# Generate values with some patterns (diagonal pattern + noise)
values = []
for i, row in enumerate(rows):
    for j, col in enumerate(cols):
        # Create pattern: higher values near diagonal, add noise
        base = 100 - abs(i - j) * 12
        noise = np.random.randn() * 10
        values.append({"x": col, "y": row, "value": base + noise})

df = pd.DataFrame(values)

# Plot - heatmap base
heatmap = (
    alt.Chart(df)
    .mark_rect()
    .encode(
        x=alt.X("x:N", title="Column", axis=alt.Axis(labelFontSize=16, titleFontSize=20)),
        y=alt.Y("y:N", title="Row", axis=alt.Axis(labelFontSize=16, titleFontSize=20)),
        color=alt.Color(
            "value:Q",
            scale=alt.Scale(scheme="blueorange", domainMid=50),
            legend=alt.Legend(title="Value", titleFontSize=18, labelFontSize=16),
        ),
        tooltip=["x:N", "y:N", "value:Q"],
    )
)

# Add text annotations
text = (
    alt.Chart(df)
    .mark_text(fontSize=18)
    .encode(
        x=alt.X("x:N"),
        y=alt.Y("y:N"),
        text=alt.Text("value:Q", format=".0f"),
        color=alt.condition(alt.datum.value > 70, alt.value("white"), alt.value("black")),
    )
)

# Combine heatmap and text, then apply configuration
chart = (
    (heatmap + text)
    .properties(width=1400, height=800, title=alt.Title("heatmap-basic · altair · pyplots.ai", fontSize=28))
    .configure_axis(labelFontSize=16, titleFontSize=20, grid=False)
    .configure_view(strokeWidth=0)
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
