"""pyplots.ai
bar-realtime: Real-Time Updating Bar Chart
Library: plotly | Python 3.13
Quality: pending | Created: 2025-01-19
"""

import numpy as np
import plotly.graph_objects as go


# Data - simulate real-time service metrics with previous state for animation effect
np.random.seed(42)

categories = ["API Gateway", "Auth Service", "Data Pipeline", "Cache Layer", "ML Engine", "Notification"]

# Current values (most recent update)
current_values = np.array([847, 623, 1152, 489, 712, 328])

# Previous values (to show motion/transition effect)
previous_values = current_values * (0.85 + np.random.rand(len(categories)) * 0.25)
previous_values = previous_values.astype(int)

# Calculate change direction for color coding
changes = current_values - previous_values

# Colors for change indicators
increase_color = "#4CAF50"  # Green for increase
decrease_color = "#F44336"  # Red for decrease

# Determine bar colors based on change direction
bar_colors = [increase_color if c > 0 else decrease_color for c in changes]

# Create figure
fig = go.Figure()

# Add ghosted previous values (showing motion/transition)
fig.add_trace(
    go.Bar(
        x=categories,
        y=previous_values,
        name="Previous State",
        marker={"color": "rgba(48, 105, 152, 0.25)", "line": {"width": 0}},
        width=0.65,
        showlegend=True,
    )
)

# Add current values
fig.add_trace(
    go.Bar(
        x=categories,
        y=current_values,
        name="Current State",
        marker={"color": bar_colors, "line": {"color": "white", "width": 2}},
        width=0.5,
        text=[f"{v:,}" for v in current_values],
        textposition="outside",
        textfont={"size": 18, "color": "#333"},
        showlegend=True,
    )
)

# Add change indicators above bars
change_texts = []
for _i, (curr, prev) in enumerate(zip(current_values, previous_values, strict=False)):
    diff = curr - prev
    sign = "+" if diff > 0 else ""
    change_texts.append(f"{sign}{diff}")

fig.add_trace(
    go.Scatter(
        x=categories,
        y=current_values + 80,
        mode="text",
        text=change_texts,
        textfont={"size": 14, "color": [increase_color if c > 0 else decrease_color for c in changes]},
        showlegend=False,
        hoverinfo="skip",
    )
)

# Layout
fig.update_layout(
    title={
        "text": "bar-realtime · plotly · pyplots.ai",
        "font": {"size": 28, "color": "#333"},
        "x": 0.5,
        "xanchor": "center",
    },
    xaxis={"title": {"text": "Service", "font": {"size": 22}}, "tickfont": {"size": 18}, "showgrid": False},
    yaxis={
        "title": {"text": "Requests per Second", "font": {"size": 22}},
        "tickfont": {"size": 18},
        "gridcolor": "rgba(0,0,0,0.1)",
        "gridwidth": 1,
        "range": [0, max(current_values) * 1.25],
    },
    barmode="overlay",
    template="plotly_white",
    legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1, "font": {"size": 16}},
    margin={"l": 80, "r": 40, "t": 100, "b": 80},
    plot_bgcolor="white",
    paper_bgcolor="white",
)

# Add annotation explaining the real-time nature
fig.add_annotation(
    text="◉ Live Updating",
    xref="paper",
    yref="paper",
    x=0.02,
    y=0.98,
    showarrow=False,
    font={"size": 16, "color": increase_color},
    bgcolor="rgba(76, 175, 80, 0.1)",
    bordercolor=increase_color,
    borderwidth=1,
    borderpad=6,
)

# Save as PNG (4800 x 2700 px)
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save interactive HTML version
fig.write_html("plot.html", include_plotlyjs="cdn")
