"""pyplots.ai
bifurcation-basic: Bifurcation Diagram for Dynamical Systems
Library: seaborn 0.13.2 | Python 3.14.3
Quality: 79/100 | Created: 2026-03-20
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Data - Logistic map: x(n+1) = r * x(n) * (1 - x(n))
r_values = np.linspace(2.5, 4.0, 5000)
transient = 300
n_plot = 200

r_all = np.empty(len(r_values) * n_plot)
x_all = np.empty(len(r_values) * n_plot)

idx = 0
for r in r_values:
    x = 0.5
    for _ in range(transient):
        x = r * x * (1.0 - x)
    for _ in range(n_plot):
        x = r * x * (1.0 - x)
        r_all[idx] = r
        x_all[idx] = x
        idx += 1

# Classify regions for color storytelling
regime = np.where(r_all < 3.0, "Stable", np.where(r_all < 3.57, "Period-Doubling", "Chaos"))

df = pd.DataFrame({"r": r_all, "x": x_all, "Regime": regime})

# Plot
sns.set_theme(
    style="ticks",
    context="talk",
    font_scale=1.1,
    rc={"font.family": "sans-serif", "axes.edgecolor": "#888888", "axes.linewidth": 0.8},
)

fig, ax = plt.subplots(figsize=(16, 9))

palette = {"Stable": "#306998", "Period-Doubling": "#8B5CF6", "Chaos": "#DC2626"}
sns.scatterplot(
    data=df,
    x="r",
    y="x",
    hue="Regime",
    palette=palette,
    s=0.2,
    alpha=0.5,
    linewidth=0,
    edgecolor="none",
    legend="brief",
    ax=ax,
    rasterized=True,
)

# Annotate key bifurcation points
bifurcation_points = [
    (3.0, "Period-2\nr ≈ 3.0", 0.04),
    (3.449, "Period-4\nr ≈ 3.449", -0.14),
    (3.544, "Period-8\nr ≈ 3.544", 0.04),
]

for r_bif, label, x_offset in bifurcation_points:
    ax.axvline(r_bif, color="#94a3b8", linewidth=0.8, linestyle="--", alpha=0.6)
    ax.annotate(
        label,
        xy=(r_bif, 0.03),
        xytext=(r_bif + x_offset, 0.13),
        fontsize=11,
        color="#475569",
        ha="left" if x_offset > 0 else "right",
        va="bottom",
        arrowprops={"arrowstyle": "-", "color": "#94a3b8", "lw": 0.8},
    )

# Style
ax.set_title("bifurcation-basic · seaborn · pyplots.ai", fontsize=24, fontweight="medium", color="#333333", pad=16)
ax.set_xlabel("Growth Rate (r)", fontsize=20, color="#444444")
ax.set_ylabel("Steady-State Population (x)", fontsize=20, color="#444444")
ax.set_xlim(2.5, 4.0)
ax.set_ylim(0, 1)
ax.tick_params(axis="both", labelsize=16, colors="#555555")
sns.despine(ax=ax)

# Refine legend
legend = ax.get_legend()
legend.set_title("Regime")
legend.get_title().set_fontsize(14)
for text in legend.get_texts():
    text.set_fontsize(13)
legend.set_frame_on(True)
legend.get_frame().set_alpha(0.9)
legend.get_frame().set_edgecolor("#cccccc")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
