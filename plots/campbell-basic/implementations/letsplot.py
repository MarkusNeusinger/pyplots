"""pyplots.ai
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
max_freq = 120

# Natural frequency modes (Hz) with realistic speed-dependent variation
# Gyroscopic effects cause slight frequency shifts with speed
modes = {
    "1st Bending": 25 + 0.0008 * speed_rpm + np.random.normal(0, 0.15, 80),
    "1st Torsional": 48 - 0.0005 * speed_rpm + np.random.normal(0, 0.12, 80),
    "2nd Bending": 72 + 0.0012 * speed_rpm + np.random.normal(0, 0.18, 80),
    "2nd Torsional": 88 + 0.0006 * speed_rpm + np.random.normal(0, 0.14, 80),
    "Axial": 105 - 0.0003 * speed_rpm + np.random.normal(0, 0.10, 80),
}

# Build long-format DataFrame for natural frequency modes
modes_df = pd.concat(
    [pd.DataFrame({"Speed": speed_rpm, "Frequency": freq, "Mode": name}) for name, freq in modes.items()],
    ignore_index=True,
)

# Engine order lines: frequency = order * speed_rpm / 60
orders = [1, 2, 3]
order_labels = ["1\u00d7", "2\u00d7", "3\u00d7"]

eo_frames = []
for order, label in zip(orders, order_labels):
    max_speed_for_order = min(6000, max_freq * 60 / order)
    eo_speed = np.linspace(0, max_speed_for_order, 80)
    eo_frames.append(pd.DataFrame({"Speed": eo_speed, "Frequency": order * eo_speed / 60, "Line Type": label}))
eo_df = pd.concat(eo_frames, ignore_index=True)

# Find critical speed intersections (where EO lines cross mode curves)
critical_rows = []
for order, olabel in zip(orders, order_labels):
    eo_freq_at_speeds = order * speed_rpm / 60
    for mname, mode_freq in modes.items():
        diff = eo_freq_at_speeds - mode_freq
        sign_changes = np.where(np.diff(np.sign(diff)))[0]
        for idx in sign_changes:
            frac = abs(diff[idx]) / (abs(diff[idx]) + abs(diff[idx + 1]))
            crit_speed = speed_rpm[idx] + frac * (speed_rpm[idx + 1] - speed_rpm[idx])
            crit_freq = order * crit_speed / 60
            if crit_freq <= max_freq:
                critical_rows.append(
                    {"Speed": crit_speed, "Frequency": crit_freq, "Intersection": f"{mname} \u00d7 {olabel}"}
                )

crit_df = pd.DataFrame(critical_rows)

# EO label positions along each line, avoiding legend area
eo_label_speeds = {1: 4800, 2: 3200, 3: 2000}
eo_label_df = pd.DataFrame(
    [
        {"Speed": eo_label_speeds[o], "Frequency": o * eo_label_speeds[o] / 60 + 3, "Label": l}
        for o, l in zip(orders, order_labels)
    ]
)

# Highlight zones around critical speeds
zone_df = pd.DataFrame(
    [
        {"xmin": s - 120, "xmax": s + 120, "ymin": f - 3, "ymax": f + 3}
        for s, f in zip(crit_df["Speed"], crit_df["Frequency"])
    ]
)

# Colorblind-safe palette for 5 modes
mode_colors = ["#306998", "#E67E22", "#17A589", "#C0392B", "#8E44AD"]
mode_order = list(modes.keys())
eo_line_color = "#999999"

# Plot
plot = (
    ggplot()
    # Subtle highlight zones around critical speed intersections
    + geom_rect(
        data=zone_df,
        mapping=aes(xmin="xmin", xmax="xmax", ymin="ymin", ymax="ymax"),
        fill="#D62728",
        alpha=0.07,
        color="transparent",
    )
    # Engine order lines mapped to Line Type for legend inclusion
    + geom_line(data=eo_df, mapping=aes(x="Speed", y="Frequency", linetype="Line Type"), color=eo_line_color, size=0.8)
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
        size=14,
        fontface="bold",
    )
    + scale_color_manual(name="Natural Frequency", values=mode_colors, limits=mode_order)
    + scale_linetype_manual(name="Engine Order", values=["dashed", "dashed", "dashed"])
    + scale_y_continuous(limits=[0, max_freq], expand=[0, 2])
    + scale_x_continuous(limits=[0, 6100], format=",d")
    + guides(linetype=guide_legend(override_aes={"color": eo_line_color}))
    + labs(
        title="campbell-basic \u00b7 letsplot \u00b7 pyplots.ai",
        subtitle="Critical speeds (red diamonds) mark resonance risk where engine excitation orders cross natural frequency modes",
        x="Rotational Speed (RPM)",
        y="Frequency (Hz)",
    )
    + flavor_high_contrast_light()
    + theme(
        plot_title=element_text(size=28, hjust=0.5, face="bold"),
        plot_subtitle=element_text(size=16, hjust=0.5, color="#555555"),
        axis_title=element_text(size=22),
        axis_text=element_text(size=18),
        legend_title=element_text(size=18, face="bold"),
        legend_text=element_text(size=16),
        legend_position=[0.98, 0.02],
        legend_justification=[1, 0],
        legend_background=element_rect(fill="white", color="#CCCCCC", size=0.5),
        panel_grid_major=element_line(color="#E0E0E0", size=0.3),
        panel_grid_minor=element_blank(),
        axis_line=element_line(color="#BBBBBB", size=0.5),
    )
    + ggsize(1600, 900)
)

# Save
ggsave(plot, "plot.png", path=".", scale=3)
ggsave(plot, "plot.html", path=".")
