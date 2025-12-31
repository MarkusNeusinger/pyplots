"""pyplots.ai
bar-3d: 3D Bar Chart
Library: altair | Python 3.13
Quality: pending | Created: 2025-12-31
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Sales by product and quarter (grid of categorical dimensions)
np.random.seed(42)

products = ["Product A", "Product B", "Product C", "Product D"]
quarters = ["Q1", "Q2", "Q3", "Q4"]

# Generate realistic sales data with variation
sales_data = []
base_sales = [85, 145, 70, 115]  # Different base performance per product

for i, product in enumerate(products):
    for j, quarter in enumerate(quarters):
        seasonal = 1.0 + 0.2 * np.sin((j + 1) * np.pi / 2)  # Seasonal variation
        trend = 1.0 + j * 0.08  # Growth trend
        noise = np.random.uniform(0.85, 1.15)
        sales = base_sales[i] * seasonal * trend * noise
        sales_data.append({"product": product, "quarter": quarter, "x_idx": i, "y_idx": j, "sales": sales})

df = pd.DataFrame(sales_data)

# 3D isometric projection parameters
bar_width = 0.55
bar_depth = 0.45  # Visual depth of each bar
spacing_x = 1.3  # Spacing between products
x_offset_per_row = 0.55  # Shift for depth illusion
y_offset_per_row = 0.35  # Vertical shift per row

# Normalize sales for bar heights
max_sales = df["sales"].max()
min_sales = df["sales"].min()
height_scale = 3.8

# Create 3D bar faces (front face + top face for each bar)
bar_faces = []

for _, row in df.iterrows():
    x_center = row["x_idx"] * spacing_x + row["y_idx"] * x_offset_per_row
    y_base = row["y_idx"] * y_offset_per_row
    height = ((row["sales"] - min_sales) / (max_sales - min_sales) * 0.85 + 0.15) * height_scale

    # Depth for painter's algorithm (back rows first)
    base_depth = row["y_idx"] * 1000 + row["x_idx"]

    # Front face (main bar)
    bar_faces.append(
        {
            "x1": x_center - bar_width / 2,
            "x2": x_center + bar_width / 2,
            "y1": y_base,
            "y2": y_base + height,
            "sales": row["sales"],
            "product": row["product"],
            "quarter": row["quarter"],
            "depth": base_depth,
            "face": "front",
            "brightness": 1.0,
        }
    )

    # Top face (parallelogram simulated as rectangle)
    bar_faces.append(
        {
            "x1": x_center - bar_width / 2,
            "x2": x_center + bar_width / 2 + bar_depth * 0.7,
            "y1": y_base + height,
            "y2": y_base + height + bar_depth * 0.5,
            "sales": row["sales"],
            "product": row["product"],
            "quarter": row["quarter"],
            "depth": base_depth - 1,  # Draw after front face
            "face": "top",
            "brightness": 0.82,
        }
    )

    # Right side face
    bar_faces.append(
        {
            "x1": x_center + bar_width / 2,
            "x2": x_center + bar_width / 2 + bar_depth * 0.7,
            "y1": y_base + bar_depth * 0.5,
            "y2": y_base + height + bar_depth * 0.5,
            "sales": row["sales"],
            "product": row["product"],
            "quarter": row["quarter"],
            "depth": base_depth - 2,  # Draw after top face
            "face": "side",
            "brightness": 0.65,
        }
    )

df_faces = pd.DataFrame(bar_faces)

# Sort by depth (back to front)
df_faces = df_faces.sort_values("depth", ascending=False).reset_index(drop=True)
df_faces["order"] = range(len(df_faces))

# Create color scale that accounts for brightness
# Using viridis but will apply opacity for shading
bars = (
    alt.Chart(df_faces)
    .mark_rect(stroke="#2a2a2a", strokeWidth=1)
    .encode(
        x=alt.X("x1:Q", scale=alt.Scale(domain=[-0.5, 6.5]), axis=alt.Axis(title=None, labels=False, ticks=False)),
        x2=alt.X2("x2:Q"),
        y=alt.Y(
            "y1:Q",
            scale=alt.Scale(domain=[-0.5, 6]),
            axis=alt.Axis(title="Sales Revenue (Relative Height)", labelFontSize=16, titleFontSize=20),
        ),
        y2=alt.Y2("y2:Q"),
        color=alt.Color(
            "sales:Q",
            scale=alt.Scale(scheme="viridis"),
            legend=alt.Legend(title="Sales ($K)", titleFontSize=20, labelFontSize=16, orient="right", offset=10),
        ),
        opacity=alt.Opacity("brightness:Q", scale=alt.Scale(domain=[0.6, 1.0], range=[0.75, 1.0]), legend=None),
        order=alt.Order("order:Q"),
        tooltip=[
            alt.Tooltip("product:N", title="Product"),
            alt.Tooltip("quarter:N", title="Quarter"),
            alt.Tooltip("sales:Q", title="Sales ($K)", format=".1f"),
        ],
    )
)

# Product labels at bottom
product_positions = [i * spacing_x + 1.5 * x_offset_per_row for i in range(len(products))]
product_labels = pd.DataFrame({"x": product_positions, "y": [-0.35] * len(products), "label": products})

product_text = (
    alt.Chart(product_labels)
    .mark_text(fontSize=18, fontWeight="bold", color="#333333")
    .encode(x="x:Q", y="y:Q", text="label:N")
)

# Quarter labels (depth dimension) - positioned to the right
quarter_labels = pd.DataFrame(
    {
        "x": [5.2 + j * x_offset_per_row * 0.4 for j in range(len(quarters))],
        "y": [j * y_offset_per_row + 2.0 for j in range(len(quarters))],
        "label": quarters,
    }
)

quarter_text = (
    alt.Chart(quarter_labels)
    .mark_text(fontSize=16, fontWeight="bold", color="#444444")
    .encode(x="x:Q", y="y:Q", text="label:N")
)

# Depth axis label
depth_label = pd.DataFrame({"x": [5.8], "y": [0.8], "label": ["Quarters →"]})

depth_text = (
    alt.Chart(depth_label)
    .mark_text(fontSize=14, fontStyle="italic", color="#666666", angle=30)
    .encode(x="x:Q", y="y:Q", text="label:N")
)

# Combine all layers
chart = (
    alt.layer(bars, product_text, quarter_text, depth_text)
    .properties(
        width=1600,
        height=900,
        title=alt.Title(
            text="bar-3d · altair · pyplots.ai",
            subtitle="Quarterly Sales by Product (Isometric 3D Projection)",
            fontSize=28,
            subtitleFontSize=18,
            subtitleColor="#666666",
        ),
    )
    .configure_axis(grid=True, gridOpacity=0.2, gridDash=[4, 4])
    .configure_view(strokeWidth=0)
)

# Save outputs
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
