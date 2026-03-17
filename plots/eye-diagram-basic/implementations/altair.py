""" pyplots.ai
eye-diagram-basic: Signal Integrity Eye Diagram
Library: altair 6.0.0 | Python 3.14.3
Quality: 79/100 | Created: 2026-03-17
"""

import altair as alt
import numpy as np
import pandas as pd


# Data
np.random.seed(42)

n_traces = 300
samples_per_ui = 200
amplitude = 1.0
noise_sigma = 0.05 * amplitude
jitter_sigma = 0.03

n_bits = n_traces + 4
bits = np.random.randint(0, 2, n_bits)

samples_per_bit = samples_per_ui
total_signal_len = n_bits * samples_per_bit
t_full = np.arange(total_signal_len) / samples_per_bit

signal_full = np.zeros(total_signal_len)
for i in range(total_signal_len):
    bit_idx = int(t_full[i])
    if bit_idx >= n_bits:
        bit_idx = n_bits - 1
    frac = t_full[i] - bit_idx

    current_level = bits[bit_idx] * amplitude
    prev_level = bits[bit_idx - 1] * amplitude if bit_idx > 0 else bits[0] * amplitude

    transition_width = 0.12
    blend = 1.0 / (1.0 + np.exp(-14 * (frac - transition_width) / transition_width))
    signal_full[i] = prev_level + (current_level - prev_level) * blend

signal_full += np.random.normal(0, noise_sigma, total_signal_len)

all_time = []
all_voltage = []
window_samples = 2 * samples_per_ui

for trace in range(n_traces):
    start_bit = trace + 1
    start_sample = start_bit * samples_per_bit
    end_sample = start_sample + window_samples

    if end_sample > total_signal_len:
        break

    jitter_offset = np.random.normal(0, jitter_sigma)
    trace_time = np.linspace(0, 2, window_samples) + jitter_offset
    trace_voltage = signal_full[start_sample:end_sample]

    all_time.extend(trace_time.tolist())
    all_voltage.extend(trace_voltage.tolist())

# Pre-bin into 2D histogram for density heatmap
time_bins = 250
voltage_bins = 150
time_edges = np.linspace(-0.1, 2.1, time_bins + 1)
voltage_edges = np.linspace(-0.25, 1.25, voltage_bins + 1)

hist, _, _ = np.histogram2d(all_time, all_voltage, bins=[time_edges, voltage_edges])

time_centers = (time_edges[:-1] + time_edges[1:]) / 2
voltage_centers = (voltage_edges[:-1] + voltage_edges[1:]) / 2

rows = []
for i in range(time_bins):
    for j in range(voltage_bins):
        if hist[i, j] > 0:
            rows.append(
                {
                    "time_ui": round(time_centers[i], 4),
                    "voltage_v": round(voltage_centers[j], 4),
                    "density": float(hist[i, j]),
                }
            )

df = pd.DataFrame(rows)
df["log_density"] = np.log1p(df["density"])

# Plot
time_step = float(time_edges[1] - time_edges[0])
voltage_step = float(voltage_edges[1] - voltage_edges[0])

chart = (
    alt.Chart(df)
    .mark_rect()
    .encode(
        x=alt.X("time_ui:Q", bin=alt.Bin(step=time_step), title="Time (UI)", scale=alt.Scale(domain=[0, 2])),
        y=alt.Y(
            "voltage_v:Q", bin=alt.Bin(step=voltage_step), title="Voltage (V)", scale=alt.Scale(domain=[-0.2, 1.2])
        ),
        color=alt.Color("sum(log_density):Q", scale=alt.Scale(scheme="inferno"), legend=None),
    )
    .properties(
        width=1600, height=900, title=alt.Title("eye-diagram-basic · altair · pyplots.ai", fontSize=28, fontWeight=500)
    )
    .configure_axis(labelFontSize=18, titleFontSize=22, grid=False)
    .configure_view(stroke=None)
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
