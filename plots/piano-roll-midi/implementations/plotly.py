"""pyplots.ai
piano-roll-midi: MIDI Piano Roll Visualization
Library: plotly | Python 3.13
Quality: pending | Created: 2026-03-07
"""

import numpy as np
import plotly.graph_objects as go


# Data - C major chord progression (I-V-vi-IV) with melody over 4 measures
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
BLACK_KEY_INDICES = {1, 3, 6, 8, 10}

notes = [
    # (start_beat, duration, midi_pitch, velocity)
    # Measure 1 - C major chord
    (0.0, 2.0, 48, 80),
    (0.0, 2.0, 52, 75),
    (0.0, 2.0, 55, 70),
    (0.0, 0.5, 72, 100),
    (0.5, 0.5, 74, 95),
    (1.0, 1.0, 76, 110),
    (2.0, 2.0, 48, 78),
    (2.0, 2.0, 52, 73),
    (2.0, 2.0, 55, 68),
    (2.0, 0.75, 79, 105),
    (2.75, 0.25, 76, 85),
    (3.0, 1.0, 77, 100),
    # Measure 2 - G major chord
    (4.0, 2.0, 43, 82),
    (4.0, 2.0, 47, 76),
    (4.0, 2.0, 55, 72),
    (4.0, 0.5, 76, 108),
    (4.5, 0.5, 74, 90),
    (5.0, 1.0, 72, 100),
    (6.0, 2.0, 43, 80),
    (6.0, 2.0, 47, 74),
    (6.0, 2.0, 55, 70),
    (6.0, 1.0, 74, 95),
    (7.0, 0.5, 72, 88),
    (7.5, 0.5, 71, 92),
    # Measure 3 - A minor chord
    (8.0, 2.0, 45, 85),
    (8.0, 2.0, 48, 78),
    (8.0, 2.0, 52, 72),
    (8.0, 1.0, 72, 112),
    (9.0, 0.5, 74, 96),
    (9.5, 0.5, 76, 90),
    (10.0, 2.0, 45, 83),
    (10.0, 2.0, 48, 76),
    (10.0, 2.0, 52, 70),
    (10.0, 1.5, 76, 105),
    (11.5, 0.5, 74, 88),
    # Measure 4 - F major chord
    (12.0, 2.0, 41, 88),
    (12.0, 2.0, 45, 80),
    (12.0, 2.0, 48, 74),
    (12.0, 1.0, 72, 115),
    (13.0, 0.5, 71, 92),
    (13.5, 0.5, 69, 85),
    (14.0, 2.0, 41, 86),
    (14.0, 2.0, 45, 78),
    (14.0, 2.0, 48, 72),
    (14.0, 2.0, 72, 120),
]

starts = np.array([n[0] for n in notes])
durations = np.array([n[1] for n in notes])
pitches = np.array([n[2] for n in notes])
velocities = np.array([n[3] for n in notes])

pitch_min = int(pitches.min()) - 1
pitch_max = int(pitches.max()) + 1
total_beats = 16
beats_per_measure = 4

# Plot
fig = go.Figure()

# Background shading for black keys
for p in range(pitch_min, pitch_max + 1):
    if (p % 12) in BLACK_KEY_INDICES:
        fig.add_shape(
            type="rect",
            x0=0,
            x1=total_beats,
            y0=p - 0.5,
            y1=p + 0.5,
            fillcolor="rgba(0, 0, 0, 0.06)",
            line={"width": 0},
            layer="below",
        )

