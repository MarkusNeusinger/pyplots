""" pyplots.ai
hierarchy-toggle-view: Interactive Treemap-Sunburst Toggle View
Library: bokeh 3.8.2 | Python 3.13.11
Quality: 62/100 | Created: 2026-01-11
"""

import numpy as np
from bokeh.io import export_png, save
from bokeh.layouts import column, row
from bokeh.models import Button, ColumnDataSource, CustomJS, Div
from bokeh.plotting import figure
from bokeh.resources import CDN


# Data - organizational budget hierarchy
np.random.seed(42)

hierarchy = [
    # Root
    {"id": "company", "parent": "", "label": "Company", "value": 0},
    # Level 1 - Departments
    {"id": "engineering", "parent": "company", "label": "Engineering", "value": 0},
    {"id": "marketing", "parent": "company", "label": "Marketing", "value": 0},
    {"id": "operations", "parent": "company", "label": "Operations", "value": 0},
    {"id": "hr", "parent": "company", "label": "HR", "value": 0},
    # Level 2 - Engineering
    {"id": "frontend", "parent": "engineering", "label": "Frontend", "value": 1200},
    {"id": "backend", "parent": "engineering", "label": "Backend", "value": 1500},
    {"id": "devops", "parent": "engineering", "label": "DevOps", "value": 800},
    {"id": "qa", "parent": "engineering", "label": "QA", "value": 600},
    # Level 2 - Marketing
    {"id": "digital", "parent": "marketing", "label": "Digital", "value": 900},
    {"id": "content", "parent": "marketing", "label": "Content", "value": 700},
    {"id": "analytics", "parent": "marketing", "label": "Analytics", "value": 500},
    # Level 2 - Operations
    {"id": "logistics", "parent": "operations", "label": "Logistics", "value": 1100},
    {"id": "facilities", "parent": "operations", "label": "Facilities", "value": 600},
    {"id": "procurement", "parent": "operations", "label": "Procurement", "value": 450},
    # Level 2 - HR
    {"id": "recruiting", "parent": "hr", "label": "Recruiting", "value": 400},
    {"id": "training", "parent": "hr", "label": "Training", "value": 350},
    {"id": "benefits", "parent": "hr", "label": "Benefits", "value": 300},
]

# Calculate parent values (sum of children)
id_to_node = {n["id"]: n for n in hierarchy}
for node in reversed(hierarchy):
    if node["value"] == 0:
        children_sum = sum(n["value"] for n in hierarchy if n["parent"] == node["id"])
        node["value"] = children_sum

# Color palette - consistent across views
colors = {
    "company": "#306998",
    "engineering": "#FFD43B",
    "marketing": "#66c2a5",
    "operations": "#fc8d62",
    "hr": "#8da0cb",
    "frontend": "#ffe066",
    "backend": "#ffd633",
    "devops": "#ffcc00",
    "qa": "#e6b800",
    "digital": "#99d8c9",
    "content": "#66c2a5",
    "analytics": "#41ae76",
    "logistics": "#fdae6b",
    "facilities": "#fd8d3c",
    "procurement": "#e6550d",
    "recruiting": "#9e9ac8",
    "training": "#807dba",
    "benefits": "#6a51a3",
}


