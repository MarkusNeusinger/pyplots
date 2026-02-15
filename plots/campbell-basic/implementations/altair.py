""" pyplots.ai
campbell-basic: Campbell Diagram
Library: altair 6.0.0 | Python 3.14.3
Quality: 81/100 | Created: 2026-02-15
"""

import altair as alt
import numpy as np
import pandas as pd


# Data
np.random.seed(42)
speeds = np.linspace(0, 6000, 80)

mode_labels = ["1st Bending", "2nd Bending", "1st Torsional", "Axial", "3rd Bending"]
base_freqs = [45, 95, 130, 175, 220]
slopes = [0.002, -0.001, 0.003, 0.0005, -0.0015]
curvatures = [3e-7, -2e-7, 1e-7, 5e-8, -1e-7]

mode_rows = []
for label, base, slope, curv in zip(mode_labels, base_freqs, slopes, curvatures, strict=True):
    freqs = base + slope * speeds + curv * speeds**2
    for s, f in zip(speeds, freqs, strict=True):
        mode_rows.append({"Speed (RPM)": s, "Frequency (Hz)": f, "Series": label, "Type": "mode"})

engine_orders = [1, 2, 3]
eo_rows = []
for order in engine_orders:
    for s in speeds:
        freq = order * s / 60
        eo_rows.append({"Speed (RPM)": s, "Frequency (Hz)": freq, "Series": f"{order}x", "Type": "eo"})

df_modes = pd.DataFrame(mode_rows)
df_eo = pd.DataFrame(eo_rows)

critical_rows = []
for label, base, slope, curv in zip(mode_labels, base_freqs, slopes, curvatures, strict=True):
    for order in engine_orders:
        dense_speeds = np.linspace(0, 6000, 5000)
        mode_freq = base + slope * dense_speeds + curv * dense_speeds**2
        eo_freq = order * dense_speeds / 60
        diff = mode_freq - eo_freq
        sign_changes = np.where(np.diff(np.sign(diff)))[0]
        for idx in sign_changes:
            s_crit = dense_speeds[idx]
            f_crit = eo_freq[idx]
            if 0 < s_crit < 6000 and 0 < f_crit < 300:
                critical_rows.append({"Speed (RPM)": s_crit, "Frequency (Hz)": f_crit, "Label": f"{label} / {order}x"})

df_critical = pd.DataFrame(critical_rows)

# Plot
mode_palette = ["#306998", "#E8833A", "#55A868", "#8172B2", "#C44E52"]

x_scale = alt.Scale(domain=[0, 6000])
y_scale = alt.Scale(domain=[0, 300])

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

eo_layers = []
eo_gray = "#888888"
for order_label in ["1x", "2x", "3x"]:
    df_single = df_eo[df_eo["Series"] == order_label].copy()
    line = (
        alt.Chart(df_single)
        .mark_line(strokeWidth=1.5, strokeDash=[8, 6], opacity=0.5)
        .encode(
            x=alt.X("Speed (RPM):Q", scale=x_scale),
            y=alt.Y("Frequency (Hz):Q", scale=y_scale),
            color=alt.value(eo_gray),
        )
    )
    eo_layers.append(line)

eo_label_rows = []
for order in engine_orders:
    max_freq = order * 6000 / 60
    if max_freq <= 295:
        eo_label_rows.append({"Speed (RPM)": 5900, "Frequency (Hz)": order * 5900 / 60, "label": f"{order}x"})
    else:
        target_speed = 285 * 60 / order
        eo_label_rows.append({"Speed (RPM)": target_speed, "Frequency (Hz)": 285, "label": f"{order}x"})

df_eo_labels = pd.DataFrame(eo_label_rows)

eo_label_chart = (
    alt.Chart(df_eo_labels)
    .mark_text(fontSize=16, fontWeight="bold", color="#666666", dx=-15, dy=-12, align="right")
    .encode(x=alt.X("Speed (RPM):Q", scale=x_scale), y=alt.Y("Frequency (Hz):Q", scale=y_scale), text="label:N")
)

critical_chart = (
    alt.Chart(df_critical)
    .mark_point(size=250, shape="diamond", filled=True, color="#D62728", stroke="white", strokeWidth=1.5)
    .encode(
        x=alt.X("Speed (RPM):Q", scale=x_scale),
        y=alt.Y("Frequency (Hz):Q", scale=y_scale),
        tooltip=["Label:N", "Speed (RPM):Q", "Frequency (Hz):Q"],
    )
)

chart = (
    (eo_layers[0] + eo_layers[1] + eo_layers[2] + modes_chart + critical_chart + eo_label_chart)
    .properties(
        width=1600, height=900, title=alt.Title("campbell-basic · altair · pyplots.ai", fontSize=28, fontWeight=500)
    )
    .configure_axis(labelFontSize=18, titleFontSize=22, grid=True, gridOpacity=0.15, gridWidth=0.8)
    .configure_view(strokeWidth=0)
    .configure_legend(orient="right", padding=10, offset=10)
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
