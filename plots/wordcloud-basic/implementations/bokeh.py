"""
wordcloud-basic: Basic Word Cloud
Library: bokeh
"""

import numpy as np
from bokeh.io import export_png, output_file, save
from bokeh.models import ColumnDataSource, Text
from bokeh.plotting import figure


# Data: Technology terms with frequencies
np.random.seed(42)
words_data = [
    ("Python", 100),
    ("Data", 95),
    ("Machine", 90),
    ("Learning", 88),
    ("Analytics", 82),
    ("Visualization", 78),
    ("Statistics", 75),
    ("Algorithm", 72),
    ("Model", 68),
    ("Neural", 65),
    ("Network", 62),
    ("Cloud", 58),
    ("API", 55),
    ("Framework", 52),
    ("Library", 48),
    ("Code", 45),
    ("Science", 42),
    ("Analysis", 38),
    ("Deep", 35),
    ("Big", 32),
]

# Scale frequencies to font sizes (20-100 pt for 4800x2700 canvas)
min_freq = min(f for _, f in words_data)
max_freq = max(f for _, f in words_data)
min_size, max_size = 24, 100


def scale_size(freq):
    """Scale frequency to font size."""
    return int(min_size + (freq - min_freq) / (max_freq - min_freq) * (max_size - min_size))


# Canvas dimensions
canvas_width = 4800
canvas_height = 2700


def estimate_width(word, size):
    """Estimate word width for collision detection."""
    return len(word) * size * 0.65


def estimate_height(size):
    """Estimate word height for collision detection."""
    return size * 1.4


def boxes_overlap(box1, box2, padding=40):
    """Check if two boxes overlap with padding."""
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    return not (x1 + w1 + padding < x2 or x2 + w2 + padding < x1 or y1 + h1 + padding < y2 or y2 + h2 + padding < y1)


def find_position(word, size, placed):
    """Find non-overlapping position using Archimedean spiral."""
    w = estimate_width(word, size)
    h = estimate_height(size)
    cx, cy = canvas_width / 2, canvas_height / 2

    # Spiral placement - wider spread for better distribution
    angle = 0
    radius = 0

    for _ in range(10000):
        # Elliptical spiral to match 16:9 aspect ratio
        x = cx + radius * 1.5 * np.cos(angle) - w / 2
        y = cy + radius * np.sin(angle) - h / 2

        # Check bounds
        if 150 < x < canvas_width - w - 150 and 250 < y < canvas_height - h - 250:
            box = (x, y, w, h)
            if not any(boxes_overlap(box, pb) for pb in placed):
                return x + w / 2, y + h / 2, box

        angle += 0.2
        radius += 2.5

    # Fallback
    return cx, cy, (cx - w / 2, cy - h / 2, w, h)


# Build word positions
words = []
x_pos = []
y_pos = []
sizes = []
colors = []
placed_boxes = []

for i, (word, freq) in enumerate(words_data):
    size = scale_size(freq)
    x, y, box = find_position(word, size, placed_boxes)
    placed_boxes.append(box)

    words.append(word)
    x_pos.append(x)
    y_pos.append(y)
    sizes.append(f"{size}pt")
    # Alternate between Python Blue and Python Yellow
    colors.append("#306998" if i % 2 == 0 else "#FFD43B")

# Create Bokeh figure
p = figure(
    width=4800,
    height=2700,
    title="wordcloud-basic \u00b7 bokeh \u00b7 pyplots.ai",
    x_range=(0, canvas_width),
    y_range=(0, canvas_height),
    tools="",
    toolbar_location=None,
)

# Clean appearance - no axes or grid
p.axis.visible = False
p.grid.visible = False
p.outline_line_color = None

# Style title
p.title.text_font_size = "36pt"
p.title.align = "center"

# Add words as text glyphs
source = ColumnDataSource(data={"x": x_pos, "y": y_pos, "text": words, "text_font_size": sizes, "text_color": colors})

text_glyph = Text(
    x="x",
    y="y",
    text="text",
    text_font_size="text_font_size",
    text_color="text_color",
    text_align="center",
    text_baseline="middle",
    text_font_style="bold",
)

p.add_glyph(source, text_glyph)

# Light background
p.background_fill_color = "#FAFAFA"

# Save outputs
export_png(p, filename="plot.png")
output_file("plot.html")
save(p)
