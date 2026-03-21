""" pyplots.ai
bode-basic: Bode Plot for Frequency Response
Library: seaborn 0.13.2 | Python 3.14.3
Quality: 86/100 | Created: 2026-03-21
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Data — open-loop transfer function: H(s) = K*p1*p2 / (s*(s+p1)*(s+p2))
# Type-1 system with two real poles — classic controls textbook example
K = 40.0
p1 = 2 * np.pi * 5  # pole at 5 Hz
p2 = 2 * np.pi * 50  # pole at 50 Hz

frequency_hz = np.logspace(-1, 3, 600)
omega = 2 * np.pi * frequency_hz
s = 1j * omega

H = K * p1 * p2 / (s * (s + p1) * (s + p2))
magnitude_db = 20 * np.log10(np.abs(H))
phase_deg = np.degrees(np.unwrap(np.angle(H)))

# Gain crossover: where magnitude crosses 0 dB (interpolated)
sign_changes = np.diff(np.sign(magnitude_db))
gc_indices = np.where(sign_changes != 0)[0]
idx = gc_indices[0]
frac = -magnitude_db[idx] / (magnitude_db[idx + 1] - magnitude_db[idx])
gain_cross_freq = frequency_hz[idx] * (frequency_hz[idx + 1] / frequency_hz[idx]) ** frac
phase_at_gain_cross = phase_deg[idx] + frac * (phase_deg[idx + 1] - phase_deg[idx])
phase_margin = 180 + phase_at_gain_cross

# Phase crossover: where phase crosses -180 deg (interpolated)
phase_shift = phase_deg + 180
sign_changes_ph = np.diff(np.sign(phase_shift))
pc_indices = np.where(sign_changes_ph != 0)[0]
idx = pc_indices[0]
frac = -phase_shift[idx] / (phase_shift[idx + 1] - phase_shift[idx])
phase_cross_freq = frequency_hz[idx] * (frequency_hz[idx + 1] / frequency_hz[idx]) ** frac
mag_at_phase_cross = magnitude_db[idx] + frac * (magnitude_db[idx + 1] - magnitude_db[idx])
gain_margin = -mag_at_phase_cross

df = pd.DataFrame({"frequency_hz": frequency_hz, "magnitude_db": magnitude_db, "phase_deg": phase_deg})

# Plot
fig, (ax_mag, ax_phase) = plt.subplots(2, 1, figsize=(16, 9), sharex=True)

sns.lineplot(data=df, x="frequency_hz", y="magnitude_db", ax=ax_mag, color="#306998", linewidth=3)
sns.lineplot(data=df, x="frequency_hz", y="phase_deg", ax=ax_phase, color="#306998", linewidth=3)

# Reference lines
ax_mag.axhline(0, color="#888888", linewidth=1.2, linestyle="--", alpha=0.6)
ax_phase.axhline(-180, color="#888888", linewidth=1.2, linestyle="--", alpha=0.6)

# Gain margin annotation (red) — vertical line at phase crossover
ax_mag.vlines(phase_cross_freq, mag_at_phase_cross, 0, color="#E74C3C", linewidth=2.5, alpha=0.85)
ax_mag.plot(phase_cross_freq, mag_at_phase_cross, "o", color="#E74C3C", markersize=10, zorder=5)
ax_mag.plot(phase_cross_freq, 0, "o", color="#E74C3C", markersize=10, zorder=5)
gm_label_y = mag_at_phase_cross / 2
ax_mag.annotate(
    f"GM = {gain_margin:.1f} dB",
    xy=(phase_cross_freq, gm_label_y),
    xytext=(phase_cross_freq * 3, gm_label_y + 8),
    fontsize=15,
    fontweight="bold",
    color="#E74C3C",
    arrowprops={"arrowstyle": "->", "color": "#E74C3C", "lw": 2},
    bbox={"boxstyle": "round,pad=0.3", "fc": "white", "ec": "#E74C3C", "alpha": 0.9},
)

# Phase margin annotation (green) — vertical line at gain crossover
ax_phase.vlines(gain_cross_freq, -180, phase_at_gain_cross, color="#27AE60", linewidth=2.5, alpha=0.85)
ax_phase.plot(gain_cross_freq, phase_at_gain_cross, "o", color="#27AE60", markersize=10, zorder=5)
ax_phase.plot(gain_cross_freq, -180, "o", color="#27AE60", markersize=10, zorder=5)
pm_label_y = (phase_at_gain_cross - 180) / 2
ax_phase.annotate(
    f"PM = {phase_margin:.1f}\u00b0",
    xy=(gain_cross_freq, pm_label_y),
    xytext=(gain_cross_freq * 3.5, pm_label_y + 15),
    fontsize=15,
    fontweight="bold",
    color="#27AE60",
    arrowprops={"arrowstyle": "->", "color": "#27AE60", "lw": 2},
    bbox={"boxstyle": "round,pad=0.3", "fc": "white", "ec": "#27AE60", "alpha": 0.9},
)

# Crossover frequency vertical markers
for ax in [ax_mag, ax_phase]:
    ax.axvline(gain_cross_freq, color="#27AE60", linewidth=1, linestyle=":", alpha=0.4)
    ax.axvline(phase_cross_freq, color="#E74C3C", linewidth=1, linestyle=":", alpha=0.4)

# Style — magnitude
ax_mag.set_ylabel("Magnitude (dB)", fontsize=20)
ax_mag.set_title("bode-basic \u00b7 seaborn \u00b7 pyplots.ai", fontsize=24, fontweight="medium", pad=16)
ax_mag.tick_params(axis="both", labelsize=16)
ax_mag.spines["top"].set_visible(False)
ax_mag.spines["right"].set_visible(False)
ax_mag.yaxis.grid(True, alpha=0.2, linewidth=0.8)
ax_mag.xaxis.grid(True, alpha=0.15, linewidth=0.5)
ax_mag.set_xscale("log")

# Style — phase
ax_phase.set_xlabel("Frequency (Hz)", fontsize=20)
ax_phase.set_ylabel("Phase (\u00b0)", fontsize=20)
ax_phase.tick_params(axis="both", labelsize=16)
ax_phase.spines["top"].set_visible(False)
ax_phase.spines["right"].set_visible(False)
ax_phase.yaxis.grid(True, alpha=0.2, linewidth=0.8)
ax_phase.xaxis.grid(True, alpha=0.15, linewidth=0.5)
ax_phase.set_xscale("log")
ax_phase.set_yticks([-90, -135, -180, -225, -270])

# Save
plt.subplots_adjust(hspace=0.08)
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
