"""pyplots.ai
raincloud-basic: Basic Raincloud Plot
Library: plotly | Python 3.13
Quality: pending | Created: 2025-12-24
"""

import numpy as np
import plotly.graph_objects as go


# Data - reaction times (ms) for different experimental conditions
np.random.seed(42)

conditions = ["Control", "Treatment A", "Treatment B", "Treatment C"]
n_per_group = 80

# Generate realistic reaction time data with different distributions
data = {
    "Control": np.random.normal(450, 60, n_per_group),
    "Treatment A": np.random.normal(380, 45, n_per_group),  # Faster, less variable
    "Treatment B": np.concatenate(
        [  # Bimodal distribution
            np.random.normal(350, 30, n_per_group // 2),
            np.random.normal(480, 35, n_per_group // 2),
        ]
    ),
    "Treatment C": np.random.normal(400, 80, n_per_group),  # More variable
}

# Add some outliers to show box plot whiskers
data["Control"] = np.append(data["Control"], [620, 650, 280])
data["Treatment C"] = np.append(data["Treatment C"], [600, 620, 250])

# Colors - Python Blue palette variations
colors = ["#306998", "#4B8BBE", "#FFD43B", "#646464"]

fig = go.Figure()

# Positioning parameters
violin_side = "positive"
box_width = 0.08
point_jitter = 0.06
violin_width = 0.4

for i, (condition, values) in enumerate(data.items()):
    color = colors[i]

    # Half-violin (cloud) - positioned on one side
    fig.add_trace(
        go.Violin(
            y=values,
            x=[condition] * len(values),
            side=violin_side,
            width=violin_width,
            line_color=color,
            fillcolor=color,
            opacity=0.6,
            meanline_visible=False,
            box_visible=False,
            points=False,
            name=condition,
            showlegend=False,
        )
    )

    # Box plot - in the middle
    fig.add_trace(
        go.Box(
            y=values,
            x=[condition] * len(values),
            width=box_width,
            marker_color=color,
            line_color="#333333",
            fillcolor="white",
            boxpoints=False,
            name=condition,
            showlegend=False,
        )
    )

    # Jittered strip points (rain) - on the opposite side using pointpos
    fig.add_trace(
        go.Violin(
            y=values,
            x=[condition] * len(values),
            side="negative",
            width=0,
            points="all",
            pointpos=-0.4,
            jitter=0.15,
            marker=dict(size=8, color=color, opacity=0.6, line=dict(width=0.5, color="#333333")),
            line_width=0,
            fillcolor="rgba(0,0,0,0)",
            name=condition,
            showlegend=False,
        )
    )

# Update layout for 4800x2700 output
fig.update_layout(
    title=dict(
        text="raincloud-basic · plotly · pyplots.ai", font=dict(size=32, color="#333333"), x=0.5, xanchor="center"
    ),
    xaxis=dict(
        title=dict(text="Experimental Condition", font=dict(size=24)),
        tickfont=dict(size=20),
        categoryorder="array",
        categoryarray=conditions,
        showgrid=False,
    ),
    yaxis=dict(
        title=dict(text="Reaction Time (ms)", font=dict(size=24)),
        tickfont=dict(size=20),
        gridcolor="rgba(0,0,0,0.1)",
        gridwidth=1,
        range=[200, 700],
    ),
    template="plotly_white",
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(l=100, r=80, t=100, b=100),
    violingap=0,
    violinmode="overlay",
)

# Save as PNG (4800x2700) and HTML
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html", include_plotlyjs="cdn")
