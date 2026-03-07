"""pyplots.ai
waveform-audio: Audio Waveform Plot
Library: seaborn | Python 3.13
Quality: pending | Created: 2026-03-07
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Data
np.random.seed(42)
sample_rate = 22050
duration = 1.0
num_samples = int(sample_rate * duration)
time = np.linspace(0, duration, num_samples)

base_freq = 220
segments = [
    np.linspace(0, 1, int(num_samples * 0.05)),
    np.ones(int(num_samples * 0.15)),
    np.exp(-3 * np.linspace(0, 1, int(num_samples * 0.3))),
    np.linspace(0.05, 0.8, int(num_samples * 0.1)),
    np.ones(int(num_samples * 0.1)),
    np.exp(-2 * np.linspace(0, 1, int(num_samples * 0.3))),
]
amplitude_envelope = np.concatenate(segments)
if len(amplitude_envelope) < num_samples:
    amplitude_envelope = np.pad(
        amplitude_envelope, (0, num_samples - len(amplitude_envelope)), constant_values=amplitude_envelope[-1]
    )
amplitude_envelope = amplitude_envelope[:num_samples]

signal = (
    0.6 * np.sin(2 * np.pi * base_freq * time)
    + 0.25 * np.sin(2 * np.pi * base_freq * 2 * time)
    + 0.1 * np.sin(2 * np.pi * base_freq * 3 * time)
    + 0.05 * np.sin(2 * np.pi * base_freq * 5 * time)
)
signal *= amplitude_envelope
signal += np.random.normal(0, 0.01, num_samples)
signal = np.clip(signal, -1.0, 1.0)

# Downsample for envelope rendering
chunk_size = 50
num_chunks = num_samples // chunk_size
time_chunks = time[: num_chunks * chunk_size].reshape(num_chunks, chunk_size)
signal_chunks = signal[: num_chunks * chunk_size].reshape(num_chunks, chunk_size)

env_time = time_chunks.mean(axis=1)
env_max = signal_chunks.max(axis=1)
env_min = signal_chunks.min(axis=1)

# Plot
sns.set_context("talk", font_scale=1.2)
fig, ax = plt.subplots(figsize=(16, 9))

ax.fill_between(env_time, env_max, env_min, color="#306998", alpha=0.45, linewidth=0)
sns.lineplot(x=env_time, y=env_max, ax=ax, color="#306998", linewidth=1.2, alpha=0.8)
sns.lineplot(x=env_time, y=env_min, ax=ax, color="#306998", linewidth=1.2, alpha=0.8)

ax.axhline(y=0, color="#888888", linewidth=1.0, alpha=0.5)

# Style
ax.set_xlabel("Time (seconds)", fontsize=20)
ax.set_ylabel("Amplitude", fontsize=20)
ax.set_title("waveform-audio · seaborn · pyplots.ai", fontsize=24, fontweight="medium")
ax.tick_params(axis="both", labelsize=16)
ax.set_ylim(-1.05, 1.05)
ax.set_xlim(0, duration)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.yaxis.grid(True, alpha=0.2, linewidth=0.8)

# Save
plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
