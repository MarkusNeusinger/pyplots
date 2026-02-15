""" pyplots.ai
campbell-basic: Campbell Diagram
Library: altair 6.0.0 | Python 3.14.3
Quality: 86/100 | Created: 2026-02-15
"""

import altair as alt
import numpy as np
import pandas as pd


# Data
np.random.seed(42)
speeds = np.linspace(0, 6000, 80)

mode_labels = ["1st Bending", "2nd Bending", "1st Torsional", "Axial", "3rd Bending"]
base_freqs = [45, 95, 130, 175, 220]
slopes = [0.004, -0.003, 0.005, 0.001, -0.004]
curvatures = [5e-7, -4e-7, 2e-7, 1e-7, -3e-7]

mode_rows = []
for label, base, slope, curv in zip(mode_labels, base_freqs, slopes, curvatures, strict=True):
    freqs = base + slope * speeds + curv * speeds**2
    for s, f in zip(speeds, freqs, strict=True):
        mode_rows.append({"Speed (RPM)": s, "Frequency (Hz)": f, "Series": label, "Category": "Natural Frequency"})

engine_orders = [1, 2, 3]
eo_rows = []
for order in engine_orders:
    for s in speeds:
        freq = order * s / 60
        eo_rows.append({"Speed (RPM)": s, "Frequency (Hz)": freq, "Series": f"{order}x EO", "Category": "Engine Order"})

df_modes = pd.DataFrame(mode_rows)
df_eo = pd.DataFrame(eo_rows)

# Find critical speed intersections
critical_rows = []
dense_speeds = np.linspace(0, 6000, 5000)
for label, base, slope, curv in zip(mode_labels, base_freqs, slopes, curvatures, strict=True):
    mode_freq = base + slope * dense_speeds + curv * dense_speeds**2
    for order in engine_orders:
        eo_freq = order * dense_speeds / 60
        diff = mode_freq - eo_freq
        sign_changes = np.where(np.diff(np.sign(diff)))[0]
        for idx in sign_changes:
            s_crit = dense_speeds[idx]
            f_crit = eo_freq[idx]
            if 100 < s_crit < 5900 and 5 < f_crit < 295:
                critical_rows.append(
                    {"Speed (RPM)": round(s_crit), "Frequency (Hz)": round(f_crit, 1), "Label": f"{label} / {order}x"}
                )

df_critical = pd.DataFrame(critical_rows)

# Select a few key critical speeds for annotation
key_annotations = df_critical.sort_values("Frequency (Hz)").head(3).reset_index(drop=True)

# Operating range band
op_min, op_max = 3000, 5000

# Plot
mode_palette = ["#306998", "#E8833A", "#55A868", "#8172B2", "#C44E52"]

x_scale = alt.Scale(domain=[0, 6200])
y_scale = alt.Scale(domain=[0, 310])

# Natural frequency mode lines
modes_chart = (
    alt.Chart(df_modes)
    .mark_line(strokeWidth=3)
    .encode(
        x=alt.X("Speed (RPM):Q", title="Rotational Speed (RPM)", scale=x_scale),
        y=alt.Y("Frequency (Hz):Q", title="Frequency (Hz)", scale=y_scale),
        color=alt.Color(
            "Series:N",
            scale=alt.Scale(domain=mode_labels, range=mode_palette),
            legend=alt.Legend(
                title="Natural Frequencies", titleFontSize=16, labelFontSize=14, symbolStrokeWidth=3, symbolSize=200
            ),
        ),
    )
)

# Engine order lines — single idiomatic chart with color encoding
eo_chart = (
    alt.Chart(df_eo)
    .mark_line(strokeWidth=1.5, strokeDash=[8, 6], opacity=0.65)
    .encode(
        x=alt.X("Speed (RPM):Q", scale=x_scale),
        y=alt.Y("Frequency (Hz):Q", scale=y_scale),
        detail="Series:N",
        color=alt.value("#777777"),
    )
)

