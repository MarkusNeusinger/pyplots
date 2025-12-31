""" pyplots.ai
network-directed: Directed Network Graph
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 82/100 | Created: 2025-12-30
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Set seaborn style
sns.set_theme(style="white")

np.random.seed(42)

# Software module dependencies data - using shorter names for clarity
modules = {
    "app": {"group": "core", "pos": (0.5, 0.92)},
    "config": {"group": "core", "pos": (0.12, 0.72)},
    "db": {"group": "data", "pos": (0.32, 0.52)},
    "cache": {"group": "data", "pos": (0.68, 0.52)},
    "api": {"group": "services", "pos": (0.5, 0.72)},
    "auth": {"group": "services", "pos": (0.88, 0.72)},
    "log": {"group": "utils", "pos": (0.15, 0.28)},
    "valid": {"group": "utils", "pos": (0.5, 0.28)},
    "router": {"group": "services", "pos": (0.85, 0.28)},
    "model": {"group": "data", "pos": (0.32, 0.08)},
    "mware": {"group": "services", "pos": (0.68, 0.08)},
}

# Directed edges (source → target): arrows point from importer to imported module
edges = [
    ("app", "config"),
    ("app", "db"),
    ("app", "api"),
    ("app", "auth"),
    ("api", "valid"),
    ("api", "router"),
    ("api", "log"),
    ("auth", "cache"),
    ("auth", "db"),
    ("auth", "log"),
    ("db", "config"),
    ("db", "log"),
    ("cache", "config"),
    ("router", "valid"),
    ("router", "mware"),
    ("model", "db"),
    ("model", "valid"),
    ("mware", "auth"),
    ("mware", "log"),
]

# Color palette using seaborn
groups = ["core", "data", "services", "utils"]
palette = sns.color_palette(["#306998", "#FFD43B", "#4CAF50", "#E57373"], n_colors=4)
group_colors = dict(zip(groups, palette, strict=True))

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Draw all edges with directed arrows
for source, target in edges:
    start = modules[source]["pos"]
    end = modules[target]["pos"]

    # Calculate direction for shortening arrows
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = np.sqrt(dx**2 + dy**2)
    dx_norm = dx / length if length > 0 else 0
    dy_norm = dy / length if length > 0 else 0

    # Shorten to avoid overlapping nodes
    shrink = 0.055
    start_adj = (start[0] + dx_norm * shrink, start[1] + dy_norm * shrink)
    end_adj = (end[0] - dx_norm * shrink, end[1] - dy_norm * shrink)

    # Draw arrow using FancyArrowPatch
    arrow = mpatches.FancyArrowPatch(
        start_adj,
        end_adj,
        connectionstyle="arc3,rad=0.1",
        arrowstyle="->,head_length=8,head_width=5",
        color="#666666",
        alpha=0.6,
        linewidth=2,
        zorder=1,
    )
    ax.add_patch(arrow)

# Draw nodes using seaborn-style scatter
for name, data in modules.items():
    color = group_colors[data["group"]]
    ax.scatter(data["pos"][0], data["pos"][1], s=3000, c=[color], edgecolors="white", linewidths=3, zorder=2)
    # Node labels
    ax.text(
        data["pos"][0],
        data["pos"][1],
        name,
        ha="center",
        va="center",
        fontsize=12,
        fontweight="bold",
        color="white" if data["group"] != "data" else "#333333",
        zorder=3,
    )

# Create legend
legend_handles = [
    plt.scatter([], [], c=[group_colors[g]], s=400, label=g.capitalize(), edgecolors="white", linewidths=2)
    for g in groups
]
ax.legend(
    handles=legend_handles,
    loc="upper left",
    fontsize=16,
    title="Module Type",
    title_fontsize=18,
    framealpha=0.95,
    markerscale=1.0,
    borderpad=1,
)

# Styling
ax.set_title("network-directed · seaborn · pyplots.ai", fontsize=24, fontweight="bold", pad=20)
ax.set_xlim(-0.02, 1.02)
ax.set_ylim(-0.02, 1.02)
ax.axis("off")
ax.set_facecolor("#fafafa")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
