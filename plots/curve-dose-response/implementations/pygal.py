"""pyplots.ai
curve-dose-response: Pharmacological Dose-Response Curve
Library: pygal 3.1.0 | Python 3.14.3
Quality: 75/100 | Created: 2026-03-18
"""

import numpy as np
import pygal
from pygal.style import Style
from scipy.optimize import curve_fit


# Data
np.random.seed(42)
concentrations = np.logspace(-9, -4, 8)
log_conc = np.log10(concentrations)


def four_pl(x, bottom, top, ec50, hill):
    return bottom + (top - bottom) / (1 + (ec50 / x) ** hill)


# Compound A — potent agonist
response_a_true = four_pl(concentrations, 5, 95, 1e-7, 1.2)
response_a_sem = np.random.uniform(2, 5, len(concentrations))
response_a = response_a_true + np.random.normal(0, response_a_sem)

# Compound B — moderate agonist
response_b_true = four_pl(concentrations, 10, 85, 1e-6, 0.9)
response_b_sem = np.random.uniform(2, 6, len(concentrations))
response_b = response_b_true + np.random.normal(0, response_b_sem)

# Fit 4PL curves
popt_a, pcov_a = curve_fit(four_pl, concentrations, response_a, p0=[0, 100, 1e-7, 1], maxfev=10000)
popt_b, pcov_b = curve_fit(four_pl, concentrations, response_b, p0=[0, 100, 1e-6, 1], maxfev=10000)

# Smooth fitted curves
conc_smooth = np.logspace(-9.5, -3.5, 200)
log_smooth = np.log10(conc_smooth)
fit_a = four_pl(conc_smooth, *popt_a)
fit_b = four_pl(conc_smooth, *popt_b)

# Extract fit parameters
bottom_a, top_a, ec50_a, hill_a = popt_a
bottom_b, top_b, ec50_b, hill_b = popt_b
half_a = bottom_a + (top_a - bottom_a) / 2
half_b = bottom_b + (top_b - bottom_b) / 2
log_ec50_a = np.log10(ec50_a)
log_ec50_b = np.log10(ec50_b)

# 95% CI for Compound A via parameter covariance sampling
np.random.seed(99)
param_samples = np.random.multivariate_normal(popt_a, pcov_a, size=200)
fit_ensemble = np.array([four_pl(conc_smooth, *p) for p in param_samples])
ci_lower = np.percentile(fit_ensemble, 2.5, axis=0)
ci_upper = np.percentile(fit_ensemble, 97.5, axis=0)

# Build error bar segments as single series per compound using node={'r': 0} to hide markers
cap = 0.06


def pt(x, y):
    return {"value": (x, y), "node": {"r": 0}}


err_bar_a = []
for i in range(len(log_conc)):
    x, y, sem = log_conc[i], response_a[i], response_a_sem[i]
    err_bar_a.extend([pt(x, y - sem), pt(x, y + sem), None])
    err_bar_a.extend([pt(x - cap, y - sem), pt(x + cap, y - sem), None])
    err_bar_a.extend([pt(x - cap, y + sem), pt(x + cap, y + sem), None])

err_bar_b = []
for i in range(len(log_conc)):
    x, y, sem = log_conc[i], response_b[i], response_b_sem[i]
    err_bar_b.extend([pt(x, y - sem), pt(x, y + sem), None])
    err_bar_b.extend([pt(x - cap, y - sem), pt(x + cap, y - sem), None])
    err_bar_b.extend([pt(x - cap, y + sem), pt(x + cap, y + sem), None])

# Colors — colorblind-safe blue + orange
palette_a = "#306998"
palette_b = "#E68A00"
palette_ci = "#89ABD0"
palette_asym = "#888888"

custom_style = Style(
    background="white",
    plot_background="#FAFAFA",
    foreground="#333",
    foreground_strong="#222",
    foreground_subtle="#DDDDDD",
    colors=(
        palette_a,
        palette_b,  # fitted curves
        palette_a,
        palette_b,  # data points
        palette_ci,
        palette_ci,  # CI bounds
        palette_a,
        palette_a,  # EC50 A (vert + horiz)
        palette_b,
        palette_b,  # EC50 B (vert + horiz)
        palette_asym,
        palette_asym,  # asymptote A (top + bottom)
        palette_asym,
        palette_asym,  # asymptote B (top + bottom)
        palette_a,
        palette_b,  # error bars
    ),
    title_font_size=36,
    label_font_size=22,
    major_label_font_size=20,
    legend_font_size=20,
    value_font_size=16,
    stroke_width=3,
)

chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="curve-dose-response \u00b7 pygal \u00b7 pyplots.ai",
    x_title="log\u2081\u2080 Concentration (M)",
    y_title="Response (%)",
    show_dots=False,
    dots_size=4,
    stroke=True,
    show_x_guides=False,
    show_y_guides=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=5,
    x_label_rotation=0,
    truncate_legend=-1,
)

# Fitted curves
chart.add(
    f"Compound A (EC\u2085\u2080={ec50_a:.1e} M)",
    list(zip(log_smooth.tolist(), fit_a.tolist(), strict=True)),
    show_dots=False,
    stroke_style={"width": 7, "linecap": "round", "linejoin": "round"},
)
chart.add(
    f"Compound B (EC\u2085\u2080={ec50_b:.1e} M)",
    list(zip(log_smooth.tolist(), fit_b.tolist(), strict=True)),
    show_dots=False,
    stroke_style={"width": 7, "linecap": "round", "linejoin": "round"},
)

# Data points
chart.add(
    "Compound A data",
    list(zip(log_conc.tolist(), response_a.tolist(), strict=True)),
    stroke=False,
    show_dots=True,
    dots_size=14,
)
chart.add(
    "Compound B data",
    list(zip(log_conc.tolist(), response_b.tolist(), strict=True)),
    stroke=False,
    show_dots=True,
    dots_size=14,
)

# 95% CI bounds for Compound A
chart.add(
    "95% CI (A)",
    list(zip(log_smooth.tolist(), ci_upper.tolist(), strict=True)),
    show_dots=False,
    stroke_style={"width": 2, "dasharray": "8, 6", "linecap": "round"},
)
chart.add(
    None,
    list(zip(log_smooth.tolist(), ci_lower.tolist(), strict=True)),
    show_dots=False,
    stroke_style={"width": 2, "dasharray": "8, 6", "linecap": "round"},
)

# EC50 reference lines — Compound A
chart.add(
    "EC\u2085\u2080 ref. lines",
    [pt(log_ec50_a, 0), pt(log_ec50_a, half_a)],
    show_dots=False,
    stroke_style={"width": 3, "dasharray": "12, 8"},
)
chart.add(
    None,
    [pt(log_smooth[0], half_a), pt(log_ec50_a, half_a)],
    show_dots=False,
    stroke_style={"width": 3, "dasharray": "12, 8"},
)

# EC50 reference lines — Compound B
chart.add(
    None, [pt(log_ec50_b, 0), pt(log_ec50_b, half_b)], show_dots=False, stroke_style={"width": 3, "dasharray": "12, 8"}
)
chart.add(
    None,
    [pt(log_smooth[0], half_b), pt(log_ec50_b, half_b)],
    show_dots=False,
    stroke_style={"width": 3, "dasharray": "12, 8"},
)

# Top and bottom asymptote lines — Compound A
x_range = [log_smooth[0], log_smooth[-1]]
chart.add(
    "Asymptotes",
    [pt(x_range[0], top_a), pt(x_range[1], top_a)],
    show_dots=False,
    stroke_style={"width": 2, "dasharray": "4, 6"},
)
chart.add(
    None,
    [pt(x_range[0], bottom_a), pt(x_range[1], bottom_a)],
    show_dots=False,
    stroke_style={"width": 2, "dasharray": "4, 6"},
)

# Top and bottom asymptote lines — Compound B
chart.add(
    None,
    [pt(x_range[0], top_b), pt(x_range[1], top_b)],
    show_dots=False,
    stroke_style={"width": 2, "dasharray": "4, 6"},
)
chart.add(
    None,
    [pt(x_range[0], bottom_b), pt(x_range[1], bottom_b)],
    show_dots=False,
    stroke_style={"width": 2, "dasharray": "4, 6"},
)

# Error bars — consolidated into one series per compound
chart.add(None, err_bar_a, stroke=True, show_dots=False, stroke_style={"width": 2})
chart.add(None, err_bar_b, stroke=True, show_dots=False, stroke_style={"width": 2})

# Save
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
