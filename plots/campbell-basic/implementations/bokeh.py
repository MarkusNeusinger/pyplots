"""pyplots.ai
campbell-basic: Campbell Diagram
Library: bokeh 3.8.2 | Python 3.14.3
Quality: 80/100 | Created: 2026-02-15
"""

import numpy as np
from bokeh.io import export_png, output_file, save
from bokeh.models import BoxAnnotation, ColumnDataSource, HoverTool, Label, Legend, LegendItem, Range1d
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
critical_speed_labels = []

for order in engine_orders:
    eo_freq = eo_frequencies[order]
    for mode_name, mode_freq in modes.items():
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
                critical_speed_labels.append(f"{order}x × {mode_name}")

# Plot
p = figure(
    width=4800,
    height=2700,
    title="campbell-basic · bokeh · pyplots.ai",
    x_axis_label="Rotational Speed (RPM)",
    y_axis_label="Frequency (Hz)",
    x_range=Range1d(-100, 6300),
    y_range=Range1d(0, 200),
)

# Operating range shading (typical continuous operating range: 3000-5000 RPM)
operating_zone = BoxAnnotation(
    left=3000,
    right=5000,
    fill_color="#306998",
    fill_alpha=0.06,
    line_color="#306998",
    line_alpha=0.25,
    line_dash="dotted",
    line_width=2,
)
p.add_layout(operating_zone)

# Operating range label
op_label = Label(
    x=4000,
    y=5,
    text="Operating Range",
    text_font_size="16pt",
    text_color="#306998",
    text_alpha=0.6,
    text_align="center",
    text_font_style="italic",
)
p.add_layout(op_label)

# Danger zone highlighting around critical speeds within operating range
for rpm_val, freq_val in zip(critical_speeds_rpm, critical_speeds_freq, strict=False):
    if 3000 <= rpm_val <= 5000:
        danger = BoxAnnotation(
            left=rpm_val - 120,
            right=rpm_val + 120,
            bottom=freq_val - 4,
            top=freq_val + 4,
            fill_color="#D62728",
            fill_alpha=0.10,
            line_color=None,
        )
        p.add_layout(danger)

# Natural frequency mode colors (Python Blue first, then complementary)
mode_colors = ["#306998", "#E8A838", "#D64545", "#7A68A6", "#48A9A6"]

# Plot natural frequency curves
legend_items = []
for i, (mode_name, mode_freq) in enumerate(modes.items()):
    source = ColumnDataSource(data={"speed": speeds, "freq": mode_freq})
    line = p.line(x="speed", y="freq", source=source, line_width=5, line_color=mode_colors[i], line_alpha=0.95)
    legend_items.append(LegendItem(label=mode_name, renderers=[line]))

# Engine order lines (stronger visibility)
eo_color = "#444444"

for order in engine_orders:
    eo_freq = eo_frequencies[order]
    mask = eo_freq <= 200
    clipped_speeds = speeds[mask]
    clipped_freq = eo_freq[mask]

    source = ColumnDataSource(data={"speed": clipped_speeds, "freq": clipped_freq})
    line = p.line(
        x="speed", y="freq", source=source, line_width=3, line_color=eo_color, line_dash=[12, 8], line_alpha=0.8
    )
    legend_items.append(LegendItem(label=f"{order}x EO", renderers=[line]))

# Engine order labels positioned clearly along each line
for order in engine_orders:
    freq_at_max = order * 6000 / 60
    if freq_at_max > 195:
        label_rpm = 193 * 60 / order
        label_freq = 190
    else:
        label_rpm = 5800
        label_freq = freq_at_max

    label = Label(
        x=label_rpm,
        y=label_freq,
        text=f" {order}x",
        text_font_size="22pt",
        text_color="#333333",
        text_font_style="bold",
        text_baseline="middle",
    )
    p.add_layout(label)

# Critical speed markers with hover tooltip
if critical_speeds_rpm:
    crit_source = ColumnDataSource(
        data={
            "rpm": critical_speeds_rpm,
            "freq": critical_speeds_freq,
            "label": critical_speed_labels,
            "rpm_display": [f"{r:.0f}" for r in critical_speeds_rpm],
            "freq_display": [f"{f:.1f}" for f in critical_speeds_freq],
        }
    )
    crit_scatter = p.scatter(
        x="rpm",
        y="freq",
        source=crit_source,
        marker="diamond",
        size=32,
        fill_color="#D62728",
        line_color="white",
        line_width=3,
        fill_alpha=0.95,
    )
    legend_items.append(LegendItem(label="Critical Speed", renderers=[crit_scatter]))

    # HoverTool for critical speed details (Bokeh distinctive feature)
    hover = HoverTool(
        renderers=[crit_scatter],
        tooltips=[("Intersection", "@label"), ("RPM", "@rpm_display"), ("Frequency", "@freq_display Hz")],
        mode="mouse",
    )
    p.add_tools(hover)

# Legend inside the plot for balanced layout
legend = Legend(
    items=legend_items,
    location="top_left",
    label_text_font_size="18pt",
    glyph_width=60,
    glyph_height=32,
    spacing=14,
    padding=20,
    background_fill_color="#FFFFFF",
    background_fill_alpha=0.92,
    border_line_color="#CCCCCC",
    border_line_alpha=0.3,
    border_line_width=1,
)
p.add_layout(legend)

# Title styling
p.title.text_font_size = "28pt"
p.title.align = "center"
p.title.text_color = "#222222"

# Axis styling
p.xaxis.axis_label_text_font_size = "22pt"
p.yaxis.axis_label_text_font_size = "22pt"
p.xaxis.major_label_text_font_size = "18pt"
p.yaxis.major_label_text_font_size = "18pt"
p.xaxis.axis_label_text_color = "#333333"
p.yaxis.axis_label_text_color = "#333333"
p.xaxis.major_label_text_color = "#555555"
p.yaxis.major_label_text_color = "#555555"
p.xaxis.axis_line_color = "#AAAAAA"
p.yaxis.axis_line_color = "#AAAAAA"
p.xaxis.major_tick_line_color = "#AAAAAA"
p.yaxis.major_tick_line_color = "#AAAAAA"
p.xaxis.minor_tick_line_color = None
p.yaxis.minor_tick_line_color = None

# Grid styling (subtle)
p.xgrid.grid_line_color = "#DDDDDD"
p.xgrid.grid_line_alpha = 0.5
p.ygrid.grid_line_color = "#DDDDDD"
p.ygrid.grid_line_alpha = 0.5

# Background and frame
p.background_fill_color = "#FAFAFA"
p.border_fill_color = "#FFFFFF"
p.outline_line_color = None

# Save
export_png(p, filename="plot.png")

output_file("plot.html")
save(p)
