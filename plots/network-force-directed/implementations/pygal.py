"""
network-force-directed: Force-Directed Graph
Library: pygal

Note: pygal does not have native network graph support.
This implementation creates a force-directed graph using custom SVG generation
with cairosvg for PNG export, following pygal's visual style.
"""

import math
import random

import cairosvg


# Data - Social network representing a small community
# Each node has an id, label, and optional group
random.seed(42)

nodes = [
    {"id": 0, "label": "Alice", "group": 0},
    {"id": 1, "label": "Bob", "group": 0},
    {"id": 2, "label": "Carol", "group": 0},
    {"id": 3, "label": "Dave", "group": 1},
    {"id": 4, "label": "Eve", "group": 1},
    {"id": 5, "label": "Frank", "group": 1},
    {"id": 6, "label": "Grace", "group": 1},
    {"id": 7, "label": "Henry", "group": 2},
    {"id": 8, "label": "Ivy", "group": 2},
    {"id": 9, "label": "Jack", "group": 2},
    {"id": 10, "label": "Kate", "group": 2},
    {"id": 11, "label": "Leo", "group": 2},
    {"id": 12, "label": "Mia", "group": 3},
    {"id": 13, "label": "Noah", "group": 3},
    {"id": 14, "label": "Olivia", "group": 3},
    {"id": 15, "label": "Pete", "group": 0},
    {"id": 16, "label": "Quinn", "group": 1},
    {"id": 17, "label": "Rose", "group": 2},
    {"id": 18, "label": "Sam", "group": 3},
    {"id": 19, "label": "Tina", "group": 3},
]

# Edges with source, target, and weight
edges = [
    # Group 0 internal (Community A)
    {"source": 0, "target": 1, "weight": 3},
    {"source": 0, "target": 2, "weight": 2},
    {"source": 1, "target": 2, "weight": 2},
    {"source": 0, "target": 15, "weight": 2},
    {"source": 1, "target": 15, "weight": 1},
    # Group 1 internal (Community B)
    {"source": 3, "target": 4, "weight": 3},
    {"source": 3, "target": 5, "weight": 2},
    {"source": 4, "target": 5, "weight": 2},
    {"source": 4, "target": 6, "weight": 2},
    {"source": 5, "target": 6, "weight": 1},
    {"source": 3, "target": 16, "weight": 2},
    {"source": 6, "target": 16, "weight": 1},
    # Group 2 internal (Community C)
    {"source": 7, "target": 8, "weight": 3},
    {"source": 7, "target": 9, "weight": 2},
    {"source": 8, "target": 9, "weight": 2},
    {"source": 8, "target": 10, "weight": 2},
    {"source": 9, "target": 10, "weight": 1},
    {"source": 10, "target": 11, "weight": 2},
    {"source": 7, "target": 17, "weight": 1},
    {"source": 11, "target": 17, "weight": 2},
    # Group 3 internal (Community D)
    {"source": 12, "target": 13, "weight": 3},
    {"source": 12, "target": 14, "weight": 2},
    {"source": 13, "target": 14, "weight": 2},
    {"source": 12, "target": 18, "weight": 2},
    {"source": 13, "target": 19, "weight": 2},
    {"source": 18, "target": 19, "weight": 1},
    # Bridge connections between communities
    {"source": 2, "target": 3, "weight": 1},  # A-B
    {"source": 15, "target": 4, "weight": 1},  # A-B
    {"source": 6, "target": 7, "weight": 1},  # B-C
    {"source": 16, "target": 9, "weight": 1},  # B-C
    {"source": 11, "target": 12, "weight": 1},  # C-D
    {"source": 17, "target": 14, "weight": 1},  # C-D
    {"source": 0, "target": 13, "weight": 1},  # A-D (long bridge)
]

# Canvas dimensions (4800x2700 px as per spec)
width = 4800
height = 2700
cx = width / 2
cy = height / 2 + 50

# Colors for groups - Python colors first, then complementary
group_colors = {
    0: "#306998",  # Python Blue
    1: "#FFD43B",  # Python Yellow
    2: "#4ECDC4",  # Teal
    3: "#FF6B6B",  # Coral
}

# Calculate node degrees (number of connections)
node_degrees = {n["id"]: 0 for n in nodes}
for edge in edges:
    node_degrees[edge["source"]] += 1
    node_degrees[edge["target"]] += 1

# Initialize node positions randomly in center area
positions = {}
for node in nodes:
    positions[node["id"]] = {"x": cx + random.uniform(-800, 800), "y": cy + random.uniform(-500, 500)}

# Force-directed layout parameters
repulsion_strength = 250000
attraction_strength = 0.015
damping = 0.85
min_distance = 180
iterations = 500

# Create adjacency lookup for faster edge checks
adjacency = {n["id"]: set() for n in nodes}
for edge in edges:
    adjacency[edge["source"]].add(edge["target"])
    adjacency[edge["target"]].add(edge["source"])

