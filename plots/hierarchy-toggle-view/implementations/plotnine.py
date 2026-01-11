""" pyplots.ai
hierarchy-toggle-view: Interactive Treemap-Sunburst Toggle View
Library: plotnine 0.15.2 | Python 3.13.11
Quality: 85/100 | Created: 2026-01-11
"""

import sys


sys.path = [p for p in sys.path if not p.endswith("implementations")]

import math  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from plotnine import (  # noqa: E402
    aes,
    annotate,
    coord_fixed,
    element_blank,
    element_rect,
    element_text,
    geom_polygon,
    geom_rect,
    geom_segment,
    geom_text,
    ggplot,
    labs,
    scale_fill_identity,
    scale_x_continuous,
    scale_y_continuous,
    theme,
)


# Data: Corporate budget allocation across departments (hierarchical structure)
# 3 levels: root -> department -> team (18 nodes total)
hierarchy_data = {
    "root": {"id": "root", "parent": None, "label": "Company", "value": 0},
    # Level 1: Departments
    "engineering": {"id": "engineering", "parent": "root", "label": "Engineering", "value": 0},
    "sales": {"id": "sales", "parent": "root", "label": "Sales", "value": 0},
    "marketing": {"id": "marketing", "parent": "root", "label": "Marketing", "value": 0},
    "operations": {"id": "operations", "parent": "root", "label": "Operations", "value": 0},
    # Level 2: Teams under Engineering
    "eng_backend": {"id": "eng_backend", "parent": "engineering", "label": "Backend", "value": 180},
    "eng_frontend": {"id": "eng_frontend", "parent": "engineering", "label": "Frontend", "value": 150},
    "eng_devops": {"id": "eng_devops", "parent": "engineering", "label": "DevOps", "value": 100},
    # Level 2: Teams under Sales
    "sales_north": {"id": "sales_north", "parent": "sales", "label": "North", "value": 140},
    "sales_south": {"id": "sales_south", "parent": "sales", "label": "South", "value": 110},
    "sales_east": {"id": "sales_east", "parent": "sales", "label": "East", "value": 90},
    # Level 2: Teams under Marketing
    "mkt_digital": {"id": "mkt_digital", "parent": "marketing", "label": "Digital", "value": 120},
    "mkt_brand": {"id": "mkt_brand", "parent": "marketing", "label": "Brand", "value": 80},
    # Level 2: Teams under Operations
    "ops_logistics": {"id": "ops_logistics", "parent": "operations", "label": "Logistics", "value": 95},
    "ops_facilities": {"id": "ops_facilities", "parent": "operations", "label": "Facilities", "value": 75},
}

# Calculate department totals from children
for node_id, node in hierarchy_data.items():
    if node["parent"] == "root" and node_id != "root":
        children_sum = sum(n["value"] for n in hierarchy_data.values() if n["parent"] == node_id)
        node["value"] = children_sum

total_value = sum(n["value"] for n in hierarchy_data.values() if n["parent"] == "root")

# Color palette - consistent across both views
dept_colors = {
    "Engineering": "#306998",  # Python Blue
    "Sales": "#FFD43B",  # Python Yellow
    "Marketing": "#2ECC71",  # Green
    "Operations": "#E74C3C",  # Red
}

# Child colors - slightly varied shades
child_colors = {
    "Backend": "#4A83AB",
    "Frontend": "#6B9DBE",
    "DevOps": "#8CBBEE",
    "North": "#F5C800",
    "South": "#E6BE35",
    "East": "#D4A72C",
    "Digital": "#58D68D",
    "Brand": "#82E0A8",
    "Logistics": "#EC7063",
    "Facilities": "#F1948A",
}

# Get departments and leaves
departments = [n for n in hierarchy_data.values() if n["parent"] == "root" and n["id"] != "root"]
departments = sorted(departments, key=lambda x: x["value"], reverse=True)
leaves = [n for n in hierarchy_data.values() if n["parent"] not in [None, "root"]]


