"""
bubble-packed: Basic Packed Bubble Chart
Library: plotly
"""

import numpy as np
import plotly.graph_objects as go


# Data - department budget allocation (shorter labels for better display)
np.random.seed(42)
data = {
    "Marketing": 2800000,
    "Engineering": 4500000,
    "Sales": 3200000,
    "Operations": 1800000,
    "HR": 950000,
    "Finance": 1200000,
    "R&D": 3800000,
    "Support": 1100000,
    "Legal": 650000,
    "IT": 2100000,
    "Product": 1500000,
    "QA": 880000,
    "Data Science": 1650000,
    "Design": 720000,
    "Admin": 450000,
}

labels = list(data.keys())
values = list(data.values())

# Circle packing simulation using force-directed approach
n = len(labels)
# Initial positions - spread in a circle
angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
radii_scale = np.sqrt(np.array(values)) / np.sqrt(max(values)) * 100

# Initial random spread
x_pos = np.cos(angles) * 200 + np.random.randn(n) * 50
y_pos = np.sin(angles) * 200 + np.random.randn(n) * 50

# Simple force simulation for packing
for _ in range(500):
    for i in range(n):
        fx, fy = 0, 0
        # Centering force
        fx -= x_pos[i] * 0.01
        fy -= y_pos[i] * 0.01
        # Repulsion from other circles
        for j in range(n):
            if i != j:
                dx = x_pos[i] - x_pos[j]
                dy = y_pos[i] - y_pos[j]
                dist = np.sqrt(dx**2 + dy**2) + 0.1
                min_dist = radii_scale[i] + radii_scale[j] + 5
                if dist < min_dist:
                    force = (min_dist - dist) * 0.3
                    fx += (dx / dist) * force
                    fy += (dy / dist) * force
        x_pos[i] += fx
        y_pos[i] += fy

# Color palette - Python colors first, then colorblind-safe
colors = [
    "#306998",  # Python Blue
    "#FFD43B",  # Python Yellow
    "#4E79A7",
    "#F28E2B",
    "#E15759",
    "#76B7B2",
    "#59A14F",
    "#EDC948",
    "#B07AA1",
    "#FF9DA7",
    "#9C755F",
    "#BAB0AC",
    "#5778A4",
    "#E49444",
    "#85B6B2",
]


# Format values for display
def format_value(v):
    if v >= 1000000:
        return f"${v / 1000000:.1f}M"
    elif v >= 1000:
        return f"${v / 1000:.0f}K"
    return f"${v}"


# Create bubble chart - add each bubble separately for individual text sizing
fig = go.Figure()

# Add markers first (all together for performance)
fig.add_trace(
    go.Scatter(
        x=x_pos,
        y=y_pos,
        mode="markers",
        marker=dict(size=radii_scale * 2, color=colors[:n], line=dict(color="white", width=2), opacity=0.85),
        hovertemplate=[
            f"<b>{lbl}</b><br>{format_value(val)}<extra></extra>" for lbl, val in zip(labels, values, strict=True)
        ],
    )
)

# Add text annotations with size based on bubble radius
for i, (label, value) in enumerate(zip(labels, values, strict=True)):
    # Scale font size based on bubble size
    font_size = max(10, min(18, int(radii_scale[i] * 0.2)))
    fig.add_annotation(
        x=x_pos[i],
        y=y_pos[i],
        text=f"<b>{label}</b><br>{format_value(value)}",
        showarrow=False,
        font=dict(size=font_size, color="white", family="Arial"),
    )

# Layout
fig.update_layout(
    title=dict(
        text="Department Budget Allocation · bubble-packed · plotly · pyplots.ai",
        font=dict(size=32, color="#333"),
        x=0.5,
        xanchor="center",
    ),
    xaxis=dict(
        showgrid=False, zeroline=False, showticklabels=False, title="", range=[min(x_pos) - 150, max(x_pos) + 150]
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showticklabels=False,
        title="",
        scaleanchor="x",
        scaleratio=1,
        range=[min(y_pos) - 150, max(y_pos) + 150],
    ),
    template="plotly_white",
    showlegend=False,
    margin=dict(l=50, r=50, t=100, b=50),
    paper_bgcolor="white",
    plot_bgcolor="white",
)

# Save outputs
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html", include_plotlyjs=True, full_html=True)
