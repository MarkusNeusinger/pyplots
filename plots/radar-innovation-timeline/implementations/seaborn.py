"""pyplots.ai
radar-innovation-timeline: Innovation Radar with Time-Horizon Rings
Library: seaborn | Python 3.13
Quality: pending | Created: 2026-02-18
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Configure seaborn style
sns.set_style("whitegrid")
sns.set_context("talk", font_scale=1.2)

# Data - Technology innovations mapped to time horizons and sectors
np.random.seed(42)

sectors = ["AI & ML", "Cloud & Infra", "Sustainability", "Biotech"]
rings = ["Adopt", "Trial", "Assess", "Hold"]
ring_radii = [1.0, 2.0, 3.0, 4.0]  # inner to outer

innovations = [
    # AI & ML
    ("LLM Agents", "Adopt", "AI & ML"),
    ("RAG Pipelines", "Adopt", "AI & ML"),
    ("Multimodal Models", "Trial", "AI & ML"),
    ("Federated Learning", "Assess", "AI & ML"),
    ("Neuromorphic Chips", "Hold", "AI & ML"),
    ("AI Code Review", "Trial", "AI & ML"),
    ("Synthetic Data Gen", "Assess", "AI & ML"),
    # Cloud & Infra
    ("Platform Engineering", "Adopt", "Cloud & Infra"),
    ("eBPF Observability", "Trial", "Cloud & Infra"),
    ("WebAssembly Edge", "Assess", "Cloud & Infra"),
    ("Confidential Compute", "Trial", "Cloud & Infra"),
    ("Serverless GPUs", "Assess", "Cloud & Infra"),
    ("Quantum Networking", "Hold", "Cloud & Infra"),
    ("RISC-V Servers", "Hold", "Cloud & Infra"),
    # Sustainability
    ("Carbon Accounting", "Adopt", "Sustainability"),
    ("Green Software", "Trial", "Sustainability"),
    ("Digital Twins", "Assess", "Sustainability"),
    ("Circular Supply Chain", "Trial", "Sustainability"),
    ("Ocean Carbon Capture", "Hold", "Sustainability"),
    ("Energy Harvesting IoT", "Assess", "Sustainability"),
    # Biotech
    ("mRNA Therapeutics", "Adopt", "Biotech"),
    ("CRISPR Diagnostics", "Trial", "Biotech"),
    ("Organ-on-Chip", "Assess", "Biotech"),
    ("Biocomputing", "Hold", "Biotech"),
    ("Precision Nutrition", "Trial", "Biotech"),
    ("Longevity Biomarkers", "Assess", "Biotech"),
    ("Phage Therapy", "Hold", "Biotech"),
]

# Sector configuration: angular spans (270 degrees total, leaving 90 for legend)
n_sectors = len(sectors)
total_angle = 270  # degrees
sector_width = total_angle / n_sectors
start_angle = 135  # start from upper-left, go clockwise

# Color palette per sector
palette = ["#306998", "#E8793A", "#4CAF50", "#9C27B0"]

# Ring mapping
ring_map = dict(zip(rings, ring_radii, strict=True))

# Compute positions for each innovation
angles_list = []
radii_list = []
sector_indices = []

for name, ring, sector in innovations:
    sector_idx = sectors.index(sector)
    ring_radius = ring_map[ring]

    # Count items in same sector+ring for jittering
    same_group = [(n, r, s) for n, r, s in innovations if s == sector and r == ring]
    item_idx = same_group.index((name, ring, sector))
    n_in_group = len(same_group)

    # Spread items within sector wedge
    sector_start = np.deg2rad(start_angle - sector_idx * sector_width)
    sector_end = np.deg2rad(start_angle - (sector_idx + 1) * sector_width)
    margin = 0.12 * (sector_start - sector_end)
    usable_start = sector_start - margin
    usable_end = sector_end + margin

    # Distribute evenly within sector
    if n_in_group == 1:
        angle = (usable_start + usable_end) / 2
    else:
        angle = usable_start + (usable_end - usable_start) * item_idx / (n_in_group - 1)

    # Add small radial jitter within ring
    radial_jitter = np.random.uniform(-0.25, 0.25)
    radius = ring_radius + radial_jitter

    angles_list.append(angle)
    radii_list.append(radius)
    sector_indices.append(sector_idx)

angles_arr = np.array(angles_list)
radii_arr = np.array(radii_list)

# Plot
fig = plt.figure(figsize=(14, 12))
ax = fig.add_subplot(111, projection="polar")

# Set orientation: 0 degrees at top, clockwise
ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)

# Draw ring boundaries with subtle fills
ring_colors_bg = ["#E8F5E9", "#FFF3E0", "#FFF9C4", "#FFEBEE"]
ring_boundaries = [0.5, 1.5, 2.5, 3.5, 4.5]
theta_fill = np.linspace(0, 2 * np.pi, 200)

for i in range(len(rings)):
    ax.fill_between(
        theta_fill, ring_boundaries[i], ring_boundaries[i + 1], color=ring_colors_bg[i], alpha=0.35, zorder=0
    )

# Draw ring boundary circles
for rb in ring_boundaries:
    ax.plot(theta_fill, np.full_like(theta_fill, rb), color="gray", linewidth=0.8, alpha=0.4, zorder=1)

# Draw sector divider lines
for i in range(n_sectors + 1):
    angle = np.deg2rad(start_angle - i * sector_width)
    ax.plot([angle, angle], [0.5, 4.5], color="gray", linewidth=1.0, alpha=0.5, zorder=1)

# Plot innovation points using seaborn scatter
for idx in range(n_sectors):
    mask = [i for i, s in enumerate(sector_indices) if s == idx]
    if mask:
        sector_angles = [angles_arr[i] for i in mask]
        sector_radii = [radii_arr[i] for i in mask]
        ax.scatter(
            sector_angles, sector_radii, c=palette[idx], s=280, edgecolors="white", linewidth=1.5, zorder=5, alpha=0.9
        )

# Add innovation labels with radial offset for readability
for i, (name, _ring, _sector) in enumerate(innovations):
    angle = angles_arr[i]
    radius = radii_arr[i]

    # Offset text radially outward from the point
    angle_deg = np.rad2deg(angle) % 360

    # Horizontal alignment based on which side of the chart
    if 30 < angle_deg < 150:
        ha = "left"
        x_off = 6
    elif 210 < angle_deg < 330:
        ha = "right"
        x_off = -6
    else:
        ha = "center"
        x_off = 0

    y_off = 5 if (0 < angle_deg < 180) else -5

    ax.annotate(
        name,
        xy=(angle, radius),
        xytext=(x_off, y_off),
        textcoords="offset points",
        fontsize=9,
        color="#333333",
        fontweight="medium",
        ha=ha,
        va="bottom" if y_off > 0 else "top",
        zorder=6,
    )

# Sector header labels along outer edge
for i, sector_name in enumerate(sectors):
    mid_angle = np.deg2rad(start_angle - (i + 0.5) * sector_width)
    ax.text(
        mid_angle,
        5.2,
        sector_name,
        ha="center",
        va="center",
        fontsize=16,
        fontweight="bold",
        color=palette[i],
        zorder=7,
    )

# Ring labels along one radial axis
label_angle = np.deg2rad(start_angle - total_angle - 8)
for ring_name, ring_r in zip(rings, ring_radii, strict=True):
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

# Configure axes
ax.set_ylim(0, 5.6)
ax.set_yticks([])
ax.set_xticks([])
ax.grid(False)
ax.spines["polar"].set_visible(False)

# Title
ax.set_title("radar-innovation-timeline · seaborn · pyplots.ai", fontsize=22, fontweight="bold", pad=30)

# Legend for sectors
legend_handles = [mpatches.Patch(facecolor=palette[i], edgecolor="white", label=sectors[i]) for i in range(n_sectors)]
ax.legend(
    handles=legend_handles,
    loc="lower right",
    bbox_to_anchor=(1.28, -0.05),
    fontsize=14,
    title="Sectors",
    title_fontsize=16,
    framealpha=0.95,
    edgecolor="lightgray",
    fancybox=True,
)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
