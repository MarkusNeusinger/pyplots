""" pyplots.ai
bullet-basic: Basic Bullet Chart
Library: plotly 6.5.0 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-23
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Data - Multiple KPIs with different performance levels
metrics = [
    {"label": "Revenue ($K)", "actual": 275, "target": 250, "ranges": [150, 200, 300]},
    {"label": "Profit ($K)", "actual": 85, "target": 100, "ranges": [50, 75, 125]},
    {"label": "Customers", "actual": 320, "target": 400, "ranges": [200, 350, 500]},
    {"label": "Satisfaction", "actual": 4.2, "target": 4.5, "ranges": [3.0, 4.0, 5.0]},
]

# Grayscale colors for qualitative ranges (poor -> satisfactory -> good)
range_colors = ["#D9D9D9", "#BFBFBF", "#A6A6A6"]

# Create subplots - one row per metric for proper scaling
fig = make_subplots(
    rows=len(metrics), cols=1, shared_xaxes=False, vertical_spacing=0.12, subplot_titles=[m["label"] for m in metrics]
)

# Create each bullet chart in its own subplot
for i, m in enumerate(metrics):
    row = i + 1

    # Add qualitative range bands (background, plotted in reverse order)
    for j, r in enumerate(reversed(m["ranges"])):
        fig.add_trace(
            go.Bar(
                x=[r],
                y=[""],
                orientation="h",
                marker=dict(color=range_colors[len(m["ranges"]) - 1 - j]),
                width=0.6,
                showlegend=False,
                hoverinfo="skip",
            ),
            row=row,
            col=1,
        )

    # Add actual value bar (primary measure) using Python Blue
    fig.add_trace(
        go.Bar(
            x=[m["actual"]],
            y=[""],
            orientation="h",
            marker=dict(color="#306998"),
            width=0.25,
            showlegend=False,
            name=m["label"],
            hovertemplate=f"{m['label']}: {m['actual']}<extra></extra>",
        ),
        row=row,
        col=1,
    )

    # Add target marker line (thin black vertical line)
    fig.add_shape(
        type="line",
        x0=m["target"],
        x1=m["target"],
        y0=-0.4,
        y1=0.4,
        line=dict(color="#1A1A1A", width=5),
        row=row,
        col=1,
    )

    # Add actual value annotation for precise reading
    max_range = m["ranges"][-1]
    fig.add_annotation(
        x=max_range * 1.02,
        y=0,
        text=f"<b>{m['actual']}</b>",
        showarrow=False,
        font=dict(size=20, color="#306998"),
        xanchor="left",
        row=row,
        col=1,
    )

    # Update x-axis range for each subplot
    fig.update_xaxes(
        range=[0, max_range * 1.15], tickfont=dict(size=16), showgrid=True, gridcolor="rgba(0,0,0,0.1)", row=row, col=1
    )

    fig.update_yaxes(showticklabels=False, row=row, col=1)

# Layout
fig.update_layout(
    title=dict(text="bullet-basic · plotly · pyplots.ai", font=dict(size=32), x=0.5, xanchor="center"),
    barmode="overlay",
    template="plotly_white",
    margin=dict(l=80, r=100, t=120, b=60),
    showlegend=False,
    height=900,
    width=1600,
)

# Update subplot titles font size
for annotation in fig["layout"]["annotations"]:
    if "text" in annotation and annotation["text"] in [m["label"] for m in metrics]:
        annotation["font"] = dict(size=22)

# Save
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html", include_plotlyjs="cdn")
