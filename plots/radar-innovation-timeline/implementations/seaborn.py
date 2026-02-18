""" pyplots.ai
radar-innovation-timeline: Innovation Radar with Time-Horizon Rings
Library: seaborn 0.13.2 | Python 3.14.3
Quality: 84/100 | Created: 2026-02-18
"""

import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# ── Seaborn configuration ──
sns.set_theme(style="white", context="talk", font_scale=1.15)
custom_palette = sns.color_palette(["#306998", "#E8793A", "#4CAF50", "#9C27B0"])

np.random.seed(42)

# ── Configuration ──
sectors = ["AI & ML", "Cloud & Infra", "Sustainability", "Biotech"]
rings = ["Adopt", "Trial", "Assess", "Hold"]

ring_radii = {"Adopt": 1.0, "Trial": 2.0, "Assess": 3.0, "Hold": 4.0}
ring_importance = {"Adopt": 4, "Trial": 3, "Assess": 2, "Hold": 1}

sector_palette = dict(zip(sectors, custom_palette, strict=True))
sector_markers = {"AI & ML": "o", "Cloud & Infra": "s", "Sustainability": "D", "Biotech": "^"}

total_angle_deg = 270
sector_width_deg = total_angle_deg / len(sectors)
start_angle_deg = 135

ring_bg_colors = sns.color_palette(["#E8F5E9", "#FFF3E0", "#FFF9C4", "#FFEBEE"])
ring_boundaries = [0.5, 1.5, 2.5, 3.5, 4.5]

# ── Innovation data ──
innovations = [
    ("LLM Agents", "Adopt", "AI & ML"),
    ("RAG Pipelines", "Adopt", "AI & ML"),
    ("Multimodal Models", "Trial", "AI & ML"),
    ("Federated Learning", "Assess", "AI & ML"),
    ("Neuromorphic Chips", "Hold", "AI & ML"),
    ("AI Code Review", "Trial", "AI & ML"),
    ("Synthetic Data Gen", "Assess", "AI & ML"),
    ("Platform Eng.", "Adopt", "Cloud & Infra"),
    ("eBPF Observability", "Trial", "Cloud & Infra"),
    ("Wasm Edge", "Assess", "Cloud & Infra"),
    ("Confid. Compute", "Trial", "Cloud & Infra"),
    ("Serverless GPUs", "Assess", "Cloud & Infra"),
    ("Quantum Network", "Hold", "Cloud & Infra"),
    ("RISC-V Servers", "Hold", "Cloud & Infra"),
    ("Carbon Accounting", "Adopt", "Sustainability"),
    ("Green Software", "Trial", "Sustainability"),
    ("Digital Twins", "Assess", "Sustainability"),
    ("Circular Supply", "Trial", "Sustainability"),
    ("Ocean Carbon Cap.", "Hold", "Sustainability"),
    ("Energy Harvest IoT", "Assess", "Sustainability"),
    ("mRNA Therapeutics", "Adopt", "Biotech"),
    ("CRISPR Diagnostics", "Trial", "Biotech"),
    ("Organ-on-Chip", "Assess", "Biotech"),
    ("Biocomputing", "Hold", "Biotech"),
    ("Precision Nutrition", "Trial", "Biotech"),
    ("Longevity Biomarkers", "Assess", "Biotech"),
    ("Phage Therapy", "Hold", "Biotech"),
]

# ── Build DataFrame with computed polar positions ──
records = []
for name, ring, sector in innovations:
    sector_idx = sectors.index(sector)
    same_group = [(n, r, s) for n, r, s in innovations if s == sector and r == ring]
    item_idx = same_group.index((name, ring, sector))
    n_in_group = len(same_group)

    sector_start = np.deg2rad(start_angle_deg - sector_idx * sector_width_deg)
    sector_end = np.deg2rad(start_angle_deg - (sector_idx + 1) * sector_width_deg)
    margin = 0.08 * (sector_start - sector_end)
    usable_start = sector_start - margin
    usable_end = sector_end + margin

    if n_in_group == 1:
        angle = (usable_start + usable_end) / 2
    elif n_in_group == 2:
        spread = 0.80
        mid = (usable_start + usable_end) / 2
        half = spread * (usable_start - usable_end) / 2
        angle = mid + half if item_idx == 0 else mid - half
    else:
        angle = usable_start + (usable_end - usable_start) * item_idx / (n_in_group - 1)

    if n_in_group == 2:
        radial_jitter = 0.22 if item_idx == 0 else -0.22
    else:
        radial_jitter = np.random.uniform(-0.2, 0.2)
    radius = ring_radii[ring] + radial_jitter

    records.append(
        {
            "name": name,
            "ring": ring,
            "sector": sector,
            "angle": angle,
            "radius": radius,
            "importance": ring_importance[ring],
        }
    )