# Treemap layout using squarified algorithm
def squarify(values, x, y, w, h):
    """Simple squarify algorithm for treemap layout."""
    if len(values) == 0:
        return []

    total = sum(values)
    if total == 0:
        return [(x, y, w / len(values), h) for _ in values]

    rects = []
    remaining = list(enumerate(values))

    while remaining:
        # Decide layout direction
        if w >= h:
            # Horizontal strip
            strip = []
            strip_sum = 0
            best_ratio = float("inf")

            for _i, (idx, v) in enumerate(remaining):
                test_strip = strip + [(idx, v)]
                test_sum = strip_sum + v
                strip_w = (test_sum / total) * w

                # Calculate aspect ratios
                ratios = []
                strip_y = y
                for _, sv in test_strip:
                    strip_h = (sv / test_sum) * h if test_sum > 0 else h / len(test_strip)
                    ratio = max(strip_w / strip_h, strip_h / strip_w) if strip_h > 0 else float("inf")
                    ratios.append(ratio)

                worst_ratio = max(ratios) if ratios else float("inf")

                if worst_ratio <= best_ratio:
                    strip = test_strip
                    strip_sum = test_sum
                    best_ratio = worst_ratio
                else:
                    break

            # Layout strip
            strip_w = (strip_sum / total) * w if total > 0 else w
            strip_y = y
            for idx, sv in strip:
                strip_h = (sv / strip_sum) * h if strip_sum > 0 else h / len(strip)
                rects.append((idx, x, strip_y, strip_w, strip_h))
                strip_y += strip_h

            x += strip_w
            w -= strip_w
            total -= strip_sum
            remaining = remaining[len(strip) :]
        else:
            # Vertical strip
            strip = []
            strip_sum = 0
            best_ratio = float("inf")

            for _i, (idx, v) in enumerate(remaining):
                test_strip = strip + [(idx, v)]
                test_sum = strip_sum + v
                strip_h = (test_sum / total) * h

                ratios = []
                strip_x = x
                for _, sv in test_strip:
                    strip_w = (sv / test_sum) * w if test_sum > 0 else w / len(test_strip)
                    ratio = max(strip_w / strip_h, strip_h / strip_w) if strip_w > 0 else float("inf")
                    ratios.append(ratio)

                worst_ratio = max(ratios) if ratios else float("inf")

                if worst_ratio <= best_ratio:
                    strip = test_strip
                    strip_sum = test_sum
                    best_ratio = worst_ratio
                else:
                    break

            strip_h = (strip_sum / total) * h if total > 0 else h
            strip_x = x
            for idx, sv in strip:
                strip_w = (sv / strip_sum) * w if strip_sum > 0 else w / len(strip)
                rects.append((idx, strip_x, y, strip_w, strip_h))
                strip_x += strip_w

            y += strip_h
            h -= strip_h
            total -= strip_sum
            remaining = remaining[len(strip) :]

    return rects


# Generate treemap rectangles for leaf nodes only
leaf_nodes = [n for n in hierarchy if not any(m["parent"] == n["id"] for m in hierarchy)]
leaf_values = [n["value"] for n in leaf_nodes]
treemap_rects = squarify(leaf_values, 0, 0, 4000, 2200)

treemap_xs = []
treemap_ys = []
treemap_widths = []
treemap_heights = []
treemap_colors = []
treemap_labels = []

treemap_text_labels = []
treemap_value_labels = []
treemap_label_ys = []
treemap_value_ys = []

for idx, x, y, w, h in treemap_rects:
    node = leaf_nodes[idx]
    cx = x + w / 2
    cy = y + h / 2
    treemap_xs.append(cx)
    treemap_ys.append(cy)
    treemap_widths.append(w - 10)
    treemap_heights.append(h - 10)
    treemap_colors.append(colors.get(node["id"], "#cccccc"))
    treemap_labels.append(f"{node['label']}: ${node['value']}K")
    treemap_text_labels.append(node["label"])
    treemap_value_labels.append(f"${node['value']}K")
    treemap_label_ys.append(cy + 30)
    treemap_value_ys.append(cy - 30)

# Generate sunburst wedges
sunburst_inner = []
sunburst_outer = []
sunburst_start = []
sunburst_end = []
sunburst_colors = []
sunburst_labels = []

cx, cy = 2000, 1100
total_value = id_to_node["company"]["value"]


def add_sunburst_wedges(parent_id, start_angle, end_angle, level):
    """Recursively add sunburst wedges."""
    children = [n for n in hierarchy if n["parent"] == parent_id]
    if not children:
        return

    inner_r = 200 + level * 280
    outer_r = 200 + (level + 1) * 280 - 20

    current_angle = start_angle
    for child in children:
        angle_span = (child["value"] / total_value) * 2 * np.pi
        end_ang = current_angle + angle_span

        sunburst_inner.append(inner_r)
        sunburst_outer.append(outer_r)
        sunburst_start.append(current_angle)
        sunburst_end.append(end_ang)
        sunburst_colors.append(colors.get(child["id"], "#cccccc"))
        sunburst_labels.append(f"{child['label']}: ${child['value']}K")

        add_sunburst_wedges(child["id"], current_angle, end_ang, level + 1)
        current_angle = end_ang


add_sunburst_wedges("company", 0, 2 * np.pi, 0)

# Convert sunburst to x,y coordinates for patches
sunburst_xs_list = []
sunburst_ys_list = []

for i in range(len(sunburst_inner)):
    angles = np.linspace(sunburst_start[i], sunburst_end[i], 30)
    inner_x = cx + sunburst_inner[i] * np.cos(angles)
    inner_y = cy + sunburst_inner[i] * np.sin(angles)
    outer_x = cx + sunburst_outer[i] * np.cos(angles[::-1])
    outer_y = cy + sunburst_outer[i] * np.sin(angles[::-1])
    xs = list(inner_x) + list(outer_x)
    ys = list(inner_y) + list(outer_y)
    sunburst_xs_list.append(xs)
    sunburst_ys_list.append(ys)

