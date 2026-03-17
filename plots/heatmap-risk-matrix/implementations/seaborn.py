""" pyplots.ai
heatmap-risk-matrix: Risk Assessment Matrix (Probability vs Impact)
Library: seaborn 0.13.2 | Python 3.14.3
Quality: 88/100 | Created: 2026-03-17
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
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
    {"name": "Staff Loss", "likelihood": 3, "impact": 3, "category": "Operational"},
    {"name": "Vendor Failure", "likelihood": 2, "impact": 3, "category": "Operational"},
    {"name": "Scope Creep", "likelihood": 5, "impact": 2, "category": "Project"},
    {"name": "Reg. Change", "likelihood": 3, "impact": 4, "category": "Financial"},
    {"name": "Cyber Attack", "likelihood": 3, "impact": 5, "category": "Technical"},
    {"name": "Supply Delay", "likelihood": 4, "impact": 4, "category": "Operational"},
    {"name": "Market Shift", "likelihood": 3, "impact": 2, "category": "Financial"},
    {"name": "Power Failure", "likelihood": 1, "impact": 3, "category": "Technical"},
    {"name": "Disputes", "likelihood": 2, "impact": 2, "category": "Financial"},
    {"name": "Defects", "likelihood": 3, "impact": 3, "category": "Project"},
    {"name": "Deadline Miss", "likelihood": 4, "impact": 2, "category": "Project"},
    {"name": "IP Theft", "likelihood": 1, "impact": 5, "category": "Technical"},
]

# Perceptually-uniform colormap for accessibility (plasma-inspired risk gradient)
cmap = LinearSegmentedColormap.from_list(
    "risk_pu", ["#f0f9e8", "#bae4bc", "#f7c948", "#e8871e", "#b5122a", "#6e0025"], N=256
)

# Seaborn style setup with custom palette
sns.set_style("white")
sns.set_context("talk", font_scale=1.0)
category_colors = sns.color_palette(["#306998", "#e8871e", "#7b4f9d", "#2ca02c"])

# Plot with extra space on right for legend
fig, ax = plt.subplots(figsize=(16, 9))
fig.subplots_adjust(right=0.76)

# Heatmap with seaborn - increased annotation visibility
sns.heatmap(
    risk_scores,
    annot=True,
    fmt="d",
    cmap=cmap,
    vmin=1,
    vmax=25,
    linewidths=2.5,
    linecolor="white",
    cbar_kws={"shrink": 0.6, "label": "Risk Score", "pad": 0.02, "aspect": 20},
    annot_kws={"size": 24, "weight": "bold", "color": "#2a2a2a", "alpha": 0.55},
    square=False,
    ax=ax,
)

# Category styling
category_palette = dict(zip(["Technical", "Financial", "Operational", "Project"], category_colors, strict=True))
category_markers = {"Technical": "o", "Financial": "s", "Operational": "D", "Project": "^"}

# Count items per cell for positioning
cell_items = {}
for risk in risks:
    cell_key = (risk["likelihood"] - 1, risk["impact"] - 1)
    if cell_key not in cell_items:
        cell_items[cell_key] = []
    cell_items[cell_key].append(risk)

offsets_map = {1: [(0, 0)], 2: [(-0.25, -0.1), (0.25, -0.1)], 3: [(-0.3, -0.16), (0.3, -0.16), (0, 0.2)]}

# Build positioned data
plot_data = []
for _cell_key, items in cell_items.items():
    n = len(items)
    offsets = offsets_map.get(n, offsets_map[3][:n])
    for i, risk in enumerate(items):
        ox, oy = offsets[i] if i < len(offsets) else (0, 0)
        score = risk["likelihood"] * risk["impact"]
        plot_data.append(
            {
                "x": risk["impact"] - 1 + 0.5 + ox,
                "y": risk["likelihood"] - 1 + 0.42 + oy,
                "name": risk["name"],
                "category": risk["category"],
                "score": score,
                "size": 160 + score * 14,
                "is_critical": score >= 16,
            }
        )

df_risks = pd.DataFrame(plot_data)

# Plot markers per category using seaborn scatterplot
for cat, marker in category_markers.items():
    cat_df = df_risks[df_risks["category"] == cat]
    if cat_df.empty:
        continue
    sns.scatterplot(
        data=cat_df,
        x="x",
        y="y",
        size="size",
        sizes=(cat_df["size"].min(), cat_df["size"].max()),
        color=category_palette[cat],
        marker=marker,
        edgecolor="white",
        linewidth=2.5,
        legend=False,
        ax=ax,
        zorder=5,
    )

# Highlight critical risks (score >= 16) with a second outer ring
critical_df = df_risks[df_risks["is_critical"]]
for _, row in critical_df.iterrows():
    ax.scatter(
        row["x"], row["y"], s=row["size"] + 200, facecolors="none", edgecolors="#6e0025", linewidths=2.5, zorder=4
    )

# Add labels with larger font size for readability
for _, row in df_risks.iterrows():
    label_y_offset = 0.30 if row["score"] >= 12 else 0.26
    fontsize = 11.5 if row["is_critical"] else 11
    ax.text(
        row["x"],
        row["y"] + label_y_offset,
        row["name"],
        ha="center",
        va="top",
        fontsize=fontsize,
        fontweight="bold",
        color="#1a1a1a",
        zorder=6,
        bbox={
            "boxstyle": "round,pad=0.15",
            "facecolor": "white",
            "edgecolor": "#6e0025" if row["is_critical"] else "none",
            "linewidth": 1.2 if row["is_critical"] else 0,
            "alpha": 0.85,
        },
    )

# Style axes
ax.set_xticklabels(impact_labels, fontsize=16, fontweight="medium")
ax.set_yticklabels(likelihood_labels, fontsize=16, rotation=0, fontweight="medium")
ax.set_xlabel("Impact", fontsize=20, fontweight="medium", labelpad=14)
ax.set_ylabel("Likelihood", fontsize=20, fontweight="medium", labelpad=14)
ax.set_title("heatmap-risk-matrix · seaborn · pyplots.ai", fontsize=24, fontweight="bold", pad=22, color="#222222")

# Colorbar styling
cbar = ax.collections[0].colorbar
cbar.ax.tick_params(labelsize=14)
cbar.ax.set_ylabel("Risk Score", fontsize=16, fontweight="medium")
cbar.outline.set_linewidth(0.5)

# Legend positioned outside the plot area
legend_handles = [
    plt.Line2D(
        [0],
        [0],
        marker=category_markers[cat],
        color="w",
        markerfacecolor=category_palette[cat],
        markersize=13,
        markeredgecolor="white",
        markeredgewidth=1.5,
        label=cat,
    )
    for cat in category_palette
]
legend_handles.append(plt.Line2D([0], [0], color="w", label=""))

# Zone color patches using colors from the colormap
zone_levels = [
    ("Low (1–4)", "#f0f9e8"),
    ("Medium (5–9)", "#bae4bc"),
    ("High (10–16)", "#e8871e"),
    ("Critical (20–25)", "#6e0025"),
]
for label, color in zone_levels:
    legend_handles.append(mpatches.Patch(facecolor=color, edgecolor="#999999", linewidth=1, label=label))

legend_handles.append(plt.Line2D([0], [0], color="w", label=""))

# Critical emphasis indicator
legend_handles.append(
    plt.Line2D(
        [0],
        [0],
        marker="o",
        color="w",
        markerfacecolor="none",
        markersize=14,
        markeredgecolor="#6e0025",
        markeredgewidth=2,
        label="Critical risk",
    )
)

# Small vs large marker size legend
legend_handles.append(
    plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="#888888", markersize=8, label="Low score")
)
legend_handles.append(
    plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="#888888", markersize=14, label="High score")
)

leg = ax.legend(
    handles=legend_handles,
    loc="center left",
    bbox_to_anchor=(1.12, 0.5),
    fontsize=12,
    framealpha=0.95,
    edgecolor="#cccccc",
    fancybox=True,
    shadow=False,
    title="Categories & Zones",
    title_fontsize=14,
    ncol=1,
    borderpad=1.0,
    labelspacing=0.9,
)
leg.get_title().set_fontweight("bold")

sns.despine(ax=ax, left=True, bottom=True)

plt.savefig("plot.png", dpi=300, bbox_inches="tight")
