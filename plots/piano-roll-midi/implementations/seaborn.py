""" pyplots.ai
piano-roll-midi: MIDI Piano Roll Visualization
Library: seaborn 0.13.2 | Python 3.14.3
Quality: 81/100 | Created: 2026-03-07
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize


# Setup
sns.set_context("talk", font_scale=1.2)
sns.set_style("white")

# MIDI helpers
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
BLACK_KEY_INDICES = {1, 3, 6, 8, 10}


# Data - A chord progression (C - Am - F - G) with melody over 8 measures
np.random.seed(42)

notes_data = []

# Chord progression pattern (each chord lasts 2 beats, repeated across measures)
chords = {
    "C": [60, 64, 67],  # C4, E4, G4
    "Am": [57, 60, 64],  # A3, C4, E4
    "F": [53, 57, 60],  # F3, A3, C4
    "G": [55, 59, 62],  # G3, B3, D4
}
progression = ["C", "Am", "F", "G"]

# Add chord tones across 8 measures (32 beats in 4/4 time)
for measure in range(8):
    chord_name = progression[measure % 4]
    pitches = chords[chord_name]
    beat_offset = measure * 4

    # Whole note chords (sustain full measure)
    for pitch in pitches:
        velocity = np.random.randint(50, 80)
        notes_data.append({"start": beat_offset, "duration": 4.0, "pitch": pitch, "velocity": velocity})

# Add a melody line on top
melody = [
    (0, 0.5, 72, 100),
    (0.5, 0.5, 74, 95),
    (1.0, 1.0, 76, 105),
    (2.0, 0.5, 77, 90),
    (2.5, 0.5, 76, 85),
    (3.0, 1.0, 74, 95),
    (4, 0.5, 72, 100),
    (4.5, 0.5, 71, 90),
    (5.0, 1.0, 69, 110),
    (6.0, 0.5, 67, 85),
    (6.5, 0.5, 69, 90),
    (7.0, 1.0, 71, 100),
    (8, 1.0, 72, 105),
    (9.0, 0.5, 74, 95),
    (9.5, 0.5, 76, 100),
    (10.0, 1.0, 77, 110),
    (11.0, 1.0, 76, 90),
    (12, 0.5, 74, 95),
    (12.5, 0.5, 72, 90),
    (13.0, 1.0, 69, 100),
    (14.0, 0.5, 67, 85),
    (14.5, 0.5, 69, 95),
    (15.0, 1.0, 71, 105),
    (16, 0.5, 72, 100),
    (16.5, 0.5, 74, 90),
    (17.0, 1.5, 76, 115),
    (18.5, 0.5, 77, 95),
    (19.0, 1.0, 79, 120),
    (20, 1.0, 77, 105),
    (21.0, 0.5, 76, 90),
    (21.5, 0.5, 74, 85),
    (22.0, 1.0, 72, 100),
    (23.0, 1.0, 74, 95),
    (24, 0.5, 76, 110),
    (24.5, 0.5, 77, 105),
    (25.0, 1.0, 79, 120),
    (26.0, 0.5, 77, 95),
    (26.5, 0.5, 76, 100),
    (27.0, 1.0, 74, 90),
    (28, 1.5, 72, 115),
    (29.5, 0.5, 71, 85),
    (30.0, 1.0, 69, 95),
    (31.0, 1.0, 72, 110),
]

for start, dur, pitch, vel in melody:
    notes_data.append({"start": start, "duration": dur, "pitch": pitch, "velocity": vel})

df = pd.DataFrame(notes_data)

# Pitch range with margin
pitch_min = df["pitch"].min() - 1
pitch_max = df["pitch"].max() + 1

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

# Background shading for black keys
for pitch in range(pitch_min, pitch_max + 1):
    if pitch % 12 in BLACK_KEY_INDICES:
        ax.axhspan(pitch - 0.5, pitch + 0.5, color="#e8e8e8", zorder=0)

# Beat grid lines
total_beats = 32
for beat in range(total_beats + 1):
    if beat % 4 == 0:
        ax.axvline(beat, color="#999999", linewidth=1.2, alpha=0.6, zorder=1)
    else:
        ax.axvline(beat, color="#cccccc", linewidth=0.6, alpha=0.4, zorder=1)

# Draw note rectangles
cmap = sns.color_palette("YlOrRd", as_cmap=True)
norm = Normalize(vmin=40, vmax=127)

rectangles = []
colors = []
for _, row in df.iterrows():
    rect = mpatches.FancyBboxPatch(
        (row["start"], row["pitch"] - 0.4), row["duration"] - 0.05, 0.8, boxstyle="round,pad=0.02"
    )
    rectangles.append(rect)
    colors.append(cmap(norm(row["velocity"])))

pc = PatchCollection(rectangles, facecolors=colors, edgecolors="white", linewidths=0.8, zorder=2)
ax.add_collection(pc)

# Colorbar
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax, pad=0.02, aspect=30, shrink=0.8)
cbar.set_label("Velocity", fontsize=18)
cbar.ax.tick_params(labelsize=14)

# Y-axis: note names
pitch_range = range(pitch_min, pitch_max + 1)
pitch_labels = [f"{NOTE_NAMES[p % 12]}{p // 12 - 1}" for p in pitch_range]
ax.set_yticks(list(pitch_range))
ax.set_yticklabels(pitch_labels, fontsize=13)

# X-axis: beats with measure numbers
measure_ticks = list(range(0, total_beats + 1, 4))
measure_labels = [f"M{i + 1}" for i in range(len(measure_ticks))]
ax.set_xticks(measure_ticks)
ax.set_xticklabels(measure_labels, fontsize=16)

# Minor ticks for individual beats
ax.set_xticks(range(total_beats + 1), minor=True)

# Style
ax.set_xlim(-0.2, total_beats + 0.2)
ax.set_ylim(pitch_min - 0.5, pitch_max + 0.5)
ax.set_xlabel("Measure", fontsize=20)
ax.set_ylabel("Pitch", fontsize=20)
ax.set_title("piano-roll-midi \u00b7 seaborn \u00b7 pyplots.ai", fontsize=24, fontweight="medium")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
