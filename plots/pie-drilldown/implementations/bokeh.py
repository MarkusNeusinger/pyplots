""" pyplots.ai
pie-drilldown: Drilldown Pie Chart with Click Navigation
Library: bokeh 3.8.1 | Python 3.13.11
Quality: 72/100 | Created: 2025-12-31
"""

import json
from math import pi

import numpy as np
from bokeh.io import export_png, save
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, CustomJS, Div, TapTool
from bokeh.plotting import figure
from bokeh.resources import INLINE


# Hierarchical data: Company expense breakdown
# Level 0: Total
# Level 1: Departments
# Level 2: Categories within departments
# Level 3: Specific items

hierarchy = {
    "root": {"name": "Total Expenses", "children": ["operations", "marketing", "research", "hr"]},
    "operations": {"name": "Operations", "parent": "root", "children": ["facilities", "logistics", "it_infra"]},
    "marketing": {"name": "Marketing", "parent": "root", "children": ["digital", "events", "content"]},
    "research": {"name": "Research", "parent": "root", "children": ["lab_equip", "materials", "personnel"]},
    "hr": {"name": "Human Resources", "parent": "root", "children": ["recruitment", "training", "benefits"]},
    # Operations subcategories
    "facilities": {"name": "Facilities", "parent": "operations", "children": ["rent", "utilities", "maintenance"]},
    "logistics": {"name": "Logistics", "parent": "operations", "children": ["shipping", "warehousing"]},
    "it_infra": {"name": "IT Infrastructure", "parent": "operations", "children": ["servers", "software", "support"]},
    # Marketing subcategories
    "digital": {"name": "Digital Marketing", "parent": "marketing", "children": ["ads", "seo", "social"]},
    "events": {"name": "Events", "parent": "marketing", "value": 180000},
    "content": {"name": "Content", "parent": "marketing", "value": 120000},
    # Research subcategories
    "lab_equip": {"name": "Lab Equipment", "parent": "research", "value": 350000},
    "materials": {"name": "Materials", "parent": "research", "value": 200000},
    "personnel": {"name": "Personnel", "parent": "research", "value": 450000},
    # HR subcategories
    "recruitment": {"name": "Recruitment", "parent": "hr", "value": 150000},
    "training": {"name": "Training", "parent": "hr", "value": 100000},
    "benefits": {"name": "Benefits", "parent": "hr", "value": 400000},
    # Facilities leaf nodes
    "rent": {"name": "Rent", "parent": "facilities", "value": 300000},
    "utilities": {"name": "Utilities", "parent": "facilities", "value": 80000},
    "maintenance": {"name": "Maintenance", "parent": "facilities", "value": 60000},
    # Logistics leaf nodes
    "shipping": {"name": "Shipping", "parent": "logistics", "value": 250000},
    "warehousing": {"name": "Warehousing", "parent": "logistics", "value": 180000},
    # IT Infrastructure leaf nodes
    "servers": {"name": "Servers", "parent": "it_infra", "value": 200000},
    "software": {"name": "Software", "parent": "it_infra", "value": 150000},
    "support": {"name": "Support", "parent": "it_infra", "value": 100000},
    # Digital Marketing leaf nodes
    "ads": {"name": "Advertising", "parent": "digital", "value": 400000},
    "seo": {"name": "SEO", "parent": "digital", "value": 80000},
    "social": {"name": "Social Media", "parent": "digital", "value": 120000},
}


def get_value(node_id):
    """Calculate total value for a node (sum of children if not leaf)."""
    node = hierarchy[node_id]
    if "value" in node:
        return node["value"]
    return sum(get_value(child) for child in node.get("children", []))


def get_level_data(parent_id):
    """Get data for displaying children of a parent node."""
    node = hierarchy[parent_id]
    children = node.get("children", [])
    if not children:
        return [], [], [], [], [], []

    names = []
    values = []
    ids = []
    has_children = []

    for child_id in children:
        child = hierarchy[child_id]
        names.append(child["name"])
        values.append(get_value(child_id))
        ids.append(child_id)
        has_children.append("children" in child)

    return names, values, ids, has_children


