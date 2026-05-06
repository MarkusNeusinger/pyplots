""" anyplot.ai
bar-grouped: Grouped Bar Chart
Library: matplotlib 3.10.9 | Python 3.13.13
Quality: 88/100 | Updated: 2026-05-06
"""

import os

import matplotlib.pyplot as plt
import numpy as np


# Theme tokens
THEME = os.getenv("ANYPLOT_THEME", "light")
PAGE_BG = "#FAF8F1" if THEME == "light" else "#1A1A17"
ELEVATED_BG = "#FFFDF6" if THEME == "light" else "#242420"
INK = "#1A1A17" if THEME == "light" else "#F0EFE8"
INK_SOFT = "#4A4A44" if THEME == "light" else "#B8B7B0"
INK_MUTED = "#6B6A63" if THEME == "light" else "#A8A79F"

# Okabe-Ito palette (position 1 is always #009E73)
OKABE_ITO = ["#009E73", "#D55E00", "#0072B2"]

# Data: Quarterly sales by product line (in thousands USD)
categories = ["Q1", "Q2", "Q3", "Q4"]
groups = ["Electronics", "Clothing", "Home & Garden"]

sales_data = {
    "Electronics": [245, 312, 287, 425],
    "Clothing": [178, 195, 285, 310],
    "Home & Garden": [125, 210, 195, 165],
}

# Setup for grouped bars
x = np.arange(len(categories))
n_groups = len(groups)
bar_width = 0.25
offsets = np.linspace(-(n_groups - 1) / 2, (n_groups - 1) / 2, n_groups) * bar_width

# Plot
fig, ax = plt.subplots(figsize=(16, 9), facecolor=PAGE_BG)
ax.set_facecolor(PAGE_BG)

bars = []
for i, (group, color) in enumerate(zip(groups, OKABE_ITO, strict=True)):
    bar = ax.bar(
        x + offsets[i],
        sales_data[group],
        bar_width,
        label=group,
        color=color,
        edgecolor=INK_SOFT,
        linewidth=1.0,
    )
    bars.append(bar)

# Add value labels on top of bars
for bar_group in bars:
    for bar in bar_group:
        height = bar.get_height()
        ax.annotate(
            f"{int(height)}",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=14,
            color=INK,
        )

# Style
ax.set_xlabel("Quarter", fontsize=20, color=INK)
ax.set_ylabel("Sales (Thousands USD)", fontsize=20, color=INK)
ax.set_title("bar-grouped · matplotlib · anyplot.ai", fontsize=24, fontweight="medium", color=INK)

ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=16, color=INK_SOFT)
ax.tick_params(axis="y", labelsize=16, colors=INK_SOFT)

# Legend with theme-adaptive styling
leg = ax.legend(fontsize=16, loc="upper right", framealpha=0.95)
if leg:
    leg.get_frame().set_facecolor(ELEVATED_BG)
    leg.get_frame().set_edgecolor(INK_SOFT)
    leg.get_frame().set_linewidth(1.0)
    plt.setp(leg.get_texts(), color=INK_SOFT)

# Grid
ax.yaxis.grid(True, alpha=0.10, linewidth=0.8, color=INK)

# Spines
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color(INK_SOFT)
ax.spines["bottom"].set_color(INK_SOFT)

# Y-axis limits
ax.set_ylim(0, max(max(v) for v in sales_data.values()) * 1.15)

plt.tight_layout()
plt.savefig(f"plot-{THEME}.png", dpi=300, bbox_inches="tight", facecolor=PAGE_BG)
