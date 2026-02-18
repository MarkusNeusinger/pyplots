"""pyplots.ai
radar-innovation-timeline: Innovation Radar with Time-Horizon Rings
Library: seaborn 0.13.2 | Python 3.14.3
"""

import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# ── Seaborn configuration ──
sns.set_theme(style="white", context="talk", font_scale=1.1)

np.random.seed(42)

# ── Configuration ──
sectors = ["AI & ML", "Cloud & Infra", "Sustainability", "Biotech"]
rings = ["Adopt", "Trial", "Assess", "Hold"]

ring_radii = {"Adopt": 1.0, "Trial": 2.0, "Assess": 3.0, "Hold": 4.0}
ring_importance = {"Adopt": 4, "Trial": 3, "Assess": 2, "Hold": 1}

sector_palette = dict(zip(sectors, sns.color_palette(["#306998", "#E8793A", "#4CAF50", "#9C27B0"]), strict=True))
sector_markers = {"AI & ML": "o", "Cloud & Infra": "s", "Sustainability": "D", "Biotech": "^"}

total_angle_deg = 270
sector_width_deg = total_angle_deg / len(sectors)
start_angle_deg = 135

ring_bg_colors = ["#E8F5E9", "#FFF3E0", "#FFF9C4", "#FFEBEE"]
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
    ("Platform Engineering", "Adopt", "Cloud & Infra"),
    ("eBPF Observability", "Trial", "Cloud & Infra"),
    ("WebAssembly Edge", "Assess", "Cloud & Infra"),
    ("Confidential Compute", "Trial", "Cloud & Infra"),
    ("Serverless GPUs", "Assess", "Cloud & Infra"),
    ("Quantum Networking", "Hold", "Cloud & Infra"),
    ("RISC-V Servers", "Hold", "Cloud & Infra"),
    ("Carbon Accounting", "Adopt", "Sustainability"),
    ("Green Software", "Trial", "Sustainability"),
    ("Digital Twins", "Assess", "Sustainability"),
    ("Circular Supply Chain", "Trial", "Sustainability"),
    ("Ocean Carbon Capture", "Hold", "Sustainability"),
    ("Energy Harvesting IoT", "Assess", "Sustainability"),
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
    margin = 0.15 * (sector_start - sector_end)
    usable_start = sector_start - margin
    usable_end = sector_end + margin

    if n_in_group == 1:
        angle = (usable_start + usable_end) / 2
    else:
        angle = usable_start + (usable_end - usable_start) * item_idx / (n_in_group - 1)

    radial_jitter = np.random.uniform(-0.3, 0.3)
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
fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(111, projection="polar")
ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)

# ── Ring background fills ──
theta_fill = np.linspace(0, 2 * np.pi, 200)
for i in range(len(rings)):
    ax.fill_between(
        theta_fill, ring_boundaries[i], ring_boundaries[i + 1], color=ring_bg_colors[i], alpha=0.35, zorder=0
    )

# Ring boundary circles
for rb in ring_boundaries:
    ax.plot(theta_fill, np.full_like(theta_fill, rb), color="gray", linewidth=0.8, alpha=0.4, zorder=1)

# Sector divider lines
for i in range(len(sectors) + 1):
    angle = np.deg2rad(start_angle_deg - i * sector_width_deg)
    ax.plot([angle, angle], [0.5, 4.5], color="gray", linewidth=1.0, alpha=0.5, zorder=1)

# ── Plot innovations using seaborn scatterplot ──
sns.scatterplot(
    data=df,
    x="angle",
    y="radius",
    hue="sector",
    style="sector",
    size="importance",
    sizes={1: 150, 2: 250, 3: 340, 4: 440},
    markers=sector_markers,
    palette=sector_palette,
    edgecolor="white",
    linewidth=1.5,
    alpha=0.9,
    legend=False,
    ax=ax,
    zorder=5,
)

# ── Innovation labels with collision mitigation ──
placed = []
for _, row in df.iterrows():
    angle = row["angle"]
    radius = row["radius"]
    name = row["name"]

    angle_deg = np.rad2deg(angle) % 360

    # Text alignment based on angular position
    if 30 < angle_deg < 150:
        ha, x_off = "left", 10
    elif 210 < angle_deg < 330:
        ha, x_off = "right", -10
    else:
        ha, x_off = "center", 0

    y_off = 9 if (0 < angle_deg < 180) else -9

    # Collision check: flip offset or increase offset if near a previously placed label
    for prev_a, prev_r, prev_y in placed:
        da = abs(angle - prev_a)
        dr = abs(radius - prev_r)
        if da < 0.2 and dr < 0.7:
            # Flip vertical direction and increase offset
            y_off = -prev_y if prev_y != 0 else 12
            if ha == "left":
                x_off = 13
            elif ha == "right":
                x_off = -13
            break

    ax.annotate(
        name,
        xy=(angle, radius),
        xytext=(x_off, y_off),
        textcoords="offset points",
        fontsize=10,
        color="#2C2C2C",
        fontweight="medium",
        ha=ha,
        va="bottom" if y_off > 0 else "top",
        bbox={"boxstyle": "round,pad=0.15", "facecolor": "white", "edgecolor": "none", "alpha": 0.85},
        zorder=6,
    )
    placed.append((angle, radius, y_off))

# ── Sector header labels ──
for i, sector_name in enumerate(sectors):
    mid_angle = np.deg2rad(start_angle_deg - (i + 0.5) * sector_width_deg)
    ax.text(
        mid_angle,
        5.3,
        sector_name,
        ha="center",
        va="center",
        fontsize=16,
        fontweight="bold",
        color=sector_palette[sector_name],
        zorder=7,
    )

# ── Ring labels along radial axis ──
label_angle = np.deg2rad(start_angle_deg - total_angle_deg - 8)
for ring_name, ring_r in zip(rings, [1.0, 2.0, 3.0, 4.0], strict=True):
    ax.text(
        label_angle,
        ring_r,
        ring_name,
        ha="center",
        va="center",
        fontsize=13,
        fontweight="bold",
        color="#555555",
        bbox={"boxstyle": "round,pad=0.2", "facecolor": "white", "edgecolor": "none", "alpha": 0.85},
        zorder=7,
    )

# ── Axes cleanup ──
ax.set_ylim(0, 5.8)
ax.set_yticks([])
ax.set_xticks([])
ax.set_xlabel("")
ax.set_ylabel("")
ax.grid(False)
ax.spines["polar"].set_visible(False)

# ── Title ──
ax.set_title("radar-innovation-timeline · seaborn · pyplots.ai", fontsize=22, fontweight="bold", pad=30)

# ── Combined legend: sectors + rings ──
sector_handles = [
    mlines.Line2D(
        [],
        [],
        marker=sector_markers[s],
        color="w",
        markerfacecolor=sector_palette[s],
        markeredgecolor="white",
        markersize=12,
        label=s,
    )
    for s in sectors
]

# Spacer
spacer = mlines.Line2D([], [], color="none", label=" ")

# Ring size legend
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
    bbox_to_anchor=(1.32, -0.05),
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