# ========== TREEMAP LAYOUT ==========
def squarify_layout(values, x, y, w, h):
    """Simple squarify algorithm for treemap layout."""
    rects = []
    total = sum(values)
    if total == 0 or not values:
        return rects

    remaining = list(values)
    rx, ry, rw, rh = x, y, w, h

    while remaining:
        if rw >= rh:
            row, row_sum = [], 0
            best_ratio = float("inf")

            for v in remaining:
                test_row = row + [v]
                test_sum = row_sum + v
                row_width = (test_sum / total) * w if total > 0 else 0

                if row_width > 0:
                    worst = 0
                    for rv in test_row:
                        rect_h = (rv / test_sum) * rh if test_sum > 0 else 0
                        ratio = max(row_width / rect_h, rect_h / row_width) if rect_h > 0 else float("inf")
                        worst = max(worst, ratio)
                    if worst <= best_ratio:
                        best_ratio = worst
                        row = test_row
                        row_sum = test_sum
                    else:
                        break
                else:
                    row = test_row
                    row_sum = test_sum

            row_width = (row_sum / total) * w if total > 0 else 0
            cy = ry
            for rv in row:
                rect_h = (rv / row_sum) * rh if row_sum > 0 else 0
                rects.append((rx, cy, row_width, rect_h))
                cy += rect_h
            rx += row_width
            rw -= row_width
            remaining = remaining[len(row) :]
        else:
            col, col_sum = [], 0
            best_ratio = float("inf")

            for v in remaining:
                test_col = col + [v]
                test_sum = col_sum + v
                col_height = (test_sum / total) * h if total > 0 else 0

                if col_height > 0:
                    worst = 0
                    for cv in test_col:
                        rect_w = (cv / test_sum) * rw if test_sum > 0 else 0
                        ratio = max(col_height / rect_w, rect_w / col_height) if rect_w > 0 else float("inf")
                        worst = max(worst, ratio)
                    if worst <= best_ratio:
                        best_ratio = worst
                        col = test_col
                        col_sum = test_sum
                    else:
                        break
                else:
                    col = test_col
                    col_sum = test_sum

            col_height = (col_sum / total) * h if total > 0 else 0
            cx = rx
            for cv in col:
                rect_w = (cv / col_sum) * rw if col_sum > 0 else 0
                rects.append((cx, ry, rect_w, col_height))
                cx += rect_w
            ry += col_height
            rh -= col_height
            remaining = remaining[len(col) :]

    return rects


# Coordinate system: treemap on left (x: 0-100), sunburst on right (centered at x=200)
# Total canvas width: 300, height: 100

# ========== BUILD TREEMAP DATA (LEFT SIDE: x 0-95) ==========
dept_values = [d["value"] for d in departments]
dept_rects = squarify_layout(dept_values, 0, 0, 95, 90)

treemap_rects = []
treemap_labels = []
padding = 1.8

for i, dept in enumerate(departments):
    dx, dy, dw, dh = dept_rects[i]
    dept_color = dept_colors.get(dept["label"], "#888888")

    # Department background rectangle
    treemap_rects.append({"xmin": dx, "ymin": dy, "xmax": dx + dw, "ymax": dy + dh, "fill": dept_color, "level": 1})

    # Get children
    children = [n for n in leaves if n["parent"] == dept["id"]]
    children = sorted(children, key=lambda x: x["value"], reverse=True)

    if children:
        child_values = [c["value"] for c in children]
        inner_x = dx + padding
        inner_y = dy + padding
        inner_w = dw - 2 * padding
        inner_h = dh - 2 * padding - 6

        child_rects = squarify_layout(child_values, inner_x, inner_y, inner_w, inner_h)

        for j, child in enumerate(children):
            cx, cy, cw, ch = child_rects[j]
            c_color = child_colors.get(child["label"], "#888888")

            treemap_rects.append(
                {"xmin": cx, "ymin": cy, "xmax": cx + cw, "ymax": cy + ch, "fill": c_color, "level": 2}
            )

            # Child label
            pct = child["value"] / total_value * 100
            if cw > 10 and ch > 8:
                treemap_labels.append(
                    {"x": cx + cw / 2, "y": cy + ch / 2, "label": f"{child['label']}\n{pct:.0f}%", "level": 2}
                )
            elif cw > 5 and ch > 5:
                treemap_labels.append({"x": cx + cw / 2, "y": cy + ch / 2, "label": f"{pct:.0f}%", "level": 2})

    # Department label
    treemap_labels.append({"x": dx + dw / 2, "y": dy + dh - 3, "label": dept["label"], "level": 1})

