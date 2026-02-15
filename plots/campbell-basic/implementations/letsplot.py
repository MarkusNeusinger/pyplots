""" pyplots.ai
campbell-basic: Campbell Diagram
Library: letsplot 4.8.2 | Python 3.14.3
Quality: 83/100 | Created: 2026-02-15
"""

import numpy as np
import pandas as pd
from lets_plot import *


LetsPlot.setup_html()

# Data
np.random.seed(42)
speed_rpm = np.linspace(0, 6000, 80)
max_freq = 115

# Natural frequency modes (Hz) with realistic speed-dependent variation
# Gyroscopic effects cause slight frequency shifts with speed
mode1_bending1 = 25 + 0.0008 * speed_rpm + np.random.normal(0, 0.15, len(speed_rpm))
mode2_torsional1 = 48 - 0.0005 * speed_rpm + np.random.normal(0, 0.12, len(speed_rpm))
mode3_bending2 = 72 + 0.0012 * speed_rpm + np.random.normal(0, 0.18, len(speed_rpm))
mode4_axial = 95 - 0.0003 * speed_rpm + np.random.normal(0, 0.10, len(speed_rpm))

mode_names = ["1st Bending", "1st Torsional", "2nd Bending", "Axial"]
mode_data = [mode1_bending1, mode2_torsional1, mode3_bending2, mode4_axial]

# Build long-format DataFrame for natural frequency modes
modes_df = pd.DataFrame(
    {
        "Speed": np.tile(speed_rpm, 4),
        "Frequency": np.concatenate(mode_data),
        "Mode": np.repeat(mode_names, len(speed_rpm)),
    }
)

# Engine order lines: frequency = order * speed_rpm / 60
orders = [1, 2, 3]
order_labels = ["1×", "2×", "3×"]

eo_rows = []
for order, label in zip(orders, order_labels, strict=True):
    max_speed_for_order = min(6000, max_freq * 60 / order)
    eo_speed = np.linspace(0, max_speed_for_order, 80)
    eo_freq = order * eo_speed / 60
    for s, f in zip(eo_speed, eo_freq, strict=True):
        eo_rows.append({"Speed": s, "Frequency": f, "Engine Order": label, "order_num": order})
eo_df = pd.DataFrame(eo_rows)

# Find critical speed intersections (where EO lines cross mode curves)
critical_speeds = []
critical_freqs = []
critical_labels = []
for order, olabel in zip(orders, order_labels, strict=True):
    eo_freq_at_speeds = order * speed_rpm / 60
    for mode_freq, mname in zip(mode_data, mode_names, strict=True):
        diff = eo_freq_at_speeds - mode_freq
        sign_changes = np.where(np.diff(np.sign(diff)))[0]
        for idx in sign_changes:
            frac = abs(diff[idx]) / (abs(diff[idx]) + abs(diff[idx + 1]))
            crit_speed = speed_rpm[idx] + frac * (speed_rpm[idx + 1] - speed_rpm[idx])
            crit_freq = order * crit_speed / 60
            if crit_freq <= max_freq:
                critical_speeds.append(crit_speed)
                critical_freqs.append(crit_freq)
                critical_labels.append(f"{mname} × {olabel}")

crit_df = pd.DataFrame({"Speed": critical_speeds, "Frequency": critical_freqs, "Intersection": critical_labels})

# EO label positions (near the end of each EO line, offset slightly)
eo_label_rows = []
for order, label in zip(orders, order_labels, strict=True):
    label_speed = min(5600, (max_freq - 5) * 60 / order)
    label_freq = order * label_speed / 60 + 2.5
    eo_label_rows.append({"Speed": label_speed, "Frequency": label_freq, "Label": label})
eo_label_df = pd.DataFrame(eo_label_rows)

# Colorblind-safe palette: blue, orange, teal, purple (avoids green-brown confusion)
mode_colors = ["#306998", "#E67E22", "#17A589", "#8E44AD"]
# Build highlight zones around critical speeds using geom_rect
zone_rows = []
for spd, frq in zip(critical_speeds, critical_freqs, strict=True):
    zone_rows.append({"xmin": spd - 120, "xmax": spd + 120, "ymin": frq - 2.5, "ymax": frq + 2.5})
zone_df = pd.DataFrame(zone_rows)

# Plot
plot = (
    ggplot()
    # Subtle highlight zones around critical speed intersections
    + geom_rect(
        data=zone_df,
        mapping=aes(xmin="xmin", xmax="xmax", ymin="ymin", ymax="ymax"),
        fill="#D62728",
        alpha=0.08,
        color="transparent",
    )
    # Engine order lines as mapped aesthetics so they appear in legend
    + geom_line(
        data=eo_df,
        mapping=aes(x="Speed", y="Frequency", group="Engine Order"),
        color="#AAAAAA",
        size=0.8,
        linetype="dashed",
    )
    # Natural frequency mode curves with interactive tooltips
    + geom_line(
        data=modes_df,
        mapping=aes(x="Speed", y="Frequency", color="Mode"),
        size=2.5,
        tooltips=layer_tooltips()
        .line("@{Mode}")
        .line("Speed|@{Speed} RPM")
        .line("Freq|@{Frequency} Hz")
        .format("Speed", ",.0f")
        .format("Frequency", ".1f"),
    )
    # Critical speed intersection markers with rich tooltips
    + geom_point(
        data=crit_df,
        mapping=aes(x="Speed", y="Frequency"),
        color="#D62728",
        fill="#D62728",
        size=8,
        shape=18,
        tooltips=layer_tooltips()
        .title("Critical Speed")
        .line("@{Intersection}")
        .line("Speed|@{Speed} RPM")
        .line("Freq|@{Frequency} Hz")
        .format("Speed", ",.0f")
        .format("Frequency", ".1f"),
    )
    # Engine order labels
    + geom_text(
        data=eo_label_df,
        mapping=aes(x="Speed", y="Frequency", label="Label"),
        color="#666666",
        size=15,
        fontface="bold",
    )
    + scale_color_manual(values=mode_colors)
    + scale_y_continuous(limits=[0, max_freq], expand=[0, 2])
    + scale_x_continuous(limits=[0, 6200], format=",d")
    + labs(
        title="campbell-basic · letsplot · pyplots.ai",
        x="Rotational Speed (RPM)",
        y="Frequency (Hz)",
        color="Mode Shape",
    )
    + flavor_high_contrast_light()
    + theme(
        plot_title=element_text(size=28, hjust=0.5, face="bold"),
        axis_title=element_text(size=22),
        axis_text=element_text(size=18),
        legend_title=element_text(size=20, face="bold"),
        legend_text=element_text(size=18),
        legend_position="right",
        panel_grid_major=element_line(color="#E8E8E8", size=0.3),
        panel_grid_minor=element_blank(),
    )
    + ggsize(1600, 900)
)

# Save
ggsave(plot, "plot.png", path=".", scale=3)
ggsave(plot, "plot.html", path=".")
