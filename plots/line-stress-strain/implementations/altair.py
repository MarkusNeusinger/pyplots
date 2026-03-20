""" pyplots.ai
line-stress-strain: Engineering Stress-Strain Curve
Library: altair 6.0.0 | Python 3.14.3
Quality: 84/100 | Created: 2026-03-20
"""

import altair as alt
import numpy as np
import pandas as pd


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

# Yield plateau (small flat region after yield)
n_plateau = 20
strain_plateau = np.linspace(yield_strain, 0.02, n_plateau)
stress_plateau = np.full(n_plateau, yield_strength) + np.random.normal(0, 1.5, n_plateau)

# Strain hardening (yield to UTS)
n_hardening = 120
strain_hardening = np.linspace(0.02, uts_strain, n_hardening)
t = (strain_hardening - 0.02) / (uts_strain - 0.02)
stress_hardening = yield_strength + (uts - yield_strength) * (1 - (1 - t) ** 0.45)
stress_hardening += np.random.normal(0, 1.5, n_hardening)

# Necking (UTS to fracture)
n_necking = 80
strain_necking = np.linspace(uts_strain, fracture_strain, n_necking)
t_neck = (strain_necking - uts_strain) / (fracture_strain - uts_strain)
stress_necking = uts - (uts - 280) * t_neck**1.5
stress_necking += np.random.normal(0, 1.5, n_necking)

# Combine all regions
strain = np.concatenate([strain_elastic, strain_plateau, strain_hardening, strain_necking])
stress = np.concatenate([stress_elastic, stress_plateau, stress_hardening, stress_necking])

df = pd.DataFrame({"Strain": strain, "Stress (MPa)": stress})

# 0.2% offset line for yield point determination
offset = 0.002
offset_strain_max = yield_strain + offset + 0.003
offset_line_strain = np.array([offset, offset_strain_max])
offset_line_stress = youngs_modulus * (offset_line_strain - offset)

offset_df = pd.DataFrame({"Strain": offset_line_strain, "Stress (MPa)": offset_line_stress})

# Key points
yield_point_strain = offset + yield_strength / youngs_modulus
yield_point_stress = yield_strength
uts_idx = np.argmax(stress)
uts_point_strain = strain[uts_idx]
uts_point_stress = stress[uts_idx]
fracture_point_strain = strain[-1]
fracture_point_stress = stress[-1]

key_points_df = pd.DataFrame(
    {
        "Strain": [yield_point_strain, uts_point_strain, fracture_point_strain],
        "Stress (MPa)": [yield_point_stress, uts_point_stress, fracture_point_stress],
        "Label": ["Yield Point (0.2% offset)", "UTS", "Fracture"],
    }
)

# Shared scales
x_scale = alt.Scale(domain=[-0.01, 0.40])
y_scale = alt.Scale(domain=[-10, 450])

# Main stress-strain curve
curve = (
    alt.Chart(df)
    .mark_line(strokeWidth=3, color="#306998")
    .encode(
        x=alt.X("Strain:Q", scale=x_scale, title="Engineering Strain"),
        y=alt.Y("Stress (MPa):Q", scale=y_scale, title="Engineering Stress (MPa)"),
    )
)

# 0.2% offset line
offset_line = (
    alt.Chart(offset_df)
    .mark_line(strokeWidth=2, strokeDash=[8, 6], color="#888888")
    .encode(x=alt.X("Strain:Q", scale=x_scale), y=alt.Y("Stress (MPa):Q", scale=y_scale))
)

# Key points
point_colors = alt.Scale(
    domain=["Yield Point (0.2% offset)", "UTS", "Fracture"], range=["#C46210", "#8B1A1A", "#2E8B57"]
)

points = (
    alt.Chart(key_points_df)
    .mark_point(filled=True, size=400, stroke="white", strokeWidth=2)
    .encode(
        x=alt.X("Strain:Q", scale=x_scale),
        y=alt.Y("Stress (MPa):Q", scale=y_scale),
        color=alt.Color("Label:N", scale=point_colors, legend=None),
        tooltip=[
            alt.Tooltip("Label:N"),
            alt.Tooltip("Strain:Q", format=".4f"),
            alt.Tooltip("Stress (MPa):Q", format=".1f"),
        ],
    )
)

