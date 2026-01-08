"""pyplots.ai
linked-views-selection: Multiple Linked Views with Selection Sync
Library: plotly | Python 3.13
Quality: pending | Created: 2025-01-08
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Data - Iris-like multivariate dataset with clear clusters
np.random.seed(42)

# Create 3 distinct groups with different characteristics
n_per_group = 50
categories = ["Setosa", "Versicolor", "Virginica"]
colors = ["#306998", "#FFD43B", "#E53935"]

# Generate clustered data
sepal_length = np.concatenate(
    [
        np.random.normal(5.0, 0.35, n_per_group),
        np.random.normal(5.9, 0.50, n_per_group),
        np.random.normal(6.6, 0.60, n_per_group),
    ]
)
sepal_width = np.concatenate(
    [
        np.random.normal(3.4, 0.38, n_per_group),
        np.random.normal(2.8, 0.30, n_per_group),
        np.random.normal(3.0, 0.32, n_per_group),
    ]
)
petal_length = np.concatenate(
    [
        np.random.normal(1.5, 0.17, n_per_group),
        np.random.normal(4.3, 0.45, n_per_group),
        np.random.normal(5.5, 0.55, n_per_group),
    ]
)
category = np.repeat(categories, n_per_group)

# Create subplots: scatter plot, histogram, and bar chart
fig = make_subplots(
    rows=2,
    cols=2,
    specs=[[{"colspan": 2}, None], [{}, {}]],
    subplot_titles=("Sepal Dimensions by Species", "Petal Length Distribution", "Species Count"),
    vertical_spacing=0.15,
    horizontal_spacing=0.12,
)

# Add scatter plot for each category (top row, spans both columns)
for i, cat in enumerate(categories):
    mask = category == cat
    fig.add_trace(
        go.Scatter(
            x=sepal_length[mask],
            y=sepal_width[mask],
            mode="markers",
            marker={"size": 14, "color": colors[i], "opacity": 0.8, "line": {"width": 1, "color": "white"}},
            name=cat,
            legendgroup=cat,
            customdata=np.where(mask)[0],
            hovertemplate=f"<b>{cat}</b><br>Sepal Length: %{{x:.2f}} cm<br>Sepal Width: %{{y:.2f}} cm<extra></extra>",
        ),
        row=1,
        col=1,
    )

# Add histogram for petal length (bottom left)
for i, cat in enumerate(categories):
    mask = category == cat
    fig.add_trace(
        go.Histogram(
            x=petal_length[mask],
            name=cat,
            marker={"color": colors[i], "opacity": 0.7, "line": {"width": 1, "color": "white"}},
            legendgroup=cat,
            showlegend=False,
            hovertemplate=f"<b>{cat}</b><br>Petal Length: %{{x:.2f}} cm<br>Count: %{{y}}<extra></extra>",
        ),
        row=2,
        col=1,
    )

# Add bar chart for species count (bottom right)
counts = [n_per_group] * 3
fig.add_trace(
    go.Bar(
        x=categories,
        y=counts,
        marker={"color": colors, "opacity": 0.85, "line": {"width": 2, "color": "white"}},
        showlegend=False,
        hovertemplate="<b>%{x}</b><br>Count: %{y}<extra></extra>",
    ),
    row=2,
    col=2,
)

# Update layout for linked selection
fig.update_layout(
    title={
        "text": "linked-views-selection · plotly · pyplots.ai",
        "font": {"size": 32, "color": "#333333"},
        "x": 0.5,
        "xanchor": "center",
    },
    template="plotly_white",
    font={"size": 18},
    legend={
        "title": {"text": "Species", "font": {"size": 20}},
        "font": {"size": 18},
        "orientation": "h",
        "yanchor": "bottom",
        "y": 1.02,
        "xanchor": "center",
        "x": 0.5,
        "itemsizing": "constant",
    },
    barmode="overlay",
    hovermode="closest",
    dragmode="select",
    margin={"l": 80, "r": 80, "t": 140, "b": 80},
    annotations=[
        {
            "text": "Click legend items to toggle visibility | Use box/lasso select to highlight points",
            "xref": "paper",
            "yref": "paper",
            "x": 0.5,
            "y": -0.08,
            "showarrow": False,
            "font": {"size": 16, "color": "#666666"},
            "xanchor": "center",
        }
    ],
)

# Update subplot titles font size
for annotation in fig.layout.annotations:
    if annotation.text in ["Sepal Dimensions by Species", "Petal Length Distribution", "Species Count"]:
        annotation.font = {"size": 22}

# Update axes
fig.update_xaxes(
    title={"text": "Sepal Length (cm)", "font": {"size": 20}},
    tickfont={"size": 16},
    gridcolor="rgba(0,0,0,0.1)",
    row=1,
    col=1,
)
fig.update_yaxes(
    title={"text": "Sepal Width (cm)", "font": {"size": 20}},
    tickfont={"size": 16},
    gridcolor="rgba(0,0,0,0.1)",
    row=1,
    col=1,
)
fig.update_xaxes(
    title={"text": "Petal Length (cm)", "font": {"size": 20}},
    tickfont={"size": 16},
    gridcolor="rgba(0,0,0,0.1)",
    row=2,
    col=1,
)
fig.update_yaxes(
    title={"text": "Count", "font": {"size": 20}}, tickfont={"size": 16}, gridcolor="rgba(0,0,0,0.1)", row=2, col=1
)
fig.update_xaxes(title={"text": "Species", "font": {"size": 20}}, tickfont={"size": 16}, row=2, col=2)
fig.update_yaxes(
    title={"text": "Count", "font": {"size": 20}}, tickfont={"size": 16}, gridcolor="rgba(0,0,0,0.1)", row=2, col=2
)

# Enable selection persistence and linked brushing via legend
fig.update_traces(selectedpoints=[], selector={"type": "scatter"})

# Configure select/lasso behavior
fig.update_layout(selectdirection="any", newselection={"line": {"color": "#306998", "width": 2}})

# Save outputs
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html", include_plotlyjs=True, full_html=True)