# Engine order text labels near the right edge
eo_label_rows = []
for order in engine_orders:
    max_freq = order * 6000 / 60
    if max_freq <= 295:
        eo_label_rows.append({"Speed (RPM)": 6050, "Frequency (Hz)": order * 6050 / 60, "label": f"{order}x"})
    else:
        target_speed = 290 * 60 / order
        eo_label_rows.append({"Speed (RPM)": target_speed + 50, "Frequency (Hz)": 295, "label": f"{order}x"})

df_eo_labels = pd.DataFrame(eo_label_rows)

eo_label_chart = (
    alt.Chart(df_eo_labels)
    .mark_text(fontSize=16, fontWeight="bold", color="#555555", align="left", dy=-10)
    .encode(x=alt.X("Speed (RPM):Q", scale=x_scale), y=alt.Y("Frequency (Hz):Q", scale=y_scale), text="label:N")
)

# Operating range shaded band
op_band_df = pd.DataFrame({"x": [op_min], "x2": [op_max]})
op_band = (
    alt.Chart(op_band_df).mark_rect(opacity=0.07, color="#306998").encode(x=alt.X("x:Q", scale=x_scale), x2="x2:Q")
)

# Operating range label
op_label_df = pd.DataFrame(
    {"Speed (RPM)": [(op_min + op_max) / 2], "Frequency (Hz)": [5], "label": ["Operating Range"]}
)
op_label = (
    alt.Chart(op_label_df)
    .mark_text(fontSize=14, fontStyle="italic", color="#306998", fontWeight="bold", dy=8)
    .encode(x=alt.X("Speed (RPM):Q", scale=x_scale), y=alt.Y("Frequency (Hz):Q", scale=y_scale), text="label:N")
)

# Critical speed markers
critical_chart = (
    alt.Chart(df_critical)
    .mark_point(size=280, shape="diamond", filled=True, color="#D62728", stroke="white", strokeWidth=2)
    .encode(
        x=alt.X("Speed (RPM):Q", scale=x_scale),
        y=alt.Y("Frequency (Hz):Q", scale=y_scale),
        tooltip=["Label:N", "Speed (RPM):Q", "Frequency (Hz):Q"],
    )
)

# Annotations for key critical speeds
annotation_chart = (
    alt.Chart(key_annotations)
    .mark_text(fontSize=12, color="#B22222", fontWeight="bold", align="left", dx=12, dy=-12)
    .encode(
        x=alt.X("Speed (RPM):Q", scale=x_scale), y=alt.Y("Frequency (Hz):Q", scale=y_scale), text=alt.Text("Label:N")
    )
)

# Dashed-line legend entry for engine orders (a small dummy chart for the legend)
eo_legend_data = pd.DataFrame({"Speed (RPM)": [None], "Frequency (Hz)": [None], "Series": ["Engine Order (dashed)"]})
eo_legend = (
    alt.Chart(eo_legend_data)
    .mark_line(strokeWidth=1.5, strokeDash=[8, 6])
    .encode(
        x=alt.X("Speed (RPM):Q", scale=x_scale),
        y=alt.Y("Frequency (Hz):Q", scale=y_scale),
        color=alt.Color(
            "Series:N",
            scale=alt.Scale(domain=["Engine Order (dashed)"], range=["#777777"]),
            legend=alt.Legend(
                title="Excitation",
                titleFontSize=16,
                labelFontSize=14,
                symbolStrokeWidth=2,
                symbolSize=200,
                symbolDash=[8, 6],
            ),
        ),
    )
)

# Compose chart
chart = (
    (op_band + eo_chart + modes_chart + critical_chart + eo_label_chart + op_label + annotation_chart + eo_legend)
    .resolve_scale(color="independent")
    .properties(
        width=1600,
        height=900,
        title=alt.Title("campbell-basic · altair · pyplots.ai", fontSize=28, fontWeight=500, anchor="start"),
    )
    .configure_axis(
        labelFontSize=18,
        titleFontSize=22,
        grid=True,
        gridOpacity=0.12,
        gridWidth=0.6,
        domainColor="#cccccc",
        tickColor="#cccccc",
    )
    .configure_view(strokeWidth=0)
    .configure_legend(orient="right", padding=12, offset=8, titlePadding=8)
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