treemap_rect_df = pd.DataFrame(treemap_rects)
treemap_label_df = pd.DataFrame(treemap_labels)

# Separate layers
treemap_bg = treemap_rect_df[treemap_rect_df["level"] == 1].reset_index(drop=True)
treemap_fg = treemap_rect_df[treemap_rect_df["level"] == 2].reset_index(drop=True)
label_dept = treemap_label_df[treemap_label_df["level"] == 1].reset_index(drop=True)
label_child = treemap_label_df[treemap_label_df["level"] == 2].reset_index(drop=True)


# ========== BUILD SUNBURST DATA (RIGHT SIDE: centered at x=200) ==========
def create_annular_segment(start_angle, end_angle, inner_r, outer_r, center_x, center_y, n_points=40):
    """Create polygon points for an annular segment."""
    gap = 0.015
    start_angle += gap
    end_angle -= gap

    points = []
    angles_out = np.linspace(end_angle, start_angle, n_points)
    for a in angles_out:
        points.append((center_x + outer_r * math.cos(a), center_y + outer_r * math.sin(a)))

    angles_in = np.linspace(start_angle, end_angle, n_points)
    for a in angles_in:
        points.append((center_x + inner_r * math.cos(a), center_y + inner_r * math.sin(a)))

    points.append(points[0])
    return points


sunburst_center_x = 200
sunburst_center_y = 45
sunburst_polygons = []
sunburst_labels = []
segment_id = 0

# Ring dimensions (scaled for the coordinate system)
r0, r1, r2 = 8, 25, 42

# First pass: departments (inner ring)
start_angle = math.pi / 2
dept_angles = {}

for dept in departments:
    pct = dept["value"] / total_value
    end_angle = start_angle - pct * 2 * math.pi
    dept_angles[dept["id"]] = (start_angle, end_angle)

    points = create_annular_segment(end_angle, start_angle, r0, r1, sunburst_center_x, sunburst_center_y)
    color = dept_colors.get(dept["label"], "#888888")

    for x, y in points:
        sunburst_polygons.append({"x": x, "y": y, "segment_id": segment_id, "fill": color})

    # Department label
    mid_angle = (start_angle + end_angle) / 2
    label_r = (r0 + r1) / 2
    sunburst_labels.append(
        {
            "x": sunburst_center_x + label_r * math.cos(mid_angle),
            "y": sunburst_center_y + label_r * math.sin(mid_angle),
            "label": dept["label"],
            "ring": 1,
        }
    )

    segment_id += 1
    start_angle = end_angle

# Second pass: children (outer ring)
for dept in departments:
    dept_start, dept_end = dept_angles[dept["id"]]
    dept_span = dept_start - dept_end

    children = [n for n in leaves if n["parent"] == dept["id"]]
    children = sorted(children, key=lambda x: x["value"], reverse=True)
    children_total = sum(c["value"] for c in children)

    child_start = dept_start
    for child in children:
        child_pct = child["value"] / children_total if children_total > 0 else 0
        child_span = child_pct * dept_span
        child_end = child_start - child_span

        points = create_annular_segment(child_end, child_start, r1, r2, sunburst_center_x, sunburst_center_y)
        color = child_colors.get(child["label"], "#888888")

        for x, y in points:
            sunburst_polygons.append({"x": x, "y": y, "segment_id": segment_id, "fill": color})

        # Child label (for larger segments)
        child_global_pct = child["value"] / total_value
        if child_global_pct > 0.05:
            mid_angle = (child_start + child_end) / 2
            label_r = (r1 + r2) / 2
            sunburst_labels.append(
                {
                    "x": sunburst_center_x + label_r * math.cos(mid_angle),
                    "y": sunburst_center_y + label_r * math.sin(mid_angle),
                    "label": child["label"],
                    "ring": 2,
                }
            )

        segment_id += 1
        child_start = child_end

sunburst_df = pd.DataFrame(sunburst_polygons)
sunburst_label_df = pd.DataFrame(sunburst_labels)

