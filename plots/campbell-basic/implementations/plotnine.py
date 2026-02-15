""" pyplots.ai
campbell-basic: Campbell Diagram
Library: plotnine 0.15.3 | Python 3.14.3
Quality: 86/100 | Created: 2026-02-15
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    annotate,
    element_blank,
    element_line,
    element_rect,
    element_text,
    geom_line,
    geom_point,
    geom_text,
    ggplot,
    guide_legend,
    guides,
    labs,
    scale_color_manual,
    scale_linetype_manual,
    scale_x_continuous,
    scale_y_continuous,
    theme,
    theme_minimal,
)


# Data - Natural frequencies vs rotational speed for a rotating machine
np.random.seed(42)
speed = np.linspace(0, 6000, 80)

# Natural frequency modes (Hz) - slight variation with speed due to gyroscopic effects
modes = {
    "1st Bending": 18 + speed * 0.0008 + np.random.normal(0, 0.15, len(speed)),
    "2nd Bending": 42 - speed * 0.0005 + np.random.normal(0, 0.15, len(speed)),
    "1st Torsional": 55 + speed * 0.0012 + np.random.normal(0, 0.15, len(speed)),
    "2nd Torsional": 72 + speed * 0.0006 + np.random.normal(0, 0.15, len(speed)),
    "Axial": 88 + speed * 0.0003 + np.random.normal(0, 0.15, len(speed)),
}

# Colorblind-safe palette (blue, amber, purple, teal, brown) - all distinguishable
mode_colors = {
    "1st Bending": "#306998",
    "2nd Bending": "#E69F00",
    "1st Torsional": "#882D9E",
    "2nd Torsional": "#D55E00",
    "Axial": "#009E73",
}
eo_color = "#555555"

# Build long-format DataFrame for natural frequency curves
df_modes = pd.DataFrame(
    [
        {"Speed": s, "Frequency": f, "Mode": name}
        for name, freqs in modes.items()
        for s, f in zip(speed, freqs, strict=True)
    ]
)

# Engine order lines: frequency = order * speed / 60
engine_orders = [1, 2, 3]
eo_speed = np.linspace(0, 6000, 80)
df_eo = pd.DataFrame(
    [
        {"Speed": s, "Frequency": order * s / 60, "Mode": f"{order}x Engine Order"}
        for order in engine_orders
        for s in eo_speed
    ]
)

# Calculate critical speed intersections (engine order line meets natural freq curve)
critical_points = []
for order in engine_orders:
    eo_freq = order * speed / 60
    for mode_name, freq_values in modes.items():
        diff = eo_freq - freq_values
        sign_changes = np.where(np.diff(np.sign(diff)))[0]
        for idx in sign_changes:
            s0, s1 = speed[idx], speed[idx + 1]
            f0_eo, f1_eo = eo_freq[idx], eo_freq[idx + 1]
            f0_mode, f1_mode = freq_values[idx], freq_values[idx + 1]
            t = (f0_mode - f0_eo) / ((f1_eo - f0_eo) - (f1_mode - f0_mode))
            crit_speed = s0 + t * (s1 - s0)
            crit_freq = f0_eo + t * (f1_eo - f0_eo)
            if 0 < crit_speed < 6000 and 0 < crit_freq < 105:
                critical_points.append(
                    {"Speed": crit_speed, "Frequency": crit_freq, "order": f"{order}x", "mode_name": mode_name}
                )

df_critical = pd.DataFrame(critical_points)

# Engine order labels positioned along the lines - place in clear areas
eo_label_data = pd.DataFrame(
    [
        {"Speed": 4800, "Frequency": 1 * 4800 / 60 + 3, "label": "1x"},
        {"Speed": 2400, "Frequency": 2 * 2400 / 60 + 3, "label": "2x"},
        {"Speed": 1600, "Frequency": 3 * 1600 / 60 + 3, "label": "3x"},
    ]
)

# Storytelling: find the 1x/1st Bending critical speed (most operationally significant)
annot_speed = annot_freq = None
if len(df_critical) > 0:
    annot_row = df_critical[(df_critical["order"] == "1x") & (df_critical["mode_name"] == "1st Bending")]
    if len(annot_row) > 0:
        annot_speed = annot_row.iloc[0]["Speed"]
        annot_freq = annot_row.iloc[0]["Frequency"]

# Build legend mappings (modes + one representative EO entry)
all_mode_names = list(mode_colors.keys())
eo_names = [f"{o}x Engine Order" for o in engine_orders]

color_values = {**mode_colors, **dict.fromkeys(eo_names, eo_color)}
linetype_values = {**dict.fromkeys(all_mode_names, "solid"), **dict.fromkeys(eo_names, "dashed")}

legend_breaks = all_mode_names + eo_names[:1]
legend_labels = all_mode_names + ["Engine Order (1x, 2x, 3x)"]

# Combine mode and EO data for unified legend via scale_color_manual
df_all_lines = pd.concat([df_modes, df_eo], ignore_index=True)

# Plot
plot = (
    ggplot(df_all_lines, aes(x="Speed", y="Frequency", color="Mode", linetype="Mode", group="Mode"))
    + geom_line(size=1.8)
    # Critical speed markers
    + geom_point(
        df_critical,
        aes(x="Speed", y="Frequency"),
        color="#C62828",
        fill="#EF5350",
        size=5,
        shape="D",
        stroke=0.8,
        inherit_aes=False,
    )
    # Engine order labels - larger and darker for better visibility
    + geom_text(
        eo_label_data,
        aes(x="Speed", y="Frequency", label="label"),
        color="#333333",
        size=12,
        fontstyle="italic",
        fontweight="bold",
        inherit_aes=False,
    )
    # Scales for legend
    + scale_color_manual(values=color_values, breaks=legend_breaks, labels=legend_labels)
    + scale_linetype_manual(values=linetype_values, breaks=legend_breaks, labels=legend_labels)
    + guides(color=guide_legend(override_aes={"size": 1.5}), linetype=guide_legend())
    + scale_x_continuous(breaks=range(0, 7000, 1000), limits=(0, 6200))
    + scale_y_continuous(breaks=range(0, 111, 10), limits=(-5, 108))
    + labs(x="Rotational Speed (RPM)", y="Frequency (Hz)", title="campbell-basic \u00b7 plotnine \u00b7 pyplots.ai")
    + theme_minimal(base_size=14)
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14, color="#333333"),
        axis_title=element_text(size=20, face="bold", color="#222222"),
        axis_text=element_text(size=16, color="#555555"),
        plot_title=element_text(size=24, ha="center", face="bold", color="#1a1a1a"),
        legend_text=element_text(size=14),
        legend_title=element_blank(),
        legend_position="bottom",
        legend_direction="horizontal",
        legend_background=element_rect(fill="white", alpha=0.85, color="#DDDDDD", size=0.3),
        legend_key_width=40,
        panel_grid_major=element_line(color="#E0E0E0", size=0.3),
        panel_grid_minor=element_blank(),
        plot_background=element_rect(fill="white", color="white"),
        panel_background=element_rect(fill="#FAFAFA", color="#EEEEEE", size=0.3),
        axis_line=element_line(color="#BBBBBB", size=0.5),
    )
)

# Add critical speed annotation for storytelling
if annot_speed is not None:
    plot = (
        plot
        + annotate(
            "segment",
            x=annot_speed,
            xend=annot_speed,
            y=0,
            yend=annot_freq,
            color="#C62828",
            linetype="dotted",
            size=0.6,
            alpha=0.5,
        )
        + annotate(
            "text",
            x=annot_speed,
            y=-3,
            label=f"{int(round(annot_speed))} RPM",
            color="#C62828",
            size=9,
            ha="center",
            fontstyle="italic",
            fontweight="bold",
        )
    )

# Save
plot.save("plot.png", dpi=300, verbose=False)
