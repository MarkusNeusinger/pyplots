"""pyplots.ai
circlepacking-basic: Circle Packing Chart
Library: pygal 3.1.0 | Python 3.13.11
Quality: 62/100 | Created: 2025-12-30
"""

import math

import cairosvg
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
PADDING = 12

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
dept_total_area = math.pi * (root_r * 0.65) ** 2  # Use 65% of root for departments
dept_radii = []
for dept in departments:
    dept_area = dept_total_area * (dept["value"] / total_dept_value)
    dept_radii.append(math.sqrt(dept_area / math.pi))

# Position departments in a ring around center
dept_ring_radius = root_r * 0.45
dept_circles = []
for i, dept in enumerate(departments):
    angle = (2 * math.pi * i / n_depts) - math.pi / 2  # Start from top
    r = dept_radii[i]
    x = CENTER_X + dept_ring_radius * math.cos(angle)
    y = CENTER_Y + dept_ring_radius * math.sin(angle)
    dept_circles.append({"node": dept, "x": x, "y": y, "r": r})
    all_circles.append({"x": x, "y": y, "r": r, "label": dept["label"], "value": dept["value"], "depth": 1})

# Pack teams within each department - scale to fit and arrange in ring
for dc in dept_circles:
    dept = dc["node"]
    teams = dept["children"]
    if not teams:
        continue

    dept_x, dept_y, dept_r = dc["x"], dc["y"], dc["r"]
    n_teams = len(teams)

    # Sort teams by value (largest first)
    sorted_teams = sorted(teams, key=lambda t: -t["value"])
    total_team_value = sum(t["value"] for t in teams)

    # Calculate scaling factor so all team circles fit inside department
    # Using a ring layout where teams are arranged around department center
    if n_teams == 1:
        # Single team - put at center with limited radius
        scale_r = dept_r * 0.6
        team_data = [{"node": sorted_teams[0], "r": scale_r, "x": dept_x, "y": dept_y}]
    else:
        # Multiple teams - arrange in a ring
        # First, calculate proportional radii
        max_single_r = dept_r * 0.35  # Max radius for any single team
        team_data = []
        for team in sorted_teams:
            # Area-proportional sizing with max limit
            proportion = team["value"] / total_team_value
            tr = min(max_single_r, dept_r * 0.5 * math.sqrt(proportion * n_teams / math.pi))
            team_data.append({"node": team, "r": tr, "x": 0.0, "y": 0.0})

        # Calculate ring radius that keeps all teams inside department
        max_team_r = max(td["r"] for td in team_data)
        ring_radius = dept_r - max_team_r - PADDING * 2

        # If ring too small, scale down all team radii
        if ring_radius < max_team_r:
            scale = (dept_r * 0.4) / max_team_r
            for td in team_data:
                td["r"] *= scale
            max_team_r = max(td["r"] for td in team_data)
            ring_radius = dept_r - max_team_r - PADDING * 2

        # Place teams around the ring
        for i, td in enumerate(team_data):
            angle = (2 * math.pi * i / n_teams) - math.pi / 2
            td["x"] = dept_x + ring_radius * 0.6 * math.cos(angle)
            td["y"] = dept_y + ring_radius * 0.6 * math.sin(angle)

    # Add team circles to all_circles
    for tc in team_data:
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

# Create base chart using Pie with dummy data (to enable legend and title rendering)
chart = pygal.Pie(
    width=WIDTH,
    height=HEIGHT,
    style=custom_style,
    title="circlepacking-basic · pygal · pyplots.ai",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=3,
    inner_radius=0.99,  # Nearly invisible inner ring - hides "No data" issue
    margin=80,
    print_values=False,
    print_labels=False,
)

# Add minimal dummy values to avoid "No data" text
chart.add("Company (Root)", [{"value": 0.001, "label": ""}])
chart.add("Departments", [{"value": 0.001, "label": ""}])
chart.add("Teams", [{"value": 0.001, "label": ""}])

# Store circle data for XML filter
circles_data = all_circles
depth_colors = DEPTH_COLORS

# Render SVG first to get the raw XML
svg_string = chart.render().decode("utf-8")
svg_root = etree.fromstring(svg_string.encode("utf-8"))

# Find the main graph group and add circle packing elements
g = etree.SubElement(svg_root, "g")
g.set("class", "circle-packing")

# Sort by depth (draw outer circles first, then inner)
sorted_circles = sorted(circles_data, key=lambda c: c["depth"])

for circle in sorted_circles:
    depth = circle["depth"]
    color = depth_colors[depth]
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

    # Labels: show dept labels above their circles, team labels inside
    if depth == 1:
        # Department label above the circle (outside child region)
        text = etree.SubElement(g, "text")
        text.set("x", f"{circle['x']:.1f}")
        text.set("y", f"{circle['y'] - circle['r'] - 15:.1f}")  # Above circle
        text.set("text-anchor", "middle")
        text.set("dominant-baseline", "auto")
        text.set("fill", "#222")
        text.set("font-size", "48")
        text.set("font-family", "sans-serif")
        text.set("font-weight", "bold")
        text.text = circle["label"]
    elif depth == 2 and circle["r"] > 40:
        # Team label inside circle
        text = etree.SubElement(g, "text")
        text.set("x", f"{circle['x']:.1f}")
        text.set("y", f"{circle['y']:.1f}")
        text.set("text-anchor", "middle")
        text.set("dominant-baseline", "middle")
        text.set("fill", "#222")
        font_size = int(min(circle["r"] * 0.4, 38))
        text.set("font-size", str(font_size))
        text.set("font-family", "sans-serif")
        text.set("font-weight", "bold")
        text.text = circle["label"]

        # Value text below label
        if circle["r"] > 55:
            val_text = etree.SubElement(g, "text")
            val_text.set("x", f"{circle['x']:.1f}")
            val_text.set("y", f"{circle['y'] + font_size * 0.9:.1f}")
            val_text.set("text-anchor", "middle")
            val_text.set("dominant-baseline", "middle")
            val_text.set("fill", "#444")
            val_text.set("font-size", str(int(font_size * 0.7)))
            val_text.set("font-family", "sans-serif")
            val_text.text = f"{circle['value']}"
    elif depth == 0:
        # Root label at center (visible through transparent circles)
        text = etree.SubElement(g, "text")
        text.set("x", f"{circle['x']:.1f}")
        text.set("y", f"{circle['y']:.1f}")
        text.set("text-anchor", "middle")
        text.set("dominant-baseline", "middle")
        text.set("fill", "#333")
        text.set("font-size", "56")
        text.set("font-family", "sans-serif")
        text.set("font-weight", "bold")
        text.set("opacity", "0.6")
        text.text = circle["label"]

# Hide any "No data" text by finding and removing it (using parent map since etree lacks getparent)
parent_map = {c: p for p in svg_root.iter() for c in p}
elements_to_remove = []
for elem in svg_root.iter():
    if elem.text and "No data" in str(elem.text):
        elements_to_remove.append(elem)
for elem in elements_to_remove:
    if elem in parent_map:
        parent_map[elem].remove(elem)

# Write modified SVG to file
svg_output = etree.tostring(svg_root, encoding="unicode")
with open("plot.html", "w") as f:
    f.write(svg_output)

# Render to PNG via cairosvg
cairosvg.svg2png(bytestring=svg_output.encode("utf-8"), write_to="plot.png")