# Run force-directed simulation
for _iteration in range(iterations):
    forces = {n["id"]: {"fx": 0, "fy": 0} for n in nodes}

    # Repulsive forces between all node pairs
    for i, node1 in enumerate(nodes):
        for node2 in nodes[i + 1 :]:
            id1, id2 = node1["id"], node2["id"]
            dx = positions[id1]["x"] - positions[id2]["x"]
            dy = positions[id1]["y"] - positions[id2]["y"]
            dist = math.sqrt(dx * dx + dy * dy)
            dist = max(dist, min_distance)

            # Repulsion force
            force = repulsion_strength / (dist * dist)
            fx = (dx / dist) * force
            fy = (dy / dist) * force

            forces[id1]["fx"] += fx
            forces[id1]["fy"] += fy
            forces[id2]["fx"] -= fx
            forces[id2]["fy"] -= fy

    # Attractive forces along edges
    for edge in edges:
        id1, id2 = edge["source"], edge["target"]
        dx = positions[id2]["x"] - positions[id1]["x"]
        dy = positions[id2]["y"] - positions[id1]["y"]
        dist = math.sqrt(dx * dx + dy * dy)
        dist = max(dist, 1)

        # Attraction force (stronger for higher weight)
        force = attraction_strength * dist * edge["weight"]
        fx = (dx / dist) * force
        fy = (dy / dist) * force

        forces[id1]["fx"] += fx
        forces[id1]["fy"] += fy
        forces[id2]["fx"] -= fx
        forces[id2]["fy"] -= fy

    # Center gravity to prevent drift
    for node in nodes:
        nid = node["id"]
        dx = cx - positions[nid]["x"]
        dy = cy - positions[nid]["y"]
        forces[nid]["fx"] += dx * 0.01
        forces[nid]["fy"] += dy * 0.01

    # Apply forces with damping
    for node in nodes:
        nid = node["id"]
        positions[nid]["x"] += forces[nid]["fx"] * damping
        positions[nid]["y"] += forces[nid]["fy"] * damping

        # Keep nodes within bounds
        margin = 250
        positions[nid]["x"] = max(margin, min(width - margin, positions[nid]["x"]))
        positions[nid]["y"] = max(margin + 100, min(height - margin, positions[nid]["y"]))

# Build SVG content
svg_elements = []

# Title
title = "Social Network · network-force-directed · pygal · pyplots.ai"
svg_elements.append(
    f'<text x="{cx}" y="80" font-size="72" font-weight="bold" '
    f'text-anchor="middle" fill="#333333" font-family="Arial, sans-serif">{title}</text>'
)

# Draw edges first (behind nodes)
for edge in edges:
    x1 = positions[edge["source"]]["x"]
    y1 = positions[edge["source"]]["y"]
    x2 = positions[edge["target"]]["x"]
    y2 = positions[edge["target"]]["y"]

    # Edge thickness based on weight
    stroke_width = 2 + edge["weight"] * 1.5

    svg_elements.append(
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
        f'stroke="#999999" stroke-width="{stroke_width}" stroke-opacity="0.6"/>'
    )

# Draw nodes
for node in nodes:
    nid = node["id"]
    x = positions[nid]["x"]
    y = positions[nid]["y"]
    color = group_colors[node["group"]]

    # Node size based on degree (number of connections)
    base_radius = 25
    radius = base_radius + node_degrees[nid] * 5

    # Node circle with border
    svg_elements.append(f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{color}" stroke="white" stroke-width="4"/>')

    # Node label
    svg_elements.append(
        f'<text x="{x}" y="{y + radius + 35}" font-size="32" '
        f'text-anchor="middle" fill="#333333" font-family="Arial, sans-serif">{node["label"]}</text>'
    )

# Add legend
legend_x = 150
legend_y = height - 300
group_names = {0: "Community A", 1: "Community B", 2: "Community C", 3: "Community D"}

svg_elements.append(
    f'<text x="{legend_x}" y="{legend_y - 50}" font-size="42" font-weight="bold" '
    f'fill="#333333" font-family="Arial, sans-serif">Communities</text>'
)

for i, (group_id, group_name) in enumerate(group_names.items()):
    y_pos = legend_y + i * 55
    color = group_colors[group_id]
    svg_elements.append(f'<circle cx="{legend_x + 18}" cy="{y_pos}" r="18" fill="{color}"/>')
    svg_elements.append(
        f'<text x="{legend_x + 50}" y="{y_pos + 10}" font-size="36" '
        f'fill="#333333" font-family="Arial, sans-serif">{group_name}</text>'
    )

# Add note about node sizes
svg_elements.append(
    f'<text x="{width - 150}" y="{height - 80}" font-size="32" '
    f'text-anchor="end" fill="#666666" font-family="Arial, sans-serif" font-style="italic">'
    f"Node size reflects number of connections</text>"
)

# Assemble full SVG
svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="white"/>
  {"".join(svg_elements)}
</svg>'''

# Save as HTML for interactive viewing
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>network-force-directed · pygal · pyplots.ai</title>
    <style>
        body {{ margin: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; background: #f5f5f5; }}
        svg {{ max-width: 100%; height: auto; background: white; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
    </style>
</head>
<body>
{svg_content}
</body>
</html>"""

with open("plot.html", "w") as f:
    f.write(html_content)

# Convert to PNG using cairosvg
cairosvg.svg2png(bytestring=svg_content.encode("utf-8"), write_to="plot.png", output_width=width, output_height=height)
