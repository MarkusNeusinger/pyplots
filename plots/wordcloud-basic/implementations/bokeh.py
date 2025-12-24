"""pyplots.ai
wordcloud-basic: Basic Word Cloud
Library: bokeh | Python 3.13
Quality: pending | Created: 2025-12-24
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

# Canvas dimensions
canvas_width = 4800
canvas_height = 2700

# Scale frequencies to font sizes (24-100 pt for 4800x2700 canvas)
min_freq = min(f for _, f in words_data)
max_freq = max(f for _, f in words_data)
min_size, max_size = 24, 100

# Build word positions using Archimedean spiral placement
words = []
x_pos = []
y_pos = []
sizes = []
colors = []
placed_boxes = []

for i, (word, freq) in enumerate(words_data):
    # Scale frequency to font size
    size = int(min_size + (freq - min_freq) / (max_freq - min_freq) * (max_size - min_size))

    # Estimate word dimensions for collision detection
    word_width = len(word) * size * 0.65
    word_height = size * 1.4

    # Find non-overlapping position using Archimedean spiral
    cx, cy = canvas_width / 2, canvas_height / 2
    angle = 0
    radius = 0
    padding = 40
    found_x, found_y = cx, cy
    found_box = (cx - word_width / 2, cy - word_height / 2, word_width, word_height)

    for _ in range(10000):
        # Elliptical spiral to match 16:9 aspect ratio
        test_x = cx + radius * 1.5 * np.cos(angle) - word_width / 2
        test_y = cy + radius * np.sin(angle) - word_height / 2

        # Check bounds
        if 150 < test_x < canvas_width - word_width - 150 and 250 < test_y < canvas_height - word_height - 250:
            test_box = (test_x, test_y, word_width, word_height)

            # Check for overlaps with placed words
            overlap = False
            for pb in placed_boxes:
                px, py, pw, ph = pb
                if not (
                    test_x + word_width + padding < px
                    or px + pw + padding < test_x
                    or test_y + word_height + padding < py
                    or py + ph + padding < test_y
                ):
                    overlap = True
                    break

            if not overlap:
                found_x = test_x + word_width / 2
                found_y = test_y + word_height / 2
                found_box = test_box
                break

        angle += 0.2
        radius += 2.5

    placed_boxes.append(found_box)
    words.append(word)
    x_pos.append(found_x)
    y_pos.append(found_y)
    sizes.append(f"{size}pt")
    # Alternate between Python Blue and Python Yellow
    colors.append("#306998" if i % 2 == 0 else "#FFD43B")

# Create Bokeh figure
p = figure(
    width=4800,
    height=2700,
    title="wordcloud-basic · bokeh · pyplots.ai",
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
