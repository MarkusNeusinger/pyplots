"""pyplots.ai
bubble-packed: Basic Packed Bubble Chart
Library: seaborn | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Data - Company market values by sector (billions USD)
np.random.seed(42)
data = {
    "Technology": [("Apple", 180), ("Microsoft", 160), ("Google", 120), ("NVIDIA", 95), ("Meta", 75)],
    "Finance": [("JPMorgan", 85), ("Visa", 70), ("Mastercard", 55), ("Goldman", 45)],
    "Healthcare": [("UnitedHealth", 90), ("J&J", 65), ("Merck", 50), ("Pfizer", 40)],
    "Retail": [("Amazon", 140), ("Walmart", 60), ("Costco", 45), ("Target", 30)],
}

# Prepare circles with group info, sorted by size (largest first for better packing)
all_circles = []
for group, items in data.items():
    for name, value in items:
        radius = np.sqrt(value) * 4  # Scale by area
        all_circles.append({"name": name, "radius": radius, "group": group, "value": value})

all_circles.sort(key=lambda x: -x["radius"])

# Set seaborn style and color palette
sns.set_style("white")
palette = sns.color_palette("Set2", n_colors=len(data))
group_colors = {group: palette[i] for i, group in enumerate(data.keys())}

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Circle packing using front-chain algorithm (place circles one by one)
placed_circles = []
cx, cy = 0, 0  # Start at origin, recenter later


def find_position(new_radius, placed, center):
    """Find position for new circle without overlap."""
    if not placed:
        return center[0], center[1]

    # Try positions around existing circles
    best_pos = None
    best_dist = float("inf")

    for p in placed:
        # Try multiple angles around each placed circle
        for angle in np.linspace(0, 2 * np.pi, 72, endpoint=False):
            dist = p["radius"] + new_radius + 2  # Small gap
            test_x = p["x"] + dist * np.cos(angle)
            test_y = p["y"] + dist * np.sin(angle)

            # Check overlap with all placed circles
            valid = True
            for other in placed:
                d = np.sqrt((test_x - other["x"]) ** 2 + (test_y - other["y"]) ** 2)
                if d < other["radius"] + new_radius + 1:
                    valid = False
                    break

            if valid:
                # Calculate distance from center (prefer closer to center)
                center_dist = np.sqrt((test_x - center[0]) ** 2 + (test_y - center[1]) ** 2)
                if center_dist < best_dist:
                    best_dist = center_dist
                    best_pos = (test_x, test_y)

    return best_pos if best_pos else (center[0] + np.random.randn() * 10, center[1] + np.random.randn() * 10)


# Place circles one by one
for circle in all_circles:
    x, y = find_position(circle["radius"], placed_circles, (cx, cy))
    placed_circles.append(
        {"x": x, "y": y, "radius": circle["radius"], "name": circle["name"], "group": circle["group"]}
    )

# Calculate bounds and recenter
all_x = [c["x"] for c in placed_circles]
all_y = [c["y"] for c in placed_circles]
all_r = [c["radius"] for c in placed_circles]

min_x = min(x - r for x, r in zip(all_x, all_r, strict=True))
max_x = max(x + r for x, r in zip(all_x, all_r, strict=True))
min_y = min(y - r for y, r in zip(all_y, all_r, strict=True))
max_y = max(y + r for y, r in zip(all_y, all_r, strict=True))

# Add padding
padding = 20
plot_width = max_x - min_x + 2 * padding
plot_height = max_y - min_y + 2 * padding

# Offset to center in plot area
offset_x = -min_x + padding
offset_y = -min_y + padding

for c in placed_circles:
    c["x"] += offset_x
    c["y"] += offset_y

# Draw circles
for c in placed_circles:
    circle_patch = patches.Circle(
        (c["x"], c["y"]), c["radius"], facecolor=group_colors[c["group"]], edgecolor="white", linewidth=3, alpha=0.9
    )
    ax.add_patch(circle_patch)

    # Add labels for larger circles
    if c["radius"] > 35:
        ax.text(c["x"], c["y"], c["name"], ha="center", va="center", fontsize=18, fontweight="bold", color="white")
    elif c["radius"] > 28:
        ax.text(c["x"], c["y"], c["name"], ha="center", va="center", fontsize=14, fontweight="bold", color="white")
    elif c["radius"] > 22:
        ax.text(c["x"], c["y"], c["name"], ha="center", va="center", fontsize=11, fontweight="bold", color="white")

# Configure axes
ax.set_xlim(0, plot_width)
ax.set_ylim(0, plot_height)
ax.set_aspect("equal")
ax.axis("off")

# Title
ax.set_title("bubble-packed · seaborn · pyplots.ai", fontsize=24, fontweight="bold", pad=20)

# Create legend (position at lower right to avoid overlap)
legend_elements = [
    patches.Patch(facecolor=group_colors[group], edgecolor="white", linewidth=2, label=group) for group in data.keys()
]
ax.legend(
    handles=legend_elements,
    loc="lower right",
    fontsize=14,
    framealpha=0.95,
    title="Sector",
    title_fontsize=16,
    edgecolor="gray",
)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
