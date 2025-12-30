"""pyplots.ai
circlepacking-basic: Circle Packing Chart
Library: pygal 3.1.0 | Python 3.13.11
Quality: 38/100 | Created: 2025-12-30
"""

import math

import pygal
from pygal.etree import etree
from pygal.style import Style


# Hierarchical data - Company structure with headcount per team
# Format: (id, parent, value, label)
hierarchy = [
    ("company", None, None, "TechCorp"),
    ("eng", "company", None, "Engineering"),
    ("mkt", "company", None, "Marketing"),
    ("ops", "company", None, "Operations"),
    ("sales", "company", None, "Sales"),
    ("eng-backend", "eng", 45, "Backend"),
    ("eng-frontend", "eng", 38, "Frontend"),
    ("eng-data", "eng", 28, "Data"),
    ("eng-devops", "eng", 18, "DevOps"),
    ("eng-qa", "eng", 15, "QA"),
    ("mkt-digital", "mkt", 22, "Digital"),
    ("mkt-brand", "mkt", 16, "Brand"),
    ("mkt-content", "mkt", 12, "Content"),
    ("mkt-events", "mkt", 8, "Events"),
    ("ops-hr", "ops", 18, "HR"),
    ("ops-finance", "ops", 14, "Finance"),
    ("ops-facilities", "ops", 10, "Facilities"),
    ("ops-legal", "ops", 6, "Legal"),
    ("sales-enterprise", "sales", 35, "Enterprise"),
    ("sales-smb", "sales", 25, "SMB"),
    ("sales-partners", "sales", 15, "Partners"),
    ("sales-support", "sales", 12, "Support"),
]

# Build tree structure
nodes = {}
for id_, parent, value, label in hierarchy:
    nodes[id_] = {"id": id_, "parent": parent, "value": value, "label": label, "children": []}

for node in nodes.values():
    if node["parent"] and node["parent"] in nodes:
        nodes[node["parent"]]["children"].append(node)

# Calculate values for parent nodes (sum of children)
stack = [nodes["company"]]
order = []
while stack:
    n = stack.pop()
    order.append(n)
    stack.extend(n["children"])
for n in reversed(order):
    if n["value"] is None:
        n["value"] = sum(c["value"] for c in n["children"])

root = nodes["company"]

# Chart dimensions (square for circle packing)
WIDTH = 3600
HEIGHT = 3600
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2

# Colors by depth level (colorblind-safe)
DEPTH_COLORS = [
    "#306998",  # Level 0 - root (Python Blue)
    "#4A90D9",  # Level 1 - departments (lighter blue)
    "#FFD43B",  # Level 2 - teams (Python Yellow)
]

# Padding between circles
PADDING = 8

# All circles to draw
all_circles = []

# Root circle
root_r = min(WIDTH, HEIGHT) * 0.44
all_circles.append(
    {"x": CENTER_X, "y": CENTER_Y, "r": root_r, "label": root["label"], "value": root["value"], "depth": 0}
)

# Calculate department positions around center (arranged in a ring)
departments = root["children"]
n_depts = len(departments)
total_dept_value = sum(d["value"] for d in departments)

# Calculate radii for each department based on value (area-proportional)
dept_total_area = math.pi * (root_r * 0.7) ** 2  # Use 70% of root for departments
dept_radii = []
for dept in departments:
    dept_area = dept_total_area * (dept["value"] / total_dept_value)
    dept_radii.append(math.sqrt(dept_area / math.pi))

# Position departments in a ring around center
dept_ring_radius = root_r * 0.42
dept_circles = []
for i, dept in enumerate(departments):
    angle = (2 * math.pi * i / n_depts) - math.pi / 2  # Start from top
    r = dept_radii[i]
    x = CENTER_X + dept_ring_radius * math.cos(angle)
    y = CENTER_Y + dept_ring_radius * math.sin(angle)
    dept_circles.append({"node": dept, "x": x, "y": y, "r": r})
    all_circles.append({"x": x, "y": y, "r": r, "label": dept["label"], "value": dept["value"], "depth": 1})