# Color palette - Python Blue variants and complementary colors
colors = [
    "#306998",  # Python Blue
    "#FFD43B",  # Python Yellow
    "#4B8BBE",  # Light Python Blue
    "#646464",  # Gray
    "#3776AB",  # Another Blue
    "#FF6B6B",  # Coral
    "#4ECDC4",  # Teal
    "#45B7D1",  # Sky Blue
]

# Get initial data (root level)
names, values, ids, has_children = get_level_data("root")
total = sum(values)
percentages = [v / total * 100 for v in values]

# Calculate angles for pie wedges
angles = [v / total * 2 * pi for v in values]
start_angles = [sum(angles[:i]) for i in range(len(angles))]
end_angles = [sum(angles[: i + 1]) for i in range(len(angles))]

# Create source data
source = ColumnDataSource(
    data={
        "names": names,
        "values": values,
        "ids": ids,
        "has_children": has_children,
        "start_angle": start_angles,
        "end_angle": end_angles,
        "color": colors[: len(names)],
        "percentage": percentages,
        "label": [f"{n}\n${v / 1000:.0f}K\n({p:.1f}%)" for n, v, p in zip(names, values, percentages, strict=True)],
    }
)

# Label source for the center of each wedge
mid_angles = [(s + e) / 2 for s, e in zip(start_angles, end_angles, strict=True)]
label_radius = 0.6
label_x = [label_radius * np.cos(a - pi / 2 + pi) for a in mid_angles]
label_y = [label_radius * np.sin(a - pi / 2 + pi) for a in mid_angles]

label_source = ColumnDataSource(
    data={
        "x": label_x,
        "y": label_y,
        "text": [f"{n}\n${v / 1000:.0f}K\n({p:.1f}%)" for n, v, p in zip(names, values, percentages, strict=True)],
    }
)

# Create figure
p = figure(
    width=3600,
    height=3600,
    title="pie-drilldown · bokeh · pyplots.ai",
    tools="tap,reset",
    toolbar_location=None,
    x_range=(-1.5, 1.5),
    y_range=(-1.5, 1.5),
)

# Style the figure
p.title.text_font_size = "36pt"
p.title.align = "center"
p.title.text_color = "#306998"
p.axis.visible = False
p.grid.visible = False
p.outline_line_color = None
p.background_fill_color = "#fafafa"

# Draw pie wedges
wedges = p.wedge(
    x=0,
    y=0,
    radius=0.9,
    start_angle="start_angle",
    end_angle="end_angle",
    color="color",
    source=source,
    line_color="white",
    line_width=3,
    direction="clock",
    start_angle_units="rad",
    end_angle_units="rad",
)

# Add labels
labels = p.text(
    x="x",
    y="y",
    text="text",
    source=label_source,
    text_font_size="18pt",
    text_align="center",
    text_baseline="middle",
    text_color="white",
    text_font_style="bold",
)

# Breadcrumb navigation div
breadcrumb = Div(
    text='<div style="font-size: 24pt; font-family: Arial, sans-serif; color: #306998; '
    'padding: 20px; text-align: center;">'
    '<span style="cursor: pointer; color: #306998; font-weight: bold;">📊 Total Expenses</span>'
    '<span style="color: #999; margin: 0 10px;"> | Click a slice to drill down</span>'
    "</div>",
    width=3600,
    height=80,
)

# Store hierarchy data as JSON for JavaScript
hierarchy_json = json.dumps(hierarchy)
colors_json = json.dumps(colors)

