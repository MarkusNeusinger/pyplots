""" pyplots.ai
smith-chart-basic: Smith Chart for RF/Impedance
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 78/100 | Created: 2026-01-15
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.lines import Line2D


# Set seaborn style for better aesthetics
sns.set_style("whitegrid")
sns.set_context("talk", font_scale=1.2)

# Reference impedance (ohms)
z0 = 50

# Generate frequency sweep data (1 GHz to 6 GHz, 50 points)
np.random.seed(42)
n_points = 50
freq_ghz = np.linspace(1, 6, n_points)

# Simulate a realistic impedance locus (antenna-like behavior)
# Start near matched, go through reactive region, return toward center
t = np.linspace(0, 2 * np.pi, n_points)
# Spiral-like pattern typical of antenna impedance vs frequency
z_real = 50 + 30 * np.sin(t) + 15 * np.cos(2 * t)
z_imag = 40 * np.sin(1.5 * t) + 20 * np.cos(t)

# Normalize impedance to reference
z_norm = (z_real + 1j * z_imag) / z0

# Calculate reflection coefficient (Gamma)
gamma = (z_norm - 1) / (z_norm + 1)
gamma_real = gamma.real
gamma_imag = gamma.imag

# Create figure (square for Smith chart)
fig, ax = plt.subplots(figsize=(12, 12))

# Draw Smith chart grid
# Constant resistance circles
r_values = [0, 0.2, 0.5, 1, 2, 5]
theta = np.linspace(0, 2 * np.pi, 200)

for r in r_values:
    # Circle center and radius in Gamma plane
    center = r / (r + 1)
    radius = 1 / (r + 1)
    # Parametric circle
    circle_x = center + radius * np.cos(theta)
    circle_y = radius * np.sin(theta)
    # Clip to unit circle
    mask = circle_x**2 + circle_y**2 <= 1.001
    ax.plot(circle_x[mask], circle_y[mask], color="#306998", alpha=0.4, linewidth=1)

# Constant reactance arcs
x_values = [0.2, 0.5, 1, 2, 5]

for x in x_values:
    # Positive reactance arc (inductive)
    center_y = 1 / x
    radius = 1 / x
    arc_theta = np.linspace(-np.pi / 2, np.pi / 2, 200)
    arc_x = 1 + radius * np.cos(arc_theta)
    arc_y = center_y + radius * np.sin(arc_theta)
    mask = (arc_x**2 + arc_y**2 <= 1.001) & (arc_x >= -0.001)
    ax.plot(arc_x[mask], arc_y[mask], color="#D4A017", alpha=0.7, linewidth=1.5)

    # Negative reactance arc (capacitive)
    arc_y_neg = -center_y + radius * np.sin(arc_theta)
    mask_neg = (arc_x**2 + arc_y_neg**2 <= 1.001) & (arc_x >= -0.001)
    ax.plot(arc_x[mask_neg], arc_y_neg[mask_neg], color="#D4A017", alpha=0.7, linewidth=1.5)

# Draw unit circle (|Gamma| = 1 boundary)
unit_theta = np.linspace(0, 2 * np.pi, 200)
ax.plot(np.cos(unit_theta), np.sin(unit_theta), color="#306998", linewidth=2.5)

# Draw horizontal axis (real axis)
ax.axhline(0, color="#306998", linewidth=1.5, alpha=0.6)

# Plot impedance locus using seaborn lineplot for the trajectory
# First plot the main line
sns.lineplot(x=gamma_real, y=gamma_imag, color="#E74C3C", linewidth=3, ax=ax, legend=False, sort=False)

# Add markers at key frequency points
key_indices = [0, n_points // 4, n_points // 2, 3 * n_points // 4, n_points - 1]
ax.scatter(
    gamma_real[key_indices], gamma_imag[key_indices], s=200, color="#E74C3C", edgecolor="white", linewidth=2, zorder=10
)

# Label key frequency points
for idx in key_indices:
    offset = (10, 10) if gamma_imag[idx] >= 0 else (10, -15)
    ax.annotate(
        f"{freq_ghz[idx]:.1f} GHz",
        (gamma_real[idx], gamma_imag[idx]),
        textcoords="offset points",
        xytext=offset,
        fontsize=14,
        fontweight="bold",
        color="#2C3E50",
    )

# Mark the center (matched condition)
ax.scatter([0], [0], s=150, color="#27AE60", marker="+", linewidths=3, zorder=10)
ax.annotate(
    "Z₀ (50Ω)", (0, 0), textcoords="offset points", xytext=(-40, -20), fontsize=14, color="#27AE60", fontweight="bold"
)

# Add VSWR circle (|Gamma| = 0.5, VSWR = 3:1)
vswr_radius = 0.5
vswr_circle_x = vswr_radius * np.cos(unit_theta)
vswr_circle_y = vswr_radius * np.sin(unit_theta)
ax.plot(vswr_circle_x, vswr_circle_y, "--", color="#9B59B6", linewidth=2, alpha=0.8)
ax.annotate("VSWR 3:1", (0.35, 0.35), fontsize=12, color="#9B59B6", fontweight="bold")

# Styling
ax.set_xlim(-1.15, 1.15)
ax.set_ylim(-1.15, 1.15)
ax.set_aspect("equal")
ax.set_xlabel("Real(Γ)", fontsize=20)
ax.set_ylabel("Imag(Γ)", fontsize=20)
ax.set_title("smith-chart-basic · seaborn · pyplots.ai", fontsize=24, fontweight="bold", pad=20)
ax.tick_params(axis="both", labelsize=16)
ax.grid(False)  # Turn off default grid, we drew our own Smith grid

# Add legend for the grid lines
legend_elements = [
    Line2D([0], [0], color="#306998", linewidth=2, alpha=0.6, label="Constant R circles"),
    Line2D([0], [0], color="#D4A017", linewidth=2, alpha=0.8, label="Constant X arcs"),
    Line2D([0], [0], color="#E74C3C", linewidth=3, label="Impedance locus"),
    Line2D([0], [0], color="#9B59B6", linewidth=2, linestyle="--", label="VSWR 3:1 circle"),
]
ax.legend(handles=legend_elements, loc="upper left", fontsize=14, framealpha=0.9)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
