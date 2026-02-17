"""pyplots.ai
line-pca-variance-cumulative: Cumulative Explained Variance for PCA Component Selection
Library: altair 6.0.0 | Python 3.14.3
Quality: 82/100 | Created: 2026-02-17
"""

import altair as alt
import numpy as np
import pandas as pd
from sklearn.datasets import load_wine
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


# Data - PCA on the Wine dataset (13 features)
wine = load_wine()
X_scaled = StandardScaler().fit_transform(wine.data)
pca = PCA().fit(X_scaled)

cumulative_variance = np.cumsum(pca.explained_variance_ratio_) * 100
n_components = np.arange(1, len(cumulative_variance) + 1)

df = pd.DataFrame({"Component": n_components, "Cumulative Variance (%)": cumulative_variance})

# Detect elbow point using maximum distance from diagonal (kneedle method)
x_norm = (n_components - n_components[0]) / (n_components[-1] - n_components[0])
y_norm = (cumulative_variance - cumulative_variance[0]) / (cumulative_variance[-1] - cumulative_variance[0])
distances = np.abs(y_norm - x_norm)
elbow_idx = int(np.argmax(distances))
elbow_component = n_components[elbow_idx]
elbow_value = cumulative_variance[elbow_idx]

# Threshold crossing points
threshold_colors = alt.Scale(domain=["90%", "95%"], range=["#4E79A7", "#F28E2B"])
thresholds = pd.DataFrame({"Threshold": [90, 95], "Label": ["90%", "95%"]})

crossing_points = []
for thresh in [90, 95]:
    idx = int(np.searchsorted(cumulative_variance, thresh))
    if idx < len(cumulative_variance):
        crossing_points.append(
            {"Component": idx + 1, "Cumulative Variance (%)": cumulative_variance[idx], "Label": f"{thresh}%"}
        )
crossing_df = pd.DataFrame(crossing_points)

# Shared scale definitions for consistent axes across layers
y_scale = alt.Scale(domain=[30, 105])
x_scale = alt.Scale(domain=[1, len(cumulative_variance)])

# Elbow annotation data
elbow_df = pd.DataFrame([{"Component": elbow_component, "Cumulative Variance (%)": elbow_value}])

# Plot - Cumulative variance line with markers
line = (
    alt.Chart(df)
    .mark_line(strokeWidth=4, color="#306998")
    .encode(
        x=alt.X(
            "Component:Q",
            title="Number of Components",
            scale=x_scale,
            axis=alt.Axis(labelFontSize=18, titleFontSize=22, tickMinStep=1),
        ),
        y=alt.Y(
            "Cumulative Variance (%):Q",
            title="Cumulative Explained Variance (%)",
            scale=y_scale,
            axis=alt.Axis(labelFontSize=18, titleFontSize=22),
        ),
    )
)

points = (
    alt.Chart(df)
    .mark_point(size=200, color="#306998", filled=True, stroke="white", strokeWidth=1.5)
    .encode(
        x=alt.X("Component:Q", scale=x_scale),
        y=alt.Y("Cumulative Variance (%):Q", scale=y_scale),
        tooltip=["Component:Q", alt.Tooltip("Cumulative Variance (%):Q", format=".1f")],
    )
)

# Threshold reference lines (colorblind-safe blue-orange palette)
threshold_lines = (
    alt.Chart(thresholds)
    .mark_rule(strokeDash=[8, 6], strokeWidth=2, opacity=0.6)
    .encode(
        y=alt.Y("Threshold:Q", scale=y_scale),
        color=alt.Color(
            "Label:N",
            scale=threshold_colors,
            legend=alt.Legend(
                title="Threshold",
                titleFontSize=20,
                labelFontSize=18,
                orient="right",
                symbolStrokeWidth=3,
                symbolSize=200,
                symbolDash=[8, 6],
            ),
        ),
    )
)

# Threshold crossing markers - diamonds where line crosses thresholds
crossing_markers = (
    alt.Chart(crossing_df)
    .mark_point(shape="diamond", size=350, filled=True, stroke="#333", strokeWidth=1.5)
    .encode(
        x=alt.X("Component:Q", scale=x_scale),
        y=alt.Y("Cumulative Variance (%):Q", scale=y_scale),
        color=alt.Color("Label:N", scale=threshold_colors, legend=None),
        tooltip=[
            alt.Tooltip("Component:Q", title="Components needed"),
            alt.Tooltip("Cumulative Variance (%):Q", format=".1f"),
            alt.Tooltip("Label:N", title="Threshold"),
        ],
    )
)

# Elbow point annotation
elbow_marker = (
    alt.Chart(elbow_df)
    .mark_point(shape="triangle-up", size=400, color="#E45756", filled=True, stroke="#333", strokeWidth=1.5)
    .encode(
        x=alt.X("Component:Q", scale=x_scale),
        y=alt.Y("Cumulative Variance (%):Q", scale=y_scale),
        tooltip=[
            alt.Tooltip("Component:Q", title="Elbow at component"),
            alt.Tooltip("Cumulative Variance (%):Q", format=".1f"),
        ],
    )
)

elbow_label = (
    alt.Chart(elbow_df)
    .mark_text(fontSize=18, fontWeight="bold", color="#E45756", dy=-22, dx=25)
    .encode(
        x=alt.X("Component:Q", scale=x_scale),
        y=alt.Y("Cumulative Variance (%):Q", scale=y_scale),
        text=alt.value(f"Elbow (PC {elbow_component})"),
    )
)

# Combine layers
chart = (
    (threshold_lines + line + points + crossing_markers + elbow_marker + elbow_label)
    .properties(
        width=1600,
        height=900,
        title=alt.Title(text="line-pca-variance-cumulative · altair · pyplots.ai", fontSize=28, anchor="middle"),
    )
    .configure_axis(grid=True, gridOpacity=0.2, gridDash=[4, 4])
    .configure_view(strokeWidth=0)
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
