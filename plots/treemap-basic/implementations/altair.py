""" pyplots.ai
treemap-basic: Basic Treemap
Library: altair 6.0.0 | Python 3.13.11
Quality: 88/100 | Created: 2025-12-14
"""

import altair as alt
import pandas as pd


# Data - Market capitalization by sector and company
data = [
    {"category": "Technology", "subcategory": "Apple", "value": 2800},
    {"category": "Technology", "subcategory": "Microsoft", "value": 2400},
    {"category": "Technology", "subcategory": "Google", "value": 1800},
    {"category": "Technology", "subcategory": "NVIDIA", "value": 1200},
    {"category": "Finance", "subcategory": "JPMorgan", "value": 500},
    {"category": "Finance", "subcategory": "BofA", "value": 300},
    {"category": "Finance", "subcategory": "Wells Fargo", "value": 200},
    {"category": "Healthcare", "subcategory": "UnitedHealth", "value": 450},
    {"category": "Healthcare", "subcategory": "Johnson & Johnson", "value": 380},
    {"category": "Healthcare", "subcategory": "Pfizer", "value": 250},
    {"category": "Energy", "subcategory": "ExxonMobil", "value": 420},
    {"category": "Energy", "subcategory": "Chevron", "value": 300},
    {"category": "Consumer", "subcategory": "Amazon", "value": 1500},
    {"category": "Consumer", "subcategory": "Walmart", "value": 400},
    {"category": "Consumer", "subcategory": "Tesla", "value": 600},
]

df = pd.DataFrame(data)

# Canvas dimensions
width = 1400
height = 800


# Simple squarify algorithm for treemap layout
def compute_treemap(values, x, y, dx, dy):
    """Compute treemap rectangles using slice-and-dice algorithm."""
    rects = []
    total = sum(values)
    if total == 0:
        return rects

    n = len(values)
    if n == 0:
        return rects

    if n == 1:
        return [{"x": x, "y": y, "dx": dx, "dy": dy}]

    # Sort values in descending order with indices
    indexed = sorted(enumerate(values), key=lambda x: -x[1])
    sorted_indices = [i for i, _ in indexed]
    sorted_values = [v for _, v in indexed]

    # Slice-and-dice: alternate horizontal and vertical splits
    result = [None] * n
    remaining_x, remaining_y = x, y
    remaining_dx, remaining_dy = dx, dy

    for idx, (orig_idx, val) in enumerate(zip(sorted_indices, sorted_values)):
        remaining_total = sum(sorted_values[idx:])
        if remaining_total == 0:
            break
        ratio = val / remaining_total

        # Alternate split direction based on remaining rectangle aspect ratio
        if remaining_dx >= remaining_dy:
            # Vertical split (cut horizontally)
            rect_dx = remaining_dx * ratio
            result[orig_idx] = {"x": remaining_x, "y": remaining_y, "dx": rect_dx, "dy": remaining_dy}
            remaining_x += rect_dx
            remaining_dx -= rect_dx
        else:
            # Horizontal split (cut vertically)
            rect_dy = remaining_dy * ratio
            result[orig_idx] = {"x": remaining_x, "y": remaining_y, "dx": remaining_dx, "dy": rect_dy}
            remaining_y += rect_dy
            remaining_dy -= rect_dy

    return [r for r in result if r is not None]


# Better squarify implementation
def squarify_layout(values, x, y, dx, dy):
    """Compute treemap using squarify algorithm for more square-like rectangles."""
    rects = []
    total = sum(values)
    if total == 0 or len(values) == 0:
        return rects

    # Normalize values to fit the area
    area = dx * dy
    normalized = [v / total * area for v in values]

    # Sort by value descending
    items = sorted(enumerate(normalized), key=lambda x: -x[1])
    indices = [i for i, _ in items]
    sizes = [v for _, v in items]

    result = [None] * len(values)
    layout_row(sizes, indices, x, y, dx, dy, result)
    return result


