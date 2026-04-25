""" anyplot.ai
venn-labeled-items: Chartgeist-Style Venn Diagram with Labeled Items
Library: seaborn 0.13.2 | Python 3.14.4
Quality: 80/100 | Created: 2026-04-25
"""

import os

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Circle


# Theme tokens
THEME = os.getenv("ANYPLOT_THEME", "light")
PAGE_BG = "#FAF8F1" if THEME == "light" else "#1A1A17"
ELEVATED_BG = "#FFFDF6" if THEME == "light" else "#242420"
INK = "#1A1A17" if THEME == "light" else "#F0EFE8"
INK_SOFT = "#4A4A44" if THEME == "light" else "#B8B7B0"
INK_MUTED = "#6B6A63" if THEME == "light" else "#A8A79F"

OKABE_GREEN = "#009E73"
OKABE_ORANGE = "#D55E00"
OKABE_BLUE = "#0072B2"

sns.set_theme(
    style="white",
    rc={
        "figure.facecolor": PAGE_BG,
        "axes.facecolor": PAGE_BG,
        "axes.edgecolor": PAGE_BG,
        "axes.labelcolor": INK,
        "text.color": INK,
        "font.family": "serif",
    },
)

# Data
circles = [
    {"name": "Overhyped", "color": OKABE_GREEN, "center": (0.00, 0.55)},
    {"name": "Actually Useful", "color": OKABE_ORANGE, "center": (-0.476, -0.275)},
    {"name": "Secretly Loved", "color": OKABE_BLUE, "center": (0.476, -0.275)},
]

zone_items = {
    "A": ["NFTs", "Metaverse", "Web3"],
    "B": ["Spreadsheets", "Calculators"],
    "C": ["Karaoke", "Bob Ross"],
    "AB": ["Crypto", "ChatGPT"],
    "AC": ["TikTok", "Pumpkin Spice"],
    "BC": ["Google Maps", "Dolly Parton", "IKEA Meatballs"],
    "ABC": ["Sourdough"],
    "outside": ["Jury Duty"],
}

zone_centroids = {
    "A": (0.00, 1.05),
    "B": (-1.00, -0.62),
    "C": (1.00, -0.62),
    "AB": (-0.55, 0.32),
    "AC": (0.55, 0.32),
    "BC": (0.00, -0.65),
    "ABC": (0.00, 0.05),
    "outside": (-2.45, 1.05),
}

# Plot
fig, ax = plt.subplots(figsize=(16, 9), facecolor=PAGE_BG)
ax.set_facecolor(PAGE_BG)
ax.set_aspect("equal")

r = 0.85
for c in circles:
    ax.add_patch(Circle(c["center"], radius=r, facecolor=c["color"], alpha=0.18, edgecolor=c["color"], linewidth=2.0))

# Category labels (outside each circle, on the outer side)
ax.text(
    0,
    0.55 + r + 0.06,
    circles[0]["name"],
    ha="center",
    va="bottom",
    fontsize=22,
    fontweight="bold",
    color=circles[0]["color"],
    clip_on=False,
)
ax.text(
    -1.40,
    -0.275 - 0.80,
    circles[1]["name"],
    ha="right",
    va="top",
    fontsize=22,
    fontweight="bold",
    color=circles[1]["color"],
    clip_on=False,
)
ax.text(
    1.40,
    -0.275 - 0.80,
    circles[2]["name"],
    ha="left",
    va="top",
    fontsize=22,
    fontweight="bold",
    color=circles[2]["color"],
    clip_on=False,
)

# Items: distribute vertically inside each region
for zone, labels in zone_items.items():
    cx, cy = zone_centroids[zone]
    n = len(labels)
    spacing = 0.20
    start_y = cy + (n - 1) * spacing / 2
    for i, label in enumerate(labels):
        y = start_y - i * spacing
        is_outside = zone == "outside"
        ax.text(
            cx,
            y,
            label,
            ha="center",
            va="center",
            fontsize=15,
            color=INK_MUTED if is_outside else INK,
            style="italic" if is_outside else "normal",
            clip_on=False,
        )

# Hint label for the "outside" stack
ax.text(
    -2.45, 1.32, "(outside all)", ha="center", va="bottom", fontsize=11, color=INK_MUTED, style="italic", clip_on=False
)

# Title (mandatory format) + editorial subtitle
fig.suptitle(
    "Tech & Trends · venn-labeled-items · seaborn · anyplot.ai", fontsize=24, fontweight="medium", color=INK, y=0.965
)
fig.text(
    0.5,
    0.915,
    "A Chartgeist-style taxonomy of what we love, use, and overrate",
    ha="center",
    va="top",
    fontsize=14,
    color=INK_SOFT,
    style="italic",
)

ax.set_xlim(-2.85, 2.85)
ax.set_ylim(-1.60, 1.60)
ax.axis("off")

plt.savefig(f"plot-{THEME}.png", dpi=300, bbox_inches="tight", facecolor=PAGE_BG)
