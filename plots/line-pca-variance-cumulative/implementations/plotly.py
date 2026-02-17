""" pyplots.ai
line-pca-variance-cumulative: Cumulative Explained Variance for PCA Component Selection
Library: plotly 6.5.2 | Python 3.14.3
Quality: 88/100 | Created: 2026-02-17
"""

import numpy as np
import plotly.graph_objects as go
from sklearn.datasets import load_wine
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


# Data - PCA on Wine dataset
wine = load_wine()
X_scaled = StandardScaler().fit_transform(wine.data)
pca = PCA().fit(X_scaled)

explained_variance = pca.explained_variance_ratio_
cumulative_variance = np.cumsum(explained_variance) * 100
n_components = np.arange(1, len(explained_variance) + 1)

# Threshold crossings
threshold_90 = np.argmax(cumulative_variance >= 90) + 1
threshold_95 = np.argmax(cumulative_variance >= 95) + 1

# Plot
fig = go.Figure()

# Individual variance as bars
fig.add_trace(
    go.Bar(
        x=n_components,
        y=explained_variance * 100,
        marker={"color": "rgba(48, 105, 152, 0.25)"},
        name="Individual",
        hovertemplate="PC%{x}<br>Variance: %{y:.1f}%<extra></extra>",
    )
)

# Cumulative variance line
fig.add_trace(
    go.Scatter(
        x=n_components,
        y=cumulative_variance,
        mode="lines+markers",
        line={"color": "#306998", "width": 5},
        marker={"size": 16, "color": "#306998"},
        name="Cumulative",
        hovertemplate="PC%{x}<br>Cumulative: %{y:.1f}%<extra></extra>",
    )
)

# 90% threshold line
fig.add_hline(
    y=90,
    line_dash="dash",
    line_color="#E8871E",
    line_width=2,
    annotation_text="90%",
    annotation_position="right",
    annotation_font={"size": 24, "color": "#E8871E"},
)

# 95% threshold line
fig.add_hline(
    y=95,
    line_dash="dash",
    line_color="#C7402D",
    line_width=2,
    annotation_text="95%",
    annotation_position="right",
    annotation_font={"size": 24, "color": "#C7402D"},
)

# Layout
fig.update_layout(
    title={
        "text": "line-pca-variance-cumulative · plotly · pyplots.ai",
        "font": {"size": 40},
        "x": 0.5,
        "xanchor": "center",
    },
    xaxis={
        "title": {"text": "Principal Component", "font": {"size": 36}},
        "tickfont": {"size": 28},
        "tickmode": "linear",
        "tick0": 1,
        "dtick": 1,
        "showgrid": False,
    },
    yaxis={
        "title": {"text": "Explained Variance (%)", "font": {"size": 36}},
        "tickfont": {"size": 28},
        "range": [0, 105],
        "showgrid": True,
        "gridwidth": 1,
        "gridcolor": "rgba(0,0,0,0.1)",
    },
    template="plotly_white",
    legend={"font": {"size": 26}, "x": 0.02, "y": 0.98, "bgcolor": "rgba(255,255,255,0.8)"},
    margin={"t": 120, "b": 100, "l": 120, "r": 80},
    bargap=0.4,
)

# Save
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html")