label_ring1 = sunburst_label_df[sunburst_label_df["ring"] == 1].reset_index(drop=True)
label_ring2 = sunburst_label_df[sunburst_label_df["ring"] == 2].reset_index(drop=True)

# ========== BUILD LEGEND DATA ==========
legend_data = []
legend_x = 105
legend_y_start = 8
legend_spacing = 5

for i, dept in enumerate(departments):
    y_pos = legend_y_start + i * legend_spacing
    color = dept_colors.get(dept["label"], "#888888")
    legend_data.append(
        {"xmin": legend_x, "ymin": y_pos - 1.5, "xmax": legend_x + 4, "ymax": y_pos + 1.5, "fill": color}
    )

legend_df = pd.DataFrame(legend_data)

legend_labels = []
for i, dept in enumerate(departments):
    y_pos = legend_y_start + i * legend_spacing
    legend_labels.append({"x": legend_x + 6, "y": y_pos, "label": dept["label"]})

legend_label_df = pd.DataFrame(legend_labels)

# ========== CREATE COMBINED PLOT ==========
plot = (
    ggplot()
    # Treemap background (departments)
    + geom_rect(
        aes(xmin="xmin", ymin="ymin", xmax="xmax", ymax="ymax", fill="fill"),
        data=treemap_bg,
        color="white",
        size=1.5,
        alpha=0.35,
    )
    # Treemap foreground (children)
    + geom_rect(
        aes(xmin="xmin", ymin="ymin", xmax="xmax", ymax="ymax", fill="fill"),
        data=treemap_fg,
        color="white",
        size=0.8,
        alpha=0.92,
    )
    # Treemap department labels
    + geom_text(aes(x="x", y="y", label="label"), data=label_dept, size=10, color="#333333", fontweight="bold")
    # Treemap child labels
    + geom_text(aes(x="x", y="y", label="label"), data=label_child, size=7, color="white", fontweight="bold")
    # Sunburst polygons
    + geom_polygon(
        aes(x="x", y="y", group="segment_id", fill="fill"), data=sunburst_df, color="white", size=0.8, alpha=0.92
    )
    # Sunburst inner ring labels
    + geom_text(aes(x="x", y="y", label="label"), data=label_ring1, size=7, color="white", fontweight="bold")
    # Sunburst outer ring labels
    + geom_text(aes(x="x", y="y", label="label"), data=label_ring2, size=6, color="#333333", fontweight="bold")
    # Center label for sunburst
    + annotate(
        "text", x=sunburst_center_x, y=sunburst_center_y + 2, label="Total", size=9, fontweight="bold", color="#306998"
    )
    + annotate("text", x=sunburst_center_x, y=sunburst_center_y - 3, label=f"${total_value}K", size=8, color="#555555")
    # View titles
    + annotate("text", x=47.5, y=95, label="Treemap View", size=14, fontweight="bold", color="#333333")
    + annotate("text", x=200, y=95, label="Sunburst View", size=14, fontweight="bold", color="#333333")
    # Legend rectangles
    + geom_rect(
        aes(xmin="xmin", ymin="ymin", xmax="xmax", ymax="ymax", fill="fill"),
        data=legend_df,
        color="white",
        size=0.5,
        alpha=0.95,
    )
    # Legend labels
    + geom_text(aes(x="x", y="y", label="label"), data=legend_label_df, size=7, ha="left", color="#333333")
    # Divider line between views
    + geom_segment(aes(x=100, xend=100, y=-5, yend=100), color="#cccccc", size=0.5, linetype="dashed")
    # Styling
    + scale_fill_identity()
    + coord_fixed(ratio=1)
    + scale_x_continuous(limits=(-5, 250), expand=(0, 0))
    + scale_y_continuous(limits=(-10, 105), expand=(0, 0))
    + labs(title="hierarchy-toggle-view · plotnine · pyplots.ai")
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=24, ha="center", face="bold", margin={"b": 15}),
        legend_position="none",
        axis_title=element_blank(),
        axis_text=element_blank(),
        axis_ticks=element_blank(),
        axis_line=element_blank(),
        panel_grid_major=element_blank(),
        panel_grid_minor=element_blank(),
        panel_background=element_rect(fill="white"),
        plot_background=element_rect(fill="white"),
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
