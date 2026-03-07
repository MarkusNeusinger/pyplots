""" pyplots.ai
piano-roll-midi: MIDI Piano Roll Visualization
Library: seaborn 0.13.2 | Python 3.14.3
Quality: 84/100 | Created: 2026-03-07
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Setup
sns.set_context("talk", font_scale=1.2)
sns.set_style("white")

# MIDI helpers
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
BLACK_KEY_INDICES = {1, 3, 6, 8, 10}

# Data - A chord progression (C - Am - F - G) with melody over 8 measures
np.random.seed(42)

notes_data = []

# Chord progression pattern
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

    for pitch in pitches:
        velocity = np.random.randint(50, 80)
        notes_data.append({"start": beat_offset, "duration": 4.0, "pitch": pitch, "velocity": velocity})

# Melody line
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
pitches = list(range(pitch_min, pitch_max + 1))
n_pitches = len(pitches)

# Create a time-pitch matrix for heatmap (resolution: 0.25 beats = sixteenth notes)
resolution = 0.25
total_beats = 32
n_steps = int(total_beats / resolution)
matrix = np.full((n_pitches, n_steps), np.nan)

for _, row in df.iterrows():
    pitch_idx = int(row["pitch"]) - pitch_min
    start_step = int(row["start"] / resolution)
    end_step = int((row["start"] + row["duration"]) / resolution)
    end_step = min(end_step, n_steps)
    for t in range(start_step, end_step):
        existing = matrix[pitch_idx, t]
        if np.isnan(existing) or row["velocity"] > existing:
            matrix[pitch_idx, t] = row["velocity"]

# Flip so highest pitch is at the top
matrix_flipped = matrix[::-1]
pitches_flipped = pitches[::-1]

# Build pitch labels
pitch_labels = [f"{NOTE_NAMES[p % 12]}{p // 12 - 1}" for p in pitches_flipped]

# Build time labels (show measure numbers at beat 0 of each measure)
time_labels = [""] * n_steps
for beat in range(0, total_beats + 1, 4):
    step = int(beat / resolution)
    if step < n_steps:
        time_labels[step] = f"M{beat // 4 + 1}"

# Create blue-to-red colormap as spec suggests
cmap = sns.color_palette("coolwarm", as_cmap=True)

# Black key row mask for background shading
black_key_mask = np.array([p % 12 in BLACK_KEY_INDICES for p in pitches_flipped])

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

# Draw background shading for black keys first
for i, is_black in enumerate(black_key_mask):
    if is_black:
        ax.axhspan(i, i + 1, color="#e8e8e8", zorder=0)

# Use seaborn heatmap as the core visualization
sns.heatmap(
    pd.DataFrame(matrix_flipped, index=pitch_labels),
    ax=ax,
    cmap=cmap,
    vmin=40,
    vmax=127,
    cbar_kws={"label": "Velocity (MIDI 0–127)", "shrink": 0.8, "aspect": 30, "pad": 0.02},
    xticklabels=False,
    yticklabels=1,
    linewidths=0,
    mask=np.isnan(matrix_flipped),
)

# Add beat grid lines
for beat in range(total_beats + 1):
    x_pos = beat / resolution
    if beat % 4 == 0:
        ax.axvline(x_pos, color="#777777", linewidth=1.2, alpha=0.6, zorder=3)
    else:
        ax.axvline(x_pos, color="#bbbbbb", linewidth=0.5, alpha=0.3, zorder=3)

# X-axis: measure labels
measure_positions = [int(b / resolution) for b in range(0, total_beats, 4)]
measure_labels_display = [f"M{i + 1}" for i in range(len(measure_positions))]
ax.set_xticks([pos + 2 / resolution for pos in measure_positions])
ax.set_xticklabels(measure_labels_display, fontsize=16)

# Y-axis styling
ax.tick_params(axis="y", labelsize=14, length=0)
ax.tick_params(axis="x", length=0)

# Colorbar styling
cbar = ax.collections[0].colorbar
cbar.ax.tick_params(labelsize=14)
cbar.set_label("Velocity (MIDI 0–127)", fontsize=18)

# Labels and title
ax.set_xlabel("Measure (4/4 time)", fontsize=20)
ax.set_ylabel("Pitch (MIDI note)", fontsize=20)
ax.set_title("piano-roll-midi · seaborn · pyplots.ai", fontsize=24, fontweight="medium", pad=15)

# Remove spines
for spine in ax.spines.values():
    spine.set_visible(False)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
