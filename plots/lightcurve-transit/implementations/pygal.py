""" pyplots.ai
lightcurve-transit: Astronomical Light Curve
Library: pygal 3.1.0 | Python 3.14.3
Quality: 74/100 | Created: 2026-03-18
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - simulated exoplanet transit (phase-folded)
np.random.seed(42)

n_points = 300
phase = np.sort(np.random.uniform(0.0, 1.0, n_points))

# Transit parameters
transit_center = 0.5
transit_duration = 0.08
transit_depth = 0.01

# Smooth transit model using a Gaussian-like dip for limb-darkened shape
model_phase = np.linspace(0.0, 1.0, 500)
sigma = transit_duration / 3.5
model_flux_curve = 1.0 - transit_depth * np.exp(-0.5 * ((model_phase - transit_center) / sigma) ** 2)

# Interpolate model at observation phases
model_flux = np.interp(phase, model_phase, model_flux_curve)

# Observed flux with noise
flux_err = np.random.uniform(0.0015, 0.003, n_points)
flux = model_flux + np.random.normal(0, 1, n_points) * flux_err

# Custom style
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#cccccc",
    colors=("#306998", "#D4513D"),
    title_font_size=56,
    label_font_size=40,
    major_label_font_size=36,
    legend_font_size=36,
    value_font_size=28,
    stroke_width=4,
    opacity=0.65,
)

# Model curve points (dense, for smooth line)
model_points = [
    (round(float(model_phase[i]), 5), round(float(model_flux_curve[i]), 6)) for i in range(len(model_phase))
]

# Scatter data points
scatter_points = [{"value": (round(float(phase[i]), 5), round(float(flux[i]), 6))} for i in range(n_points)]

# Plot
flux_min = float(np.min(flux)) - 0.003
flux_max = float(np.max(flux)) + 0.003

chart = pygal.XY(
    style=custom_style,
    width=4800,
    height=2700,
    title="lightcurve-transit · pygal · pyplots.ai",
    x_title="Orbital Phase",
    y_title="Relative Flux",
    show_x_guides=False,
    show_y_guides=True,
    dots_size=6,
    range=(flux_min, flux_max),
    xrange=(0.0, 1.0),
    margin_right=50,
    x_value_formatter=lambda x: f"{x:.2f}",
    y_value_formatter=lambda y: f"{y:.4f}",
)

# Add data series
chart.add("Observed Flux", scatter_points, stroke=False, dots_size=6)
chart.add("Transit Model", model_points, stroke=True, show_dots=False, stroke_width=5)

# Save
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
