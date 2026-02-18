""" pyplots.ai
radar-innovation-timeline: Innovation Radar with Time-Horizon Rings
Library: matplotlib 3.10.8 | Python 3.14.3
Quality: 76/100 | Created: 2026-02-18
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - Technology innovations mapped to time horizons and categories
np.random.seed(42)

rings = ["Adopt", "Trial", "Assess", "Hold"]
sectors = ["AI & ML", "Cloud & Infra", "Data Engineering", "Security"]
n_sectors = len(sectors)

innovations = [
    # AI & ML
    ("LLM Agents", "Adopt", "AI & ML"),
    ("RAG Pipelines", "Trial", "AI & ML"),
    ("Vision Transformers", "Trial", "AI & ML"),
    ("Federated Learning", "Assess", "AI & ML"),
    ("Neuromorphic Chips", "Hold", "AI & ML"),
    ("AI Code Assistants", "Adopt", "AI & ML"),
    # Cloud & Infra
    ("Kubernetes", "Adopt", "Cloud & Infra"),
    ("FinOps Tooling", "Trial", "Cloud & Infra"),
    ("Edge Computing", "Assess", "Cloud & Infra"),
    ("Serverless Containers", "Assess", "Cloud & Infra"),
    ("Quantum Cloud APIs", "Hold", "Cloud & Infra"),
    ("Platform Engineering", "Trial", "Cloud & Infra"),
    # Data Engineering
    ("Apache Iceberg", "Adopt", "Data Engineering"),
    ("Real-time Lakehouse", "Trial", "Data Engineering"),
    ("Data Contracts", "Trial", "Data Engineering"),
    ("Streaming SQL", "Assess", "Data Engineering"),
    ("Data Mesh", "Hold", "Data Engineering"),
    # Security
    ("Zero Trust Arch", "Adopt", "Security"),
    ("SBOM Tooling", "Trial", "Security"),
    ("AI Threat Detection", "Assess", "Security"),
    ("Post-Quantum Crypto", "Assess", "Security"),
    ("Confidential Computing", "Hold", "Security"),
    ("Homomorphic Encryption", "Hold", "Security"),
]

# Indices
ring_index = {name: i for i, name in enumerate(rings)}
sector_index = {name: i for i, name in enumerate(sectors)}

# Sector colors (colorblind-safe)
sector_colors = {"AI & ML": "#306998", "Cloud & Infra": "#E69F00", "Data Engineering": "#009E73", "Security": "#CC79A7"}

sector_markers = {"AI & ML": "o", "Cloud & Infra": "s", "Data Engineering": "D", "Security": "^"}

# Layout: 270 degrees arc, gap at bottom-right for ring labels + legend
arc_span = 3 / 4 * 2 * np.pi
arc_start = np.pi * 3 / 4
sector_width = arc_span / n_sectors

# Ring band boundaries
ring_boundaries = [0.5, 1.5, 2.5, 3.5, 4.5]

# Count items per ring-sector for even spacing
sector_ring_counts = {}
for _, ring_name, sector_name in innovations:
    key = (ring_name, sector_name)
    sector_ring_counts[key] = sector_ring_counts.get(key, 0) + 1

# Compute positions with deterministic spreading
positions = []
sector_ring_placed = {}
for name, ring_name, sector_name in innovations:
    r_idx = ring_index[ring_name]
    s_idx = sector_index[sector_name]
    key = (ring_name, sector_name)

    placed = sector_ring_placed.get(key, 0)
    total = sector_ring_counts[key]
    sector_ring_placed[key] = placed + 1

    # Spread radially within ring band
    r_lo = ring_boundaries[r_idx] + 0.15
    r_hi = ring_boundaries[r_idx + 1] - 0.15
    if total == 1:
        r = (r_lo + r_hi) / 2
    elif total == 2:
        r = r_lo + (r_hi - r_lo) * (0.3 + 0.4 * placed)
    else:
        r = r_lo + (r_hi - r_lo) * (placed + 0.5) / total

    # Spread angularly within sector
    sector_start = arc_start + s_idx * sector_width
    margin = sector_width * 0.12
    a_lo = sector_start + margin
    a_hi = sector_start + sector_width - margin
    if total == 1:
        theta = (a_lo + a_hi) / 2
    elif total == 2:
        theta = a_lo + (a_hi - a_lo) * (0.3 + 0.4 * placed)
    else:
        theta = a_lo + (a_hi - a_lo) * placed / (total - 1)

    # Tiny jitter for natural look
    theta += np.random.uniform(-0.02, 0.02)
    r += np.random.uniform(-0.04, 0.04)

    positions.append((name, theta, r, sector_name))

# Plot
fig, ax = plt.subplots(figsize=(14, 14), subplot_kw={"polar": True})

# Ring fills with subtle coloring
ring_fill_colors = ["#DAEAF6", "#DEF2DE", "#FDF5D6", "#F8D7DA"]
for i in range(len(rings)):
    theta_fill = np.linspace(arc_start, arc_start + arc_span, 300)
    ax.fill_between(
        theta_fill,
        np.full(300, ring_boundaries[i]),
        np.full(300, ring_boundaries[i + 1]),
        color=ring_fill_colors[i],
        alpha=0.45,
    )

# Ring boundary arcs
for boundary in ring_boundaries:
    theta_arc = np.linspace(arc_start, arc_start + arc_span, 300)
    ax.plot(theta_arc, np.full(300, boundary), color="#B0B0B0", linewidth=0.8, alpha=0.6)

# Sector divider lines
for i in range(n_sectors + 1):
    angle = arc_start + i * sector_width
    ax.plot([angle, angle], [ring_boundaries[0], ring_boundaries[-1]], color="#B0B0B0", linewidth=0.8, alpha=0.6)

# Ring labels along the gap (right side of arc end)
label_angle = arc_start + arc_span + 0.12
for i, ring_name in enumerate(rings):
    r_mid = (ring_boundaries[i] + ring_boundaries[i + 1]) / 2
    ax.text(
        label_angle,
        r_mid,
        ring_name,
        ha="left",
        va="center",
        fontsize=14,
        fontweight="bold",
        color="#555555",
        fontstyle="italic",
    )

# Sector labels along outer edge
for i, sector_name in enumerate(sectors):
    angle = arc_start + (i + 0.5) * sector_width
    ax.text(
        angle,
        ring_boundaries[-1] + 0.55,
        sector_name,
        ha="center",
        va="center",
        fontsize=16,
        fontweight="bold",
        color="#333333",
    )

# Plot innovation points and labels
for name, theta, r, sector_name in positions:
    color = sector_colors[sector_name]
    marker = sector_markers[sector_name]
    ax.scatter(theta, r, s=200, color=color, marker=marker, edgecolors="white", linewidth=0.8, zorder=5)
    ax.text(theta, r + 0.2, name, fontsize=8, ha="center", va="bottom", color="#333333", fontweight="medium")

# Style
ax.set_ylim(0, ring_boundaries[-1] + 1.3)
ax.set_yticklabels([])
ax.set_xticklabels([])
ax.set_xticks([])
ax.set_yticks([])
ax.grid(False)
ax.spines["polar"].set_visible(False)

# Title
ax.set_title(
    "Technology Radar 2026 · radar-innovation-timeline · matplotlib · pyplots.ai",
    fontsize=22,
    fontweight="medium",
    pad=30,
)

# Legend with correct marker shapes
legend_handles = [
    plt.scatter(
        [], [], s=120, color=sector_colors[s], marker=sector_markers[s], edgecolors="white", linewidth=0.8, label=s
    )
    for s in sectors
]
ax.legend(
    handles=legend_handles,
    loc="lower right",
    bbox_to_anchor=(1.22, -0.02),
    fontsize=15,
    framealpha=0.9,
    edgecolor="#CCCCCC",
    title="Sectors",
    title_fontsize=16,
    handletextpad=0.8,
    borderpad=1,
)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
