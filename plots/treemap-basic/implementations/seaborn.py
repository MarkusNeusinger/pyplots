""" pyplots.ai
treemap-basic: Basic Treemap
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 85/100 | Created: 2025-12-24
"""

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch, Rectangle


# Set seaborn style for clean aesthetics
sns.set_style("white")

# Data - Budget allocation by department and project (sorted by value descending)
data = [
    ("Engineering", "Product Dev", 45),
    ("Sales", "Enterprise", 35),
    ("Marketing", "Digital", 30),
    ("Engineering", "Infrastructure", 25),
    ("Sales", "SMB", 25),
    ("Marketing", "Events", 20),
    ("Operations", "Logistics", 20),
    ("Engineering", "QA", 15),
    ("Sales", "Partners", 15),
    ("Operations", "Support", 15),
    ("HR", "Recruiting", 12),
    ("HR", "Training", 8),
]

categories = [d[0] for d in data]
subcategories = [d[1] for d in data]
values = [d[2] for d in data]

# Use seaborn color palette for main categories
unique_categories = ["Engineering", "Sales", "Marketing", "Operations", "HR"]
palette = sns.color_palette("colorblind", n_colors=len(unique_categories))
category_colors = dict(zip(unique_categories, palette, strict=True))

# Normalize values to fill a 160x90 area (matching figsize aspect ratio)
total = sum(values)
width, height = 160, 90
normalized = [v / total * width * height for v in values]

# Squarify algorithm - compute rectangle positions
rects = []
remaining = list(zip(normalized, range(len(normalized)), strict=True))
x, y, w, h = 0, 0, width, height

while remaining:
    strip_items = []
    strip_area = 0

    if w >= h:
        # Vertical strip
        for area, idx in remaining:
            strip_items.append((area, idx))
            strip_area += area
            strip_width = strip_area / h
            if len(strip_items) > 1:
                aspects = [
                    max(strip_width / (a / strip_width), (a / strip_width) / strip_width) for a, _ in strip_items
                ]
                prev_area = strip_area - area
                if prev_area > 0:
                    prev_width = prev_area / h
                    prev_aspects = [
                        max(prev_width / (a / prev_width), (a / prev_width) / prev_width) for a, _ in strip_items[:-1]
                    ]
                    if max(aspects) > max(prev_aspects):
                        strip_items.pop()
                        strip_area -= area
                        break
        strip_width = strip_area / h if h > 0 else 0
        cy = y
        for area, idx in strip_items:
            rect_h = area / strip_width if strip_width > 0 else 0
            rects.append((x, cy, strip_width, rect_h, idx))
            cy += rect_h
        x += strip_width
        w -= strip_width
    else:
        # Horizontal strip
        for area, idx in remaining:
            strip_items.append((area, idx))
            strip_area += area
            strip_height = strip_area / w
            if len(strip_items) > 1:
                aspects = [
                    max(strip_height / (a / strip_height), (a / strip_height) / strip_height) for a, _ in strip_items
                ]
                prev_area = strip_area - area
                if prev_area > 0:
                    prev_height = prev_area / w
                    prev_aspects = [
                        max(prev_height / (a / prev_height), (a / prev_height) / prev_height)
                        for a, _ in strip_items[:-1]
                    ]
                    if max(aspects) > max(prev_aspects):
                        strip_items.pop()
                        strip_area -= area
                        break
        strip_height = strip_area / w if w > 0 else 0
        cx = x
        for area, idx in strip_items:
            rect_w = area / strip_height if strip_height > 0 else 0
            rects.append((cx, y, rect_w, strip_height, idx))
            cx += rect_w
        y += strip_height
        h -= strip_height

    placed_indices = {idx for _, idx in strip_items}
    remaining = [(a, i) for a, i in remaining if i not in placed_indices]

# Create plot (4800x2700 px at 300 dpi)
fig, ax = plt.subplots(figsize=(16, 9))

# Draw rectangles
for rx, ry, rw, rh, idx in rects:
    color = category_colors[categories[idx]]
    rect = Rectangle((rx, ry), rw, rh, facecolor=color, edgecolor="white", linewidth=3, alpha=0.85)
    ax.add_patch(rect)

    # Add label for larger rectangles
    area = rw * rh
    if area > 150:
        # Determine text color based on luminance
        r_val, g_val, b_val = color[:3]
        luminance = 0.299 * r_val + 0.587 * g_val + 0.114 * b_val
        text_color = "white" if luminance < 0.5 else "black"
        fontsize = min(18, max(12, int(area**0.35)))

        label = f"{subcategories[idx]}\n${values[idx]}M"
        ax.text(
            rx + rw / 2,
            ry + rh / 2,
            label,
            ha="center",
            va="center",
            fontsize=fontsize,
            fontweight="bold",
            color=text_color,
        )

# Set axis limits and remove axes
ax.set_xlim(0, width)
ax.set_ylim(0, height)
ax.axis("off")
ax.set_aspect("equal")

# Title
ax.set_title(
    "Budget Allocation by Department · treemap-basic · seaborn · pyplots.ai", fontsize=24, fontweight="bold", pad=20
)

# Legend for categories using seaborn palette colors
legend_handles = [Patch(facecolor=category_colors[cat], label=cat, edgecolor="white") for cat in unique_categories]
ax.legend(
    handles=legend_handles,
    loc="upper center",
    fontsize=14,
    framealpha=0.95,
    edgecolor="gray",
    ncol=5,
    bbox_to_anchor=(0.5, -0.02),
)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