# Measure boundary lines (thicker)
for m in range(total_beats // beats_per_measure + 1):
    fig.add_shape(
        type="line",
        x0=m * beats_per_measure,
        x1=m * beats_per_measure,
        y0=pitch_min - 0.5,
        y1=pitch_max + 0.5,
        line={"color": "rgba(0, 0, 0, 0.3)", "width": 2},
        layer="below",
    )

# Beat grid lines (thinner)
for b in range(total_beats + 1):
    if b % beats_per_measure != 0:
        fig.add_shape(
            type="line",
            x0=b,
            x1=b,
            y0=pitch_min - 0.5,
            y1=pitch_max + 0.5,
            line={"color": "rgba(0, 0, 0, 0.08)", "width": 1},
            layer="below",
        )

# Horizontal pitch grid lines
for p in range(pitch_min, pitch_max + 2):
    fig.add_shape(
        type="line",
        x0=0,
        x1=total_beats,
        y0=p - 0.5,
        y1=p - 0.5,
        line={"color": "rgba(0, 0, 0, 0.06)", "width": 1},
        layer="below",
    )

# Color interpolation: blue (soft/pp) to red (loud/ff)
vel_normalized = (velocities - velocities.min()) / (velocities.max() - velocities.min())
r_vals = (59 + vel_normalized * (239 - 59)).astype(int)
g_vals = (130 + vel_normalized * (68 - 130)).astype(int)
b_vals = (246 + vel_normalized * (68 - 246)).astype(int)

# Note rectangles
for i in range(len(notes)):
    fig.add_shape(
        type="rect",
        x0=starts[i],
        x1=starts[i] + durations[i],
        y0=pitches[i] - 0.4,
        y1=pitches[i] + 0.4,
        fillcolor=f"rgb({r_vals[i]}, {g_vals[i]}, {b_vals[i]})",
        line={"color": "white", "width": 1.5},
        layer="above",
        opacity=0.92,
    )

# Velocity colorscale
colorscale = [[0.0, "#3B82F6"], [0.3, "#6366F1"], [0.6, "#F59E0B"], [1.0, "#EF4444"]]

# Invisible scatter for hover info and colorbar
hover_labels = [
    f"{NOTE_NAMES[p % 12]}{p // 12 - 1}<br>Beat: {s:.1f}<br>Duration: {d:.1f}<br>Velocity: {v}" for s, d, p, v in notes
]
fig.add_trace(
    go.Scatter(
        x=starts + durations / 2,
        y=pitches,
        mode="markers",
        marker={
            "size": 1,
            "opacity": 0,
            "color": velocities,
            "colorscale": colorscale,
            "colorbar": {
                "title": {"text": "Velocity", "font": {"size": 20}},
                "tickfont": {"size": 16},
                "thickness": 20,
                "len": 0.6,
            },
            "cmin": int(velocities.min()),
            "cmax": int(velocities.max()),
        },
        text=hover_labels,
        hoverinfo="text",
        showlegend=False,
    )
)

# Y-axis: note names
pitch_range = list(range(pitch_min, pitch_max + 1))
tick_labels = [f"{NOTE_NAMES[p % 12]}{p // 12 - 1}" for p in pitch_range]

# X-axis: measure.beat labels
beat_ticks = list(range(total_beats + 1))
beat_labels = [f"M{b // beats_per_measure + 1}.{b % beats_per_measure + 1}" for b in beat_ticks]

# Style
fig.update_layout(
    title={"text": "piano-roll-midi · plotly · pyplots.ai", "font": {"size": 28}, "x": 0.5, "xanchor": "center"},
    xaxis={
        "title": {"text": "Beat Position", "font": {"size": 22}},
        "tickvals": beat_ticks,
        "ticktext": beat_labels,
        "tickfont": {"size": 14},
        "range": [-0.2, total_beats + 0.2],
        "showgrid": False,
    },
    yaxis={
        "title": {"text": "Pitch", "font": {"size": 22}},
        "tickvals": pitch_range,
        "ticktext": tick_labels,
        "tickfont": {"size": 14},
        "range": [pitch_min - 0.8, pitch_max + 0.8],
        "showgrid": False,
    },
    template="plotly_white",
    margin={"l": 100, "r": 100, "t": 100, "b": 80},
    plot_bgcolor="white",
)

# Save
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html", include_plotlyjs="cdn")
