""" pyplots.ai
eye-diagram-basic: Signal Integrity Eye Diagram
Library: plotly 6.6.0 | Python 3.14.3
Quality: 89/100 | Created: 2026-03-17
"""

import numpy as np
import plotly.graph_objects as go


# Data
np.random.seed(42)

n_traces = 400
samples_per_ui = 150
n_ui = 2
total_samples = n_ui * samples_per_ui

# Time axis normalized to unit intervals
time = np.linspace(0, n_ui, total_samples)

# Generate random NRZ bit sequences (3 bits to cover 2 UI with transitions)
n_bits = 4
bit_sequences = np.random.randint(0, 2, size=(n_traces, n_bits))

# Build smooth NRZ waveforms with raised-cosine transitions
rolloff = 0.15  # Transition sharpness (fraction of UI)
noise_sigma = 0.05  # 5% of amplitude
jitter_sigma = 0.03  # 3% of UI

all_time = []
all_voltage = []

for i in range(n_traces):
    bits = bit_sequences[i]
    trace_jitter = np.random.normal(0, jitter_sigma, n_bits)
    voltage = np.zeros(total_samples)

    for t_idx, t in enumerate(time):
        # Determine which bit we're in (with jitter on transitions)
        signal = float(bits[0])
        for b in range(1, n_bits):
            transition_time = b - 1.0 + trace_jitter[b]
            # Sigmoid-like raised cosine transition
            transition = 0.5 * (1 + np.tanh((t - transition_time) / rolloff))
            signal = signal * (1 - transition) + float(bits[b]) * transition
        voltage[t_idx] = signal

    # Add Gaussian noise
    voltage += np.random.normal(0, noise_sigma, total_samples)

    all_time.extend(time)
    all_voltage.extend(voltage)

all_time = np.array(all_time)
all_voltage = np.array(all_voltage)

# Plot - density heatmap using Histogram2d
fig = go.Figure(
    data=go.Histogram2d(
        x=all_time,
        y=all_voltage,
        nbinsx=300,
        nbinsy=200,
        colorscale=[
            [0.0, "#0d0d2b"],
            [0.05, "#1a0a4e"],
            [0.15, "#3b0f8a"],
            [0.3, "#6a1cb4"],
            [0.5, "#c23a6e"],
            [0.7, "#ef6d35"],
            [0.85, "#f5b731"],
            [1.0, "#fef200"],
        ],
        colorbar={
            "title": {"text": "Trace Density", "font": {"size": 20}},
            "tickfont": {"size": 16},
            "thickness": 18,
            "len": 0.75,
            "outlinewidth": 0,
        },
        hovertemplate="Time: %{x:.2f} UI<br>Voltage: %{y:.3f} V<br>Density: %{z}<extra></extra>",
    )
)

# Layout
fig.update_layout(
    title={
        "text": "eye-diagram-basic · plotly · pyplots.ai",
        "font": {"size": 28, "color": "#e0e0e0"},
        "x": 0.5,
        "xanchor": "center",
        "y": 0.97,
        "yanchor": "top",
    },
    xaxis={
        "title": {"text": "Time (UI)", "font": {"size": 22, "color": "#cccccc"}},
        "tickfont": {"size": 18, "color": "#aaaaaa"},
        "tickvals": [0, 0.5, 1.0, 1.5, 2.0],
        "gridcolor": "rgba(255,255,255,0.08)",
        "zeroline": False,
    },
    yaxis={
        "title": {"text": "Voltage (V)", "font": {"size": 22, "color": "#cccccc"}},
        "tickfont": {"size": 18, "color": "#aaaaaa"},
        "gridcolor": "rgba(255,255,255,0.08)",
        "zeroline": False,
    },
    template="plotly_dark",
    paper_bgcolor="#0d0d2b",
    plot_bgcolor="#0d0d2b",
    margin={"l": 80, "r": 60, "t": 80, "b": 65},
    width=1600,
    height=900,
)

# Save
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html", include_plotlyjs="cdn")
