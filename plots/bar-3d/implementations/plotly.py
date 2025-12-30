"""pyplots.ai
bar-3d: 3D Bar Chart
Library: plotly | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import numpy as np
import plotly.graph_objects as go


# Data - Quarterly sales by product category (5 products x 4 quarters)
np.random.seed(42)

products = ["Electronics", "Clothing", "Food", "Home", "Sports"]
quarters = ["Q1", "Q2", "Q3", "Q4"]

# Create sales data with realistic patterns (values in thousands)
base_sales = np.array([120, 85, 95, 70, 55])
seasonal_factors = np.array([0.8, 1.0, 0.9, 1.3])  # Q4 holiday boost
sales_matrix = np.outer(base_sales, seasonal_factors) + np.random.randn(5, 4) * 10
sales_matrix = np.maximum(sales_matrix, 10)  # Ensure positive values

# Create 3D bar coordinates
x_coords = []
y_coords = []
z_coords = []
colors = []

# Python-inspired colorscale
colorscale = ["#306998", "#4A8BB2", "#6AADCC", "#FFD43B", "#FFE873"]

for i, _product in enumerate(products):
    for j, _quarter in enumerate(quarters):
        x_coords.append(i)
        y_coords.append(j)
        z_coords.append(sales_matrix[i, j])
        colors.append(colorscale[i])

# Create 3D bars using Mesh3d for each bar
fig = go.Figure()

bar_width = 0.35
bar_depth = 0.35

for i in range(len(x_coords)):
    x, y, z = x_coords[i], y_coords[i], z_coords[i]

    # Define the 8 vertices of each bar
    vertices_x = [
        x - bar_width,
        x + bar_width,
        x + bar_width,
        x - bar_width,
        x - bar_width,
        x + bar_width,
        x + bar_width,
        x - bar_width,
    ]
    vertices_y = [
        y - bar_depth,
        y - bar_depth,
        y + bar_depth,
        y + bar_depth,
        y - bar_depth,
        y - bar_depth,
        y + bar_depth,
        y + bar_depth,
    ]
    vertices_z = [0, 0, 0, 0, z, z, z, z]

    # Define faces using triangular indices
    faces_i = [0, 0, 4, 4, 0, 0, 1, 1, 0, 0, 3, 3]
    faces_j = [1, 2, 5, 6, 1, 4, 2, 5, 3, 4, 2, 6]
    faces_k = [2, 3, 6, 7, 4, 5, 5, 6, 4, 7, 6, 7]

    fig.add_trace(
        go.Mesh3d(
            x=vertices_x,
            y=vertices_y,
            z=vertices_z,
            i=faces_i,
            j=faces_j,
            k=faces_k,
            color=colors[i],
            opacity=0.9,
            flatshading=True,
            showlegend=False,
            hovertemplate=f"{products[x_coords[i]]}<br>{quarters[y_coords[i]]}<br>Sales: ${z:.0f}K<extra></extra>",
        )
    )

# Add legend traces for products
for i, product in enumerate(products):
    fig.add_trace(
        go.Scatter3d(
            x=[None],
            y=[None],
            z=[None],
            mode="markers",
            marker=dict(size=16, color=colorscale[i]),
            name=product,
            showlegend=True,
        )
    )

# Update layout
fig.update_layout(
    title=dict(
        text="bar-3d \u00b7 plotly \u00b7 pyplots.ai", font=dict(size=32, color="#333333"), x=0.5, xanchor="center"
    ),
    scene=dict(
        xaxis=dict(
            title=dict(text="Product Category", font=dict(size=20)),
            ticktext=products,
            tickvals=list(range(len(products))),
            tickfont=dict(size=14),
            gridcolor="rgba(0,0,0,0.1)",
            showbackground=True,
            backgroundcolor="rgba(240,240,240,0.9)",
        ),
        yaxis=dict(
            title=dict(text="Quarter", font=dict(size=20)),
            ticktext=quarters,
            tickvals=list(range(len(quarters))),
            tickfont=dict(size=14),
            gridcolor="rgba(0,0,0,0.1)",
            showbackground=True,
            backgroundcolor="rgba(240,240,240,0.9)",
        ),
        zaxis=dict(
            title=dict(text="Sales ($K)", font=dict(size=20)),
            tickfont=dict(size=14),
            gridcolor="rgba(0,0,0,0.1)",
            showbackground=True,
            backgroundcolor="rgba(240,240,240,0.9)",
        ),
        camera=dict(eye=dict(x=1.8, y=1.8, z=1.2)),
        aspectmode="manual",
        aspectratio=dict(x=1.2, y=1, z=0.8),
    ),
    legend=dict(
        font=dict(size=16), x=0.92, y=0.9, bgcolor="rgba(255,255,255,0.9)", bordercolor="rgba(0,0,0,0.2)", borderwidth=1
    ),
    margin=dict(l=20, r=20, t=80, b=20),
    paper_bgcolor="white",
    width=1600,
    height=900,
)

# Save as PNG and HTML
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html", include_plotlyjs="cdn")