def layout_row(sizes, indices, x, y, dx, dy, result):
    """Recursively layout rectangles."""
    if not sizes:
        return

    if len(sizes) == 1:
        result[indices[0]] = {"x": x, "y": y, "dx": dx, "dy": dy}
        return

    # Find the best split point
    total = sum(sizes)
    if dx >= dy:
        # Lay out in columns
        width_per_unit = dx / total
        current_x = x
        for i, (idx, size) in enumerate(zip(indices, sizes)):
            rect_width = size * width_per_unit
            result[idx] = {"x": current_x, "y": y, "dx": rect_width, "dy": dy}
            current_x += rect_width
    else:
        # Lay out in rows
        height_per_unit = dy / total
        current_y = y
        for i, (idx, size) in enumerate(zip(indices, sizes)):
            rect_height = size * height_per_unit
            result[idx] = {"x": x, "y": current_y, "dx": dx, "dy": rect_height}
            current_y += rect_height


# Compute treemap layout using hierarchical approach
# First group by category, then layout within each category
categories = df["category"].unique()
category_totals = df.groupby("category")["value"].sum().to_dict()

# Sort categories by total value
sorted_cats = sorted(categories, key=lambda c: -category_totals[c])
cat_values = [category_totals[c] for c in sorted_cats]

# Layout category rectangles
cat_rects = squarify_layout(cat_values, 0, 0, width, height)

# For each category, layout subcategories within its rectangle
all_rects = []
for cat, cat_rect in zip(sorted_cats, cat_rects):
    cat_df = df[df["category"] == cat]
    sub_values = cat_df["value"].tolist()
    sub_names = cat_df["subcategory"].tolist()

    # Layout subcategories within category rectangle
    sub_rects = squarify_layout(sub_values, cat_rect["x"], cat_rect["y"], cat_rect["dx"], cat_rect["dy"])

    for sub_rect, name, val in zip(sub_rects, sub_names, sub_values):
        all_rects.append(
            {
                "category": cat,
                "subcategory": name,
                "value": val,
                "x": sub_rect["x"],
                "y": sub_rect["y"],
                "dx": sub_rect["dx"],
                "dy": sub_rect["dy"],
            }
        )

rects_df = pd.DataFrame(all_rects)

# Calculate coordinates for Altair (x2, y2 for mark_rect)
rects_df["x2"] = rects_df["x"] + rects_df["dx"]
rects_df["y2"] = rects_df["y"] + rects_df["dy"]
rects_df["x_center"] = rects_df["x"] + rects_df["dx"] / 2
rects_df["y_center"] = rects_df["y"] + rects_df["dy"] / 2

# Format value for display
rects_df["display_value"] = rects_df["value"].apply(lambda x: f"${x}B")

# Color palette - distinct colors per main category
colors = {
    "Technology": "#306998",
    "Finance": "#FFD43B",
    "Healthcare": "#4ECDC4",
    "Energy": "#FF6B6B",
    "Consumer": "#95E1D3",
}

# Treemap rectangles
rects_chart = (
    alt.Chart(rects_df)
    .mark_rect(stroke="#ffffff", strokeWidth=3)
    .encode(
        x=alt.X("x:Q", scale=alt.Scale(domain=[0, width]), axis=None),
        y=alt.Y("y:Q", scale=alt.Scale(domain=[0, height]), axis=None),
        x2="x2:Q",
        y2="y2:Q",
        color=alt.Color(
            "category:N",
            scale=alt.Scale(domain=list(colors.keys()), range=list(colors.values())),
            legend=alt.Legend(title="Sector", titleFontSize=20, labelFontSize=18, symbolSize=300, orient="right"),
        ),
        tooltip=[
            alt.Tooltip("category:N", title="Sector"),
            alt.Tooltip("subcategory:N", title="Company"),
            alt.Tooltip("display_value:N", title="Market Cap"),
        ],
    )
)

# Text labels - show company name for rectangles large enough
rects_df["area"] = rects_df["dx"] * rects_df["dy"]
min_area_for_label = width * height * 0.015
labels_df = rects_df[rects_df["area"] >= min_area_for_label].copy()

text_chart = (
    alt.Chart(labels_df)
    .mark_text(fontSize=18, fontWeight="bold", color="#ffffff")
    .encode(
        x=alt.X("x_center:Q", scale=alt.Scale(domain=[0, width])),
        y=alt.Y("y_center:Q", scale=alt.Scale(domain=[0, height])),
        text="subcategory:N",
    )
)

# Combine layers
chart = (
    alt.layer(rects_chart, text_chart)
    .properties(
        width=width,
        height=height,
        title=alt.Title(text="treemap-basic · altair · pyplots.ai", fontSize=28, anchor="middle"),
    )
    .configure_view(strokeWidth=0)
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
