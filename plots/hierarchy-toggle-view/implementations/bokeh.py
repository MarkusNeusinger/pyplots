""" pyplots.ai
hierarchy-toggle-view: Interactive Treemap-Sunburst Toggle View
Library: bokeh 3.8.2 | Python 3.13.11
Quality: 58/100 | Created: 2026-01-11
"""

import numpy as np
from bokeh.io import export_png, save
from bokeh.layouts import column, row
from bokeh.models import Button, ColumnDataSource, CustomJS, Div, LabelSet
from bokeh.plotting import figure
from bokeh.resources import CDN


# Data - organizational budget hierarchy
np.random.seed(42)

hierarchy = [
    {"id": "company", "parent": "", "label": "Company", "value": 0},
    {"id": "engineering", "parent": "company", "label": "Engineering", "value": 0},
    {"id": "marketing", "parent": "company", "label": "Marketing", "value": 0},
    {"id": "operations", "parent": "company", "label": "Operations", "value": 0},
    {"id": "hr", "parent": "company", "label": "HR", "value": 0},
    {"id": "frontend", "parent": "engineering", "label": "Frontend", "value": 1200},
    {"id": "backend", "parent": "engineering", "label": "Backend", "value": 1500},
    {"id": "devops", "parent": "engineering", "label": "DevOps", "value": 800},
    {"id": "qa", "parent": "engineering", "label": "QA", "value": 600},
    {"id": "digital", "parent": "marketing", "label": "Digital", "value": 900},
    {"id": "content", "parent": "marketing", "label": "Content", "value": 700},
    {"id": "analytics", "parent": "marketing", "label": "Analytics", "value": 500},
    {"id": "logistics", "parent": "operations", "label": "Logistics", "value": 1100},
    {"id": "facilities", "parent": "operations", "label": "Facilities", "value": 600},
    {"id": "procurement", "parent": "operations", "label": "Procurement", "value": 450},
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

# Color palette - more distinct colors for Engineering sub-departments
colors = {
    "company": "#306998",
    "engineering": "#FFD43B",
    "marketing": "#66c2a5",
    "operations": "#fc8d62",
    "hr": "#8da0cb",
    "frontend": "#f94144",
    "backend": "#277da1",
    "devops": "#43aa8b",
    "qa": "#f9c74f",
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

# Get leaf nodes for treemap
leaf_nodes = [n for n in hierarchy if not any(m["parent"] == n["id"] for m in hierarchy)]
leaf_values = [n["value"] for n in leaf_nodes]

# Inline squarify algorithm for treemap layout
treemap_rects = []
remaining_nodes = list(enumerate(leaf_values))
total = sum(leaf_values)
x, y, w, h = 0, 0, 4000, 2200

while remaining_nodes:
    if w >= h:
        strip = []
        strip_sum = 0
        best_ratio = float("inf")
        strip_idx = 0
        for i, (idx, v) in enumerate(remaining_nodes):
            test_strip = strip + [(idx, v)]
            test_sum = strip_sum + v
            strip_w = (test_sum / total) * w if total > 0 else w
            ratios = []
            for _, sv in test_strip:
                strip_h = (sv / test_sum) * h if test_sum > 0 else h / len(test_strip)
                ratio = max(strip_w / strip_h, strip_h / strip_w) if strip_h > 0 else float("inf")
                ratios.append(ratio)
            worst_ratio = max(ratios) if ratios else float("inf")
            if worst_ratio <= best_ratio:
                strip = test_strip
                strip_sum = test_sum
                best_ratio = worst_ratio
                strip_idx = i + 1
            else:
                break
        strip_w = (strip_sum / total) * w if total > 0 else w
        strip_y = y
        for idx, sv in strip:
            strip_h = (sv / strip_sum) * h if strip_sum > 0 else h / len(strip)
            treemap_rects.append((idx, x, strip_y, strip_w, strip_h))
            strip_y += strip_h
        x += strip_w
        w -= strip_w
        total -= strip_sum
        remaining_nodes = remaining_nodes[strip_idx:]
    else:
        strip = []
        strip_sum = 0
        best_ratio = float("inf")
        strip_idx = 0
        for i, (idx, v) in enumerate(remaining_nodes):
            test_strip = strip + [(idx, v)]
            test_sum = strip_sum + v
            strip_h = (test_sum / total) * h if total > 0 else h
            ratios = []
            for _, sv in test_strip:
                strip_w = (sv / test_sum) * w if test_sum > 0 else w / len(test_strip)
                ratio = max(strip_w / strip_h, strip_h / strip_w) if strip_w > 0 else float("inf")
                ratios.append(ratio)
            worst_ratio = max(ratios) if ratios else float("inf")
            if worst_ratio <= best_ratio:
                strip = test_strip
                strip_sum = test_sum
                best_ratio = worst_ratio
                strip_idx = i + 1
            else:
                break
        strip_h = (strip_sum / total) * h if total > 0 else h
        strip_x = x
        for idx, sv in strip:
            strip_w = (sv / strip_sum) * w if strip_sum > 0 else w / len(strip)
            treemap_rects.append((idx, strip_x, y, strip_w, strip_h))
            strip_x += strip_w
        y += strip_h
        h -= strip_h
        total -= strip_sum
        remaining_nodes = remaining_nodes[strip_idx:]

# Build treemap data
treemap_xs = []
treemap_ys = []
treemap_widths = []
treemap_heights = []
treemap_colors = []
treemap_labels = []
treemap_text_labels = []
treemap_value_labels = []
treemap_label_xs = []
treemap_label_ys = []
treemap_value_xs = []
treemap_value_ys = []

for idx, rx, ry, rw, rh in treemap_rects:
    node = leaf_nodes[idx]
    cx = rx + rw / 2
    cy = ry + rh / 2
    treemap_xs.append(cx)
    treemap_ys.append(cy)
    treemap_widths.append(rw - 10)
    treemap_heights.append(rh - 10)
    treemap_colors.append(colors.get(node["id"], "#cccccc"))
    treemap_labels.append(f"{node['label']}: ${node['value']}K")
    treemap_text_labels.append(node["label"])
    treemap_value_labels.append(f"${node['value']}K")
    treemap_label_xs.append(cx)
    treemap_label_ys.append(cy + 40)
    treemap_value_xs.append(cx)
    treemap_value_ys.append(cy - 40)

# Generate sunburst wedges inline
sunburst_inner = []
sunburst_outer = []
sunburst_start = []
sunburst_end = []
sunburst_colors = []
sunburst_labels = []

scx, scy = 2000, 1100
total_value = id_to_node["company"]["value"]

# Level 0: process company's children (departments)
level_0_start = 0.0
for dept in [n for n in hierarchy if n["parent"] == "company"]:
    angle_span = (dept["value"] / total_value) * 2 * np.pi
    sunburst_inner.append(200)
    sunburst_outer.append(460)
    sunburst_start.append(level_0_start)
    sunburst_end.append(level_0_start + angle_span)
    sunburst_colors.append(colors.get(dept["id"], "#cccccc"))
    sunburst_labels.append(f"{dept['label']}: ${dept['value']}K")

    # Level 1: process department's children (sub-departments)
    level_1_start = level_0_start
    for subdept in [n for n in hierarchy if n["parent"] == dept["id"]]:
        sub_angle_span = (subdept["value"] / total_value) * 2 * np.pi
        sunburst_inner.append(480)
        sunburst_outer.append(740)
        sunburst_start.append(level_1_start)
        sunburst_end.append(level_1_start + sub_angle_span)
        sunburst_colors.append(colors.get(subdept["id"], "#cccccc"))
        sunburst_labels.append(f"{subdept['label']}: ${subdept['value']}K")
        level_1_start += sub_angle_span

    level_0_start += angle_span

# Convert sunburst to x,y coordinates for patches
sunburst_xs_list = []
sunburst_ys_list = []

for i in range(len(sunburst_inner)):
    angles = np.linspace(sunburst_start[i], sunburst_end[i], 30)
    inner_x = scx + sunburst_inner[i] * np.cos(angles)
    inner_y = scy + sunburst_inner[i] * np.sin(angles)
    outer_x = scx + sunburst_outer[i] * np.cos(angles[::-1])
    outer_y = scy + sunburst_outer[i] * np.sin(angles[::-1])
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

treemap_label_source = ColumnDataSource(
    data={"x": treemap_label_xs, "y": treemap_label_ys, "text": treemap_text_labels}
)

treemap_value_source = ColumnDataSource(
    data={"x": treemap_value_xs, "y": treemap_value_ys, "text": treemap_value_labels}
)

sunburst_source = ColumnDataSource(
    data={"xs": sunburst_xs_list, "ys": sunburst_ys_list, "color": sunburst_colors, "labels": sunburst_labels}
)

# Draw treemap rectangles
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

# Add labels using LabelSet for proper PNG export
treemap_labels_renderer = LabelSet(
    x="x",
    y="y",
    text="text",
    source=treemap_label_source,
    text_font_size="22pt",
    text_color="#222222",
    text_align="center",
    text_baseline="middle",
    text_font_style="bold",
)
p.add_layout(treemap_labels_renderer)

treemap_values_renderer = LabelSet(
    x="x",
    y="y",
    text="text",
    source=treemap_value_source,
    text_font_size="18pt",
    text_color="#444444",
    text_align="center",
    text_baseline="middle",
)
p.add_layout(treemap_values_renderer)

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

title_div = Div(
    text="<h2 style='font-size: 24px; color: #306998; margin: 10px;'>Company Budget Allocation</h2>",
    width=400,
    height=50,
)

button_row = row(treemap_btn, sunburst_btn)
layout = column(title_div, button_row, p)

# Save HTML for interactive version
save(layout, filename="plot.html", resources=CDN, title="Hierarchy Toggle View")

# For PNG export, ensure treemap view is shown
treemap_renderer.visible = True
sunburst_renderer.visible = False
treemap_labels_renderer.visible = True
treemap_values_renderer.visible = True
export_png(p, filename="plot.png")
