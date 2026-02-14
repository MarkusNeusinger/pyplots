""" pyplots.ai
raincloud-basic: Basic Raincloud Plot
Library: plotly 6.5.2 | Python 3.14
Quality: 87/100 | Created: 2025-12-25
"""

import numpy as np
import plotly.graph_objects as go


# Data - reaction times (ms) for different experimental conditions
np.random.seed(42)

conditions = ["Control", "Treatment A", "Treatment B", "Treatment C"]
n_per_group = 80

data = {
    "Control": np.random.normal(450, 60, n_per_group),
    "Treatment A": np.random.normal(380, 45, n_per_group),
    "Treatment B": np.concatenate(
        [np.random.normal(350, 30, n_per_group // 2), np.random.normal(480, 35, n_per_group // 2)]
    ),
    "Treatment C": np.random.normal(400, 80, n_per_group),
}

data["Control"] = np.append(data["Control"], [620, 650, 280])
data["Treatment C"] = np.append(data["Treatment C"], [600, 620, 250])

# Cohesive blue-teal palette: good contrast on white, colorblind-safe
colors = ["#306998", "#4B8BBE", "#2A9D8F", "#7B68AE"]

fig = go.Figure()

violin_width = 0.45

for i, (condition, values) in enumerate(data.items()):
    color = colors[i]

    # Cloud (half-violin) - extends UPWARD (positive y-direction)
    fig.add_trace(
        go.Violin(
            x=values,
            y=[condition] * len(values),
            side="positive",
            width=violin_width,
            line_color=color,
            fillcolor=color,
            opacity=0.55,
            meanline_visible=False,
            box_visible=False,
            points=False,
            name=condition,
            legendgroup=condition,
            showlegend=True,
            hoverinfo="x+name",
            hoveron="violins",
            orientation="h",
        )
    )

    # Box plot - centered on category baseline
    fig.add_trace(
        go.Box(
            x=values,
            y=[condition] * len(values),
            width=0.08,
            marker_color=color,
            line_color="#2D2D2D",
            fillcolor="white",
            boxpoints=False,
            name=condition,
            legendgroup=condition,
            showlegend=False,
            orientation="h",
        )
    )

    # Rain (jittered points) - falls DOWNWARD (negative y-direction)
    fig.add_trace(
        go.Violin(
            x=values,
            y=[condition] * len(values),
            side="negative",
            width=0,
            points="all",
            pointpos=-0.4,
            jitter=0.08,
            marker={"size": 7, "color": color, "opacity": 0.6, "line": {"width": 0.5, "color": "#2D2D2D"}},
            line_width=0,
            fillcolor="rgba(0,0,0,0)",
            name=condition,
            legendgroup=condition,
            showlegend=False,
            orientation="h",
            hovertemplate=f"<b>{condition}</b><br>Value: %{{x:.0f}} ms<extra></extra>",
        )
    )

# Annotations for data storytelling
fig.add_annotation(
    x=415,
    y="Treatment B",
    text="Bimodal: two distinct<br>response clusters",
    showarrow=True,
    arrowhead=2,
    arrowsize=1,
    arrowwidth=1.5,
    arrowcolor="#555555",
    ax=0,
    ay=-55,
    font={"size": 15, "color": "#2D2D2D"},
    bgcolor="rgba(255,255,255,0.85)",
    bordercolor="#2A9D8F",
    borderwidth=1.5,
    borderpad=4,
)

fig.add_annotation(
    x=650,
    y="Control",
    text="Outliers",
    showarrow=True,
    arrowhead=2,
    arrowsize=1,
    arrowwidth=1.5,
    arrowcolor="#555555",
    ax=30,
    ay=-35,
    font={"size": 14, "color": "#2D2D2D"},
    bgcolor="rgba(255,255,255,0.85)",
    bordercolor="#306998",
    borderwidth=1.5,
    borderpad=4,
)

fig.add_annotation(
    x=380,
    y="Treatment A",
    text="Tight cluster (low variance)",
    showarrow=True,
    arrowhead=2,
    arrowsize=1,
    arrowwidth=1.5,
    arrowcolor="#555555",
    ax=-80,
    ay=-45,
    font={"size": 14, "color": "#2D2D2D"},
    bgcolor="rgba(255,255,255,0.85)",
    bordercolor="#4B8BBE",
    borderwidth=1.5,
    borderpad=4,
)

# Layout - HORIZONTAL orientation with categories on y-axis, values on x-axis
fig.update_layout(
    title={
        "text": "raincloud-basic \u00b7 plotly \u00b7 pyplots.ai",
        "font": {"size": 32, "color": "#2D2D2D", "family": "Arial, sans-serif"},
        "x": 0.5,
        "xanchor": "center",
    },
    yaxis={
        "title": {"text": "Experimental Condition", "font": {"size": 24, "color": "#444444"}},
        "tickfont": {"size": 20, "color": "#333333"},
        "categoryorder": "array",
        "categoryarray": conditions,
        "showgrid": False,
        "zeroline": False,
    },
    xaxis={
        "title": {"text": "Reaction Time (ms)", "font": {"size": 24, "color": "#444444"}},
        "tickfont": {"size": 20, "color": "#333333"},
        "gridcolor": "rgba(0,0,0,0.06)",
        "gridwidth": 1,
        "range": [210, 700],
        "zeroline": False,
        "showline": True,
        "linecolor": "rgba(0,0,0,0.15)",
        "linewidth": 1,
    },
    template="plotly_white",
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin={"l": 170, "r": 60, "t": 85, "b": 75},
    violingap=0,
    violinmode="overlay",
    legend={
        "title": {"text": "Condition", "font": {"size": 18, "color": "#333333"}},
        "font": {"size": 16},
        "bgcolor": "rgba(255,255,255,0.9)",
        "bordercolor": "rgba(0,0,0,0.15)",
        "borderwidth": 1,
    },
    hoverlabel={"bgcolor": "white", "bordercolor": "#2D2D2D", "font": {"size": 16, "color": "#2D2D2D"}},
)

# Save
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Add range slider for interactive HTML exploration
fig.update_xaxes(rangeslider={"visible": True, "thickness": 0.05})
fig.write_html("plot.html", include_plotlyjs="cdn")
