""" pyplots.ai
spectrogram-mel: Mel-Spectrogram for Audio Analysis
Library: pygal 3.1.0 | Python 3.14.3
Quality: 81/100 | Created: 2026-03-11
"""

import sys

import numpy as np
from scipy import signal


# Temporarily remove current directory from path to avoid name collision
_cwd = sys.path[0] if sys.path[0] else "."
if _cwd in sys.path:
    sys.path.remove(_cwd)

from pygal.graph.graph import Graph  # noqa: E402
from pygal.style import Style  # noqa: E402


# Restore path
sys.path.insert(0, _cwd)


class MelSpectrogramChart(Graph):
    """Custom mel-spectrogram visualization for pygal."""

    def __init__(self, *args, **kwargs):
        self.spectrogram_data = kwargs.pop("spectrogram_data", [])
        self.time_bins = kwargs.pop("time_bins", [])
        self.mel_freq_labels = kwargs.pop("mel_freq_labels", [])
        self.mel_freq_positions = kwargs.pop("mel_freq_positions", [])
        self.db_min = kwargs.pop("db_min", -80)
        self.db_max = kwargs.pop("db_max", 0)
        self.colormap = kwargs.pop(
            "colormap",
            [
                "#000004",
                "#1b0c41",
                "#4a0c6b",
                "#781c6d",
                "#a52c60",
                "#cf4446",
                "#ed6925",
                "#fb9b06",
                "#f7d13d",
                "#fcffa4",
            ],
        )
        super().__init__(*args, **kwargs)

    def _interpolate_color(self, value, min_val, max_val):
        if max_val == min_val:
            return self.colormap[-1]
        normalized = (value - min_val) / (max_val - min_val)
        normalized = max(0, min(1, normalized))
        pos = normalized * (len(self.colormap) - 1)
        idx1 = int(pos)
        idx2 = min(idx1 + 1, len(self.colormap) - 1)
        frac = pos - idx1
        c1 = self.colormap[idx1]
        c2 = self.colormap[idx2]
        r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
        r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
        r = int(r1 + (r2 - r1) * frac)
        g = int(g1 + (g2 - g1) * frac)
        b = int(b1 + (b2 - b1) * frac)
        return f"#{r:02x}{g:02x}{b:02x}"

    def _plot(self):
        if len(self.spectrogram_data) == 0:
            return

        n_mels = len(self.spectrogram_data)
        n_time = len(self.spectrogram_data[0]) if n_mels > 0 else 0

        min_val = self.db_min
        max_val = self.db_max

        plot_width = self.view.width
        plot_height = self.view.height

        label_margin_left = 300
        label_margin_bottom = 200
        label_margin_top = 80
        label_margin_right = 300

        available_width = plot_width - label_margin_left - label_margin_right
        available_height = plot_height - label_margin_bottom - label_margin_top

        cell_width = available_width / n_time
        cell_height = available_height / n_mels

        x_offset = self.view.x(0) + label_margin_left
        y_offset = self.view.y(n_mels) + label_margin_top

        plot_node = self.nodes["plot"]
        spec_group = self.svg.node(plot_node, class_="mel-spectrogram")

        # Draw cells (mel band 0 at bottom, highest mel band at top)
        for i in range(n_mels):
            for j in range(n_time):
                value = self.spectrogram_data[n_mels - 1 - i][j]
                color = self._interpolate_color(value, min_val, max_val)
                x = x_offset + j * cell_width
                y = y_offset + i * cell_height
                rect = self.svg.node(spec_group, "rect", x=x, y=y, width=cell_width + 0.5, height=cell_height + 0.5)
                rect.set("fill", color)
                rect.set("stroke", "none")

        # Axes border
        border = self.svg.node(
            spec_group, "rect", x=x_offset, y=y_offset, width=available_width, height=available_height
        )
        border.set("fill", "none")
        border.set("stroke", "#333333")
        border.set("stroke-width", "3")

        # X-axis label
        axis_label_size = 52
        x_label_x = x_offset + available_width / 2
        x_label_y = y_offset + available_height + 150
        text_node = self.svg.node(spec_group, "text", x=x_label_x, y=x_label_y)
        text_node.set("text-anchor", "middle")
        text_node.set("fill", "#333333")
        text_node.set("style", f"font-size:{axis_label_size}px;font-weight:bold;font-family:sans-serif")
        text_node.text = "Time (s)"

        # Y-axis label
        y_label_x = x_offset - 220
        y_label_y = y_offset + available_height / 2
        text_node = self.svg.node(
            spec_group, "text", x=y_label_x, y=y_label_y, transform=f"rotate(-90, {y_label_x}, {y_label_y})"
        )
        text_node.set("text-anchor", "middle")
        text_node.set("fill", "#333333")
        text_node.set("style", f"font-size:{axis_label_size}px;font-weight:bold;font-family:sans-serif")
        text_node.text = "Frequency (Hz)"

        # X-axis ticks
        tick_font_size = 38
        n_x_ticks = 6
        for i in range(n_x_ticks):
            tick_x = x_offset + (i / (n_x_ticks - 1)) * available_width
            tick_y = y_offset + available_height
            line = self.svg.node(spec_group, "line", x1=tick_x, y1=tick_y, x2=tick_x, y2=tick_y + 15)
            line.set("stroke", "#333333")
            line.set("stroke-width", "2")
            time_val = self.time_bins[int(i / (n_x_ticks - 1) * (len(self.time_bins) - 1))]
            text_node = self.svg.node(spec_group, "text", x=tick_x, y=tick_y + 55)
            text_node.set("text-anchor", "middle")
            text_node.set("fill", "#333333")
            text_node.set("style", f"font-size:{tick_font_size}px;font-family:sans-serif")
            text_node.text = f"{time_val:.1f}"

        # Y-axis ticks at mel band edge frequencies
        for freq_hz, norm_pos in zip(self.mel_freq_labels, self.mel_freq_positions, strict=True):
            tick_x = x_offset
            tick_y = y_offset + (1 - norm_pos) * available_height
            line = self.svg.node(spec_group, "line", x1=tick_x - 15, y1=tick_y, x2=tick_x, y2=tick_y)
            line.set("stroke", "#333333")
            line.set("stroke-width", "2")
            text_node = self.svg.node(spec_group, "text", x=tick_x - 25, y=tick_y + 12)
            text_node.set("text-anchor", "end")
            text_node.set("fill", "#333333")
            text_node.set("style", f"font-size:{tick_font_size}px;font-family:sans-serif")
            if freq_hz >= 1000:
                text_node.text = f"{freq_hz / 1000:.1f}k"
            else:
                text_node.text = f"{int(freq_hz)}"

        # Colorbar
        colorbar_width = 50
        colorbar_height = available_height * 0.8
        colorbar_x = x_offset + available_width + 60
        colorbar_y = y_offset + (available_height - colorbar_height) / 2

        n_segments = 80
        segment_height = colorbar_height / n_segments
        for i in range(n_segments):
            seg_value = min_val + (max_val - min_val) * (n_segments - 1 - i) / (n_segments - 1)
            seg_color = self._interpolate_color(seg_value, min_val, max_val)
            seg_y = colorbar_y + i * segment_height
            self.svg.node(
                spec_group,
                "rect",
                x=colorbar_x,
                y=seg_y,
                width=colorbar_width,
                height=segment_height + 1,
                fill=seg_color,
            )

        # Colorbar border
        self.svg.node(
            spec_group,
            "rect",
            x=colorbar_x,
            y=colorbar_y,
            width=colorbar_width,
            height=colorbar_height,
            fill="none",
            stroke="#333333",
        )

        # Colorbar tick labels
        cb_label_size = 36
        n_cb_ticks = 6
        for i in range(n_cb_ticks):
            pos = i / (n_cb_ticks - 1)
            val = max_val - (max_val - min_val) * pos
            text_y = colorbar_y + pos * colorbar_height + cb_label_size * 0.35
            tick_line = self.svg.node(
                spec_group,
                "line",
                x1=colorbar_x + colorbar_width,
                y1=colorbar_y + pos * colorbar_height,
                x2=colorbar_x + colorbar_width + 10,
                y2=colorbar_y + pos * colorbar_height,
            )
            tick_line.set("stroke", "#333333")
            tick_line.set("stroke-width", "2")
            text_node = self.svg.node(spec_group, "text", x=colorbar_x + colorbar_width + 20, y=text_y)
            text_node.set("fill", "#333333")
            text_node.set("style", f"font-size:{cb_label_size}px;font-family:sans-serif")
            text_node.text = f"{val:.0f}"

        # Colorbar title
        cb_title_size = 42
        cb_title_x = colorbar_x + colorbar_width / 2
        cb_title_y = colorbar_y - 30
        text_node = self.svg.node(spec_group, "text", x=cb_title_x, y=cb_title_y)
        text_node.set("text-anchor", "middle")
        text_node.set("fill", "#333333")
        text_node.set("style", f"font-size:{cb_title_size}px;font-weight:bold;font-family:sans-serif")
        text_node.text = "dB"

    def _compute(self):
        n_mels = len(self.spectrogram_data) if len(self.spectrogram_data) > 0 else 1
        n_time = (
            len(self.spectrogram_data[0]) if len(self.spectrogram_data) > 0 and len(self.spectrogram_data[0]) > 0 else 1
        )
        self._box.xmin = 0
        self._box.xmax = n_time
        self._box.ymin = 0
        self._box.ymax = n_mels


