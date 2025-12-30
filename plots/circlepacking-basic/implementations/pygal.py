""" pyplots.ai
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
def calc_values(node):
    if node["value"] is not None:
        return node["value"]
    total = sum(calc_values(child) for child in node["children"])
    node["value"] = total
    return total


root = nodes["company"]
calc_values(root)

# Chart dimensions
WIDTH = 3600
HEIGHT = 3600
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2

# Colors by depth level
DEPTH_COLORS = [
    "#306998",  # Level 0 - root (Python Blue)
    "#4A90D9",  # Level 1 - departments
    "#FFD43B",  # Level 2 - teams (Python Yellow)
]

PADDING = 12


# Circle packing algorithm for children within a parent circle
def pack_circles(children, container_r, container_x, container_y):
    if not children:
        return []

    # Scale radii proportionally
    total_value = sum(c["value"] for c in children)
    usable_area = math.pi * (container_r * 0.85) ** 2
    scale = usable_area / (math.pi * total_value) * 0.6

    packed = []
    for child in sorted(children, key=lambda x: -x["value"]):
        r = math.sqrt(child["value"] * scale)
        packed.append({"node": child, "r": r, "x": 0, "y": 0})

    if len(packed) == 1:
        packed[0]["x"] = container_x
        packed[0]["y"] = container_y
        return packed

    # Place first circle at center
    packed[0]["x"] = container_x
    packed[0]["y"] = container_y
    placed = [packed[0]]

    # Place remaining circles
    for circle in packed[1:]:
        best_pos = None
        min_dist = float("inf")

        for existing in placed:
            for angle_deg in range(0, 360, 10):
                angle = math.radians(angle_deg)
                dist = existing["r"] + circle["r"] + PADDING
                nx = existing["x"] + math.cos(angle) * dist
                ny = existing["y"] + math.sin(angle) * dist

                # Check within container
                d_from_center = math.sqrt((nx - container_x) ** 2 + (ny - container_y) ** 2)
                if d_from_center + circle["r"] + PADDING > container_r * 0.92:
                    continue

                # Check overlaps
                valid = True
                for other in placed:
                    dx = nx - other["x"]
                    dy = ny - other["y"]
                    min_gap = circle["r"] + other["r"] + PADDING * 0.3
                    if math.sqrt(dx * dx + dy * dy) < min_gap:
                        valid = False
                        break

                if valid and d_from_center < min_dist:
                    min_dist = d_from_center
                    best_pos = (nx, ny)

        if best_pos:
            circle["x"], circle["y"] = best_pos
        else:
            # Fallback position
            circle["x"] = container_x
            circle["y"] = container_y
        placed.append(circle)

    return packed


# Generate all circles with positions
all_circles = []

# Root circle
root_r = min(WIDTH, HEIGHT) * 0.42
all_circles.append(
    {"x": CENTER_X, "y": CENTER_Y, "r": root_r, "label": root["label"], "value": root["value"], "depth": 0}
)

# Level 1 - departments
dept_packed = pack_circles(root["children"], root_r, CENTER_X, CENTER_Y)
for dept in dept_packed:
    node = dept["node"]
    all_circles.append(
        {"x": dept["x"], "y": dept["y"], "r": dept["r"], "label": node["label"], "value": node["value"], "depth": 1}
    )

    # Level 2 - teams within department
    team_packed = pack_circles(node["children"], dept["r"], dept["x"], dept["y"])
    for team in team_packed:
        team_node = team["node"]
        all_circles.append(
            {
                "x": team["x"],
                "y": team["y"],
                "r": team["r"],
                "label": team_node["label"],
                "value": team_node["value"],
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

# Create base chart
chart = pygal.Pie(
    width=WIDTH,
    height=HEIGHT,
    style=custom_style,
    title="circlepacking-basic \u00b7 pygal \u00b7 pyplots.ai",
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


# XML filter to add circle packing
def add_circle_packing(svg_root):
    g = etree.SubElement(svg_root, "g")
    g.set("class", "circle-packing")

    # Sort by depth (draw outer circles first)
    sorted_circles = sorted(all_circles, key=lambda c: c["depth"])

    for circle in sorted_circles:
        depth = circle["depth"]
        color = DEPTH_COLORS[depth]
        opacity = 0.3 if depth == 0 else (0.5 if depth == 1 else 0.85)

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

        # Label for larger circles
        min_label_r = 40 if depth == 2 else 80
        if circle["r"] > min_label_r:
            # Label text
            text = etree.SubElement(g, "text")
            text.set("x", f"{circle['x']:.1f}")
            y_offset = 0 if depth == 2 else -circle["r"] * 0.1
            text.set("y", f"{circle['y'] + y_offset:.1f}")
            text.set("text-anchor", "middle")
            text.set("dominant-baseline", "middle")
            text.set("fill", "#333" if depth < 2 else "white")
            font_size = int(min(circle["r"] * 0.4, 48 if depth == 2 else 56))
            text.set("font-size", str(font_size))
            text.set("font-family", "sans-serif")
            text.set("font-weight", "bold")
            text.text = circle["label"]

            # Value text for leaf nodes
            if depth == 2 and circle["r"] > 55:
                val_text = etree.SubElement(g, "text")
                val_text.set("x", f"{circle['x']:.1f}")
                val_text.set("y", f"{circle['y'] + font_size * 0.9:.1f}")
                val_text.set("text-anchor", "middle")
                val_text.set("dominant-baseline", "middle")
                val_text.set("fill", "white")
                val_text.set("font-size", str(int(font_size * 0.7)))
                val_text.set("font-family", "sans-serif")
                val_text.text = f"{circle['value']}"

    return svg_root


chart.add_xml_filter(add_circle_packing)

# Save
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