# JavaScript callback for drilling down on click
callback = CustomJS(
    args={
        "source": source,
        "label_source": label_source,
        "breadcrumb": breadcrumb,
        "hierarchy_json": hierarchy_json,
        "colors_json": colors_json,
    },
    code="""
    const hierarchy = JSON.parse(hierarchy_json);
    const colors = JSON.parse(colors_json);

    // Track navigation path
    if (!window.nav_path) {
        window.nav_path = ['root'];
    }

    const indices = source.selected.indices;
    if (indices.length === 0) return;

    const clicked_id = source.data['ids'][indices[0]];
    const clicked_node = hierarchy[clicked_id];

    // Check if node has children (can drill down)
    if (!clicked_node.children || clicked_node.children.length === 0) {
        // Leaf node - show message
        return;
    }

    // Calculate value recursively
    function getValue(node_id) {
        const node = hierarchy[node_id];
        if (node.value !== undefined) return node.value;
        if (!node.children) return 0;
        return node.children.reduce((sum, child) => sum + getValue(child), 0);
    }

    // Get children data
    const children = clicked_node.children;
    const names = children.map(id => hierarchy[id].name);
    const values = children.map(id => getValue(id));
    const total = values.reduce((a, b) => a + b, 0);
    const percentages = values.map(v => v / total * 100);
    const has_children = children.map(id => hierarchy[id].children !== undefined);

    // Calculate angles
    const angles = values.map(v => v / total * 2 * Math.PI);
    const start_angles = [];
    const end_angles = [];
    let cumsum = 0;
    for (let i = 0; i < angles.length; i++) {
        start_angles.push(cumsum);
        cumsum += angles[i];
        end_angles.push(cumsum);
    }

    // Update source
    source.data['names'] = names;
    source.data['values'] = values;
    source.data['ids'] = children;
    source.data['has_children'] = has_children;
    source.data['start_angle'] = start_angles;
    source.data['end_angle'] = end_angles;
    source.data['color'] = colors.slice(0, names.length);
    source.data['percentage'] = percentages;
    source.data['label'] = names.map((n, i) =>
        n + '\\n$' + (values[i]/1000).toFixed(0) + 'K\\n(' + percentages[i].toFixed(1) + '%)'
    );

    // Update label positions
    const mid_angles = start_angles.map((s, i) => (s + end_angles[i]) / 2);
    const label_radius = 0.6;
    label_source.data['x'] = mid_angles.map(a => label_radius * Math.cos(a - Math.PI/2 + Math.PI));
    label_source.data['y'] = mid_angles.map(a => label_radius * Math.sin(a - Math.PI/2 + Math.PI));
    label_source.data['text'] = names.map((n, i) =>
        n + '\\n$' + (values[i]/1000).toFixed(0) + 'K\\n(' + percentages[i].toFixed(1) + '%)'
    );

    // Update navigation path
    window.nav_path.push(clicked_id);

    // Update breadcrumb
    let breadcrumb_html = '<div style="font-size: 24pt; font-family: Arial, sans-serif; color: #306998; padding: 20px; text-align: center;">';
    for (let i = 0; i < window.nav_path.length; i++) {
        const node_id = window.nav_path[i];
        const node = hierarchy[node_id];
        if (i > 0) breadcrumb_html += ' › ';
        breadcrumb_html += '<span style="cursor: pointer; font-weight: bold;" onclick="window.navTo(' + i + ')">' + node.name + '</span>';
    }
    breadcrumb_html += '</div>';
    breadcrumb.text = breadcrumb_html;

    source.change.emit();
    label_source.change.emit();
    source.selected.indices = [];
""",
)

# Add tap tool with callback
p.select(type=TapTool).callback = callback

# Add hover effect by using selection
wedges.selection_glyph = wedges.glyph
wedges.nonselection_glyph = wedges.glyph

# Create layout
layout = column(breadcrumb, p)

# Save HTML with full interactivity
save(layout, filename="plot.html", resources=INLINE, title="pie-drilldown · bokeh · pyplots.ai")

# Export static PNG (shows initial state)
export_png(p, filename="plot.png")