# Create the figure
p = figure(
    width=4800,
    height=2700,
    title="hierarchy-toggle-view · bokeh · pyplots.ai",
    x_range=(-500, 4500),
    y_range=(-300, 2500),
    tools="hover",
    tooltips="@labels",
)

# Style the figure
p.title.text_font_size = "28pt"
p.title.text_color = "#306998"
p.xaxis.visible = False
p.yaxis.visible = False
p.grid.visible = False
p.outline_line_color = None
p.background_fill_color = "#fafafa"

# Create data sources
treemap_source = ColumnDataSource(
    data={
        "x": treemap_xs,
        "y": treemap_ys,
        "width": treemap_widths,
        "height": treemap_heights,
        "color": treemap_colors,
        "labels": treemap_labels,
    }
)

treemap_label_source = ColumnDataSource(data={"x": treemap_xs, "y": treemap_label_ys, "text": treemap_text_labels})

treemap_value_source = ColumnDataSource(data={"x": treemap_xs, "y": treemap_value_ys, "text": treemap_value_labels})

sunburst_source = ColumnDataSource(
    data={"xs": sunburst_xs_list, "ys": sunburst_ys_list, "color": sunburst_colors, "labels": sunburst_labels}
)

# Draw treemap (visible initially)
treemap_renderer = p.rect(
    x="x",
    y="y",
    width="width",
    height="height",
    color="color",
    source=treemap_source,
    line_color="white",
    line_width=3,
    alpha=0.9,
)

# Add labels to treemap using text glyph
treemap_labels_renderer = p.text(
    x="x",
    y="y",
    text="text",
    source=treemap_label_source,
    text_font_size="20pt",
    text_color="#333333",
    text_align="center",
    text_baseline="middle",
)

treemap_values_renderer = p.text(
    x="x",
    y="y",
    text="text",
    source=treemap_value_source,
    text_font_size="16pt",
    text_color="#555555",
    text_align="center",
    text_baseline="middle",
)

# Draw sunburst (hidden initially)
sunburst_renderer = p.patches(
    xs="xs", ys="ys", color="color", source=sunburst_source, line_color="white", line_width=2, alpha=0.9
)
sunburst_renderer.visible = False

# Create toggle buttons
treemap_btn = Button(label="Treemap View", button_type="primary", width=200, height=50)
sunburst_btn = Button(label="Sunburst View", button_type="default", width=200, height=50)

# Toggle callbacks
toggle_to_treemap = CustomJS(
    args={
        "treemap": treemap_renderer,
        "sunburst": sunburst_renderer,
        "tm_labels": treemap_labels_renderer,
        "tm_values": treemap_values_renderer,
        "tm_btn": treemap_btn,
        "sb_btn": sunburst_btn,
    },
    code="""
    treemap.visible = true;
    sunburst.visible = false;
    tm_labels.visible = true;
    tm_values.visible = true;
    tm_btn.button_type = 'primary';
    sb_btn.button_type = 'default';
""",
)

toggle_to_sunburst = CustomJS(
    args={
        "treemap": treemap_renderer,
        "sunburst": sunburst_renderer,
        "tm_labels": treemap_labels_renderer,
        "tm_values": treemap_values_renderer,
        "tm_btn": treemap_btn,
        "sb_btn": sunburst_btn,
    },
    code="""
    treemap.visible = false;
    sunburst.visible = true;
    tm_labels.visible = false;
    tm_values.visible = false;
    tm_btn.button_type = 'default';
    sb_btn.button_type = 'primary';
""",
)

treemap_btn.js_on_click(toggle_to_treemap)
sunburst_btn.js_on_click(toggle_to_sunburst)

# Title label
title_div = Div(
    text="<h2 style='font-size: 24px; color: #306998; margin: 10px;'>Company Budget Allocation</h2>",
    width=400,
    height=50,
)

# Layout
button_row = row(treemap_btn, sunburst_btn)
layout = column(title_div, button_row, p)

# Save HTML for interactive version
save(layout, filename="plot.html", resources=CDN, title="Hierarchy Toggle View")

# For PNG export, show treemap view (default)
treemap_renderer.visible = True
sunburst_renderer.visible = False
export_png(p, filename="plot.png")