# Mel-scale helper functions
def hz_to_mel(hz):
    return 2595.0 * np.log10(1.0 + hz / 700.0)


def mel_to_hz(mel):
    return 700.0 * (10.0 ** (mel / 2595.0) - 1.0)


def mel_filterbank(n_mels, n_fft, sample_rate):
    fmax = sample_rate / 2.0
    mel_min = hz_to_mel(0)
    mel_max = hz_to_mel(fmax)
    mel_points = np.linspace(mel_min, mel_max, n_mels + 2)
    hz_points = mel_to_hz(mel_points)
    bin_points = np.floor((n_fft + 1) * hz_points / sample_rate).astype(int)

    filters = np.zeros((n_mels, n_fft // 2 + 1))
    for m in range(1, n_mels + 1):
        f_left = bin_points[m - 1]
        f_center = bin_points[m]
        f_right = bin_points[m + 1]
        for k in range(f_left, f_center):
            if f_center != f_left:
                filters[m - 1, k] = (k - f_left) / (f_center - f_left)
        for k in range(f_center, f_right):
            if f_right != f_center:
                filters[m - 1, k] = (f_right - k) / (f_right - f_center)

    return filters, hz_points[1:-1]


# Data - synthesize audio with multiple frequency components
np.random.seed(42)

sample_rate = 22050
duration = 3.0
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# Melody: sequence of notes with harmonics (C4, E4, G4, C5 arpeggio pattern)
note_freqs = [261.6, 329.6, 392.0, 523.3, 392.0, 329.6]
note_duration = duration / len(note_freqs)
audio_signal = np.zeros_like(t)

for idx, freq in enumerate(note_freqs):
    start = int(idx * note_duration * sample_rate)
    end = int((idx + 1) * note_duration * sample_rate)
    note_t = t[start:end] - t[start]
    envelope = np.exp(-2.0 * note_t / note_duration)
    audio_signal[start:end] += envelope * np.sin(2 * np.pi * freq * note_t)
    audio_signal[start:end] += 0.5 * envelope * np.sin(2 * np.pi * 2 * freq * note_t)
    audio_signal[start:end] += 0.25 * envelope * np.sin(2 * np.pi * 3 * freq * note_t)

# Add subtle broadband noise
audio_signal += 0.02 * np.random.randn(len(t))

# Compute mel spectrogram
n_fft = 2048
hop_length = 512
n_mels_count = 128

# STFT
frequencies_stft, times_stft, Zxx = signal.stft(
    audio_signal, fs=sample_rate, nperseg=n_fft, noverlap=n_fft - hop_length
)
power_spectrum = np.abs(Zxx) ** 2

# Apply mel filterbank
mel_filters, mel_center_freqs = mel_filterbank(n_mels_count, n_fft, sample_rate)
mel_spec = mel_filters @ power_spectrum

# Convert to dB
mel_spec_db = 10 * np.log10(mel_spec + 1e-10)
db_max = np.max(mel_spec_db)
mel_spec_db = mel_spec_db - db_max  # Normalize so max is 0 dB
db_floor = -80.0
mel_spec_db = np.maximum(mel_spec_db, db_floor)

# Downsample for pygal rendering performance
time_step = max(1, len(times_stft) // 150)
mel_step = max(1, n_mels_count // 96)
mel_spec_display = mel_spec_db[::mel_step, ::time_step]
times_display = times_stft[::time_step]

# Compute y-axis tick positions (Hz labels at key mel band edges)
tick_freqs_hz = [100, 200, 500, 1000, 2000, 4000, 8000]
tick_freqs_hz = [f for f in tick_freqs_hz if f <= sample_rate / 2]
n_display_mels = mel_spec_display.shape[0]
mel_tick_positions = []
mel_tick_labels = []
for f in tick_freqs_hz:
    mel_val = hz_to_mel(f)
    mel_max_val = hz_to_mel(sample_rate / 2)
    norm_pos = mel_val / mel_max_val
    if 0 <= norm_pos <= 1:
        mel_tick_positions.append(norm_pos)
        mel_tick_labels.append(f)

# Inferno colormap
inferno_colormap = [
    "#000004",
    "#1b0c41",
    "#4a0c6b",
    "#781c6d",
    "#a52c60",
    "#cf4446",
    "#ed6925",
    "#fb9b06",
    "#f7d13d",
    "#fcffa4",
]

# Style
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998",),
    title_font_size=72,
    legend_font_size=48,
    label_font_size=42,
    value_font_size=36,
    font_family="sans-serif",
)

# Plot
chart = MelSpectrogramChart(
    width=4800,
    height=2700,
    style=custom_style,
    title="spectrogram-mel \u00b7 pygal \u00b7 pyplots.ai",
    spectrogram_data=mel_spec_display.tolist(),
    time_bins=times_display.tolist(),
    mel_freq_labels=mel_tick_labels,
    mel_freq_positions=mel_tick_positions,
    db_min=db_floor,
    db_max=0,
    colormap=inferno_colormap,
    show_legend=False,
    margin=120,
    margin_top=200,
    margin_bottom=100,
    show_x_labels=False,
    show_y_labels=False,
)

chart.add("", [0])

# Save
chart.render_to_file("plot.svg")
chart.render_to_png("plot.png")

html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>spectrogram-mel - pygal</title>
    <style>
        body {{ margin: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; background: #f5f5f5; }}
        .chart {{ max-width: 100%; height: auto; }}
    </style>
</head>
<body>
    <figure class="chart">
        {chart.render(is_unicode=True)}
    </figure>
</body>
</html>
"""

with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)
