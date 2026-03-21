"""pyplots.ai
line-arrhenius: Arrhenius Plot for Reaction Kinetics
Library: pygal 3.1.0 | Python 3.14.3
Quality: 82/100 | Created: 2026-03-21
"""

import numpy as np
import pygal
from pygal.style import Style
from scipy import stats


# Data — First-order decomposition reaction rate constants at various temperatures
temperature_K = np.array([300, 330, 360, 400, 440, 480, 520, 560, 600])
np.random.seed(42)
activation_energy = 75000  # J/mol (75 kJ/mol)
R = 8.314  # Gas constant J/(mol·K)
pre_exponential = 1.0e12  # s⁻¹
rate_constant_k = pre_exponential * np.exp(-activation_energy / (R * temperature_K))
rate_constant_k *= np.exp(np.random.normal(0, 0.08, len(temperature_K)))

# Transformed coordinates for Arrhenius plot
inv_T = 1000.0 / temperature_K  # 1000/T for readable axis values (×10⁻³ K⁻¹)
ln_k = np.log(rate_constant_k)

# Linear regression: ln(k) = ln(A) - Ea/R × (1/T)
slope, intercept, r_value, p_value, std_err = stats.linregress(inv_T, ln_k)
r_squared = r_value**2
Ea_extracted = -slope * R * 1000  # Convert back (factor of 1000 from 1000/T scaling)

# Regression line — tightly constrained to data range
inv_T_fit = np.linspace(float(min(inv_T)), float(max(inv_T)), 50)
ln_k_fit = slope * inv_T_fit + intercept

# Style — orange fit line vs blue data for clear color contrast
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#2c3e50",
    foreground_strong="#2c3e50",
    foreground_subtle="#e0e0e0",
    colors=("#e67e22", "#306998", "#c0392b"),
    guide_stroke_color="#e8e8e8",
    major_guide_stroke_color="#d0d0d0",
    guide_stroke_dasharray="2,2",
    title_font_size=68,
    label_font_size=44,
    major_label_font_size=40,
    legend_font_size=42,
    value_font_size=32,
    tooltip_font_size=34,
    stroke_width=4,
    opacity=0.95,
    opacity_hover=1.0,
)

# Custom Y-axis labels at clean intervals
y_min, y_max = float(min(ln_k)), float(max(ln_k))
y_labels_list = list(range(int(np.floor(y_min)) - 1, int(np.ceil(y_max)) + 2, 2))

# Chart — pygal XY with explicit range control and custom labels
chart = pygal.XY(
    style=custom_style,
    width=4800,
    height=2700,
    title="line-arrhenius · pygal · pyplots.ai",
    x_title="1000/T (K⁻¹)",
    y_title="ln(k)",
    show_dots=True,
    dots_size=16,
    show_x_guides=False,
    show_y_guides=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=3,
    legend_box_size=28,
    truncate_legend=-1,
    margin=50,
    margin_top=80,
    margin_bottom=200,
    margin_left=180,
    tooltip_fancy_mode=True,
    tooltip_border_radius=8,
    x_value_formatter=lambda x: f"{x:.2f}",
    y_value_formatter=lambda y: f"{y:.0f}",
    range=(y_labels_list[0], y_labels_list[-1]),
    xrange=(float(min(inv_T) - 0.08), float(max(inv_T) + 0.08)),
    y_labels=y_labels_list,
    y_labels_major_every=1,
    print_values=False,
    css=["file://style.css", "file://graph.css", "inline:.axis > .line { stroke: transparent !important; }"],
)

# X-axis labels: show 1000/T values with corresponding temperature in K
x_label_temps = np.array([300, 360, 440, 520, 600])
x_label_positions = sorted(1000.0 / x_label_temps)
chart.x_labels = [float(x) for x in x_label_positions]
chart.x_labels_major = [float(x) for x in x_label_positions]
chart.x_label_rotation = 0
chart.x_value_formatter = lambda x: f"{x:.2f} ({int(round(1000.0 / x))} K)"

# Regression fit line (plotted first so data points appear on top)
fit_points = [
    {"value": (float(x), float(y)), "label": f"Fit: ln(k) = {slope:.2f} × (1000/T) + {intercept:.2f}"}
    for x, y in zip(inv_T_fit, ln_k_fit, strict=False)
]
chart.add(f"Linear Fit (R² = {r_squared:.4f})", fit_points, show_dots=False, stroke_style={"width": 5})

# Experimental data points — rich tooltips with multi-line labels
data_points = [
    {"value": (float(x), float(y)), "label": f"T = {int(t)} K | k = {k:.3e} s⁻¹ | ln(k) = {y:.2f}"}
    for x, y, t, k in zip(inv_T, ln_k, temperature_K, rate_constant_k, strict=False)
]
chart.add("Experimental Data", data_points, stroke=False, dots_size=18)

# Slope annotation — dashed segment highlighting Ea extraction
x_ann_start = float(inv_T[1])
x_ann_end = float(inv_T[-2])
y_ann_start = slope * x_ann_start + intercept
y_ann_end = slope * x_ann_end + intercept
slope_annotation = [
    {"value": (x_ann_start, y_ann_start), "label": f"Slope = {slope:.1f} → Eₐ = {Ea_extracted / 1000:.1f} kJ/mol"},
    {"value": (x_ann_end, y_ann_end), "label": f"Eₐ/R = {-slope * 1000:.0f} K"},
]
chart.add(
    f"Slope = {slope:.1f} · Eₐ = {Ea_extracted / 1000:.1f} kJ/mol",
    slope_annotation,
    show_dots=True,
    dots_size=14,
    stroke_style={"width": 5, "dasharray": "14,8"},
)

# Save — PNG for static output, HTML with pygal's interactive SVG tooltips
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
