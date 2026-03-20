""" pyplots.ai
line-stress-strain: Engineering Stress-Strain Curve
Library: letsplot 4.9.0 | Python 3.14.3
Quality: 86/100 | Created: 2026-03-20
"""

import numpy as np
import pandas as pd
from lets_plot import *  # noqa: F403
from lets_plot.export import ggsave as export_ggsave


LetsPlot.setup_html()  # noqa: F405

# Data - Mild steel tensile test simulation
np.random.seed(42)

# Material properties for mild steel
youngs_modulus = 210000  # MPa
yield_strength = 250  # MPa
uts = 400  # MPa (ultimate tensile strength)
fracture_strain = 0.35
uts_strain = 0.22
yield_strain = yield_strength / youngs_modulus  # ~0.00119

# Elastic region (0 to yield)
n_elastic = 60
strain_elastic = np.linspace(0, yield_strain, n_elastic)
stress_elastic = youngs_modulus * strain_elastic

# Yield plateau (mild steel has a distinct yield point)
n_plateau = 20
strain_plateau = np.linspace(yield_strain, 0.015, n_plateau)
stress_plateau = yield_strength + np.random.normal(0, 1.5, n_plateau)

# Strain hardening region (from end of plateau to UTS)
n_hardening = 120
strain_hardening = np.linspace(0.015, uts_strain, n_hardening)
stress_hardening = yield_strength + (uts - yield_strength) * (
    1 - np.exp(-8 * (strain_hardening - 0.015) / (uts_strain - 0.015))
)
stress_hardening += np.random.normal(0, 1.0, n_hardening)

# Necking region (UTS to fracture)
n_necking = 60
strain_necking = np.linspace(uts_strain, fracture_strain, n_necking)
stress_necking = uts - (uts - 280) * ((strain_necking - uts_strain) / (fracture_strain - uts_strain)) ** 1.5
stress_necking += np.random.normal(0, 1.5, n_necking)

# Combine all regions
strain = np.concatenate([strain_elastic, strain_plateau, strain_hardening, strain_necking])
stress = np.concatenate([stress_elastic, stress_plateau, stress_hardening, stress_necking])

df = pd.DataFrame({"strain": strain, "stress": stress})

# 0.2% offset line for yield point determination
offset = 0.002
offset_line_strain = np.linspace(offset, offset + yield_strength / youngs_modulus + 0.003, 50)
offset_line_stress = youngs_modulus * (offset_line_strain - offset)
offset_line_stress = np.clip(offset_line_stress, 0, yield_strength + 30)
df_offset = pd.DataFrame({"strain": offset_line_strain, "stress": offset_line_stress})

# Key points
yield_point_strain = offset + yield_strength / youngs_modulus
yield_point_stress = yield_strength
fracture_stress = stress_necking[-1]

df_points = pd.DataFrame(
    {
        "strain": [yield_point_strain, uts_strain, fracture_strain],
        "stress": [yield_point_stress, uts, fracture_stress],
        "type": ["Yield", "UTS", "Fracture"],
    }
)

# Annotation labels
df_yield_label = pd.DataFrame(
    {
        "x": [yield_point_strain + 0.012],
        "y": [yield_point_stress + 15],
        "label": [f"Yield Point\n({yield_strength} MPa)"],
    }
)
df_uts_label = pd.DataFrame({"x": [uts_strain + 0.015], "y": [uts + 10], "label": [f"UTS ({uts} MPa)"]})
df_fracture_label = pd.DataFrame({"x": [fracture_strain - 0.045], "y": [fracture_stress - 30], "label": ["Fracture"]})
df_modulus_label = pd.DataFrame({"x": [0.008], "y": [130], "label": [f"E = {youngs_modulus // 1000} GPa"]})
df_offset_label = pd.DataFrame({"x": [0.007], "y": [60], "label": ["0.2% offset"]})

# Region labels
df_region_elastic = pd.DataFrame({"x": [0.005], "y": [350], "label": ["Elastic"]})
df_region_hardening = pd.DataFrame({"x": [0.11], "y": [350], "label": ["Strain Hardening"]})
df_region_necking = pd.DataFrame({"x": [0.29], "y": [350], "label": ["Necking"]})

# Plot
plot = (
    ggplot()
    # Main stress-strain curve
    + geom_line(aes(x="strain", y="stress"), data=df, color="#306998", size=2.0)
    # 0.2% offset line
    + geom_line(aes(x="strain", y="stress"), data=df_offset, color="#D95319", size=1.2, linetype="dashed")
    # Key points
    + geom_point(aes(x="strain", y="stress", fill="type"), data=df_points, color="white", size=7, shape=21, stroke=1.2)
    + scale_fill_manual(values={"Yield": "#D95319", "UTS": "#2CA02C", "Fracture": "#7F7F7F"})
    + guides(fill="none")
    # Annotations - Yield point
    + geom_text(aes(x="x", y="y", label="label"), data=df_yield_label, size=11, color="#D95319", hjust=0)
    # Annotations - UTS
    + geom_text(aes(x="x", y="y", label="label"), data=df_uts_label, size=11, color="#2CA02C", hjust=0)
    # Annotations - Fracture
    + geom_text(aes(x="x", y="y", label="label"), data=df_fracture_label, size=11, color="#7F7F7F", hjust=0.5)
    # Elastic modulus annotation
    + geom_text(
        aes(x="x", y="y", label="label"), data=df_modulus_label, size=10, color="#306998", hjust=0, fontface="italic"
    )
    # Offset label
    + geom_text(
        aes(x="x", y="y", label="label"), data=df_offset_label, size=9, color="#D95319", hjust=0, fontface="italic"
    )
    # Region labels
    + geom_text(aes(x="x", y="y", label="label"), data=df_region_elastic, size=12, color="#888888", fontface="italic")
    + geom_text(aes(x="x", y="y", label="label"), data=df_region_hardening, size=12, color="#888888", fontface="italic")
    + geom_text(aes(x="x", y="y", label="label"), data=df_region_necking, size=12, color="#888888", fontface="italic")
    # Styling
    + labs(
        x="Engineering Strain",
        y="Engineering Stress (MPa)",
        title="Mild Steel Tensile Test · line-stress-strain · letsplot · pyplots.ai",
    )
    + scale_x_continuous(breaks=[0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35])
    + scale_y_continuous(breaks=[0, 50, 100, 150, 200, 250, 300, 350, 400, 450])
    + ggsize(1600, 900)
    + theme_minimal()
    + theme(
        axis_text=element_text(size=16, color="#555555"),
        axis_title=element_text(size=20, color="#333333"),
        plot_title=element_text(size=22, color="#222222", face="bold"),
        panel_grid_major_x=element_blank(),
        panel_grid_major_y=element_line(color="#E0E0E0", size=0.3),
        panel_grid_minor=element_blank(),
        plot_background=element_rect(fill="#FAFAFA", color="#FAFAFA"),
        panel_background=element_rect(fill="#FAFAFA", color="#FAFAFA"),
        axis_ticks=element_blank(),
        axis_ticks_length=0,
        plot_margin=[30, 40, 20, 20],
    )
)

# Save
export_ggsave(plot, filename="plot.png", path=".", scale=3)
export_ggsave(plot, filename="plot.html", path=".")
