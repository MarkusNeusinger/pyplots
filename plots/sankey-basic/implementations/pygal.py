""" pyplots.ai
sankey-basic: Basic Sankey Diagram
Library: pygal 3.1.0 | Python 3.13.11
Quality: 87/100 | Created: 2025-12-14
"""

import cairosvg


# Data - Energy flow from sources to sectors
flows_data = [
    ("Coal", "Industrial", 35),
    ("Coal", "Residential", 15),
    ("Gas", "Industrial", 25),
    ("Gas", "Commercial", 20),
    ("Gas", "Residential", 15),
    ("Nuclear", "Commercial", 18),
    ("Nuclear", "Residential", 12),
    ("Renewables", "Commercial", 8),
    ("Renewables", "Residential", 12),
]

# Node definitions
sources = ["Coal", "Gas", "Nuclear", "Renewables"]
targets = ["Industrial", "Commercial", "Residential"]

# Colors - Python Blue as primary, then complementary colors
color_map = {"Coal": "#306998", "Gas": "#FFD43B", "Nuclear": "#4ECDC4", "Renewables": "#2ECC71"}

# Canvas dimensions (4800x2700 px as per spec)
width = 4800
height = 2700

# Layout parameters
margin_left = 400
margin_right = 400
margin_top = 200
margin_bottom = 150
node_width = 80
node_gap = 40

# Calculate total flows
source_totals = dict.fromkeys(sources, 0)
target_totals = dict.fromkeys(targets, 0)
for src, tgt, val in flows_data:
    source_totals[src] += val
    target_totals[tgt] += val

total_flow = sum(val for _, _, val in flows_data)

# Available height for nodes
available_height = height - margin_top - margin_bottom - (len(sources) - 1) * node_gap

# Calculate source node positions (left side)
source_positions = {}
current_y = margin_top
for src in sources:
    node_height = (source_totals[src] / total_flow) * available_height
    source_positions[src] = {"x": margin_left, "y": current_y, "height": node_height, "flow_offset": 0}
    current_y += node_height + node_gap

# Calculate target node positions (right side)
target_available_height = height - margin_top - margin_bottom - (len(targets) - 1) * node_gap
target_positions = {}
current_y = margin_top
for tgt in targets:
    node_height = (target_totals[tgt] / total_flow) * target_available_height
    target_positions[tgt] = {
        "x": width - margin_right - node_width,
        "y": current_y,
        "height": node_height,
        "flow_offset": 0,
    }
    current_y += node_height + node_gap


# Generate cubic bezier path for smooth flow
def create_flow_path(x1, y1_top, y1_bot, x2, y2_top, y2_bot):
    """Create a smooth curved flow path between two nodes."""
    cx1 = x1 + (x2 - x1) * 0.4
    cx2 = x1 + (x2 - x1) * 0.6
    path = f"M {x1} {y1_top} "
    path += f"C {cx1} {y1_top}, {cx2} {y2_top}, {x2} {y2_top} "
    path += f"L {x2} {y2_bot} "
    path += f"C {cx2} {y2_bot}, {cx1} {y1_bot}, {x1} {y1_bot} "
    path += "Z"
    return path


# Build SVG content
svg_elements = []

# Title
title = "Energy Flow · sankey-basic · pygal · pyplots.ai"
svg_elements.append(
    f'<text x="{width // 2}" y="80" font-size="72" font-weight="bold" '
    f'text-anchor="middle" fill="#333333" font-family="Arial, sans-serif">{title}</text>'
)

# Column labels
svg_elements.append(
    f'<text x="{margin_left + node_width // 2}" y="{height - 60}" font-size="48" '
    f'text-anchor="middle" fill="#555555" font-family="Arial, sans-serif" font-weight="bold">Sources</text>'
)
svg_elements.append(
    f'<text x="{width - margin_right - node_width // 2}" y="{height - 60}" font-size="48" '
    f'text-anchor="middle" fill="#555555" font-family="Arial, sans-serif" font-weight="bold">Sectors</text>'
)

# Draw flow paths first (so they appear behind nodes)
for src, tgt, val in flows_data:
    src_pos = source_positions[src]
    tgt_pos = target_positions[tgt]

    # Calculate flow height proportionally
    flow_height_src = (val / total_flow) * available_height
    flow_height_tgt = (val / total_flow) * target_available_height

    # Source connection points
    src_y_top = src_pos["y"] + src_pos["flow_offset"]
    src_y_bot = src_y_top + flow_height_src
    src_pos["flow_offset"] += flow_height_src

    # Target connection points
    tgt_y_top = tgt_pos["y"] + tgt_pos["flow_offset"]
    tgt_y_bot = tgt_y_top + flow_height_tgt
    tgt_pos["flow_offset"] += flow_height_tgt

    # Create flow path
    x1 = margin_left + node_width
    x2 = width - margin_right - node_width
    path = create_flow_path(x1, src_y_top, src_y_bot, x2, tgt_y_top, tgt_y_bot)

    color = color_map[src]
    svg_elements.append(f'<path d="{path}" fill="{color}" fill-opacity="0.5" stroke="none"/>')

# Draw source nodes and labels
for src in sources:
    pos = source_positions[src]
    x, y, h = pos["x"], pos["y"], pos["height"]
    color = color_map[src]

    # Node rectangle
    svg_elements.append(
        f'<rect x="{x}" y="{y}" width="{node_width}" height="{h}" fill="{color}" stroke="white" stroke-width="2"/>'
    )

    # Node label (left of node)
    label_y = y + h / 2
    svg_elements.append(
        f'<text x="{x - 20}" y="{label_y}" font-size="42" font-weight="bold" '
        f'text-anchor="end" dominant-baseline="middle" fill="#333333" font-family="Arial, sans-serif">{src}</text>'
    )

    # Value label (inside or near node)
    svg_elements.append(
        f'<text x="{x + node_width + 15}" y="{label_y}" font-size="36" '
        f'text-anchor="start" dominant-baseline="middle" fill="#666666" font-family="Arial, sans-serif">{source_totals[src]}</text>'
    )

# Draw target nodes and labels
for tgt in targets:
    pos = target_positions[tgt]
    x, y, h = pos["x"], pos["y"], pos["height"]

    # Node rectangle (gray for targets)
    svg_elements.append(
        f'<rect x="{x}" y="{y}" width="{node_width}" height="{h}" fill="#888888" stroke="white" stroke-width="2"/>'
    )

    # Node label (right of node)
    label_y = y + h / 2
    svg_elements.append(
        f'<text x="{x + node_width + 20}" y="{label_y}" font-size="42" font-weight="bold" '
        f'text-anchor="start" dominant-baseline="middle" fill="#333333" font-family="Arial, sans-serif">{tgt}</text>'
    )

    # Value label
    svg_elements.append(
        f'<text x="{x - 15}" y="{label_y}" font-size="36" '
        f'text-anchor="end" dominant-baseline="middle" fill="#666666" font-family="Arial, sans-serif">{target_totals[tgt]}</text>'
    )

# Assemble full SVG
svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="white"/>
  {"".join(svg_elements)}
</svg>'''

# Save SVG and PNG
with open("plot.svg", "w") as f:
    f.write(svg_content)

# Convert to PNG
cairosvg.svg2png(bytestring=svg_content.encode(), write_to="plot.png", output_width=width, output_height=height)

# Also save HTML for interactive viewing
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>sankey-basic · pygal · pyplots.ai</title>
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
