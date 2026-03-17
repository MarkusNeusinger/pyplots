""" pyplots.ai
heatmap-chromagram: Music Chromagram (Pitch Class Distribution over Time)
Library: plotly 6.6.0 | Python 3.14.3
Quality: 87/100 | Created: 2026-03-17
"""

import numpy as np
import plotly.graph_objects as go


# Data
np.random.seed(42)

pitch_classes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
n_frames = 120
frame_duration = 0.05
time_frames = np.arange(n_frames) * frame_duration

# Chord profiles (energy distribution across 12 pitch classes)
c_major = np.array([1.0, 0.05, 0.1, 0.05, 0.8, 0.1, 0.05, 0.7, 0.05, 0.1, 0.05, 0.1])
g_major = np.array([0.1, 0.05, 0.7, 0.05, 0.1, 0.05, 0.05, 1.0, 0.05, 0.1, 0.05, 0.8])
a_minor = np.array([0.7, 0.05, 0.1, 0.05, 0.8, 0.1, 0.05, 0.1, 0.05, 1.0, 0.05, 0.1])
f_major = np.array([0.8, 0.05, 0.1, 0.05, 0.1, 1.0, 0.05, 0.1, 0.05, 0.7, 0.05, 0.1])

# Build chromagram with chord progression: C -> G -> Am -> F (repeated)
chords = [c_major, g_major, a_minor, f_major]
segment_length = n_frames // len(chords)

energy = np.zeros((12, n_frames))
for i, chord in enumerate(chords):
    start = i * segment_length
    end = start + segment_length if i < len(chords) - 1 else n_frames
    for t in range(start, end):
        noise = np.random.normal(0, 0.06, 12)
        energy[:, t] = np.clip(chord + noise, 0, 1.2)

# Smooth transitions between chords
for i in range(1, len(chords)):
    boundary = i * segment_length
    blend_width = 4
    for offset in range(-blend_width, blend_width):
        t = boundary + offset
        if 0 <= t < n_frames:
            alpha = (offset + blend_width) / (2 * blend_width)
            prev_chord = chords[i - 1]
            curr_chord = chords[i]
            blended = (1 - alpha) * prev_chord + alpha * curr_chord
            noise = np.random.normal(0, 0.04, 12)
            energy[:, t] = np.clip(blended + noise, 0, 1.2)

# Plot
fig = go.Figure(
    data=go.Heatmap(
        z=energy,
        x=np.round(time_frames, 2),
        y=pitch_classes,
        colorscale="Inferno",
        colorbar={
            "title": {"text": "Energy", "font": {"size": 20}},
            "tickfont": {"size": 16},
            "thickness": 18,
            "len": 0.85,
        },
        hoverongaps=False,
        hovertemplate="Time: %{x}s<br>Pitch: %{y}<br>Energy: %{z:.2f}<extra></extra>",
    )
)

# Style
fig.update_layout(
    title={"text": "heatmap-chromagram · plotly · pyplots.ai", "font": {"size": 28}, "x": 0.5, "xanchor": "center"},
    xaxis={
        "title": {"text": "Time (seconds)", "font": {"size": 22}},
        "tickfont": {"size": 16},
        "showgrid": False,
        "dtick": 0.5,
    },
    yaxis={
        "title": {"text": "Pitch Class", "font": {"size": 22}},
        "tickfont": {"size": 16},
        "showgrid": False,
        "categoryorder": "array",
        "categoryarray": pitch_classes,
    },
    template="plotly_white",
    plot_bgcolor="white",
    margin={"l": 80, "r": 40, "t": 80, "b": 60},
)

# Save
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html", include_plotlyjs="cdn")
