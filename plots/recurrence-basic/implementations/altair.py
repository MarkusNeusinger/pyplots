""" pyplots.ai
recurrence-basic: Recurrence Plot for Nonlinear Time Series
Library: altair 6.0.0 | Python 3.14.3
Quality: 89/100 | Created: 2026-03-14
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Logistic map near type-I intermittency (r=3.8284)
np.random.seed(42)
n_steps = 200
r = 3.8284
x = np.zeros(n_steps)
x[0] = 0.1
for i in range(1, n_steps):
    x[i] = r * x[i - 1] * (1 - x[i - 1])

# Time-delay embedding (dimension=3, delay=1)
embedding_dim = 3
delay = 1
n_embedded = n_steps - (embedding_dim - 1) * delay
embedded = np.column_stack([x[d * delay : d * delay + n_embedded] for d in range(embedding_dim)])

# Compute pairwise Euclidean distance matrix
diff = embedded[:, np.newaxis, :] - embedded[np.newaxis, :, :]
distance_matrix = np.sqrt(np.sum(diff**2, axis=2))
threshold = 0.15
recurrence_matrix = distance_matrix < threshold

# Build long-form dataframe for recurrence points with distance values
rows, cols = np.where(recurrence_matrix)
distances = distance_matrix[rows, cols]
df = pd.DataFrame({"time_i": rows, "time_j": cols, "distance": distances})

# Interactive selection for cross-highlighting rows/columns on hover
hover = alt.selection_point(on="pointerover", fields=["time_i"], nearest=True, empty=False)

# Main recurrence heatmap layer
heatmap = (
    alt.Chart(df)
    .mark_rect()
    .encode(
        x=alt.X(
            "time_i:O",
            title="Time Index (step)",
            axis=alt.Axis(
                labelFontSize=16, titleFontSize=20, titlePadding=12, values=list(range(0, n_embedded, 25)), grid=False
            ),
            scale=alt.Scale(paddingInner=0, paddingOuter=0),
        ),
        y=alt.Y(
            "time_j:O",
            title="Time Index (step)",
            axis=alt.Axis(
                labelFontSize=16, titleFontSize=20, titlePadding=12, values=list(range(0, n_embedded, 25)), grid=False
            ),
            scale=alt.Scale(paddingInner=0, paddingOuter=0),
        ),
        color=alt.Color(
            "distance:Q",
            title="Distance",
            scale=alt.Scale(scheme="viridis", reverse=True, domain=[0, threshold]),
            legend=alt.Legend(
                titleFontSize=16,
                labelFontSize=14,
                orient="right",
                gradientLength=350,
                gradientThickness=18,
                titlePadding=8,
            ),
        ),
        opacity=alt.condition(hover, alt.value(1.0), alt.value(0.85)),
        tooltip=[
            alt.Tooltip("time_i:Q", title="Time i"),
            alt.Tooltip("time_j:Q", title="Time j"),
            alt.Tooltip("distance:Q", title="Distance", format=".4f"),
        ],
    )
    .add_params(hover)
)

# Annotation markers for key structural features
annotations_data = pd.DataFrame(
    {"label": ["Main diagonal\n(self-recurrence)", "Laminar\nphase"], "x": [50, 135], "y": [50, 135]}
)

annotation_marks = (
    alt.Chart(annotations_data)
    .mark_text(fontSize=14, fontWeight="bold", color="#1a1a1a", align="left", dx=12, dy=-10, lineBreak="\n")
    .encode(x=alt.X("x:O"), y=alt.Y("y:O"), text="label:N")
)

# Layer the heatmap and annotations
chart = (
    alt.layer(heatmap, annotation_marks)
    .properties(
        width=1100,
        height=1100,
        title=alt.Title(
            "recurrence-basic · altair · pyplots.ai",
            subtitle=[
                "Logistic map (r = 3.8284) · Euclidean distance with ε = 0.15 · dim = 3, τ = 1",
                "Bright cells = near-identical states · Diagonal lines = determinism · Vertical/horizontal lines = laminar states",
            ],
            fontSize=28,
            subtitleFontSize=17,
            subtitleColor="#555555",
            anchor="start",
            offset=20,
        ),
        padding={"left": 24, "right": 24, "top": 24, "bottom": 24},
    )
    .configure_axis(grid=False)
    .configure_view(strokeWidth=0)
)

# Save
chart.save("plot.png", scale_factor=3.3)
chart.save("plot.html")
