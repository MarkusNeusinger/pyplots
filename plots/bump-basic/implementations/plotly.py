"""
bump-basic: Basic Bump Chart
Library: plotly
"""

import plotly.graph_objects as go


# Data: Tech company rankings over 6 quarters
companies = ["Alpha Tech", "Beta Corp", "Gamma Inc", "Delta Ltd", "Epsilon Co"]
periods = ["Q1 2023", "Q2 2023", "Q3 2023", "Q4 2023", "Q1 2024", "Q2 2024"]

# Rankings for each company across periods (1 = best)
rankings = {
    "Alpha Tech": [2, 1, 1, 2, 3, 4],
    "Beta Corp": [1, 2, 3, 3, 2, 1],
    "Gamma Inc": [4, 4, 2, 1, 1, 2],
    "Delta Ltd": [3, 3, 4, 4, 5, 5],
    "Epsilon Co": [5, 5, 5, 5, 4, 3],
}

# Colors: Python Blue first, then colorblind-safe palette
colors = ["#306998", "#FFD43B", "#2CA02C", "#D62728", "#9467BD"]

# Create figure
fig = go.Figure()

# Add traces for each company
for i, company in enumerate(companies):
    ranks = rankings[company]
    fig.add_trace(
        go.Scatter(
            x=periods,
            y=ranks,
            mode="lines+markers",
            name=company,
            line={"width": 4, "color": colors[i]},
            marker={"size": 18, "color": colors[i], "line": {"width": 2, "color": "white"}},
            hovertemplate=f"{company}<br>Period: %{{x}}<br>Rank: %{{y}}<extra></extra>",
        )
    )

# Layout for 4800x2700 px
fig.update_layout(
    title={"text": "bump-basic · plotly · pyplots.ai", "font": {"size": 32}, "x": 0.5, "xanchor": "center"},
    xaxis={
        "title": {"text": "Period", "font": {"size": 24}},
        "tickfont": {"size": 18},
        "showgrid": True,
        "gridcolor": "rgba(0,0,0,0.1)",
        "gridwidth": 1,
    },
    yaxis={
        "title": {"text": "Rank", "font": {"size": 24}},
        "tickfont": {"size": 18},
        "autorange": "reversed",  # Rank 1 at top
        "dtick": 1,
        "showgrid": True,
        "gridcolor": "rgba(0,0,0,0.1)",
        "gridwidth": 1,
    },
    legend={"font": {"size": 18}, "x": 1.02, "y": 0.5, "yanchor": "middle"},
    template="plotly_white",
    margin={"l": 80, "r": 180, "t": 100, "b": 80},
)

# Save as PNG (4800x2700 via scale)
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save interactive HTML
fig.write_html("plot.html", include_plotlyjs="cdn")
