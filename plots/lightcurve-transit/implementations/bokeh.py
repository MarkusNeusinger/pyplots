"""pyplots.ai
lightcurve-transit: Astronomical Light Curve
Library: bokeh 3.9.0 | Python 3.14.3
Quality: 79/100 | Created: 2026-03-18
"""

import numpy as np
from bokeh.io import export_png, output_file, save
from bokeh.models import Band, ColumnDataSource, HoverTool, Whisker
from bokeh.plotting import figure


# Data - simulated exoplanet transit (phase-folded, hot Jupiter style)
np.random.seed(42)

n_points = 600
phase = np.sort(np.random.uniform(0.0, 1.0, n_points))

# Transit parameters (wide transit for visual clarity)
transit_center = 0.5
transit_depth = 0.012  # ~1.2% dip
half_duration = 0.06  # half of total transit duration in phase

# Simple smooth transit model using a cosine-bell shape
dist = np.abs(phase - transit_center)
in_transit = dist < half_duration
model_flux = np.ones(n_points)
model_flux[in_transit] = 1.0 - transit_depth * (0.5 + 0.5 * np.cos(np.pi * dist[in_transit] / half_duration))

# Photometric noise
flux_err = np.random.uniform(0.001, 0.002, n_points)
flux = model_flux + np.random.normal(0, 1, n_points) * flux_err

# Smooth model for overlay line
phase_model = np.linspace(0.0, 1.0, 3000)
dist_m = np.abs(phase_model - transit_center)
in_transit_m = dist_m < half_duration
model_smooth = np.ones(3000)
model_smooth[in_transit_m] = 1.0 - transit_depth * (0.5 + 0.5 * np.cos(np.pi * dist_m[in_transit_m] / half_duration))

# 1-sigma band around model (narrower for cleaner look)
model_band_upper = model_smooth + 0.0008
model_band_lower = model_smooth - 0.0008
source_band = ColumnDataSource(data={"phase": phase_model, "upper": model_band_upper, "lower": model_band_lower})

# Data sources
source_data = ColumnDataSource(
    data={
        "phase": phase,
        "flux": flux,
        "flux_err": flux_err,
        "model_flux": model_flux,
        "residual": (flux - model_flux) * 1000,
        "upper": flux + flux_err,
        "lower": flux - flux_err,
    }
)

source_model = ColumnDataSource(data={"phase": phase_model, "model": model_smooth})

# Plot
p = figure(
    width=4800,
    height=2700,
    title="lightcurve-transit · bokeh · pyplots.ai",
    x_axis_label="Orbital Phase",
    y_axis_label="Relative Flux",
    background_fill_color="#F8F9FA",
)

# Confidence band around transit model
band = Band(
    base="phase",
    upper="upper",
    lower="lower",
    source=source_band,
    fill_color="#306998",
    fill_alpha=0.12,
    line_color=None,
)
p.add_layout(band)

# Error bars (reduced alpha to avoid visual noise)
whisker = Whisker(
    base="phase", upper="upper", lower="lower", source=source_data, line_color="#306998", line_alpha=0.08, line_width=1
)
whisker.upper_head.size = 0
whisker.lower_head.size = 0
p.add_layout(whisker)

# Data points (larger markers)
scatter_renderer = p.scatter(
    x="phase",
    y="flux",
    source=source_data,
    size=14,
    color="#306998",
    alpha=0.5,
    line_color="#1A3A5C",
    line_width=1,
    legend_label="Photometric Data",
)

# Transit model curve (colorblind-friendly amber/gold instead of red-orange)
p.line(
    x="phase",
    y="model",
    source=source_model,
    line_color="#D4A017",
    line_width=5,
    line_alpha=0.95,
    legend_label="Transit Model",
)

# HoverTool for interactive exploration
hover = HoverTool(
    renderers=[scatter_renderer],
    tooltips=[
        ("Phase", "@phase{0.0000}"),
        ("Flux", "@flux{0.00000}"),
        ("Error", "±@flux_err{0.00000}"),
        ("Residual", "@residual{+0.000} ppt"),
    ],
    mode="mouse",
)
p.add_tools(hover)

# Typography
p.title.text_font_size = "32pt"
p.title.text_color = "#2C3E50"
p.xaxis.axis_label_text_font_size = "24pt"
p.yaxis.axis_label_text_font_size = "24pt"
p.xaxis.major_label_text_font_size = "18pt"
p.yaxis.major_label_text_font_size = "18pt"
p.xaxis.axis_label_text_color = "#34495E"
p.yaxis.axis_label_text_color = "#34495E"

# Remove spines (outline) for cleaner look
p.outline_line_color = None

# Axis styling
p.xaxis.axis_line_color = "#BDC3C7"
p.yaxis.axis_line_color = "#BDC3C7"
p.xaxis.major_tick_line_color = "#BDC3C7"
p.yaxis.major_tick_line_color = "#BDC3C7"
p.xaxis.minor_tick_line_color = None
p.yaxis.minor_tick_line_color = None

# Grid
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = "#E0E0E0"
p.ygrid.grid_line_alpha = 0.4
p.ygrid.grid_line_dash = [4, 4]

# Legend
p.legend.location = "top_left"
p.legend.label_text_font_size = "22pt"
p.legend.background_fill_alpha = 0.85
p.legend.background_fill_color = "#FFFFFF"
p.legend.border_line_color = "#BDC3C7"
p.legend.border_line_alpha = 0.5
p.legend.padding = 15
p.legend.spacing = 8
p.legend.glyph_height = 25
p.legend.glyph_width = 25

# Save
export_png(p, filename="plot.png")
output_file("plot.html", title="lightcurve-transit · bokeh · pyplots.ai")
save(p)