# Pack teams within each department
for dc in dept_circles:
    dept = dc["node"]
    teams = dept["children"]
    if not teams:
        continue

    dept_x, dept_y, dept_r = dc["x"], dc["y"], dc["r"]

    # Calculate team radii (area-proportional to value)
    total_team_value = sum(t["value"] for t in teams)
    team_usable_area = math.pi * (dept_r * 0.82) ** 2
    team_circles = []
    for team in sorted(teams, key=lambda t: -t["value"]):
        team_area = team_usable_area * (team["value"] / total_team_value)
        tr = math.sqrt(team_area / math.pi)
        team_circles.append({"node": team, "r": tr, "x": 0, "y": 0})

    # Place teams using simple circular arrangement within department
    n_teams = len(team_circles)
    if n_teams == 1:
        team_circles[0]["x"] = dept_x
        team_circles[0]["y"] = dept_y
    else:
        # Calculate ring radius that keeps teams inside department
        max_team_r = max(tc["r"] for tc in team_circles)
        team_ring_r = dept_r - max_team_r - PADDING

        for i, tc in enumerate(team_circles):
            angle = (2 * math.pi * i / n_teams) - math.pi / 2
            tc["x"] = dept_x + team_ring_r * 0.5 * math.cos(angle)
            tc["y"] = dept_y + team_ring_r * 0.5 * math.sin(angle)

    # Add team circles to all_circles
    for tc in team_circles:
        all_circles.append(
            {
                "x": tc["x"],
                "y": tc["y"],
                "r": tc["r"],
                "label": tc["node"]["label"],
                "value": tc["node"]["value"],
                "depth": 2,
            }
        )

# Custom style
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333",
    foreground_strong="#333",
    foreground_subtle="#666",
    colors=DEPTH_COLORS,
    title_font_size=72,
    legend_font_size=48,
)

# Create base chart (using Pie as canvas with XML filter for circles)
chart = pygal.Pie(
    width=WIDTH,
    height=HEIGHT,
    style=custom_style,
    title="circlepacking-basic · pygal · pyplots.ai",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=3,
    inner_radius=0,
    margin=80,
)

# Add legend entries
chart.add("Company (Root)", [])
chart.add("Departments", [])
chart.add("Teams", [])


# XML filter to render circle packing
circles_data = all_circles  # Capture for closure


def add_circle_packing_filter(svg_root):
    g = etree.SubElement(svg_root, "g")
    g.set("class", "circle-packing")

    # Sort by depth (draw outer circles first, then inner)
    sorted_circles = sorted(circles_data, key=lambda c: c["depth"])

    for circle in sorted_circles:
        depth = circle["depth"]
        color = DEPTH_COLORS[depth]
        opacity = 0.25 if depth == 0 else (0.45 if depth == 1 else 0.9)

        # Circle element
        elem = etree.SubElement(g, "circle")
        elem.set("cx", f"{circle['x']:.1f}")
        elem.set("cy", f"{circle['y']:.1f}")
        elem.set("r", f"{circle['r']:.1f}")
        elem.set("fill", color)
        elem.set("fill-opacity", str(opacity))
        elem.set("stroke", "#333")
        elem.set("stroke-width", "3" if depth < 2 else "2")

        # Tooltip
        title = etree.SubElement(elem, "title")
        title.text = f"{circle['label']}: {circle['value']} people"

        # Label for circles
        min_label_r = 35 if depth == 2 else 70
        if circle["r"] > min_label_r:
            text = etree.SubElement(g, "text")
            text.set("x", f"{circle['x']:.1f}")
            y_offset = 0 if depth == 2 else -circle["r"] * 0.15
            text.set("y", f"{circle['y'] + y_offset:.1f}")
            text.set("text-anchor", "middle")
            text.set("dominant-baseline", "middle")
            text.set("fill", "#333" if depth < 2 else "#222")
            font_size = int(min(circle["r"] * 0.35, 44 if depth == 2 else 52))
            text.set("font-size", str(font_size))
            text.set("font-family", "sans-serif")
            text.set("font-weight", "bold")
            text.text = circle["label"]

            # Value text for leaf nodes
            if depth == 2 and circle["r"] > 50:
                val_text = etree.SubElement(g, "text")
                val_text.set("x", f"{circle['x']:.1f}")
                val_text.set("y", f"{circle['y'] + font_size * 0.85:.1f}")
                val_text.set("text-anchor", "middle")
                val_text.set("dominant-baseline", "middle")
                val_text.set("fill", "#444")
                val_text.set("font-size", str(int(font_size * 0.7)))
                val_text.set("font-family", "sans-serif")
                val_text.text = f"{circle['value']}"

    return svg_root


chart.add_xml_filter(add_circle_packing_filter)

# Save
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
