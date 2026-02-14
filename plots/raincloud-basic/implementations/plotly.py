"""pyplots.ai
raincloud-basic: Basic Raincloud Plot
Library: plotly 6.5.2 | Python 3.14
Quality: /100 | Updated: 2026-02-14
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

# Colors - Python Blue palette variations
colors = ["#306998", "#4B8BBE", "#FFD43B", "#646464"]

fig = go.Figure()

# Positioning parameters
violin_width = 0.4

for i, (condition, values) in enumerate(data.items()):
    color = colors[i]
    median_val = np.median(values)
    q1 = np.percentile(values, 25)
    q3 = np.percentile(values, 75)
    mean_val = np.mean(values)
    std_val = np.std(values)

    # Cloud (half-violin) - extends UPWARD (positive y-direction)
    fig.add_trace(
        go.Violin(
            x=values,
            y=[condition] * len(values),
            side="positive",
            width=violin_width,
            line_color=color,
            fillcolor=color,
            opacity=0.6,
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
            line_color="#333333",
            fillcolor="white",
            boxpoints=False,
            name=condition,
            legendgroup=condition,
            showlegend=False,
            orientation="h",
            hovertemplate=(
                f"<b>{condition}</b><br>"
                f"Median: {median_val:.0f} ms<br>"
                f"Q1-Q3: {q1:.0f}-{q3:.0f} ms<br>"
                f"Mean: {mean_val:.1f} \u00b1 {std_val:.1f} ms"
                "<extra></extra>"
            ),
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
            jitter=0.15,
            marker={"size": 8, "color": color, "opacity": 0.6, "line": {"width": 0.5, "color": "#333333"}},
            line_width=0,
            fillcolor="rgba(0,0,0,0)",
            name=condition,
            legendgroup=condition,
            showlegend=False,
            orientation="h",
            hovertemplate=f"<b>{condition}</b><br>Value: %{{x:.0f}} ms<extra></extra>",
        )
    )

# Layout - HORIZONTAL orientation with categories on y-axis, values on x-axis
fig.update_layout(
    title={
        "text": "raincloud-basic \u00b7 plotly \u00b7 pyplots.ai",
        "font": {"size": 32, "color": "#333333"},
        "x": 0.5,
        "xanchor": "center",
    },
    yaxis={
        "title": {"text": "Experimental Condition", "font": {"size": 24}},
        "tickfont": {"size": 20},
        "categoryorder": "array",
        "categoryarray": conditions,
        "showgrid": False,
    },
    xaxis={
        "title": {"text": "Reaction Time (ms)", "font": {"size": 24}},
        "tickfont": {"size": 20},
        "gridcolor": "rgba(0,0,0,0.1)",
        "gridwidth": 1,
        "range": [200, 700],
    },
    template="plotly_white",
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin={"l": 180, "r": 80, "t": 100, "b": 100},
    violingap=0,
    violinmode="overlay",
    legend={
        "title": {"text": "Condition", "font": {"size": 18}},
        "font": {"size": 16},
        "bgcolor": "rgba(255,255,255,0.9)",
        "bordercolor": "rgba(0,0,0,0.2)",
        "borderwidth": 1,
    },
    hoverlabel={"bgcolor": "white", "bordercolor": "#333333", "font": {"size": 16, "color": "#333333"}},
)

# Save
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Add range slider for interactive HTML exploration
fig.update_xaxes(rangeslider={"visible": True, "thickness": 0.05})
fig.write_html("plot.html", include_plotlyjs="cdn")
