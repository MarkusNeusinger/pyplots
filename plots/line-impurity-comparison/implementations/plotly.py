"""pyplots.ai
line-impurity-comparison: Gini Impurity vs Entropy Comparison
Library: plotly | Python 3.13
Quality: pending | Created: 2026-02-17
"""

import numpy as np
import plotly.graph_objects as go


# Data
p = np.linspace(0, 1, 200)

gini_raw = 2 * p * (1 - p)
gini = gini_raw / gini_raw.max()

entropy_raw = np.where((p == 0) | (p == 1), 0.0, -p * np.log2(p) - (1 - p) * np.log2(1 - p))
entropy = entropy_raw / entropy_raw.max()

# Plot
fig = go.Figure()

fig.add_trace(
    go.Scatter(x=p, y=gini, mode="lines", name="Gini: 2p(1−p) [scaled]", line={"color": "#306998", "width": 3.5})
)

fig.add_trace(
    go.Scatter(
        x=p,
        y=entropy,
        mode="lines",
        name="Entropy: −p log₂p − (1−p) log₂(1−p)",
        line={"color": "#E8833A", "width": 3.5, "dash": "dash"},
    )
)

# Annotation at p=0.5 maximum
fig.add_annotation(
    x=0.5,
    y=1.0,
    text="Max impurity at p = 0.5",
    showarrow=True,
    arrowhead=2,
    arrowsize=1.5,
    arrowwidth=2,
    arrowcolor="#555555",
    ax=0,
    ay=-50,
    font={"size": 18, "color": "#333333"},
    bgcolor="rgba(255,255,255,0.85)",
    bordercolor="#CCCCCC",
    borderwidth=1,
    borderpad=6,
)

# Style
fig.update_layout(
    title={
        "text": "line-impurity-comparison · plotly · pyplots.ai",
        "font": {"size": 28, "color": "#222222"},
        "x": 0.5,
        "xanchor": "center",
    },
    xaxis={
        "title": {"text": "Probability (p)", "font": {"size": 22}},
        "tickfont": {"size": 18},
        "range": [-0.02, 1.02],
        "showgrid": False,
        "showline": True,
        "linecolor": "#CCCCCC",
        "zeroline": False,
    },
    yaxis={
        "title": {"text": "Impurity Measure (normalized)", "font": {"size": 22}},
        "tickfont": {"size": 18},
        "range": [-0.02, 1.08],
        "showgrid": True,
        "gridcolor": "rgba(0,0,0,0.08)",
        "gridwidth": 1,
        "showline": True,
        "linecolor": "#CCCCCC",
        "zeroline": False,
    },
    template="plotly_white",
    legend={
        "font": {"size": 16},
        "x": 0.02,
        "y": 0.55,
        "bgcolor": "rgba(255,255,255,0.85)",
        "bordercolor": "#DDDDDD",
        "borderwidth": 1,
    },
    plot_bgcolor="#FFFFFF",
    paper_bgcolor="#FFFFFF",
    margin={"l": 80, "r": 40, "t": 80, "b": 60},
)

# Save
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html", include_plotlyjs="cdn")
