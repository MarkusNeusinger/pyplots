"""pyplots.ai
scatter-constellation-diagram: Digital Modulation Constellation Diagram
Library: pygal | Python 3.13
Quality: pending | Created: 2026-03-17
"""

import numpy as np
import pygal
from pygal.style import Style


# Data — 16-QAM constellation with received symbols under additive Gaussian noise
np.random.seed(42)

# Ideal 16-QAM constellation points on a 4x4 grid at +/-1, +/-3
ideal_vals = [-3, -1, 1, 3]
ideal_i = np.array([i for i in ideal_vals for _ in ideal_vals])
ideal_q = np.array([q for _ in ideal_vals for q in ideal_vals])

# Generate received symbols — 1000 symbols with Gaussian noise (SNR ~20 dB)
n_symbols = 1000
symbol_indices = np.random.randint(0, 16, n_symbols)
snr_db = 20
noise_std = np.sqrt(10 ** (-snr_db / 10) * np.mean(ideal_i**2 + ideal_q**2))
received_i = ideal_i[symbol_indices] + np.random.normal(0, noise_std, n_symbols)
received_q = ideal_q[symbol_indices] + np.random.normal(0, noise_std, n_symbols)

# Compute EVM (Error Vector Magnitude)
error_vectors = np.sqrt((received_i - ideal_i[symbol_indices]) ** 2 + (received_q - ideal_q[symbol_indices]) ** 2)
avg_power = np.sqrt(np.mean(ideal_i**2 + ideal_q**2))
evm_percent = float(np.mean(error_vectors) / avg_power * 100)

# Style — 1:1 aspect ratio for constellation accuracy
font = "DejaVu Sans, Helvetica, Arial, sans-serif"
custom_style = Style(
    background="white",
    plot_background="#fafafa",
    foreground="#2a2a2a",
    foreground_strong="#2a2a2a",
    foreground_subtle="#e0e0e0",
    guide_stroke_color="#bbbbbb",
    guide_stroke_dasharray="6, 4",
    colors=("#cccccc", "#cccccc", "#cccccc", "#cccccc", "#cccccc", "#cccccc", "#306998", "#d64541"),
    font_family=font,
    title_font_family=font,
    title_font_size=52,
    label_font_size=40,
    major_label_font_size=36,
    legend_font_size=32,
    legend_font_family=font,
    value_font_size=26,
    tooltip_font_size=26,
    tooltip_font_family=font,
    opacity=0.35,
    opacity_hover=0.85,
    stroke_opacity=1,
    stroke_opacity_hover=1,
)

# Chart — square canvas for equal aspect ratio
chart = pygal.XY(
    width=3600,
    height=3600,
    style=custom_style,
    title=f"scatter-constellation-diagram · pygal · pyplots.ai  |  EVM = {evm_percent:.1f}%",
    x_title="In-Phase (I)",
    y_title="Quadrature (Q)",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=3,
    legend_box_size=22,
    stroke=False,
    dots_size=4,
    show_x_guides=True,
    show_y_guides=True,
    x_value_formatter=lambda x: f"{x:.1f}",
    value_formatter=lambda y: f"{y:.1f}",
    margin_bottom=100,
    margin_left=60,
    margin_right=40,
    margin_top=50,
    range=(-5, 5),
    xrange=(-5, 5),
    print_values=False,
    print_zeroes=False,
    truncate_legend=-1,
    js=[],
)

# Decision boundaries — dashed lines at +/-2, 0 on both axes
boundary_vals = [-2.0, 0.0, 2.0]
for bv in boundary_vals:
    chart.add(
        None,
        [{"value": (bv, -4.8)}, {"value": (bv, 4.8)}],
        stroke=True,
        show_dots=False,
        stroke_style={"width": 3, "dasharray": "12, 8", "linecap": "butt"},
    )
    chart.add(
        None,
        [{"value": (-4.8, bv)}, {"value": (4.8, bv)}],
        stroke=True,
        show_dots=False,
        stroke_style={"width": 3, "dasharray": "12, 8", "linecap": "butt"},
    )

# Received symbols — semi-transparent scatter points
rx_points = [(float(received_i[i]), float(received_q[i])) for i in range(n_symbols)]
chart.add(f"Received Symbols (n={n_symbols})", rx_points, stroke=False, dots_size=4)

# Ideal constellation points — large, prominent markers
ideal_points = [{"value": (float(ideal_i[k]), float(ideal_q[k]))} for k in range(16)]
chart.add("Ideal 16-QAM Points", ideal_points, stroke=False, dots_size=14)

# Save
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