df = pd.DataFrame(records)

# ── Create polar figure ──
fig = plt.figure(figsize=(14, 14))
ax = fig.add_subplot(111, projection="polar")
ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)

# ── Ring background fills ──
theta_fill = np.linspace(0, 2 * np.pi, 200)
for i in range(len(rings)):
    ax.fill_between(
        theta_fill, ring_boundaries[i], ring_boundaries[i + 1], color=ring_bg_colors[i], alpha=0.35, zorder=0
    )

for rb in ring_boundaries:
    ax.plot(theta_fill, np.full_like(theta_fill, rb), color="gray", linewidth=0.8, alpha=0.4, zorder=1)

for i in range(len(sectors) + 1):
    angle = np.deg2rad(start_angle_deg - i * sector_width_deg)
    ax.plot([angle, angle], [0.5, 4.5], color="gray", linewidth=1.0, alpha=0.5, zorder=1)

# ── Plot innovations using seaborn scatterplot with multi-encoding ──
size_map = {1: 150, 2: 250, 3: 340, 4: 440}
sns.scatterplot(
    data=df,
    x="angle",
    y="radius",
    hue="sector",
    style="sector",
    size="importance",
    sizes=size_map,
    markers=sector_markers,
    palette=sector_palette,
    edgecolor="white",
    linewidth=1.5,
    alpha=0.9,
    legend=False,
    ax=ax,
    zorder=5,
)

# ── Subtle halo per sector (seaborn layer) ──
for sector_name in sectors:
    sector_df = df[df["sector"] == sector_name]
    sector_color = sector_palette[sector_name]
    sns.scatterplot(
        data=sector_df, x="angle", y="radius", color=sector_color, s=600, alpha=0.08, legend=False, ax=ax, zorder=3
    )

# ── Axes setup (before label placement so transforms are correct) ──
ax.set_ylim(0, 6.0)
ax.set_yticks([])
ax.set_xticks([])
ax.set_xlabel("")
ax.set_ylabel("")
ax.grid(False)
ax.spines["polar"].set_visible(False)

# Initialize transforms by drawing
fig.canvas.draw()

# ── Innovation labels with display-space collision detection ──
placed_display_boxes = []  # List of (x_disp, y_disp, width, height) in display coords
DPI = fig.dpi
PT_TO_DISP = DPI / 72.0  # Points to display pixels
FONT_SIZE = 12
CHAR_W = FONT_SIZE * 0.62 * PT_TO_DISP  # Approx char width in display pixels
CHAR_H = FONT_SIZE * 1.3 * PT_TO_DISP  # Approx line height in display pixels
PAD = 4 * PT_TO_DISP  # Padding around label


def data_to_display(angle, radius):
    """Convert polar data coords to display coords."""
    return ax.transData.transform((angle, radius))


def label_display_box(dx, dy, y_off, x_off, text_len, ha, va):
    """Estimate label bounding box in display coordinates."""
    cx = dx + x_off * PT_TO_DISP
    cy = dy + y_off * PT_TO_DISP
    w = text_len * CHAR_W + PAD * 2
    h = CHAR_H + PAD * 2

    if ha == "left":
        x0 = cx
    elif ha == "right":
        x0 = cx - w
    else:
        x0 = cx - w / 2

    if va == "bottom":
        y0 = cy
    else:
        y0 = cy - h

    return (x0, y0, w, h)


def boxes_overlap(b1, b2):
    """Check if two (x, y, w, h) boxes overlap with some margin."""
    margin = 2 * PT_TO_DISP
    x1, y1, w1, h1 = b1
    x2, y2, w2, h2 = b2
    return not (x1 + w1 + margin < x2 or x2 + w2 + margin < x1 or y1 + h1 + margin < y2 or y2 + h2 + margin < y1)


def count_overlaps(dx, dy, y_off, x_off, text_len, ha, placed):
    """Count how many placed labels overlap with candidate position."""
    va = "bottom" if y_off > 0 else "top"
    candidate = label_display_box(dx, dy, y_off, x_off, text_len, ha, va)
    return sum(1 for p in placed if boxes_overlap(candidate, p))


