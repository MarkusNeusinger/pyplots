""" pyplots.ai
waveform-audio: Audio Waveform Plot
Library: matplotlib 3.10.8 | Python 3.14.3
Quality: 88/100 | Created: 2026-03-07
"""

import matplotlib.pyplot as plt
import numpy as np


# Data
np.random.seed(42)
sample_rate = 22050
duration = 1.5
num_samples = int(sample_rate * duration)
time = np.linspace(0, duration, num_samples)

# Synthesize a rich audio waveform: fundamental + harmonics with amplitude envelope
fundamental_freq = 220  # A3 note
signal = (
    0.6 * np.sin(2 * np.pi * fundamental_freq * time)
    + 0.25 * np.sin(2 * np.pi * fundamental_freq * 2 * time)
    + 0.10 * np.sin(2 * np.pi * fundamental_freq * 3 * time)
    + 0.05 * np.sin(2 * np.pi * fundamental_freq * 5 * time)
)

# Amplitude envelope: attack-sustain-release shape
envelope = np.ones(num_samples)
attack = int(0.05 * sample_rate)
release = int(0.3 * sample_rate)
envelope[:attack] = np.linspace(0, 1, attack)
envelope[-release:] = np.linspace(1, 0, release)

# Add a brief silence gap and second burst for visual interest
gap_start = int(0.55 * sample_rate)
gap_end = int(0.7 * sample_rate)
envelope[gap_start:gap_end] *= np.linspace(1, 0.05, gap_end - gap_start)
burst_start = int(0.7 * sample_rate)
burst_end = int(0.85 * sample_rate)
envelope[burst_start:burst_end] *= np.linspace(0.05, 0.9, burst_end - burst_start)

amplitude = signal * envelope

# Min/max envelope for dense rendering
chunk_size = 64
num_chunks = num_samples // chunk_size
amplitude_trimmed = amplitude[: num_chunks * chunk_size].reshape(num_chunks, chunk_size)
time_trimmed = time[: num_chunks * chunk_size].reshape(num_chunks, chunk_size)
env_max = amplitude_trimmed.max(axis=1)
env_min = amplitude_trimmed.min(axis=1)
env_time = time_trimmed.mean(axis=1)

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

ax.fill_between(env_time, env_max, env_min, color="#306998", alpha=0.45, linewidth=0)
ax.plot(env_time, env_max, color="#306998", linewidth=1.2, alpha=0.8)
ax.plot(env_time, env_min, color="#306998", linewidth=1.2, alpha=0.8)
ax.axhline(y=0, color="#888888", linewidth=1.0, alpha=0.5)

# Style
ax.set_xlabel("Time (seconds)", fontsize=20)
ax.set_ylabel("Amplitude", fontsize=20)
ax.set_title("waveform-audio \u00b7 matplotlib \u00b7 pyplots.ai", fontsize=24, fontweight="medium")
ax.tick_params(axis="both", labelsize=16)
ax.set_ylim(-1.05, 1.05)
ax.set_xlim(0, duration)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.yaxis.grid(True, alpha=0.2, linewidth=0.8)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
