""" pyplots.ai
eye-diagram-basic: Signal Integrity Eye Diagram
Library: bokeh 3.9.0 | Python 3.14.3
Quality: 85/100 | Created: 2026-03-17
"""

import numpy as np
from bokeh.io import export_png, save
from bokeh.models import ColorBar, LinearColorMapper
from bokeh.palettes import Inferno256
from bokeh.plotting import figure
from bokeh.resources import CDN


# Data - Simulate NRZ eye diagram
np.random.seed(42)

n_traces = 400
samples_per_ui = 150
n_bits = 3
total_samples = samples_per_ui * n_bits

noise_sigma = 0.05
jitter_sigma = 0.03

# Generate all traces
all_time = []
all_voltage = []

for _ in range(n_traces):
    bits = np.random.randint(0, 2, n_bits + 2)
    signal = np.zeros(total_samples)

    for i in range(n_bits):
        prev_bit = bits[i]
        curr_bit = bits[i + 1]

        t_local = np.linspace(0, 1, samples_per_ui)
        jitter = np.random.normal(0, jitter_sigma)

        if prev_bit != curr_bit:
            transition_point = 0.0 + jitter
            steepness = 12
            transition = 1 / (1 + np.exp(-steepness * (t_local - transition_point)))
            if prev_bit > curr_bit:
                segment = 1 - transition
            else:
                segment = transition
        else:
            segment = np.full(samples_per_ui, float(curr_bit))

        signal[i * samples_per_ui : (i + 1) * samples_per_ui] = segment

    signal += np.random.normal(0, noise_sigma, total_samples)

    # Extract 2-UI window centered on the middle bit
    start = samples_per_ui // 2
    end = start + 2 * samples_per_ui
    window_time = np.linspace(0, 2, end - start)
    window_voltage = signal[start:end]

    all_time.append(window_time)
    all_voltage.append(window_voltage)

all_time = np.array(all_time)
all_voltage = np.array(all_voltage)

# Build 2D histogram for density heatmap
time_bins = 300
voltage_bins = 200
time_edges = np.linspace(0, 2, time_bins + 1)
voltage_edges = np.linspace(-0.3, 1.3, voltage_bins + 1)

histogram, _, _ = np.histogram2d(all_time.ravel(), all_voltage.ravel(), bins=[time_edges, voltage_edges])

# Log-scale for better contrast
histogram = np.log1p(histogram).T

# Plot
p = figure(
    width=4800,
    height=2700,
    title="eye-diagram-basic · bokeh · pyplots.ai",
    x_axis_label="Time (UI)",
    y_axis_label="Voltage (V)",
    x_range=(0, 2),
    y_range=(-0.3, 1.3),
    min_border_right=250,
)

color_mapper = LinearColorMapper(palette=Inferno256, low=0, high=float(histogram.max()))

p.image(image=[histogram], x=0, y=-0.3, dw=2, dh=1.6, color_mapper=color_mapper)

color_bar = ColorBar(
    color_mapper=color_mapper,
    label_standoff=16,
    width=40,
    location=(0, 0),
    major_label_text_font_size="16pt",
    padding=20,
)
p.add_layout(color_bar, "right")

# Style
p.title.text_font_size = "28pt"
p.title.text_font_style = "normal"
p.xaxis.axis_label_text_font_size = "22pt"
p.yaxis.axis_label_text_font_size = "22pt"
p.xaxis.major_label_text_font_size = "18pt"
p.yaxis.major_label_text_font_size = "18pt"

p.xgrid.grid_line_alpha = 0.2
p.ygrid.grid_line_alpha = 0.2

p.background_fill_color = "#000000"
p.border_fill_color = "#ffffff"

p.xaxis.axis_line_color = "#666666"
p.yaxis.axis_line_color = "#666666"
p.xaxis.major_tick_line_color = "#666666"
p.yaxis.major_tick_line_color = "#666666"
p.xaxis.major_label_text_color = "#333333"
p.yaxis.major_label_text_color = "#333333"
p.xaxis.axis_label_text_color = "#333333"
p.yaxis.axis_label_text_color = "#333333"
p.title.text_color = "#333333"

p.xgrid.grid_line_color = "#444444"
p.ygrid.grid_line_color = "#444444"

p.outline_line_color = None

# Save
export_png(p, filename="plot.png")
save(p, filename="plot.html", resources=CDN, title="eye-diagram-basic · bokeh · pyplots.ai")
