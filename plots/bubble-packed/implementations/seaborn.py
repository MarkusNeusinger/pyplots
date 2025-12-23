"""pyplots.ai
bubble-packed: Basic Packed Bubble Chart
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 85/100 | Created: 2025-12-23
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Data - Company market values by sector (billions USD)
np.random.seed(42)
data = {
    "Technology": [("Apple", 180), ("Microsoft", 160), ("Google", 120), ("NVIDIA", 95), ("Meta", 75)],
    "Finance": [("JPMorgan", 85), ("Visa", 70), ("Mastercard", 55), ("Goldman Sachs", 45)],
    "Healthcare": [("UnitedHealth", 90), ("J&J", 65), ("Merck", 50), ("Pfizer", 40)],
    "Retail": [("Amazon", 140), ("Walmart", 60), ("Costco", 45), ("Target", 30)],
}

# Prepare circles sorted by size (largest first for better packing)
all_circles = []
for group, items in data.items():
    for name, value in items:
        radius = np.sqrt(value) * 4  # Scale by area
        all_circles.append({"name": name, "radius": radius, "group": group, "value": value})

all_circles.sort(key=lambda x: -x["radius"])

# Circle packing - place circles one by one without overlap (inline, no functions)
placed_circles = []
cx, cy = 0, 0

for circle in all_circles:
    new_radius = circle["radius"]

    if not placed_circles:
        # First circle at origin
        best_x, best_y = cx, cy
    else:
        # Try positions around existing circles, find closest to center
        best_pos = None
        best_dist = float("inf")

        for p in placed_circles:
            for angle in np.linspace(0, 2 * np.pi, 72, endpoint=False):
                dist = p["radius"] + new_radius + 2
                test_x = p["x"] + dist * np.cos(angle)
                test_y = p["y"] + dist * np.sin(angle)

                # Check overlap with all placed circles
                valid = True
                for other in placed_circles:
                    d = np.sqrt((test_x - other["x"]) ** 2 + (test_y - other["y"]) ** 2)
                    if d < other["radius"] + new_radius + 1:
                        valid = False
                        break

                if valid:
                    center_dist = np.sqrt((test_x - cx) ** 2 + (test_y - cy) ** 2)
                    if center_dist < best_dist:
                        best_dist = center_dist
                        best_pos = (test_x, test_y)

        best_x, best_y = best_pos if best_pos else (cx, cy)

    placed_circles.append(
        {
            "x": best_x,
            "y": best_y,
            "radius": new_radius,
            "name": circle["name"],
            "group": circle["group"],
            "value": circle["value"],
        }
    )

# Calculate bounds and recenter
all_x = [c["x"] for c in placed_circles]
all_y = [c["y"] for c in placed_circles]
all_r = [c["radius"] for c in placed_circles]

min_x = min(x - r for x, r in zip(all_x, all_r, strict=True))
max_x = max(x + r for x, r in zip(all_x, all_r, strict=True))
min_y = min(y - r for y, r in zip(all_y, all_r, strict=True))
max_y = max(y + r for y, r in zip(all_y, all_r, strict=True))

# Offset to center in plot area
padding = 20
offset_x = -min_x + padding
offset_y = -min_y + padding

for c in placed_circles:
    c["x"] += offset_x
    c["y"] += offset_y

plot_width = max_x - min_x + 2 * padding
plot_height = max_y - min_y + 2 * padding

# Create DataFrame for seaborn
df = pd.DataFrame(placed_circles)
# Scale marker size for scatterplot (s parameter uses area in points^2)
df["marker_size"] = (df["radius"] * 2) ** 2 * 3.14  # Convert radius to area for proper sizing

# Set seaborn style
sns.set_style("white")
palette = sns.color_palette("Set2", n_colors=len(data))
group_colors = {group: palette[i] for i, group in enumerate(data.keys())}

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Use seaborn scatterplot for the bubbles
sns.scatterplot(
    data=df,
    x="x",
    y="y",
    hue="group",
    size="marker_size",
    sizes=(df["marker_size"].min(), df["marker_size"].max()),
    palette="Set2",
    alpha=0.9,
    edgecolor="white",
    linewidth=3,
    legend=False,
    ax=ax,
)

# Add labels for all circles using annotations
# Sort by x position to manage external annotation placement
df_sorted = df.sort_values("x")
used_y_positions = []  # Track y positions for external labels to avoid overlap

for _, row in df_sorted.iterrows():
    name = row["name"]
    # Abbreviate long names for internal labels
    short_name = name if len(name) <= 10 else name[:9] + "."

    if row["radius"] > 38:
        # Large circles - full name with large font
        ax.text(row["x"], row["y"], short_name, ha="center", va="center", fontsize=18, fontweight="bold", color="white")
    elif row["radius"] > 32:
        # Medium-large circles
        ax.text(row["x"], row["y"], short_name, ha="center", va="center", fontsize=14, fontweight="bold", color="white")
    elif row["radius"] > 26:
        # Medium circles - smaller font
        ax.text(row["x"], row["y"], short_name, ha="center", va="center", fontsize=11, fontweight="bold", color="white")
    else:
        # Small circles - external annotation with arrow
        # Determine label position (alternate left/right based on position)
        if row["x"] < plot_width / 2:
            # Left side - annotate to the left
            offset_x = -row["radius"] - 20
            ha = "right"
        else:
            # Right side - annotate to the right
            offset_x = row["radius"] + 20
            ha = "left"

        # Adjust y to avoid overlapping labels
        target_y = row["y"]
        for used_y in used_y_positions:
            if abs(target_y - used_y) < 25:
                target_y = used_y + 25 if target_y >= used_y else used_y - 25
        used_y_positions.append(target_y)

        ax.annotate(
            name,
            xy=(row["x"], row["y"]),
            xytext=(row["x"] + offset_x, target_y),
            fontsize=11,
            fontweight="bold",
            color="#444444",
            arrowprops={"arrowstyle": "->", "color": "#888888", "lw": 1.5, "connectionstyle": "arc3,rad=0.1"},
            ha=ha,
            va="center",
        )

# Configure axes
ax.set_xlim(0, plot_width)
ax.set_ylim(0, plot_height)
ax.set_aspect("equal")
ax.axis("off")

# Title
ax.set_title("bubble-packed · seaborn · pyplots.ai", fontsize=24, fontweight="bold", pad=20)

# Create legend - position below the plot to avoid any overlap with data
legend_elements = [
    mpatches.Patch(facecolor=group_colors[group], edgecolor="white", linewidth=2, label=group) for group in data.keys()
]
ax.legend(
    handles=legend_elements,
    loc="upper center",
    bbox_to_anchor=(0.5, -0.02),
    ncol=4,
    fontsize=14,
    framealpha=0.95,
    title="Sector",
    title_fontsize=16,
    edgecolor="gray",
)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