# Point labels
label_offsets = pd.DataFrame(
    {
        "Strain": [yield_point_strain + 0.015, uts_point_strain + 0.02, fracture_point_strain - 0.005],
        "Stress (MPa)": [yield_point_stress - 30, uts_point_stress + 25, fracture_point_stress + 30],
        "text": ["Yield Point\n(0.2% offset)", "UTS (400 MPa)", "Fracture"],
        "color_val": ["#C46210", "#8B1A1A", "#2E8B57"],
    }
)

yield_label = (
    alt.Chart(label_offsets.iloc[[0]])
    .mark_text(fontSize=17, align="left", fontWeight="bold", color="#C46210")
    .encode(x=alt.X("Strain:Q", scale=x_scale), y=alt.Y("Stress (MPa):Q", scale=y_scale), text="text:N")
)

uts_label = (
    alt.Chart(label_offsets.iloc[[1]])
    .mark_text(fontSize=17, align="left", fontWeight="bold", color="#8B1A1A")
    .encode(x=alt.X("Strain:Q", scale=x_scale), y=alt.Y("Stress (MPa):Q", scale=y_scale), text="text:N")
)

fracture_label = (
    alt.Chart(label_offsets.iloc[[2]])
    .mark_text(fontSize=17, align="center", fontWeight="bold", color="#2E8B57")
    .encode(x=alt.X("Strain:Q", scale=x_scale), y=alt.Y("Stress (MPa):Q", scale=y_scale), text="text:N")
)

# Region labels
region_labels_df = pd.DataFrame(
    {"Strain": [0.001, 0.11, 0.30], "Stress (MPa)": [430, 430, 430], "text": ["Elastic", "Strain Hardening", "Necking"]}
)

region_text = (
    alt.Chart(region_labels_df)
    .mark_text(fontSize=16, fontStyle="italic", color="#777777")
    .encode(x=alt.X("Strain:Q", scale=x_scale), y=alt.Y("Stress (MPa):Q", scale=y_scale), text="text:N")
)

# Young's modulus annotation
modulus_label_df = pd.DataFrame({"Strain": [0.012], "Stress (MPa)": [120], "text": [f"E = {youngs_modulus:,} MPa"]})

modulus_text = (
    alt.Chart(modulus_label_df)
    .mark_text(fontSize=16, align="left", fontWeight="bold", color="#306998")
    .encode(x=alt.X("Strain:Q", scale=x_scale), y=alt.Y("Stress (MPa):Q", scale=y_scale), text="text:N")
)

# 0.2% offset label
offset_label_df = pd.DataFrame({"Strain": [offset + 0.003], "Stress (MPa)": [50], "text": ["0.2% offset"]})

offset_text = (
    alt.Chart(offset_label_df)
    .mark_text(fontSize=14, align="left", color="#888888")
    .encode(x=alt.X("Strain:Q", scale=x_scale), y=alt.Y("Stress (MPa):Q", scale=y_scale), text="text:N")
)

# Combine all layers
chart = (
    alt.layer(
        curve, offset_line, points, yield_label, uts_label, fracture_label, region_text, modulus_text, offset_text
    )
    .properties(
        width=1600,
        height=900,
        title=alt.Title("Mild Steel Tensile Test · line-stress-strain · altair · pyplots.ai", fontSize=28),
    )
    .configure_axis(
        labelFontSize=18,
        titleFontSize=22,
        titleColor="#333333",
        labelColor="#555555",
        grid=False,
        domainColor="#aaaaaa",
        domainWidth=0.6,
        tickColor="#aaaaaa",
        tickSize=5,
        tickWidth=0.6,
    )
    .configure_title(color="#222222")
    .configure_view(strokeWidth=0)
    .interactive()
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
