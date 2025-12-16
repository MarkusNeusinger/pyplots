"""
wordcloud-basic: Basic Word Cloud
Library: pygal
"""

import xml.etree.ElementTree as ET

import numpy as np
import pygal
from pygal.style import Style


# Data: Tech industry buzzwords with frequencies
np.random.seed(42)
word_frequencies = {
    "Python": 100,
    "Data": 95,
    "Machine": 90,
    "Learning": 88,
    "Analytics": 82,
    "Cloud": 78,
    "API": 75,
    "DevOps": 72,
    "Docker": 68,
    "Security": 65,
    "Database": 62,
    "Kubernetes": 58,
    "AI": 55,
    "Automation": 52,
    "Microservices": 48,
    "Agile": 45,
    "Testing": 42,
    "Git": 38,
    "Linux": 35,
    "Scalability": 32,
    "AWS": 30,
    "React": 28,
    "Azure": 26,
    "Terraform": 24,
    "GraphQL": 22,
}

# Scale frequencies to font sizes
min_freq = min(word_frequencies.values())
max_freq = max(word_frequencies.values())
min_size = 40
max_size = 160


def scale_size(freq):
    """Scale frequency to font size."""
    return int(min_size + (freq - min_freq) / (max_freq - min_freq) * (max_size - min_size))


def estimate_width(word, size):
    """Estimate word width for collision detection."""
    return len(word) * size * 0.55


def estimate_height(size):
    """Estimate word height for collision detection."""
    return size * 1.2


def boxes_overlap(box1, box2, padding=40):
    """Check if two boxes overlap with padding."""
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    return not (x1 + w1 + padding < x2 or x2 + w2 + padding < x1 or y1 + h1 + padding < y2 or y2 + h2 + padding < y1)


def find_position(word, size, placed, canvas_w=4800, canvas_h=2700):
    """Find non-overlapping position using spiral algorithm."""
    w = estimate_width(word, size)
    h = estimate_height(size)
    cx, cy = canvas_w / 2, canvas_h / 2 + 50  # Offset down slightly for title

    angle = 0
    radius = 0

    for _ in range(10000):
        # Elliptical spiral for 16:9 aspect ratio
        x = cx + radius * 1.6 * np.cos(angle) - w / 2
        y = cy + radius * np.sin(angle) - h / 2

        # Check bounds (leave margin for edges and title)
        if 100 < x < canvas_w - w - 100 and 200 < y < canvas_h - h - 100:
            box = (x, y, w, h)
            if not any(boxes_overlap(box, pb) for pb in placed):
                return x + w / 2, y + h / 2, box

        angle += 0.2
        radius += 1.5

    # Fallback position
    return cx, cy, (cx - w / 2, cy - h / 2, w, h)


# Sort by frequency (largest first for better placement)
sorted_words = sorted(word_frequencies.items(), key=lambda x: x[1], reverse=True)

# Color palette based on pyplots primary colors
color_palette = ["#306998", "#FFD43B", "#4B8BBE", "#646464", "#3776AB", "#FFE873"]

# Build word positions
word_data = []
placed_boxes = []

for i, (word, freq) in enumerate(sorted_words):
    size = scale_size(freq)
    x, y, box = find_position(word, size, placed_boxes)
    placed_boxes.append(box)
    word_data.append({"word": word, "x": x, "y": y, "size": size, "color": color_palette[i % len(color_palette)]})


def add_word_cloud_elements(root):
    """Add word cloud text elements to the SVG root element."""
    # Add title
    title = ET.SubElement(root, "text")
    title.set("x", "2400")
    title.set("y", "100")
    title.set("font-size", "72")
    title.set("font-weight", "bold")
    title.set("fill", "#333")
    title.set("text-anchor", "middle")
    title.set("font-family", "sans-serif")
    title.text = "wordcloud-basic · pygal · pyplots.ai"

    # Add word cloud text elements
    for item in word_data:
        text_elem = ET.SubElement(root, "text")
        text_elem.set("x", str(int(item["x"])))
        text_elem.set("y", str(int(item["y"])))
        text_elem.set("font-size", str(item["size"]))
        text_elem.set("font-weight", "bold")
        text_elem.set("fill", item["color"])
        text_elem.set("text-anchor", "middle")
        text_elem.set("dominant-baseline", "middle")
        text_elem.set("font-family", "sans-serif")
        text_elem.text = item["word"]

    return root


# Create minimal chart as canvas
custom_style = Style(background="white", plot_background="white")

chart = pygal.XY(
    style=custom_style,
    width=4800,
    height=2700,
    show_legend=False,
    show_x_labels=False,
    show_y_labels=False,
    show_x_guides=False,
    show_y_guides=False,
    show_dots=False,
    stroke=False,
    margin=0,
)

# Add XML filter to inject word cloud elements
chart.add_xml_filter(add_word_cloud_elements)

# Add dummy data (required for chart to render)
chart.add("", [(0, 0)])

# Save outputs
chart.render_to_file("plot.svg")
chart.render_to_png("plot.png")

# Also save as HTML for interactive viewing
with open("plot.html", "w") as f:
    svg_content = chart.render(is_unicode=True)
    f.write(
        f"""<!DOCTYPE html>
<html>
<head>
    <title>wordcloud-basic · pygal · pyplots.ai</title>
    <style>
        body {{ margin: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; background: #f5f5f5; }}
        svg {{ max-width: 100%; height: auto; }}
    </style>
</head>
<body>
{svg_content}
</body>
</html>"""
    )
