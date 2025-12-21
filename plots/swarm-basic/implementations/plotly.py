""" pyplots.ai
swarm-basic: Basic Swarm Plot
Library: plotly 6.5.0 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-17
"""

import numpy as np
import plotly.graph_objects as go


# Data - student test scores across 4 classrooms with varied distributions
np.random.seed(42)
classrooms = ["Room A", "Room B", "Room C", "Room D"]
colors = ["#306998", "#FFD43B", "#5A9BD4", "#E07B39"]

data = {
    "Room A": np.concatenate(
        [np.random.normal(75, 8, 35), np.random.normal(90, 5, 10)]
    ),  # Main cluster + high performers
    "Room B": np.random.normal(68, 12, 50),  # Wide spread
    "Room C": np.concatenate([np.random.normal(60, 6, 20), np.random.normal(82, 6, 25)]),  # Bimodal
    "Room D": np.random.normal(78, 6, 40),  # Tight cluster
}


# Beeswarm jitter function - spreads points horizontally based on density
def beeswarm_positions(values, category_pos, width=0.35, point_size=0.015):
    """Calculate x positions for beeswarm effect."""
    sorted_indices = np.argsort(values)
    y_sorted = values[sorted_indices]
    x_positions = np.zeros(len(values))

    for i, idx in enumerate(sorted_indices):
        y_val = y_sorted[i]
        # Find nearby points already placed
        placed_y = y_sorted[:i]
        placed_x = x_positions[sorted_indices[:i]]

        # Find points within point_size distance vertically
        nearby_mask = np.abs(placed_y - y_val) < (point_size * (values.max() - values.min()))
        if not np.any(nearby_mask):
            x_positions[idx] = category_pos
        else:
            nearby_x = placed_x[nearby_mask]
            # Find available slot by alternating left/right
            offset = 0.02
            for sign in [1, -1, 1, -1, 1, -1, 1, -1]:
                test_x = category_pos + sign * offset
                if not np.any(np.abs(nearby_x - test_x) < 0.015):
                    x_positions[idx] = test_x
                    break
                offset += 0.015
            else:
                x_positions[idx] = category_pos + np.random.uniform(-width / 2, width / 2)

    return x_positions


# Create figure
fig = go.Figure()

# Add swarm points for each category
for i, (classroom, scores) in enumerate(data.items()):
    x_pos = beeswarm_positions(scores, i, width=0.4)

    fig.add_trace(
        go.Scatter(
            x=x_pos,
            y=scores,
            mode="markers",
            name=classroom,
            marker={"size": 14, "color": colors[i], "opacity": 0.75, "line": {"width": 1, "color": "#333333"}},
            hovertemplate=f"{classroom}<br>Score: %{{y:.1f}}<extra></extra>",
        )
    )

    # Add mean marker for each category
    mean_val = np.mean(scores)
    fig.add_trace(
        go.Scatter(
            x=[i],
            y=[mean_val],
            mode="markers",
            marker={"symbol": "diamond", "size": 18, "color": "white", "line": {"width": 3, "color": colors[i]}},
            showlegend=False,
            hovertemplate=f"{classroom} Mean: {mean_val:.1f}<extra></extra>",
        )
    )

# Layout
fig.update_layout(
    title={"text": "swarm-basic · plotly · pyplots.ai", "font": {"size": 32}, "x": 0.5, "xanchor": "center"},
    xaxis={
        "title": {"text": "Classroom", "font": {"size": 24}},
        "tickfont": {"size": 20},
        "tickmode": "array",
        "tickvals": list(range(len(classrooms))),
        "ticktext": classrooms,
        "gridcolor": "rgba(0,0,0,0.05)",
    },
    yaxis={
        "title": {"text": "Test Score", "font": {"size": 24}},
        "tickfont": {"size": 20},
        "gridcolor": "rgba(0,0,0,0.1)",
        "gridwidth": 1,
        "range": [35, 105],
    },
    template="plotly_white",
    showlegend=True,
    legend={"font": {"size": 18}, "x": 1.02, "y": 0.98, "xanchor": "left"},
    margin={"l": 100, "r": 150, "t": 100, "b": 80},
)

# Save
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html", include_plotlyjs="cdn")
