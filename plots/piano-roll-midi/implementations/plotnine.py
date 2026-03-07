""" pyplots.ai
piano-roll-midi: MIDI Piano Roll Visualization
Library: plotnine 0.15.3 | Python 3.14.3
Quality: 82/100 | Created: 2026-03-07
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    coord_cartesian,
    element_blank,
    element_rect,
    element_text,
    geom_rect,
    geom_vline,
    ggplot,
    labs,
    scale_fill_gradient2,
    scale_x_continuous,
    scale_y_continuous,
    theme,
    theme_minimal,
)


# Data - A short chord progression with melody (C major -> F major -> G major -> C major)
np.random.seed(42)

notes = [
    # Measure 1: C major chord + melody
    (0.0, 2.0, 48, 80),  # C3 bass
    (0.0, 2.0, 52, 70),  # E3
    (0.0, 2.0, 55, 70),  # G3
    (0.0, 1.0, 60, 100),  # C4 melody
    (1.0, 0.5, 62, 90),  # D4
    (1.5, 0.5, 64, 95),  # E4
    (2.0, 1.0, 65, 105),  # F4
    (3.0, 0.5, 64, 85),  # E4
    (3.5, 0.5, 62, 80),  # D4
    # Measure 2: F major chord + melody
    (4.0, 2.0, 53, 75),  # F3 bass
    (4.0, 2.0, 57, 65),  # A3
    (4.0, 2.0, 60, 65),  # C4
    (4.0, 1.0, 65, 110),  # F4 melody
    (5.0, 0.5, 67, 95),  # G4
    (5.5, 0.5, 69, 100),  # A4
    (6.0, 1.5, 72, 115),  # C5 high point
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
    # Measure 4: C major resolution
    (12.0, 2.0, 48, 90),  # C3 bass
    (12.0, 2.0, 52, 75),  # E3
    (12.0, 2.0, 55, 75),  # G3
    (12.0, 3.0, 60, 110),  # C4 melody - long resolution
    (14.0, 1.0, 64, 70),  # E4
    (15.0, 1.0, 60, 60),  # C4 ending
]

df = pd.DataFrame(notes, columns=["start", "duration", "pitch", "velocity"])
df["end"] = df["start"] + df["duration"]

# MIDI note name mapping
note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

pitch_min = df["pitch"].min() - 1
pitch_max = df["pitch"].max() + 1

# Background rows for black/white key distinction
black_key_semitones = {1, 3, 6, 8, 10}  # C#, D#, F#, G#, A#
bg_rows = []
for p in range(pitch_min, pitch_max + 1):
    semitone = p % 12
    key_type = "black" if semitone in black_key_semitones else "white"
    bg_rows.append({"pitch": p, "ymin": p - 0.5, "ymax": p + 0.5, "key_type": key_type})

bg_df = pd.DataFrame(bg_rows)

# Y-axis labels: show note names
pitch_range = range(pitch_min, pitch_max + 1)
pitch_labels = {p: f"{note_names[p % 12]}{p // 12 - 1}" for p in pitch_range}
label_pitches = [p for p in pitch_range if p % 12 in (0, 4, 5, 7)]  # C, E, F, G
label_names = [pitch_labels[p] for p in label_pitches]

# Measure lines (every 4 beats) and beat lines
total_beats = 16
measure_lines = [0, 4, 8, 12, 16]
beat_lines = [b for b in range(total_beats + 1) if b not in measure_lines]

# Plot
plot = (
    ggplot()
    # Background: black key rows
    + geom_rect(
        bg_df[bg_df["key_type"] == "black"],
        aes(xmin=-0.2, xmax=total_beats + 0.2, ymin="ymin", ymax="ymax"),
        fill="#e8e8ec",
        color=None,
    )
    # Beat grid lines (lighter)
    + geom_vline(xintercept=beat_lines, color="#d0d0d5", size=0.3)
    # Measure grid lines (stronger)
    + geom_vline(xintercept=measure_lines, color="#a0a0a8", size=0.6)
    # Note rectangles
    + geom_rect(
        df,
        aes(xmin="start", xmax="end", ymin="pitch - 0.4", ymax="pitch + 0.4", fill="velocity"),
        color="white",
        size=0.3,
    )
    # Color scale: blue (soft) to red (loud)
    + scale_fill_gradient2(low="#3a6fb0", mid="#e8c840", high="#c0392b", midpoint=90, limits=(55, 120), name="Velocity")
    + scale_y_continuous(breaks=label_pitches, labels=label_names)
    + scale_x_continuous(breaks=measure_lines, minor_breaks=beat_lines, limits=(-0.2, total_beats + 0.2))
    + coord_cartesian(ylim=(pitch_min - 0.5, pitch_max + 0.5))
    + labs(x="Beats", y="Pitch", title="piano-roll-midi \u00b7 plotnine \u00b7 pyplots.ai")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=24, weight="bold"),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        axis_text_y=element_text(size=14),
        legend_title=element_text(size=16),
        legend_text=element_text(size=14),
        panel_grid_major_y=element_blank(),
        panel_grid_minor_y=element_blank(),
        panel_grid_major_x=element_blank(),
        panel_grid_minor_x=element_blank(),
        panel_background=element_rect(fill="white", color=None),
        plot_background=element_rect(fill="white", color=None),
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
