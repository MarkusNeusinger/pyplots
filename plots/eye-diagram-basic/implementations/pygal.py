"""pyplots.ai
eye-diagram-basic: Signal Integrity Eye Diagram
Library: pygal | Python 3.13
Quality: pending | Created: 2026-03-17
"""

import importlib
import sys

import numpy as np


# Import pygal avoiding name collision with this filename
_cwd = sys.path[0]
sys.path[:] = [p for p in sys.path if p != _cwd]
_pygal = importlib.import_module("pygal")
_Style = importlib.import_module("pygal.style").Style
_cairosvg = importlib.import_module("cairosvg")
sys.path.insert(0, _cwd)

# Data — Simulated NRZ eye diagram
np.random.seed(42)

n_traces = 300
samples_per_ui = 150
total_samples = samples_per_ui * 2  # 2 UI window

time_ui = np.linspace(0, 2, total_samples)

# Sigmoid transition filter
transition_width = 0.08  # UI, controls bandwidth-limited rise/fall

all_voltages = []
for _ in range(n_traces):
    # Random 4-bit sequence (need bits before and after the 2-UI window for transitions)
    bits = np.random.randint(0, 2, 6)

    # Build ideal NRZ waveform with smooth transitions over extended window
    extended_time = np.linspace(-1, 3, samples_per_ui * 4)
    voltage = np.zeros_like(extended_time)
    for bit_idx in range(len(bits)):
        bit_start = bit_idx - 1  # offset since bits cover [-1, 5] UI range
        for s_idx in range(len(extended_time)):
            t = extended_time[s_idx]
            # Sigmoid transition at each bit boundary
            if bit_idx > 0:
                boundary = bit_start
                contrib = (bits[bit_idx] - bits[bit_idx - 1]) * (
                    1.0 / (1.0 + np.exp(-(t - boundary) / transition_width))
                )
                voltage[s_idx] += contrib

    voltage += bits[0]  # base level from first bit

    # Clip to reasonable range
    voltage = np.clip(voltage, -0.2, 1.2)

    # Extract the 2-UI window [0, 2]
    mask = (extended_time >= 0) & (extended_time <= 2)
    trace_voltage = voltage[mask][:total_samples]

    # Add Gaussian noise (sigma ~5% of amplitude)
    noise = np.random.normal(0, 0.05, len(trace_voltage))
    trace_voltage = trace_voltage + noise

    # Add random jitter (sigma ~3% of UI) by shifting time axis
    jitter = np.random.normal(0, 0.03)
    jittered_time = time_ui + jitter

    all_voltages.append((jittered_time, trace_voltage))

# Build 2D density histogram for heatmap coloring
n_xbins = 120
n_ybins = 80
x_edges = np.linspace(-0.1, 2.1, n_xbins + 1)
y_edges = np.linspace(-0.3, 1.3, n_ybins + 1)

density = np.zeros((n_ybins, n_xbins))
for jittered_time, trace_voltage in all_voltages:
    for t_val, v_val in zip(jittered_time, trace_voltage, strict=False):
        xi = int((t_val - x_edges[0]) / (x_edges[-1] - x_edges[0]) * n_xbins)
        yi = int((v_val - y_edges[0]) / (y_edges[-1] - y_edges[0]) * n_ybins)
        if 0 <= xi < n_xbins and 0 <= yi < n_ybins:
            density[yi, xi] += 1

# Smooth the density with a simple box filter (3x3 average, applied twice)
for _ in range(2):
    padded = np.pad(density, 1, mode="edge")
    density = (
        padded[:-2, :-2]
        + padded[:-2, 1:-1]
        + padded[:-2, 2:]
        + padded[1:-1, :-2]
        + padded[1:-1, 1:-1]
        + padded[1:-1, 2:]
        + padded[2:, :-2]
        + padded[2:, 1:-1]
        + padded[2:, 2:]
    ) / 9.0
max_density = density.max()

# Color palette: dark blue (low) -> cyan -> green -> yellow -> red (high)
color_stops = [
    (0.00, (10, 10, 40)),
    (0.10, (20, 50, 120)),
    (0.25, (30, 100, 180)),
    (0.40, (40, 170, 180)),
    (0.55, (60, 200, 100)),
    (0.70, (180, 220, 50)),
    (0.85, (240, 180, 30)),
    (1.00, (240, 60, 30)),
]

