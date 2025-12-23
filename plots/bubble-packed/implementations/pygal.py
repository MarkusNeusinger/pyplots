"""pyplots.ai
bubble-packed: Basic Packed Bubble Chart
Library: pygal | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import math

import pygal
from pygal.etree import etree
from pygal.style import Style


# Data - Department budget allocation (values determine circle size)
data = [
    {"label": "Software Development", "value": 450, "group": "Technology"},
    {"label": "Cloud Infrastructure", "value": 280, "group": "Technology"},
    {"label": "Data Analytics", "value": 180, "group": "Technology"},
    {"label": "Security", "value": 120, "group": "Technology"},
    {"label": "Digital Marketing", "value": 350, "group": "Marketing"},
    {"label": "Brand & Creative", "value": 220, "group": "Marketing"},
    {"label": "Events", "value": 150, "group": "Marketing"},
    {"label": "PR", "value": 90, "group": "Marketing"},
    {"label": "Facilities", "value": 280, "group": "Operations"},
    {"label": "HR & Recruiting", "value": 200, "group": "Operations"},
    {"label": "Legal", "value": 160, "group": "Operations"},
    {"label": "Admin", "value": 100, "group": "Operations"},
    {"label": "Enterprise", "value": 380, "group": "Sales"},
    {"label": "SMB", "value": 250, "group": "Sales"},
    {"label": "Partners", "value": 170, "group": "Sales"},
    {"label": "Support", "value": 110, "group": "Sales"},
]

# Chart dimensions
WIDTH = 4800
HEIGHT = 2700
PADDING = 15

# Group colors matching pyplots style
GROUP_COLORS = {"Technology": "#306998", "Marketing": "#FFD43B", "Operations": "#4ECDC4", "Sales": "#FF6B6B"}

# Scale values to radii (by area for accurate visual perception)
max_val = max(item["value"] for item in data)
max_radius = min(WIDTH, HEIGHT) * 0.11

circles = []
for item in data:
    r = math.sqrt(item["value"] / max_val) * max_radius
    circles.append({"r": r, "item": item, "x": 0, "y": 0})

# Sort by radius descending for better packing
circles.sort(key=lambda c: -c["r"])

# Place first circle at center
cx, cy = WIDTH / 2, HEIGHT / 2
circles[0]["x"] = cx
circles[0]["y"] = cy
placed = [circles[0]]

# Place remaining circles using greedy packing
for circle in circles[1:]:
    best_pos = None
    min_dist_from_center = float("inf")

    # Try placing adjacent to each existing circle
    for existing in placed:
        for angle_deg in range(0, 360, 8):
            angle = math.radians(angle_deg)
            dist = existing["r"] + circle["r"] + PADDING
            nx = existing["x"] + math.cos(angle) * dist
            ny = existing["y"] + math.sin(angle) * dist

            # Check for overlaps
            valid = True
            for other in placed:
                dx = nx - other["x"]
                dy = ny - other["y"]
                min_gap = circle["r"] + other["r"] + PADDING * 0.5
                if math.sqrt(dx * dx + dy * dy) < min_gap:
                    valid = False
                    break

            if valid:
                d = math.sqrt((nx - cx) ** 2 + (ny - cy) ** 2)
                if d < min_dist_from_center:
                    min_dist_from_center = d
                    best_pos = (nx, ny)

    if best_pos:
        circle["x"], circle["y"] = best_pos
    else:
        circle["x"] = cx
        circle["y"] = max(c["y"] + c["r"] for c in placed) + circle["r"] + PADDING

    placed.append(circle)

# Prepare packed data for rendering
packed = [(c["x"], c["y"], c["r"], c["item"]) for c in placed]

# Custom style
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333",
    foreground_strong="#333",
    foreground_subtle="#666",
    colors=list(GROUP_COLORS.values()),
    title_font_size=72,
    legend_font_size=42,
)

# Create base chart (Pie with no data, just for structure)
chart = pygal.Pie(
    width=WIDTH,
    height=HEIGHT,
    style=custom_style,
    title="bubble-packed · pygal · pyplots.ai",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=4,
    inner_radius=0,
    margin=100,
)

# Add legend entries (empty slices just for legend)
for group in ["Technology", "Marketing", "Operations", "Sales"]:
    chart.add(group, [])


# XML filter to add packed bubbles to SVG
def add_packed_bubbles(root):
    g = etree.SubElement(root, "g")
    g.set("class", "packed-bubbles")

    for x, y, r, item in packed:
        color = GROUP_COLORS[item["group"]]

        # Circle element
        circle_elem = etree.SubElement(g, "circle")
        circle_elem.set("cx", f"{x:.1f}")
        circle_elem.set("cy", f"{y:.1f}")
        circle_elem.set("r", f"{r:.1f}")
        circle_elem.set("fill", color)
        circle_elem.set("fill-opacity", "0.85")
        circle_elem.set("stroke", "#333")
        circle_elem.set("stroke-width", "3")

        # Tooltip
        title = etree.SubElement(circle_elem, "title")
        title.text = f"{item['label']}: ${item['value']}K"

        # Value label for large circles
        if r > 80:
            text = etree.SubElement(g, "text")
            text.set("x", f"{x:.1f}")
            text.set("y", f"{y:.1f}")
            text.set("text-anchor", "middle")
            text.set("dominant-baseline", "middle")
            text.set("fill", "white")
            text.set("font-size", f"{int(r * 0.32)}")
            text.set("font-family", "sans-serif")
            text.set("font-weight", "bold")
            text.text = f"${item['value']}K"

    return root


chart.add_xml_filter(add_packed_bubbles)

# Render and save
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
