""" pyplots.ai
campbell-basic: Campbell Diagram
Library: bokeh 3.8.2 | Python 3.14.3
Quality: 80/100 | Created: 2026-02-15
"""

import numpy as np
from bokeh.io import export_png, output_file, save
from bokeh.models import ColumnDataSource, Label, Legend
from bokeh.plotting import figure


# Data
np.random.seed(42)
speeds = np.linspace(0, 6000, 100)

# Natural frequency modes (Hz) with realistic rotordynamic behavior
# Gyroscopic stiffening raises forward-whirl modes, lowers backward-whirl modes
mode_1_bending = 22 + 0.003 * speeds + 1.2 * np.sin(speeds / 3000 * np.pi)
mode_2_bending = 55 - 0.0015 * speeds + 0.8 * np.sin(speeds / 2500 * np.pi)
mode_1_torsional = 78 + 0.002 * speeds
mode_axial = 105 + 0.0008 * speeds - 0.5 * np.sin(speeds / 4000 * np.pi)
mode_3_bending = 140 - 0.003 * speeds + 1.5 * np.cos(speeds / 3500 * np.pi)

modes = {
    "1st Bending": mode_1_bending,
    "2nd Bending": mode_2_bending,
    "1st Torsional": mode_1_torsional,
    "Axial": mode_axial,
    "3rd Bending": mode_3_bending,
}

# Engine order lines: frequency = order * speed / 60
engine_orders = [1, 2, 3]
eo_frequencies = {order: order * speeds / 60 for order in engine_orders}

# Find critical speed intersections
critical_speeds_rpm = []
critical_speeds_freq = []

for order in engine_orders:
    eo_freq = eo_frequencies[order]
    for mode_freq in modes.values():
        diff = eo_freq - mode_freq
        sign_changes = np.where(np.diff(np.sign(diff)))[0]
        for idx in sign_changes:
            denom = abs(diff[idx]) + abs(diff[idx + 1])
            if denom == 0:
                continue
            frac = abs(diff[idx]) / denom
            rpm_interp = speeds[idx] + frac * (speeds[idx + 1] - speeds[idx])
            freq_interp = mode_freq[idx] + frac * (mode_freq[idx + 1] - mode_freq[idx])
            if 100 < rpm_interp < 5900 and 5 < freq_interp < 195:
                critical_speeds_rpm.append(rpm_interp)
                critical_speeds_freq.append(freq_interp)

# Plot
p = figure(
    width=4800,
    height=2700,
    title="campbell-basic \u00b7 bokeh \u00b7 pyplots.ai",
    x_axis_label="Rotational Speed (RPM)",
    y_axis_label="Frequency (Hz)",
    x_range=(-100, 6300),
    y_range=(0, 200),
)

# Natural frequency mode colors (Python Blue first, then complementary)
mode_colors = ["#306998", "#E8A838", "#D64545", "#7A68A6", "#48A9A6"]

# Plot natural frequency curves
legend_items = []
for i, (mode_name, mode_freq) in enumerate(modes.items()):
    source = ColumnDataSource(data={"speed": speeds, "freq": mode_freq})
    line = p.line(x="speed", y="freq", source=source, line_width=5, line_color=mode_colors[i], line_alpha=0.95)
    legend_items.append((mode_name, [line]))

# Engine order lines (distinct gray shades with clear dash pattern)
eo_colors = ["#555555", "#777777", "#999999"]

for j, order in enumerate(engine_orders):
    eo_freq = eo_frequencies[order]
    # Clip engine order lines to y_range for cleaner appearance
    mask = eo_freq <= 200
    clipped_speeds = speeds[mask]
    clipped_freq = eo_freq[mask]

    source = ColumnDataSource(data={"speed": clipped_speeds, "freq": clipped_freq})
    line = p.line(
        x="speed", y="freq", source=source, line_width=3, line_color=eo_colors[j], line_dash="dashed", line_alpha=0.65
    )
    legend_items.append((f"{order}x EO", [line]))

# Engine order labels near top of each line
for order in engine_orders:
    freq_at_max = order * 6000 / 60
    if freq_at_max > 195:
        # Place label where line hits top of plot
        label_rpm = 195 * 60 / order
        label_freq = 193
    else:
        label_rpm = 5950
        label_freq = freq_at_max - 3

    label = Label(
        x=label_rpm,
        y=label_freq,
        text=f" {order}x",
        text_font_size="20pt",
        text_color="#444444",
        text_font_style="bold",
    )
    p.add_layout(label)

# Critical speed markers
if critical_speeds_rpm:
    crit_source = ColumnDataSource(data={"rpm": critical_speeds_rpm, "freq": critical_speeds_freq})
    crit_scatter = p.scatter(
        x="rpm",
        y="freq",
        source=crit_source,
        marker="diamond",
        size=30,
        fill_color="#D62728",
        line_color="white",
        line_width=2.5,
        fill_alpha=0.95,
    )
    legend_items.append(("Critical Speed", [crit_scatter]))

# Legend
legend = Legend(
    items=legend_items,
    location="top_left",
    label_text_font_size="18pt",
    glyph_width=50,
    glyph_height=28,
    spacing=12,
    padding=20,
    background_fill_alpha=0.85,
    border_line_alpha=0.2,
)
p.add_layout(legend, "right")

# Title styling
p.title.text_font_size = "28pt"
p.title.align = "center"

# Axis styling
p.xaxis.axis_label_text_font_size = "22pt"
p.yaxis.axis_label_text_font_size = "22pt"
p.xaxis.major_label_text_font_size = "18pt"
p.yaxis.major_label_text_font_size = "18pt"

# Grid styling
p.xgrid.grid_line_alpha = 0.15
p.ygrid.grid_line_alpha = 0.15

# Background and frame
p.background_fill_color = "#FFFFFF"
p.border_fill_color = "#FFFFFF"
p.outline_line_color = None

# Save
export_png(p, filename="plot.png")

output_file("plot.html")
save(p)
