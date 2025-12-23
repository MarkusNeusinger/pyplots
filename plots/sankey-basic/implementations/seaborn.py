"""pyplots.ai
sankey-basic: Basic Sankey Diagram
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 45/100 | Created: 2025-12-23
"""

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Set seed for reproducibility
np.random.seed(42)

# Apply seaborn styling
sns.set_theme(style="white", context="talk", font_scale=1.2)

# Data - Energy flow from sources to sectors (in TWh)
flows_data = {
    "source": ["Coal", "Coal", "Coal", "Gas", "Gas", "Gas", "Nuclear", "Nuclear", "Nuclear"],
    "target": [
        "Residential",
        "Commercial",
        "Industrial",
        "Residential",
        "Commercial",
        "Industrial",
        "Residential",
        "Commercial",
        "Industrial",
    ],
    "value": [15, 12, 33, 20, 18, 22, 15, 15, 15],
}
df = pd.DataFrame(flows_data)

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Use seaborn color palette - distinct colors for each source
source_names = df["source"].unique()
palette = sns.color_palette("Set2", n_colors=len(source_names))
source_colors = dict(zip(source_names, palette, strict=True))

# Calculate node positions
sources = df.groupby("source")["value"].sum().sort_values(ascending=False)
targets = df.groupby("target")["value"].sum().sort_values(ascending=False)

# Node dimensions
node_width = 0.08
x_source = 0.15
x_target = 0.85
gap = 0.03

# Calculate source node positions (left side)
total_source = sources.sum()
source_positions = {}
y_pos = 0.95
for source, value in sources.items():
    height = (value / total_source) * 0.8
    source_positions[source] = {"y": y_pos - height, "height": height}
    y_pos -= height + gap

# Calculate target node positions (right side)
total_target = targets.sum()
target_positions = {}
y_pos = 0.95
for target, value in targets.items():
    height = (value / total_target) * 0.8
    target_positions[target] = {"y": y_pos - height, "height": height}
    y_pos -= height + gap

# Track current position for stacking flows at each node
source_current_y = {s: source_positions[s]["y"] + source_positions[s]["height"] for s in sources.index}
target_current_y = {t: target_positions[t]["y"] + target_positions[t]["height"] for t in targets.index}

# Bezier curve parameters
n_points = 50
t = np.linspace(0, 1, n_points)

# Draw flows - sort by value for better visual stacking
df_sorted = df.sort_values("value", ascending=False)

for _, row in df_sorted.iterrows():
    source = row["source"]
    target = row["target"]
    value = row["value"]
    color = source_colors[source]

    # Calculate band height based on value
    source_band_height = (value / sources[source]) * source_positions[source]["height"]
    target_band_height = (value / targets[target]) * target_positions[target]["height"]

    # Source side coordinates
    y0_top = source_current_y[source]
    y0_bot = y0_top - source_band_height
    source_current_y[source] = y0_bot

    # Target side coordinates
    y1_top = target_current_y[target]
    y1_bot = y1_top - target_band_height
    target_current_y[target] = y1_bot

    # Draw the flow band using bezier curves
    x0 = x_source + node_width
    x1 = x_target
    cx0 = x0 + (x1 - x0) * 0.4
    cx1 = x0 + (x1 - x0) * 0.6

    # Top and bottom curves
    top_x = (1 - t) ** 3 * x0 + 3 * (1 - t) ** 2 * t * cx0 + 3 * (1 - t) * t**2 * cx1 + t**3 * x1
    top_y = (1 - t) ** 3 * y0_top + 3 * (1 - t) ** 2 * t * y0_top + 3 * (1 - t) * t**2 * y1_top + t**3 * y1_top
    bot_y = (1 - t) ** 3 * y0_bot + 3 * (1 - t) ** 2 * t * y0_bot + 3 * (1 - t) * t**2 * y1_bot + t**3 * y1_bot

    # Use seaborn's fill_between via lineplot data
    flow_df = pd.DataFrame({"x": top_x, "y_top": top_y, "y_bot": bot_y})
    ax.fill_between(
        flow_df["x"], flow_df["y_bot"], flow_df["y_top"], color=color, alpha=0.6, linewidth=0.5, edgecolor=color
    )

# Draw source nodes (left)
for source in sources.index:
    pos = source_positions[source]
    rect = patches.FancyBboxPatch(
        (x_source, pos["y"]),
        node_width,
        pos["height"],
        boxstyle="round,pad=0.01,rounding_size=0.02",
        facecolor=source_colors[source],
        edgecolor="white",
        linewidth=2,
    )
    ax.add_patch(rect)
    ax.text(
        x_source - 0.02,
        pos["y"] + pos["height"] / 2,
        f"{source}\n({sources[source]:.0f} TWh)",
        ha="right",
        va="center",
        fontsize=18,
        fontweight="bold",
        color="#333333",
    )

# Draw target nodes (right)
target_color = sns.color_palette("Greys", n_colors=3)[1]
for target in targets.index:
    pos = target_positions[target]
    rect = patches.FancyBboxPatch(
        (x_target, pos["y"]),
        node_width,
        pos["height"],
        boxstyle="round,pad=0.01,rounding_size=0.02",
        facecolor=target_color,
        edgecolor="white",
        linewidth=2,
    )
    ax.add_patch(rect)
    ax.text(
        x_target + node_width + 0.02,
        pos["y"] + pos["height"] / 2,
        f"{target}\n({targets[target]:.0f} TWh)",
        ha="left",
        va="center",
        fontsize=18,
        fontweight="bold",
        color="#333333",
    )

# Create legend using seaborn scatterplot
legend_df = pd.DataFrame({"Source": source_names, "x": [-0.5] * len(source_names), "y": [-0.5] * len(source_names)})
sns.scatterplot(
    data=legend_df, x="x", y="y", hue="Source", palette=source_colors, s=400, marker="s", legend="full", ax=ax
)

# Style legend
legend = ax.legend(
    title="Energy Source",
    loc="upper center",
    bbox_to_anchor=(0.5, 0.02),
    ncol=3,
    frameon=True,
    fontsize=16,
    title_fontsize=18,
    markerscale=2,
)
legend.get_frame().set_facecolor("white")
legend.get_frame().set_edgecolor("#cccccc")

# Set title using the required format
ax.set_title("sankey-basic · seaborn · pyplots.ai", fontsize=24, fontweight="bold", pad=20)

# Set axis limits and remove decorations
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