# Sort items by ring (outer first) so outer labels get placed first
df_sorted = df.sort_values("radius", ascending=False).reset_index(drop=True)

for _, row in df_sorted.iterrows():
    angle = row["angle"]
    radius = row["radius"]
    name = row["name"]

    angle_deg = np.rad2deg(angle) % 360
    dx, dy = data_to_display(angle, radius)

    if 30 < angle_deg < 150:
        ha = "left"
        base_x = 10
    elif 210 < angle_deg < 330:
        ha = "right"
        base_x = -10
    else:
        ha = "center"
        base_x = 0

    # Generate offset candidates: (y_offset, x_offset)
    candidates = []
    for y in [11, -11, 17, -17, 23, -23, 30, -30]:
        for dx_adj in [0, 7, -7, 14, -14]:
            candidates.append((y, base_x + dx_adj))

    best_pos = candidates[0]
    best_score = float("inf")
    for y_off, x_off in candidates:
        score = count_overlaps(dx, dy, y_off, x_off, len(name), ha, placed_display_boxes)
        if score < best_score:
            best_score = score
            best_pos = (y_off, x_off)
            if score == 0:
                break

    y_off, x_off = best_pos
    va = "bottom" if y_off > 0 else "top"

    ax.annotate(
        name,
        xy=(angle, radius),
        xytext=(x_off, y_off),
        textcoords="offset points",
        fontsize=FONT_SIZE,
        color="#2C2C2C",
        fontweight="medium",
        ha=ha,
        va=va,
        bbox={"boxstyle": "round,pad=0.18", "facecolor": "white", "edgecolor": "none", "alpha": 0.88},
        arrowprops={"arrowstyle": "-", "color": "#bbbbbb", "linewidth": 0.5},
        zorder=6,
    )
    box = label_display_box(dx, dy, y_off, x_off, len(name), ha, va)
    placed_display_boxes.append(box)

# ── Sector header labels ──
for i, sector_name in enumerate(sectors):
    mid_angle = np.deg2rad(start_angle_deg - (i + 0.5) * sector_width_deg)
    ax.text(
        mid_angle,
        5.4,
        sector_name,
        ha="center",
        va="center",
        fontsize=18,
        fontweight="bold",
        color=sector_palette[sector_name],
        zorder=7,
    )

# ── Ring labels ──
label_angle = np.deg2rad(start_angle_deg - total_angle_deg - 8)
for ring_name, ring_r in zip(rings, [1.0, 2.0, 3.0, 4.0], strict=True):
    ax.text(
        label_angle,
        ring_r,
        ring_name,
        ha="center",
        va="center",
        fontsize=14,
        fontweight="bold",
        color="#555555",
        bbox={"boxstyle": "round,pad=0.2", "facecolor": "white", "edgecolor": "none", "alpha": 0.88},
        zorder=7,
    )

# ── Title (>=24pt per guidelines) ──
ax.set_title(
    "radar-innovation-timeline · seaborn · pyplots.ai", fontsize=26, fontweight="bold", pad=35, color="#1a1a1a"
)

# ── Combined legend ──
sector_handles = [
    mlines.Line2D(
        [],
        [],
        marker=sector_markers[s],
        color="w",
        markerfacecolor=sector_palette[s],
        markeredgecolor="white",
        markersize=13,
        label=s,
    )
    for s in sectors
]

spacer = mlines.Line2D([], [], color="none", label=" ")

ring_sizes_legend = {"Adopt (Now)": 440, "Trial (Next)": 340, "Assess (Explore)": 250, "Hold (Watch)": 150}
ring_handles = [
    mlines.Line2D(
        [],
        [],
        marker="o",
        color="w",
        markerfacecolor="#999999",
        markeredgecolor="white",
        markersize=np.sqrt(sz) / 3,
        label=label,
    )
    for label, sz in ring_sizes_legend.items()
]

all_handles = sector_handles + [spacer] + ring_handles
legend = ax.legend(
    handles=all_handles,
    loc="lower right",
    bbox_to_anchor=(1.22, 0.02),
    fontsize=13,
    title="Sectors & Time Horizons",
    title_fontsize=15,
    framealpha=0.95,
    edgecolor="lightgray",
    fancybox=True,
    handletextpad=1.0,
    borderpad=1.0,
)
legend._legend_box.sep = 8

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
