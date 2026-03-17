"""pyplots.ai
heatmap-risk-matrix: Risk Assessment Matrix (Probability vs Impact)
Library: seaborn | Python 3.13
Quality: pending | Created: 2026-03-17
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap


# Data
np.random.seed(42)

likelihood_labels = ["Rare", "Unlikely", "Possible", "Likely", "Almost\nCertain"]
impact_labels = ["Negligible", "Minor", "Moderate", "Major", "Catastrophic"]

# Risk score matrix (likelihood x impact)
risk_scores = np.array([[1, 2, 3, 4, 5], [2, 4, 6, 8, 10], [3, 6, 9, 12, 15], [4, 8, 12, 16, 20], [5, 10, 15, 20, 25]])

# Risk items with categories
risks = [
    {"name": "Server Outage", "likelihood": 2, "impact": 4, "category": "Technical"},
    {"name": "Data Breach", "likelihood": 2, "impact": 5, "category": "Technical"},
    {"name": "Budget Overrun", "likelihood": 4, "impact": 3, "category": "Financial"},
    {"name": "Key Staff Loss", "likelihood": 3, "impact": 3, "category": "Operational"},
    {"name": "Vendor Failure", "likelihood": 2, "impact": 3, "category": "Operational"},
    {"name": "Scope Creep", "likelihood": 5, "impact": 2, "category": "Project"},
    {"name": "Regulatory Change", "likelihood": 3, "impact": 4, "category": "Financial"},
    {"name": "Cyber Attack", "likelihood": 3, "impact": 5, "category": "Technical"},
    {"name": "Supply Chain Delay", "likelihood": 4, "impact": 4, "category": "Operational"},
    {"name": "Market Shift", "likelihood": 3, "impact": 2, "category": "Financial"},
    {"name": "Power Failure", "likelihood": 1, "impact": 3, "category": "Technical"},
    {"name": "Contract Dispute", "likelihood": 2, "impact": 2, "category": "Financial"},
    {"name": "Quality Defect", "likelihood": 3, "impact": 3, "category": "Project"},
    {"name": "Deadline Miss", "likelihood": 4, "impact": 2, "category": "Project"},
    {"name": "IP Theft", "likelihood": 1, "impact": 5, "category": "Technical"},
]

# Custom colormap: green -> yellow -> orange -> red
colors_list = ["#2ecc71", "#f1c40f", "#e67e22", "#e74c3c", "#c0392b"]
cmap = LinearSegmentedColormap.from_list("risk", colors_list, N=256)

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

sns.heatmap(
    risk_scores,
    annot=True,
    fmt="d",
    cmap=cmap,
    vmin=1,
    vmax=25,
    linewidths=2.5,
    linecolor="white",
    cbar_kws={"shrink": 0.7, "label": "Risk Score"},
    annot_kws={"size": 20, "weight": "bold", "color": "white", "alpha": 0.35},
    square=False,
    ax=ax,
)

# Plot risk items with jitter
category_colors = {"Technical": "#2c3e50", "Financial": "#1a5276", "Operational": "#4a235a", "Project": "#0e6655"}
category_markers = {"Technical": "o", "Financial": "s", "Operational": "D", "Project": "^"}

# Count items per cell for positioning
cell_items = {}
for risk in risks:
    cell_key = (risk["likelihood"] - 1, risk["impact"] - 1)
    if cell_key not in cell_items:
        cell_items[cell_key] = []
    cell_items[cell_key].append(risk)

# Position offsets for 1, 2, and 3 items in a cell
offsets_map = {1: [(0, 0)], 2: [(-0.22, -0.05), (0.22, -0.05)], 3: [(-0.25, -0.1), (0.25, -0.1), (0, 0.15)]}

for _cell_key, items in cell_items.items():
    n = len(items)
    offsets = offsets_map.get(n, offsets_map[3][:n])
    for i, risk in enumerate(items):
        ox, oy = offsets[i] if i < len(offsets) else (0, 0)
        x = risk["impact"] - 1 + 0.5 + ox
        y = risk["likelihood"] - 1 + 0.45 + oy

        marker = category_markers[risk["category"]]
        color = category_colors[risk["category"]]

        ax.scatter(x, y, s=300, c=color, marker=marker, edgecolors="white", linewidths=1.8, zorder=5)
        ax.text(
            x, y + 0.28, risk["name"], ha="center", va="top", fontsize=8.5, fontweight="bold", color="#1a1a1a", zorder=6
        )

# Style
ax.set_xticklabels(impact_labels, fontsize=16)
ax.set_yticklabels(likelihood_labels, fontsize=16, rotation=0)
ax.set_xlabel("Impact", fontsize=20, labelpad=12)
ax.set_ylabel("Likelihood", fontsize=20, labelpad=12)
ax.set_title("heatmap-risk-matrix · seaborn · pyplots.ai", fontsize=24, fontweight="medium", pad=20)

# Colorbar styling
cbar = ax.collections[0].colorbar
cbar.ax.tick_params(labelsize=14)
cbar.ax.set_ylabel("Risk Score", fontsize=16)

# Category legend with markers
legend_handles = [
    plt.Line2D(
        [0],
        [0],
        marker=category_markers[cat],
        color="w",
        markerfacecolor=category_colors[cat],
        markersize=12,
        markeredgecolor="white",
        markeredgewidth=1.5,
        label=cat,
    )
    for cat in category_colors
]
# Zone legend entries
zone_levels = [
    ("Low (1–4)", "#2ecc71"),
    ("Medium (5–9)", "#f1c40f"),
    ("High (10–16)", "#e67e22"),
    ("Critical (20–25)", "#c0392b"),
]
legend_handles.append(plt.Line2D([0], [0], color="w", label=""))
for label, color in zone_levels:
    legend_handles.append(mpatches.Patch(facecolor=color, edgecolor="#666666", linewidth=0.8, label=label))

ax.legend(
    handles=legend_handles,
    loc="lower right",
    fontsize=11,
    framealpha=0.95,
    edgecolor="#cccccc",
    title="Risk Zones & Categories",
    title_fontsize=12,
    ncol=1,
)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
