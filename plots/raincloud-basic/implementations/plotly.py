""" pyplots.ai
raincloud-basic: Basic Raincloud Plot
Library: plotly 6.5.0 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-25
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
box_width = 0.08
violin_width = 0.4

for i, (condition, values) in enumerate(data.items()):
    color = colors[i]

    # Calculate statistics for hover info
    median_val = np.median(values)
    q1 = np.percentile(values, 25)
    q3 = np.percentile(values, 75)
    mean_val = np.mean(values)
    std_val = np.std(values)

    # Half-violin (cloud) - positioned on top (positive side)
    fig.add_trace(
        go.Violin(
            y=values,
            x=[condition] * len(values),
            side="positive",
            width=violin_width,
            line_color=color,
            fillcolor=color,
            opacity=0.6,
            meanline_visible=False,
            box_visible=False,
            points=False,
            name=f"{condition} (Cloud)",
            legendgroup=condition,
            showlegend=True,
            hoverinfo="y+name",
            hoveron="violins",
        )
    )

    # Box plot - in the middle with custom hover
    fig.add_trace(
        go.Box(
            y=values,
            x=[condition] * len(values),
            width=box_width,
            marker_color=color,
            line_color="#333333",
            fillcolor="white",
            boxpoints=False,
            name=f"{condition} (Stats)",
            legendgroup=condition,
            showlegend=False,
            hovertemplate=(
                f"<b>{condition}</b><br>"
                f"Median: {median_val:.0f} ms<br>"
                f"Q1-Q3: {q1:.0f}-{q3:.0f} ms<br>"
                f"Mean: {mean_val:.1f} ± {std_val:.1f} ms"
                "<extra></extra>"
            ),
        )
    )

    # Jittered strip points (rain) - on the bottom (negative side)
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
            name=f"{condition} (Rain)",
            legendgroup=condition,
            showlegend=False,
            hovertemplate=f"<b>{condition}</b><br>Value: %{{y:.0f}} ms<extra></extra>",
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
    margin=dict(l=100, r=180, t=100, b=100),
    violingap=0,
    violinmode="overlay",
    legend=dict(
        title=dict(text="Components", font=dict(size=18)),
        font=dict(size=16),
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor="rgba(0,0,0,0.2)",
        borderwidth=1,
        x=1.02,
        y=0.98,
        xanchor="left",
        yanchor="top",
    ),
    hoverlabel=dict(bgcolor="white", bordercolor="#333333", font=dict(size=16, color="#333333")),
)

# Save as PNG (4800x2700) and HTML
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html", include_plotlyjs="cdn")