# Build SVG directly for the density heatmap eye diagram
W, H = 4800, 2700
margin_left = 500
margin_right = 500
margin_top = 300
margin_bottom = 350
plot_w = W - margin_left - margin_right
plot_h = H - margin_top - margin_bottom

svg_elements = []
svg_elements.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')

# Background
svg_elements.append(f'<rect width="{W}" height="{H}" fill="white"/>')

# Plot background (dark for eye diagram contrast)
svg_elements.append(f'<rect x="{margin_left}" y="{margin_top}" width="{plot_w}" height="{plot_h}" fill="#0a0a28"/>')

# Draw density heatmap cells
cell_w = plot_w / n_xbins
cell_h = plot_h / n_ybins

for yi in range(n_ybins):
    for xi in range(n_xbins):
        val = density[yi, xi]
        if val < 0.5:
            continue
        t = min(1.0, val / (max_density * 0.7))  # boost contrast

        # Interpolate color
        r, g, b = color_stops[-1][1]
        for k in range(len(color_stops) - 1):
            t0, c0 = color_stops[k]
            t1, c1 = color_stops[k + 1]
            if t <= t1:
                frac = (t - t0) / (t1 - t0) if t1 > t0 else 0
                r = int(c0[0] + (c1[0] - c0[0]) * frac)
                g = int(c0[1] + (c1[1] - c0[1]) * frac)
                b = int(c0[2] + (c1[2] - c0[2]) * frac)
                break

        px = margin_left + xi * cell_w
        # Flip y: low voltage at bottom, high at top
        py = margin_top + (n_ybins - 1 - yi) * cell_h
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        svg_elements.append(
            f'<rect x="{px:.1f}" y="{py:.1f}" width="{cell_w + 0.5:.1f}" '
            f'height="{cell_h + 0.5:.1f}" fill="{hex_color}"/>'
        )

# Axis lines (left and bottom only)
svg_elements.append(
    f'<line x1="{margin_left}" y1="{margin_top}" x2="{margin_left}" '
    f'y2="{margin_top + plot_h}" stroke="#333333" stroke-width="3"/>'
)
svg_elements.append(
    f'<line x1="{margin_left}" y1="{margin_top + plot_h}" x2="{margin_left + plot_w}" '
    f'y2="{margin_top + plot_h}" stroke="#333333" stroke-width="3"/>'
)

# X-axis labels (Unit Intervals)
x_ticks = [0.0, 0.5, 1.0, 1.5, 2.0]
for xt in x_ticks:
    px = margin_left + (xt - x_edges[0]) / (x_edges[-1] - x_edges[0]) * plot_w
    label_y = margin_top + plot_h + 60
    svg_elements.append(
        f'<text x="{px:.0f}" y="{label_y}" text-anchor="middle" fill="#333333" '
        f'style="font-size:42px;font-family:sans-serif">{xt:.1f}</text>'
    )
    # Tick mark
    svg_elements.append(
        f'<line x1="{px:.0f}" y1="{margin_top + plot_h}" x2="{px:.0f}" '
        f'y2="{margin_top + plot_h + 12}" stroke="#333333" stroke-width="2"/>'
    )

# Y-axis labels (Voltage)
y_ticks = [-0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2]
for yt in y_ticks:
    py = margin_top + plot_h - (yt - y_edges[0]) / (y_edges[-1] - y_edges[0]) * plot_h
    if py < margin_top or py > margin_top + plot_h:
        continue
    svg_elements.append(
        f'<text x="{margin_left - 20}" y="{py + 14:.0f}" text-anchor="end" fill="#333333" '
        f'style="font-size:42px;font-family:sans-serif">{yt:.1f}</text>'
    )
    # Tick mark
    svg_elements.append(
        f'<line x1="{margin_left - 12}" y1="{py:.0f}" x2="{margin_left}" '
        f'y2="{py:.0f}" stroke="#333333" stroke-width="2"/>'
    )

