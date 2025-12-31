""" pyplots.ai
bar-3d: 3D Bar Chart
Library: altair 6.0.0 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-31
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Sales by product and quarter (grid of categorical dimensions)
np.random.seed(42)

products = ["Product A", "Product B", "Product C", "Product D"]
quarters = ["Q1", "Q2", "Q3", "Q4"]

# Generate realistic sales data with variation (in thousands $)
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

# 3D isometric projection parameters - adjusted for better alignment
bar_width = 0.50
iso_x_scale = 0.60  # Isometric x-shift per depth unit
iso_y_scale = 0.30  # Isometric y-shift per depth unit
spacing_x = 1.4  # Spacing between products

# Scale sales directly for visual height (using actual sales values)
max_sales = df["sales"].max()
min_sales = df["sales"].min()
sales_range = max_sales - min_sales

# Create 3D bar faces (front face + top face + side face for each bar)
bar_faces = []

for _, row in df.iterrows():
    # Calculate isometric position
    depth_idx = row["y_idx"]  # Quarter determines depth
    x_base = row["x_idx"] * spacing_x
    x_shift = depth_idx * iso_x_scale  # Shift right for depth
    y_shift = depth_idx * iso_y_scale  # Shift up for depth

    x_center = x_base + x_shift
    y_base = y_shift

    # Bar height scaled from actual sales (preserving actual value relationship)
    normalized_sales = (row["sales"] - min_sales) / sales_range
    height = normalized_sales * 3.2 + 0.6  # Scale for visualization

    # Depth for painter's algorithm (back rows first, left to right within row)
    base_depth = (3 - row["y_idx"]) * 100 + row["x_idx"]

    # Front face (main bar) - full opacity, brightest
    bar_faces.append(
        {
            "x1": x_center - bar_width / 2,
            "x2": x_center + bar_width / 2,
            "y1": y_base,
            "y2": y_base + height,
            "sales": row["sales"],
            "product": row["product"],
            "quarter": row["quarter"],
            "depth": base_depth + 2,
            "face": "front",
            "brightness": 1.0,
        }
    )

    # Top face (parallelogram) - aligned precisely with front face top edge
    top_depth = iso_x_scale * 0.8  # Depth extent of top face
    bar_faces.append(
        {
            "x1": x_center - bar_width / 2,
            "x2": x_center + bar_width / 2 + top_depth,
            "y1": y_base + height,
            "y2": y_base + height + iso_y_scale * 0.8,
            "sales": row["sales"],
            "product": row["product"],
            "quarter": row["quarter"],
            "depth": base_depth + 1,
            "face": "top",
            "brightness": 0.80,
        }
    )

    # Right side face - aligned with front face right edge
    bar_faces.append(
        {
            "x1": x_center + bar_width / 2,
            "x2": x_center + bar_width / 2 + top_depth,
            "y1": y_base + iso_y_scale * 0.8,
            "y2": y_base + height + iso_y_scale * 0.8,
            "sales": row["sales"],
            "product": row["product"],
            "quarter": row["quarter"],
            "depth": base_depth,
            "face": "side",
            "brightness": 0.60,
        }
    )

df_faces = pd.DataFrame(bar_faces)

# Sort by depth (back to front for proper occlusion)
df_faces = df_faces.sort_values("depth", ascending=True).reset_index(drop=True)
df_faces["order"] = range(len(df_faces))

# Create color scale with brightness for shading effect
bars = (
    alt.Chart(df_faces)
    .mark_rect(stroke="#2a2a2a", strokeWidth=1.2)
    .encode(
        x=alt.X("x1:Q", scale=alt.Scale(domain=[-0.5, 7.0]), axis=alt.Axis(title=None, labels=False, ticks=False)),
        x2=alt.X2("x2:Q"),
        y=alt.Y(
            "y1:Q",
            scale=alt.Scale(domain=[-0.8, 5.5]),
            axis=alt.Axis(
                title="Sales Revenue ($K)",
                labelFontSize=16,
                titleFontSize=20,
                values=[0, 1, 2, 3, 4, 5],
                labelExpr="datum.value * 40 + 60",  # Map visual height to approximate sales values
            ),
        ),
        y2=alt.Y2("y2:Q"),
        color=alt.Color(
            "sales:Q",
            scale=alt.Scale(scheme="viridis", domain=[min_sales, max_sales]),
            legend=alt.Legend(
                title="Sales ($K)", titleFontSize=18, labelFontSize=14, orient="right", offset=15, format=".0f"
            ),
        ),
        opacity=alt.Opacity("brightness:Q", scale=alt.Scale(domain=[0.5, 1.0], range=[0.70, 1.0]), legend=None),
        order=alt.Order("order:Q"),
        tooltip=[
            alt.Tooltip("product:N", title="Product"),
            alt.Tooltip("quarter:N", title="Quarter"),
            alt.Tooltip("sales:Q", title="Sales ($K)", format=".1f"),
        ],
    )
)

# Product labels at bottom - positioned below the front row
product_positions = [i * spacing_x + 0.15 for i in range(len(products))]
product_labels_df = pd.DataFrame({"x": product_positions, "y": [-0.5] * len(products), "label": products})

product_text = (
    alt.Chart(product_labels_df)
    .mark_text(fontSize=18, fontWeight="bold", color="#333333")
    .encode(x="x:Q", y="y:Q", text="label:N")
)

# Quarter labels integrated into the 3D perspective - along the depth axis
# Position each quarter label at the back of each row, aligned with isometric projection
quarter_labels_df = pd.DataFrame(
    {
        "x": [-0.5 + j * iso_x_scale for j in range(len(quarters))],
        "y": [j * iso_y_scale + 0.1 for j in range(len(quarters))],
        "label": quarters,
    }
)

quarter_text = (
    alt.Chart(quarter_labels_df)
    .mark_text(fontSize=16, fontWeight="bold", color="#444444", align="right")
    .encode(x="x:Q", y="y:Q", text="label:N")
)

# Depth axis indicator - angled to match isometric direction
depth_arrow = pd.DataFrame({"x": [-0.3], "y": [1.5], "label": ["← Quarters"]})

depth_text = (
    alt.Chart(depth_arrow)
    .mark_text(fontSize=14, fontStyle="italic", color="#666666", angle=334, align="right")
    .encode(x="x:Q", y="y:Q", text="label:N")
)

# Combine all layers with interactive pan/zoom
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
    .interactive()
)

# Save outputs
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
