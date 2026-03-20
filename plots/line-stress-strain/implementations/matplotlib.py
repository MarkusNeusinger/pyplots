"""pyplots.ai
line-stress-strain: Engineering Stress-Strain Curve
Library: matplotlib | Python 3.13
Quality: pending | Created: 2026-03-20
"""

import matplotlib.pyplot as plt
import numpy as np


# Data — Mild steel tensile test (realistic stress-strain behavior)
np.random.seed(42)

youngs_modulus = 210000  # MPa
yield_stress = 250  # MPa
uts = 400  # MPa
fracture_strain = 0.35
uts_strain = 0.22
yield_strain = yield_stress / youngs_modulus

# Elastic region
strain_elastic = np.linspace(0, yield_strain, 60)
stress_elastic = youngs_modulus * strain_elastic

# Yield plateau (Lüders band, mild steel specific)
strain_plateau = np.linspace(yield_strain, 0.02, 30)
stress_plateau = np.full_like(strain_plateau, yield_stress) + np.random.normal(0, 1, len(strain_plateau))

# Strain hardening region
strain_hardening = np.linspace(0.02, uts_strain, 120)
t = (strain_hardening - 0.02) / (uts_strain - 0.02)
stress_hardening = yield_stress + (uts - yield_stress) * (1 - (1 - t) ** 2.5)

# Necking region (stress drops after UTS)
strain_necking = np.linspace(uts_strain, fracture_strain, 60)
t_neck = (strain_necking - uts_strain) / (fracture_strain - uts_strain)
stress_necking = uts - (uts - 300) * t_neck**1.5

# Combine all regions
strain = np.concatenate([strain_elastic, strain_plateau, strain_hardening, strain_necking])
stress = np.concatenate([stress_elastic, stress_plateau, stress_hardening, stress_necking])

# 0.2% offset yield point
offset = 0.002
offset_line_strain = np.linspace(offset, offset + yield_stress / youngs_modulus + 0.003, 50)
offset_line_stress = youngs_modulus * (offset_line_strain - offset)
offset_yield_strain = offset + yield_stress / youngs_modulus
offset_yield_stress = yield_stress

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

ax.plot(strain, stress, linewidth=3, color="#306998", zorder=5)

# 0.2% offset line
ax.plot(
    offset_line_strain,
    offset_line_stress,
    linewidth=2,
    color="#888888",
    linestyle="--",
    zorder=4,
    label="0.2% Offset Line",
)

# Mark critical points
ax.plot(
    offset_yield_strain,
    offset_yield_stress,
    "o",
    markersize=12,
    color="#D4762C",
    markeredgecolor="white",
    markeredgewidth=1.5,
    zorder=6,
)
ax.annotate(
    "Yield Point\n(0.2% Offset)",
    xy=(offset_yield_strain, offset_yield_stress),
    xytext=(0.04, yield_stress + 40),
    fontsize=14,
    color="#D4762C",
    fontweight="bold",
    arrowprops={"arrowstyle": "->", "color": "#D4762C", "lw": 1.5},
)

ax.plot(uts_strain, uts, "o", markersize=12, color="#C44E52", markeredgecolor="white", markeredgewidth=1.5, zorder=6)
ax.annotate(
    "UTS",
    xy=(uts_strain, uts),
    xytext=(uts_strain + 0.02, uts + 20),
    fontsize=14,
    color="#C44E52",
    fontweight="bold",
    arrowprops={"arrowstyle": "->", "color": "#C44E52", "lw": 1.5},
)

fracture_stress = stress_necking[-1]
ax.plot(
    fracture_strain,
    fracture_stress,
    "X",
    markersize=14,
    color="#8C564B",
    markeredgecolor="white",
    markeredgewidth=1.5,
    zorder=6,
)
ax.annotate(
    "Fracture",
    xy=(fracture_strain, fracture_stress),
    xytext=(fracture_strain - 0.01, fracture_stress - 50),
    fontsize=14,
    color="#8C564B",
    fontweight="bold",
    arrowprops={"arrowstyle": "->", "color": "#8C564B", "lw": 1.5},
)

# Region labels with background shading
ax.axvspan(0, yield_strain, alpha=0.06, color="#306998", zorder=1)
ax.text(yield_strain / 2, 30, "Elastic", fontsize=13, ha="center", color="#306998", fontstyle="italic", alpha=0.8)

ax.axvspan(yield_strain, 0.02, alpha=0.06, color="#D4762C", zorder=1)

ax.text(0.11, 30, "Strain Hardening", fontsize=13, ha="center", color="#306998", fontstyle="italic", alpha=0.8)

ax.text(0.29, 30, "Necking", fontsize=13, ha="center", color="#8C564B", fontstyle="italic", alpha=0.8)

# Elastic modulus annotation
mid_elastic = len(strain_elastic) // 3
ax.annotate(
    f"E = {youngs_modulus:,} MPa",
    xy=(strain_elastic[mid_elastic], stress_elastic[mid_elastic]),
    xytext=(0.03, 150),
    fontsize=13,
    color="#555555",
    arrowprops={"arrowstyle": "->", "color": "#555555", "lw": 1.2},
)

# Style
ax.set_xlabel("Engineering Strain (mm/mm)", fontsize=20)
ax.set_ylabel("Engineering Stress (MPa)", fontsize=20)
ax.set_title("Mild Steel Tensile Test · line-stress-strain · matplotlib · pyplots.ai", fontsize=24, fontweight="medium")
ax.tick_params(axis="both", labelsize=16)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.yaxis.grid(True, alpha=0.2, linewidth=0.8)
ax.set_xlim(-0.01, 0.40)
ax.set_ylim(-10, 470)
ax.legend(fontsize=14, loc="center right")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
