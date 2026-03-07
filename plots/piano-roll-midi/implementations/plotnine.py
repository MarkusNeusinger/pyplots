""" pyplots.ai
piano-roll-midi: MIDI Piano Roll Visualization
Library: plotnine 0.15.3 | Python 3.14.3
Quality: 88/100 | Created: 2026-03-07
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    coord_cartesian,
    element_line,
    element_rect,
    element_text,
    geom_rect,
    geom_segment,
    geom_text,
    geom_vline,
    ggplot,
    guide_colorbar,
    labs,
    scale_fill_gradientn,
    scale_x_continuous,
    scale_y_continuous,
    theme,
    theme_void,
)


# Data - A short chord progression with melody (C major -> F major -> G major -> C major)
np.random.seed(42)

notes = [
    # Measure 1: C major chord + melody (opening)
    (0.0, 2.0, 48, 80),  # C3 bass
    (0.0, 2.0, 52, 70),  # E3
    (0.0, 2.0, 55, 70),  # G3
    (0.0, 1.0, 60, 100),  # C4 melody
    (1.0, 0.5, 62, 90),  # D4
    (1.5, 0.5, 64, 95),  # E4
    (2.0, 1.0, 65, 105),  # F4
    (3.0, 0.5, 64, 85),  # E4
    (3.5, 0.5, 62, 80),  # D4
    # Measure 2: F major chord + melody (building)
    (4.0, 2.0, 53, 75),  # F3 bass
    (4.0, 2.0, 57, 65),  # A3
    (4.0, 2.0, 60, 65),  # C4
    (4.0, 1.0, 65, 110),  # F4 melody
    (5.0, 0.5, 67, 95),  # G4
    (5.5, 0.5, 69, 100),  # A4
    (6.0, 1.5, 72, 115),  # C5 high point - CLIMAX
    (7.5, 0.5, 69, 80),  # A4
    # Measure 3: G major chord + descending melody
    (8.0, 2.0, 43, 85),  # G2 bass
    (8.0, 2.0, 55, 70),  # G3
    (8.0, 2.0, 59, 70),  # B3
    (8.0, 1.0, 71, 105),  # B4 melody
    (9.0, 0.5, 69, 90),  # A4
    (9.5, 0.5, 67, 85),  # G4
    (10.0, 1.0, 65, 95),  # F4
    (11.0, 0.5, 64, 80),  # E4
    (11.5, 0.5, 62, 75),  # D4
    # Measure 4: C major resolution (ending)
    (12.0, 2.0, 48, 90),  # C3 bass
    (12.0, 2.0, 52, 75),  # E3
    (12.0, 2.0, 55, 75),  # G3
    (12.0, 3.0, 60, 110),  # C4 melody - long resolution
    (14.0, 1.0, 64, 70),  # E4
    (15.0, 1.0, 60, 60),  # C4 ending - soft fade
]

df = pd.DataFrame(notes, columns=["start", "duration", "pitch", "velocity"])
df["end"] = df["start"] + df["duration"]
df["ymin"] = df["pitch"] - 0.4
df["ymax"] = df["pitch"] + 0.4

# MIDI note name mapping
note_names = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B"]

pitch_min = df["pitch"].min() - 1
pitch_max = df["pitch"].max() + 1

# Background rows for black/white key distinction
black_key_semitones = {1, 3, 6, 8, 10}
bg_rows = []
for p in range(pitch_min, pitch_max + 1):
    semitone = p % 12
    is_black = semitone in black_key_semitones
    bg_rows.append({"ymin": p - 0.5, "ymax": p + 0.5, "fill_color": "#e6e4ef" if is_black else "#f8f7fc"})

bg_df = pd.DataFrame(bg_rows)

# Y-axis labels: show note names for every pitch that has data
used_pitches = sorted(df["pitch"].unique())
pitch_labels_map = {p: f"{note_names[p % 12]}{p // 12 - 1}" for p in range(pitch_min, pitch_max + 1)}
label_pitches = used_pitches
label_names = [pitch_labels_map[p] for p in label_pitches]

# Measure structure
total_beats = 16
measure_lines = [0, 4, 8, 12, 16]
beat_lines = [b for b in range(total_beats + 1) if b not in measure_lines]

# Measure labels at top
measure_labels = pd.DataFrame(
    {"x": [2, 6, 10, 14], "label": ["I  (C)", "IV  (F)", "V  (G)", "I  (C)"], "y": [pitch_max + 0.8] * 4}
)

# Horizontal separators at octave boundaries (every C note)
octave_cs = [p for p in range(pitch_min, pitch_max + 1) if p % 12 == 0]
octave_lines = pd.DataFrame(
    {"y": [c - 0.5 for c in octave_cs], "xstart": [-0.3] * len(octave_cs), "xend": [total_beats + 0.3] * len(octave_cs)}
)

# Plot using theme_void as base for maximum control (plotnine-distinctive)
plot = (
    ggplot()
    # Background rows - alternating shading for black/white keys
    + geom_rect(
        bg_df,
        aes(xmin=-0.3, xmax=total_beats + 0.3, ymin="ymin", ymax="ymax"),
        fill=bg_df["fill_color"].tolist(),
        color=None,
        show_legend=False,
    )
    # Beat grid lines (subtle)
    + geom_vline(xintercept=beat_lines, color="#d4d2e0", size=0.25, linetype="dotted")
    # Measure grid lines (stronger)
    + geom_vline(xintercept=measure_lines, color="#9895b0", size=0.5, linetype="solid")
    # Octave boundary lines
    + geom_segment(
        octave_lines, aes(x="xstart", xend="xend", y="y", yend="y"), color="#b0adc5", size=0.35, linetype="dashed"
    )
    # Note rectangles with velocity color mapping
    + geom_rect(
        df, aes(xmin="start", xmax="end", ymin="ymin", ymax="ymax", fill="velocity"), color="#2d2a3e", size=0.25
    )
    # Measure chord labels at top
    + geom_text(measure_labels, aes(x="x", y="y", label="label"), size=11, color="#4a4568", fontstyle="italic")
    # Color scale: perceptually uniform blue → purple → orange → red
    + scale_fill_gradientn(
        colors=["#2166ac", "#5e4fa2", "#b2477d", "#e05634", "#d62f27"],
        limits=(55, 120),
        name="Velocity",
        guide=guide_colorbar(nbin=200),
    )
    + scale_y_continuous(breaks=label_pitches, labels=label_names, expand=(0.02, 0.02))
    + scale_x_continuous(breaks=measure_lines, labels=["0", "4", "8", "12", "16"], expand=(0.01, 0.01))
    + coord_cartesian(xlim=(-0.3, total_beats + 0.3), ylim=(pitch_min - 0.5, pitch_max + 1.5))
    + labs(x="Beats", y="Pitch", title="piano-roll-midi · plotnine · pyplots.ai")
    # Start from theme_void for full control, then add back what we need
    + theme_void()
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=24, weight="bold", color="#2d2a3e", margin={"b": 15}),
        axis_title_x=element_text(size=20, color="#4a4568", margin={"t": 10}),
        axis_title_y=element_text(size=20, color="#4a4568", margin={"r": 10}),
        axis_text_x=element_text(size=16, color="#4a4568"),
        axis_text_y=element_text(size=16, color="#4a4568"),
        axis_ticks_major=element_line(color="#9895b0", size=0.5),
        axis_ticks_length=4,
        legend_position="right",
        legend_title=element_text(size=16, color="#4a4568"),
        legend_text=element_text(size=14, color="#4a4568"),
        legend_background=element_rect(fill="#f8f7fc", color=None),
        legend_key_height=40,
        legend_key_width=12,
        panel_background=element_rect(fill="#f8f7fc", color=None),
        plot_background=element_rect(fill="white", color=None),
        plot_margin=0.02,
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