# Axis titles
svg_elements.append(
    f'<text x="{margin_left + plot_w / 2}" y="{margin_top + plot_h + 130}" '
    f'text-anchor="middle" fill="#333333" '
    f'style="font-size:52px;font-weight:bold;font-family:sans-serif">Time (UI)</text>'
)
mid_y = margin_top + plot_h / 2
svg_elements.append(
    f'<text x="{margin_left - 160}" y="{mid_y}" text-anchor="middle" fill="#333333" '
    f'style="font-size:52px;font-weight:bold;font-family:sans-serif" '
    f'transform="rotate(-90, {margin_left - 160}, {mid_y})">Voltage (V)</text>'
)

# Title
svg_elements.append(
    f'<text x="{W / 2}" y="80" text-anchor="middle" fill="#333333" '
    f'style="font-size:72px;font-weight:600;font-family:sans-serif">'
    f"eye-diagram-basic \u00b7 pygal \u00b7 pyplots.ai</text>"
)

# Subtitle
svg_elements.append(
    f'<text x="{W / 2}" y="140" text-anchor="middle" fill="#666666" '
    f'style="font-size:38px;font-family:sans-serif">'
    f"NRZ Signal \u2014 300 overlaid traces with jitter and noise</text>"
)

# Colorbar
cb_x = margin_left + plot_w + 40
cb_w = 40
cb_top = margin_top + 30
cb_bot = margin_top + plot_h - 30
cb_h = cb_bot - cb_top
n_segs = 80

for s in range(n_segs):
    frac = 1.0 - s / (n_segs - 1)  # top = high density
    r, g, b = color_stops[-1][1]
    for k in range(len(color_stops) - 1):
        t0, c0 = color_stops[k]
        t1, c1 = color_stops[k + 1]
        if frac <= t1:
            f2 = (frac - t0) / (t1 - t0) if t1 > t0 else 0
            r = int(c0[0] + (c1[0] - c0[0]) * f2)
            g = int(c0[1] + (c1[1] - c0[1]) * f2)
            b = int(c0[2] + (c1[2] - c0[2]) * f2)
            break
    sy = cb_top + cb_h * s / n_segs
    hex_c = f"#{r:02x}{g:02x}{b:02x}"
    svg_elements.append(
        f'<rect x="{cb_x}" y="{sy:.1f}" width="{cb_w}" height="{cb_h / n_segs + 1:.1f}" fill="{hex_c}"/>'
    )

svg_elements.append(
    f'<rect x="{cb_x}" y="{cb_top}" width="{cb_w}" height="{cb_h}" fill="none" stroke="#666666" stroke-width="1.5"/>'
)

# Colorbar labels
svg_elements.append(
    f'<text x="{cb_x + cb_w + 16}" y="{cb_top + 14}" fill="#333333" '
    f'style="font-size:34px;font-family:sans-serif">High</text>'
)
svg_elements.append(
    f'<text x="{cb_x + cb_w + 16}" y="{cb_bot + 8}" fill="#333333" '
    f'style="font-size:34px;font-family:sans-serif">Low</text>'
)
svg_elements.append(
    f'<text x="{cb_x + cb_w / 2}" y="{cb_top - 20}" text-anchor="middle" '
    f'fill="#333333" style="font-size:36px;font-weight:bold;font-family:sans-serif">'
    f"Density</text>"
)

# Dashed reference lines at logic levels 0 and 1
for level in [0.0, 1.0]:
    py = margin_top + plot_h - (level - y_edges[0]) / (y_edges[-1] - y_edges[0]) * plot_h
    svg_elements.append(
        f'<line x1="{margin_left}" y1="{py:.0f}" x2="{margin_left + plot_w}" '
        f'y2="{py:.0f}" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="12,8" '
        f'opacity="0.4"/>'
    )

svg_elements.append("</svg>")
svg_content = "\n".join(svg_elements)

# Save PNG
_cairosvg.svg2png(bytestring=svg_content.encode("utf-8"), write_to="plot.png", output_width=W, output_height=H)

# Save interactive HTML with embedded SVG
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>eye-diagram-basic - pygal</title>
    <style>
        body {{ margin: 0; display: flex; justify-content: center; align-items: center;
               min-height: 100vh; background: #f5f5f5; }}
        .chart {{ max-width: 100%; height: auto; }}
    </style>
</head>
<body>
    <figure class="chart">
        {svg_content}
    </figure>
</body>
</html>
"""

with open("plot.html", "w", encoding="utf-8") as fout:
    fout.write(html_content)
