""" pyplots.ai
campbell-basic: Campbell Diagram
Library: letsplot 4.8.2 | Python 3.14.3
Quality: 86/100 | Created: 2026-02-15
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
        "Series": np.repeat(mode_names, len(speed_rpm)),
    }
)

# Engine order lines: frequency = order * speed_rpm / 60
# Clip to max_freq range for cleaner display
orders = [1, 2, 3]
order_labels = ["1×", "2×", "3×"]

eo_rows = []
for order, label in zip(orders, order_labels):
    max_speed_for_order = min(6000, max_freq * 60 / order)
    eo_speed = np.array([0, max_speed_for_order])
    eo_freq = order * eo_speed / 60
    eo_rows.append(pd.DataFrame({"Speed": eo_speed, "Frequency": eo_freq, "Series": label}))
eo_df = pd.concat(eo_rows, ignore_index=True)

# Find critical speed intersections (where EO lines cross mode curves)
critical_speeds = []
critical_freqs = []
for order in orders:
    eo_freq_at_speeds = order * speed_rpm / 60
    for mode_freq in mode_data:
        diff = eo_freq_at_speeds - mode_freq
        sign_changes = np.where(np.diff(np.sign(diff)))[0]
        for idx in sign_changes:
            frac = abs(diff[idx]) / (abs(diff[idx]) + abs(diff[idx + 1]))
            crit_speed = speed_rpm[idx] + frac * (speed_rpm[idx + 1] - speed_rpm[idx])
            crit_freq = order * crit_speed / 60
            if crit_freq <= max_freq:
                critical_speeds.append(crit_speed)
                critical_freqs.append(crit_freq)

crit_df = pd.DataFrame({"Speed": critical_speeds, "Frequency": critical_freqs})

# EO label positions (near the end of each EO line, offset slightly)
eo_label_rows = []
for order, label in zip(orders, order_labels):
    label_speed = min(5600, (max_freq - 3) * 60 / order)
    label_freq = order * label_speed / 60 + 2
    eo_label_rows.append({"Speed": label_speed, "Frequency": label_freq, "Label": label})
eo_label_df = pd.DataFrame(eo_label_rows)

# Color palette
mode_colors = ["#306998", "#2CA02C", "#8C564B", "#7F7F7F"]
eo_color = "#B0B0B0"

# Plot
plot = (
    ggplot()
    + geom_line(data=modes_df, mapping=aes(x="Speed", y="Frequency", color="Series"), size=2.5)
    + geom_line(
        data=eo_df, mapping=aes(x="Speed", y="Frequency", group="Series"), color=eo_color, size=1.0, linetype="dashed"
    )
    + geom_point(data=crit_df, mapping=aes(x="Speed", y="Frequency"), color="#D62728", fill="#D62728", size=6, shape=18)
    + geom_text(
        data=eo_label_df,
        mapping=aes(x="Speed", y="Frequency", label="Label"),
        color="#888888",
        size=14,
        fontface="bold",
    )
    + scale_color_manual(values=mode_colors)
    + scale_y_continuous(limits=[0, max_freq])
    + scale_x_continuous(limits=[0, 6000])
    + labs(
        title="campbell-basic · letsplot · pyplots.ai",
        x="Rotational Speed (RPM)",
        y="Frequency (Hz)",
        color="Mode Shape",
    )
    + theme_minimal()
    + theme(
        plot_title=element_text(size=28, hjust=0.5),
        axis_title=element_text(size=22),
        axis_text=element_text(size=18),
        legend_title=element_text(size=20),
        legend_text=element_text(size=18),
        legend_position="right",
        panel_grid_major=element_line(color="#E0E0E0", size=0.4),
        panel_grid_minor=element_blank(),
    )
    + ggsize(1600, 900)
)

# Save
ggsave(plot, "plot.png", path=".", scale=3)
ggsave(plot, "plot.html", path=".")
