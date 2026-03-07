""" pyplots.ai
scatter-hr-diagram: Hertzsprung-Russell Diagram
Library: matplotlib 3.10.8 | Python 3.14.3
Quality: 86/100 | Created: 2026-03-07
"""

import matplotlib.pyplot as plt
import numpy as np


# Data
np.random.seed(42)

spectral_colors = {
    "O": "#4477cc",
    "B": "#6699dd",
    "A": "#99aacc",
    "F": "#ccb833",
    "G": "#ffcc00",
    "K": "#ff8800",
    "M": "#cc3300",
}

temp_ranges = {
    "O": (30000, 40000),
    "B": (10000, 30000),
    "A": (7500, 10000),
    "F": (6000, 7500),
    "G": (5200, 6000),
    "K": (3700, 5200),
    "M": (2400, 3700),
}

temp_boundaries = sorted([(t_lo, t_hi, sp) for sp, (t_lo, t_hi) in temp_ranges.items()], key=lambda x: x[0])


def classify_temp(t):
    for _t_lo, t_hi, sp in temp_boundaries:
        if t < t_hi:
            return sp
    return temp_boundaries[-1][2]


# Main sequence stars (250)
ms_temps = []
ms_lums = []
ms_types = []

for sp_type, (t_lo, t_hi) in temp_ranges.items():
    n = {"O": 8, "B": 20, "A": 30, "F": 35, "G": 45, "K": 55, "M": 57}[sp_type]
    temps = np.random.uniform(t_lo, t_hi, n)
    for t in temps:
        log_lum = 4.0 * np.log10(t / 5778) + np.random.normal(0, 0.3)
        ms_temps.append(t)
        ms_lums.append(10**log_lum)
        ms_types.append(sp_type)

# Red giants (50)
rg_temps = np.random.uniform(3000, 5200, 50)
rg_lums = 10 ** np.random.uniform(1.0, 3.0, 50)
rg_types = [classify_temp(t) for t in rg_temps]

# Supergiants (35)
sg_temps = np.random.uniform(3500, 30000, 35)
sg_lums = 10 ** np.random.uniform(3.5, 5.5, 35)
sg_types = [classify_temp(t) for t in sg_temps]

# White dwarfs (30)
wd_temps = np.random.uniform(5000, 30000, 30)
wd_lums = 10 ** np.random.uniform(-4.0, -1.5, 30)
wd_types = [classify_temp(t) for t in wd_temps]

all_temps = np.array(ms_temps + list(rg_temps) + list(sg_temps) + list(wd_temps))
all_lums = np.array(ms_lums + list(rg_lums) + list(sg_lums) + list(wd_lums))
all_types = ms_types + rg_types + sg_types + wd_types

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

for sp_type in ["O", "B", "A", "F", "G", "K", "M"]:
    mask = np.array([t == sp_type for t in all_types])
    if mask.any():
        ax.scatter(
            all_temps[mask],
            all_lums[mask],
            c=spectral_colors[sp_type],
            label=sp_type,
            s=60,
            alpha=0.65,
            edgecolors="white",
            linewidth=0.5,
            zorder=3,
        )

# Sun reference point
ax.scatter(5778, 1.0, c="#ffcc00", s=500, edgecolors="#333333", linewidth=2, zorder=5, marker="*")
ax.annotate(
    "Sun", (5778, 1.0), textcoords="offset points", xytext=(14, -10), fontsize=16, fontweight="bold", color="#333333"
)

# Region labels (positioned away from dense data clusters)
ax.annotate(
    "Main Sequence",
    xy=(15000, 200),
    fontsize=15,
    fontstyle="italic",
    color="#444444",
    rotation=-42,
    ha="center",
    bbox={"boxstyle": "round,pad=0.2", "fc": "white", "ec": "none", "alpha": 0.7},
)
ax.annotate(
    "Red Giants",
    xy=(3200, 150),
    fontsize=15,
    fontstyle="italic",
    color="#444444",
    ha="center",
    bbox={"boxstyle": "round,pad=0.2", "fc": "white", "ec": "none", "alpha": 0.7},
)
ax.annotate("Supergiants", xy=(8000, 400000), fontsize=15, fontstyle="italic", color="#444444", ha="center")
ax.annotate("White Dwarfs", xy=(15000, 0.00008), fontsize=15, fontstyle="italic", color="#444444", ha="center")

# Style
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(45000, 2000)
ax.set_ylim(1e-5, 2e6)

ax.set_xlabel("Surface Temperature (K)", fontsize=20)
ax.set_ylabel("Luminosity (L/L☉)", fontsize=20)
ax.set_title("scatter-hr-diagram · matplotlib · pyplots.ai", fontsize=24, fontweight="medium")
ax.tick_params(axis="both", labelsize=16)

ax.legend(title="Spectral Type", fontsize=14, title_fontsize=16, loc="upper right", framealpha=0.8, edgecolor="#cccccc")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.yaxis.grid(True, alpha=0.2, linewidth=0.8, which="both")

# Secondary x-axis for spectral classes
ax2 = ax.twiny()
spectral_positions = [35000, 20000, 8750, 6750, 5600, 4450, 3050]
spectral_labels = ["O", "B", "A", "F", "G", "K", "M"]
ax2.set_xscale("log")
ax2.set_xlim(ax.get_xlim())
ax2.set_xticks(spectral_positions)
ax2.set_xticklabels(spectral_labels, fontsize=16)
ax2.set_xlabel("Spectral Class", fontsize=18, labelpad=12)
ax2.tick_params(axis="x", length=0)
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
