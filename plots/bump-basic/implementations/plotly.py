"""
bump-basic: Basic Bump Chart
Library: plotly
"""

import plotly.graph_objects as go


# Data - Sports league standings over a season
entities = ["Team Alpha", "Team Beta", "Team Gamma", "Team Delta", "Team Epsilon"]
periods = ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5", "Week 6"]

# Rankings for each team across periods (1 = best)
rankings = {
    "Team Alpha": [3, 2, 1, 1, 2, 1],
    "Team Beta": [1, 1, 2, 3, 3, 2],
    "Team Gamma": [2, 3, 3, 2, 1, 3],
    "Team Delta": [4, 4, 5, 4, 4, 4],
    "Team Epsilon": [5, 5, 4, 5, 5, 5],
}

# Colors - Python Blue first, then colorblind-safe palette
colors = ["#306998", "#FFD43B", "#2ecc71", "#e74c3c", "#9b59b6"]

# Create figure
fig = go.Figure()

for i, (entity, ranks) in enumerate(rankings.items()):
    fig.add_trace(
        go.Scatter(
            x=periods,
            y=ranks,
            mode="lines+markers",
            name=entity,
            line={"width": 4, "color": colors[i]},
            marker={"size": 16, "color": colors[i]},
        )
    )

# Layout with inverted Y-axis (rank 1 at top)
fig.update_layout(
    title={"text": "bump-basic · plotly · pyplots.ai", "font": {"size": 28}},
    xaxis={"title": {"text": "Period", "font": {"size": 22}}, "tickfont": {"size": 18}},
    yaxis={
        "title": {"text": "Rank", "font": {"size": 22}},
        "tickfont": {"size": 18},
        "autorange": "reversed",  # Invert so rank 1 is at top
        "tickmode": "linear",
        "tick0": 1,
        "dtick": 1,
    },
    legend={"font": {"size": 18}, "x": 1.02, "y": 1, "xanchor": "left"},
    template="plotly_white",
    margin={"r": 150},  # Extra margin for legend
)

# Save as PNG (4800x2700 px)
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save interactive HTML
fig.write_html("plot.html")
