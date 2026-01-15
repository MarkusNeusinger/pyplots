""" pyplots.ai
smith-chart-basic: Smith Chart for RF/Impedance
Library: pygal 3.1.0 | Python 3.13.11
Quality: 79/100 | Created: 2026-01-15
"""

import numpy as np
import pygal
from pygal.style import Style


# Reference impedance
Z0 = 50  # ohms

# Generate Smith chart grid lines
r_values = [0, 0.2, 0.5, 1, 2, 5]  # Constant resistance circles
x_values = [0.2, 0.5, 1, 2, 5]  # Constant reactance arcs


def z_to_gamma(z_norm):
    """Convert normalized impedance to reflection coefficient."""
    return (z_norm - 1) / (z_norm + 1)


def get_resistance_circle(r, num_points=200):
    """Get points for constant resistance circle."""
    x_range = np.concatenate([np.linspace(-50, -0.01, num_points // 2), np.linspace(0.01, 50, num_points // 2)])
    points = []
    for x in x_range:
        z_norm = complex(r, x)
        gamma = z_to_gamma(z_norm)
        if abs(gamma) <= 1.001:
            points.append((gamma.real, gamma.imag))
    return points


def get_reactance_arc(x, num_points=100):
    """Get points for constant reactance arc."""
    r_range = np.linspace(0.001, 50, num_points)
    points = []
    for r in r_range:
        z_norm = complex(r, x)
        gamma = z_to_gamma(z_norm)
        if abs(gamma) <= 1.001:
            points.append((gamma.real, gamma.imag))
    return points


def get_unit_circle(num_points=100):
    """Get points for the outer unit circle boundary."""
    theta = np.linspace(0, 2 * np.pi, num_points)
    return [(np.cos(t), np.sin(t)) for t in theta]


# Custom style - Python Blue boundary, gray grid, prominent data
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#888888",
    colors=("#306998", "#BBBBBB", "#BBBBBB", "#555555", "#E74C3C", "#FFD43B"),
    title_font_size=56,
    label_font_size=24,
    major_label_font_size=22,
    legend_font_size=28,
    value_font_size=20,
    stroke_width=2,
    opacity=1.0,
    opacity_hover=1.0,
)

# Create XY chart for Smith chart
chart = pygal.XY(
    width=3600,
    height=3600,
    style=custom_style,
    title="smith-chart-basic · pygal · pyplots.ai",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=3,
    show_x_guides=False,
    show_y_guides=False,
    show_x_labels=False,
    show_y_labels=False,
    dots_size=5,
    stroke_style={"width": 2},
    range=(-1.25, 1.25),
    xrange=(-1.25, 1.25),
    margin=60,
)

# Add unit circle boundary (|gamma| = 1) - Python Blue
unit_circle = get_unit_circle(200)
chart.add("|Γ|=1 Boundary", unit_circle, show_dots=False, stroke_style={"width": 4})

# Add constant resistance circles as a single combined grid element - light gray
all_r_points = []
for r in r_values:
    circle_points = get_resistance_circle(r)
    all_r_points.extend(circle_points)
    all_r_points.append((None, None))
chart.add("R Grid", all_r_points, show_dots=False, stroke_style={"width": 1.5, "dasharray": "8,4"})

# Add constant reactance arcs combined - light gray
all_x_points = []
for x in x_values:
    pos_arc = get_reactance_arc(x)
    all_x_points.extend(pos_arc)
    all_x_points.append((None, None))
    neg_arc = get_reactance_arc(-x)
    all_x_points.extend(neg_arc)
    all_x_points.append((None, None))
chart.add("X Grid", all_x_points, show_dots=False, stroke_style={"width": 1.5, "dasharray": "8,4"})

# Add horizontal axis (real axis) - dark gray
chart.add("Real Axis", [(-1, 0), (1, 0)], show_dots=False, stroke_style={"width": 3})

# Generate example impedance data - antenna impedance sweep 1-6 GHz
np.random.seed(42)
num_points = 50
frequencies = np.linspace(1e9, 6e9, num_points)  # 1-6 GHz

# Simulate antenna impedance that varies with frequency
base_r = 25 + 50 * np.exp(-frequencies / 3e9)
base_x = 30 * np.sin(2 * np.pi * frequencies / 2e9) + 20 * np.cos(frequencies / 1e9)
z_real = base_r + np.random.randn(num_points) * 3
z_imag = base_x + np.random.randn(num_points) * 5

# Normalize impedance and convert to reflection coefficient
z_complex = z_real + 1j * z_imag
z_normalized = z_complex / Z0
gamma = z_to_gamma(z_normalized)

# Create impedance locus data points
impedance_locus = [(g.real, g.imag) for g in gamma]

# Add impedance locus curve - Red for visibility
chart.add("Antenna Z(f)", impedance_locus, show_dots=True, stroke_style={"width": 4}, dots_size=5)

# Add frequency markers at key points - Yellow for prominence
marker_indices = [0, num_points // 2, num_points - 1]
marker_points = [(gamma[i].real, gamma[i].imag) for i in marker_indices]
chart.add("1/3.5/6 GHz", marker_points, show_dots=True, dots_size=14, stroke=False)

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
