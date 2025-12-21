""" pyplots.ai
wordcloud-basic: Basic Word Cloud
Library: altair 6.0.0 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-16
"""

import altair as alt
import numpy as np
import pandas as pd


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

# Scale frequencies to font sizes (20-80 for Altair text marks)
min_freq = min(word_frequencies.values())
max_freq = max(word_frequencies.values())
min_size = 24
max_size = 80


def scale_size(freq):
    """Scale frequency to font size."""
    return int(min_size + (freq - min_freq) / (max_freq - min_freq) * (max_size - min_size))


def estimate_width(word, size):
    """Estimate word width for collision detection."""
    return len(word) * size * 0.6


def estimate_height(size):
    """Estimate word height for collision detection."""
    return size * 1.3


def boxes_overlap(box1, box2, padding=30):
    """Check if two boxes overlap with padding."""
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    return not (x1 + w1 + padding < x2 or x2 + w2 + padding < x1 or y1 + h1 + padding < y2 or y2 + h2 + padding < y1)


def find_position(word, size, placed, canvas_w=1600, canvas_h=900):
    """Find non-overlapping position using spiral algorithm."""
    w = estimate_width(word, size)
    h = estimate_height(size)
    cx, cy = canvas_w / 2, canvas_h / 2

    angle = 0
    radius = 0

    for _ in range(8000):
        # Elliptical spiral for 16:9 aspect ratio
        x = cx + radius * 1.6 * np.cos(angle) - w / 2
        y = cy + radius * np.sin(angle) - h / 2

        # Check bounds (leave margin for title and edges)
        if 50 < x < canvas_w - w - 50 and 80 < y < canvas_h - h - 50:
            box = (x, y, w, h)
            if not any(boxes_overlap(box, pb) for pb in placed):
                return x + w / 2, y + h / 2, box

        angle += 0.25
        radius += 2

    # Fallback position
    return cx, cy, (cx - w / 2, cy - h / 2, w, h)


# Build dataframe with positions
words_list = []
x_positions = []
y_positions = []
font_sizes = []
colors = []
placed_boxes = []

# Sort by frequency (largest first for better placement)
sorted_words = sorted(word_frequencies.items(), key=lambda x: x[1], reverse=True)

color_palette = ["#306998", "#FFD43B", "#4B8BBE", "#646464", "#3776AB", "#FFE873"]

for i, (word, freq) in enumerate(sorted_words):
    size = scale_size(freq)
    x, y, box = find_position(word, size, placed_boxes)
    placed_boxes.append(box)

    words_list.append(word)
    x_positions.append(x)
    y_positions.append(y)
    font_sizes.append(size)
    colors.append(color_palette[i % len(color_palette)])

# Create DataFrame
df = pd.DataFrame({"word": words_list, "x": x_positions, "y": y_positions, "size": font_sizes, "color": colors})

# Create Altair chart
chart = (
    alt.Chart(df)
    .mark_text(fontWeight="bold")
    .encode(
        x=alt.X("x:Q", scale=alt.Scale(domain=[0, 1600]), axis=None),
        y=alt.Y("y:Q", scale=alt.Scale(domain=[0, 900]), axis=None),
        text="word:N",
        size=alt.Size("size:Q", scale=None, legend=None),
        color=alt.Color("color:N", scale=None, legend=None),
    )
    .properties(
        width=1600, height=900, title=alt.Title("wordcloud-basic · altair · pyplots.ai", fontSize=28, anchor="middle")
    )
    .configure_view(strokeWidth=0)
)

# Save outputs
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
