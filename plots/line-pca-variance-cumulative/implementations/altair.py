"""pyplots.ai
line-pca-variance-cumulative: Cumulative Explained Variance for PCA Component Selection
Library: altair | Python 3.13
Quality: pending | Created: 2026-02-17
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

# Threshold lines
thresholds = pd.DataFrame({"Threshold": [90, 95], "Label": ["90%", "95%"]})

# Plot - Cumulative variance line with markers
line = (
    alt.Chart(df)
    .mark_line(strokeWidth=4, color="#306998")
    .encode(
        x=alt.X(
            "Component:Q",
            title="Number of Components",
            scale=alt.Scale(domain=[1, len(cumulative_variance)]),
            axis=alt.Axis(labelFontSize=18, titleFontSize=22, tickMinStep=1),
        ),
        y=alt.Y(
            "Cumulative Variance (%):Q",
            title="Cumulative Explained Variance (%)",
            scale=alt.Scale(domain=[0, 105]),
            axis=alt.Axis(labelFontSize=18, titleFontSize=22),
        ),
    )
)

points = (
    alt.Chart(df)
    .mark_point(size=200, color="#306998", filled=True, stroke="white", strokeWidth=1.5)
    .encode(
        x="Component:Q",
        y="Cumulative Variance (%):Q",
        tooltip=["Component:Q", alt.Tooltip("Cumulative Variance (%):Q", format=".1f")],
    )
)

# Threshold reference lines
threshold_lines = (
    alt.Chart(thresholds)
    .mark_rule(strokeDash=[8, 6], strokeWidth=2, opacity=0.6)
    .encode(
        y="Threshold:Q",
        color=alt.Color(
            "Label:N",
            scale=alt.Scale(domain=["90%", "95%"], range=["#E15759", "#59A14F"]),
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

# Threshold labels on the right side
threshold_text = (
    alt.Chart(thresholds)
    .mark_text(align="right", baseline="bottom", fontSize=18, fontWeight="bold", dx=-10, dy=-6)
    .encode(
        x=alt.value(1600),
        y="Threshold:Q",
        text="Label:N",
        color=alt.Color("Label:N", scale=alt.Scale(domain=["90%", "95%"], range=["#E15759", "#59A14F"]), legend=None),
    )
)

# Combine layers
chart = (
    (threshold_lines + threshold_text + line + points)
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
