""" pyplots.ai
campbell-basic: Campbell Diagram
Library: plotnine 0.15.3 | Python 3.14.3
Quality: 86/100 | Created: 2026-02-15
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_blank,
    element_line,
    element_text,
    geom_line,
    geom_point,
    geom_text,
    ggplot,
    labs,
    scale_color_identity,
    scale_linetype_identity,
    scale_x_continuous,
    scale_y_continuous,
    theme,
    theme_minimal,
)


# Data - Natural frequencies vs rotational speed for a rotating machine
np.random.seed(42)
speed = np.linspace(0, 6000, 80)

# Natural frequency modes (Hz) - slight variation with speed due to gyroscopic effects
mode_1_bending = 18 + speed * 0.0008 + np.random.normal(0, 0.15, len(speed))
mode_2_bending = 42 - speed * 0.0005 + np.random.normal(0, 0.15, len(speed))
mode_1_torsional = 65 + speed * 0.0012 + np.random.normal(0, 0.15, len(speed))
mode_axial = 88 + speed * 0.0003 + np.random.normal(0, 0.15, len(speed))

modes = {
    "1st Bending": mode_1_bending,
    "2nd Bending": mode_2_bending,
    "1st Torsional": mode_1_torsional,
    "Axial": mode_axial,
}

# Build long-format DataFrame for natural frequency curves
records = []
for mode_name, freq_values in modes.items():
    for s, f in zip(speed, freq_values, strict=True):
        records.append({"Speed (RPM)": s, "Frequency (Hz)": f, "label": mode_name})

df_modes = pd.DataFrame(records)

# Engine order lines: frequency = order * speed / 60
engine_orders = [1, 2, 3]
eo_max_speed = 6000
eo_records = []
for order in engine_orders:
    for s in [0, eo_max_speed]:
        f = order * s / 60
        eo_records.append({"Speed (RPM)": s, "Frequency (Hz)": f, "label": f"{order}x"})

df_eo = pd.DataFrame(eo_records)

# Calculate critical speed intersections (engine order line meets natural freq curve)
critical_points = []
for order in engine_orders:
    eo_freq = order * speed / 60
    for _mode_name, freq_values in modes.items():
        diff = eo_freq - freq_values
        sign_changes = np.where(np.diff(np.sign(diff)))[0]
        for idx in sign_changes:
            s0, s1 = speed[idx], speed[idx + 1]
            f0_eo, f1_eo = eo_freq[idx], eo_freq[idx + 1]
            f0_mode, f1_mode = freq_values[idx], freq_values[idx + 1]
            t = (f0_mode - f0_eo) / ((f1_eo - f0_eo) - (f1_mode - f0_mode))
            crit_speed = s0 + t * (s1 - s0)
            crit_freq = f0_eo + t * (f1_eo - f0_eo)
            if 0 < crit_speed < 6000 and 0 < crit_freq < 110:
                critical_points.append({"Speed (RPM)": crit_speed, "Frequency (Hz)": crit_freq})

df_critical = pd.DataFrame(critical_points)

# Colors for mode curves
mode_colors = {"1st Bending": "#306998", "2nd Bending": "#E57373", "1st Torsional": "#81C784", "Axial": "#FFB74D"}
df_modes["color"] = df_modes["label"].map(mode_colors)

# Engine order line color
eo_color = "#9E9E9E"
df_eo["color"] = eo_color

# Mode label positions (at right edge of each curve)
mode_label_data = []
for mode_name, freq_values in modes.items():
    mode_label_data.append(
        {
            "Speed (RPM)": speed[-1] + 80,
            "Frequency (Hz)": freq_values[-1],
            "label": mode_name,
            "color": mode_colors[mode_name],
        }
    )
df_mode_labels = pd.DataFrame(mode_label_data)

# Engine order label positions (near top of each line within plot area)
eo_label_data = []
for order in engine_orders:
    label_speed = min(100 / (order / 60) * 0.92, 5600)
    label_freq = order * label_speed / 60
    eo_label_data.append(
        {"Speed (RPM)": label_speed, "Frequency (Hz)": label_freq + 2.5, "label": f"{order}x", "color": eo_color}
    )
df_eo_labels = pd.DataFrame(eo_label_data)

# Plot
plot = (
    ggplot()
    # Natural frequency curves
    + geom_line(df_modes, aes(x="Speed (RPM)", y="Frequency (Hz)", group="label", color="color"), size=2.2)
    # Engine order lines
    + geom_line(
        df_eo, aes(x="Speed (RPM)", y="Frequency (Hz)", group="label", color="color"), size=1.2, linetype="dashed"
    )
    # Critical speed markers
    + geom_point(
        df_critical, aes(x="Speed (RPM)", y="Frequency (Hz)"), color="#D32F2F", fill="#D32F2F", size=5, shape="D"
    )
    # Mode labels at right edge
    + geom_text(
        df_mode_labels, aes(x="Speed (RPM)", y="Frequency (Hz)", label="label", color="color"), size=11, ha="left"
    )
    # Engine order labels
    + geom_text(
        df_eo_labels,
        aes(x="Speed (RPM)", y="Frequency (Hz)", label="label", color="color"),
        size=11,
        fontstyle="italic",
    )
    + scale_color_identity()
    + scale_linetype_identity()
    + scale_x_continuous(breaks=range(0, 7000, 1000), limits=(0, 6800))
    + scale_y_continuous(breaks=range(0, 121, 20), limits=(0, 115))
    + labs(x="Rotational Speed (RPM)", y="Frequency (Hz)", title="campbell-basic · plotnine · pyplots.ai")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24, ha="center"),
        panel_grid_major=element_line(color="#E0E0E0", size=0.5, alpha=0.25),
        panel_grid_minor=element_blank(),
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
