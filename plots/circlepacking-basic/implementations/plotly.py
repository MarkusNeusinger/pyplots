"""pyplots.ai
circlepacking-basic: Circle Packing Chart
Library: plotly | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import numpy as np
import plotly.graph_objects as go


# Data: File system hierarchy with sizes (in MB)
np.random.seed(42)

hierarchy = {
    "Documents": {"Reports": 180, "Spreadsheets": 120, "Presentations": 220},
    "Media": {"Photos": 340, "Videos": 450, "Music": 280},
    "Projects": {"Python": 160, "Web": 140, "Data": 200},
    "System": {"Logs": 90, "Config": 60, "Cache": 130},
}

# Color palette - Python colors first
colors = {
    "Documents": "#306998",  # Python Blue
    "Media": "#FFD43B",  # Python Yellow
    "Projects": "#4B8BBE",  # Light Blue
    "System": "#FFE873",  # Light Yellow
}

# Build circle data with proper sizing
all_circles = []

# Position main categories in quadrants
positions = [(-300, 300), (300, 300), (-300, -300), (300, -300)]

for idx, (cat, subcats) in enumerate(hierarchy.items()):
    cat_total = sum(subcats.values())
    cat_radius = np.sqrt(cat_total) * 7.5

    cx, cy = positions[idx]

    # Add parent category circle
    all_circles.append(
        {"x": cx, "y": cy, "r": cat_radius, "label": cat, "value": cat_total, "color": colors[cat], "level": "category"}
    )

    # Position children in upper portion of parent circle
    sub_items = list(subcats.items())
    n_subs = len(sub_items)

    for j, (sub_name, sub_value) in enumerate(sub_items):
        sub_radius = np.sqrt(sub_value) * 3.5  # Smaller children

        # Arrange in arc at top of parent circle
        if n_subs == 3:
            # Left, right, top positions
            offsets = [
                (-0.35, 0.25),  # Left
                (0.35, 0.25),  # Right
                (0, -0.35),  # Bottom
            ]
        else:
            offsets = [(0, 0)]

        ox, oy = offsets[j]
        sx = cx + cat_radius * ox
        sy = cy + cat_radius * oy

        all_circles.append(
            {
                "x": sx,
                "y": sy,
                "r": sub_radius,
                "label": sub_name,
                "value": sub_value,
                "color": colors[cat],
                "level": "subcategory",
            }
        )

# Create figure
fig = go.Figure()

# Draw parent circles first (background)
for circle in all_circles:
    if circle["level"] == "category":
        fig.add_shape(
            type="circle",
            xref="x",
            yref="y",
            x0=circle["x"] - circle["r"],
            y0=circle["y"] - circle["r"],
            x1=circle["x"] + circle["r"],
            y1=circle["y"] + circle["r"],
            fillcolor=circle["color"],
            opacity=0.85,
            line=dict(color="white", width=4),
            layer="below",
        )

# Draw child circles (foreground)
for circle in all_circles:
    if circle["level"] == "subcategory":
        fig.add_shape(
            type="circle",
            xref="x",
            yref="y",
            x0=circle["x"] - circle["r"],
            y0=circle["y"] - circle["r"],
            x1=circle["x"] + circle["r"],
            y1=circle["y"] + circle["r"],
            fillcolor=circle["color"],
            opacity=0.95,
            line=dict(color="white", width=3),
            layer="above",
        )

# Add labels for subcategories
for circle in all_circles:
    if circle["level"] == "subcategory":
        text_color = "white" if circle["color"] in ["#306998", "#4B8BBE"] else "#333333"
        fig.add_annotation(
            x=circle["x"],
            y=circle["y"],
            text=f"{circle['label']}<br>{circle['value']}",
            showarrow=False,
            font=dict(size=16, color=text_color, family="Arial"),
            align="center",
        )

# Add labels for categories (positioned below children)
for circle in all_circles:
    if circle["level"] == "category":
        text_color = "white" if circle["color"] in ["#306998", "#4B8BBE"] else "#333333"
        # Position at bottom of circle
        label_y = circle["y"] - circle["r"] * 0.7
        fig.add_annotation(
            x=circle["x"],
            y=label_y,
            text=f"<b>{circle['label']}</b><br>{circle['value']} MB",
            showarrow=False,
            font=dict(size=22, color=text_color, family="Arial"),
            align="center",
        )

# Add invisible scatter for hover interactivity
for circle in all_circles:
    fig.add_trace(
        go.Scatter(
            x=[circle["x"]],
            y=[circle["y"]],
            mode="markers",
            marker=dict(size=circle["r"] * 1.5, opacity=0),
            hovertemplate=f"<b>{circle['label']}</b><br>Size: {circle['value']} MB<extra></extra>",
            showlegend=False,
        )
    )

# Layout
fig.update_layout(
    title=dict(
        text="Storage Analysis · circlepacking-basic · plotly · pyplots.ai",
        font=dict(size=32, color="#333333"),
        x=0.5,
        xanchor="center",
        y=0.97,
    ),
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-620, 620], scaleanchor="y", scaleratio=1),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-620, 620]),
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(t=100, l=30, r=30, b=30),
    showlegend=False,
)

# Save outputs
fig.write_image("plot.png", width=1200, height=1200, scale=3)
fig.write_html("plot.html")
