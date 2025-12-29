"""pyplots.ai
survival-kaplan-meier: Kaplan-Meier Survival Plot
Library: pygal 3.1.0 | Python 3.13.11
Quality: 78/100 | Created: 2025-12-29
"""

import numpy as np
import pygal
from pygal.style import Style


# Set seed for reproducibility
np.random.seed(42)

# Generate synthetic clinical trial survival data
# Two treatment groups: Standard (control) and Experimental (new treatment)
n_per_group = 80

# Standard treatment group - shorter median survival
survival_times_standard = np.concatenate(
    [np.random.exponential(scale=18, size=50), np.random.exponential(scale=8, size=30)]
)
censored_standard = np.random.binomial(1, 0.25, size=n_per_group)
event_standard = 1 - censored_standard

# Experimental treatment group - longer median survival
survival_times_experimental = np.concatenate(
    [np.random.exponential(scale=28, size=55), np.random.exponential(scale=12, size=25)]
)
censored_experimental = np.random.binomial(1, 0.30, size=n_per_group)
event_experimental = 1 - censored_experimental

# Calculate Kaplan-Meier for Standard treatment
order_std = np.argsort(survival_times_standard)
times_std_sorted = survival_times_standard[order_std]
events_std_sorted = event_standard[order_std]
censored_std_sorted = censored_standard[order_std]

unique_times_std = np.unique(times_std_sorted[events_std_sorted == 1])
survival_std = [1.0]
time_points_std = [0.0]
n_at_risk_std = len(times_std_sorted)

for t in unique_times_std:
    d = np.sum((times_std_sorted == t) & (events_std_sorted == 1))
    if len(time_points_std) > 1:
        prev_t = time_points_std[-1]
        lost = np.sum((times_std_sorted > prev_t) & (times_std_sorted < t))
        n_at_risk_std -= lost
    if n_at_risk_std > 0:
        s = survival_std[-1] * (1 - d / n_at_risk_std)
    else:
        s = survival_std[-1]
    time_points_std.append(t)
    survival_std.append(s)
    n_at_risk_std -= d

time_std = np.array(time_points_std)
surv_std = np.array(survival_std)

# Calculate Kaplan-Meier for Experimental treatment
order_exp = np.argsort(survival_times_experimental)
times_exp_sorted = survival_times_experimental[order_exp]
events_exp_sorted = event_experimental[order_exp]
censored_exp_sorted = censored_experimental[order_exp]

unique_times_exp = np.unique(times_exp_sorted[events_exp_sorted == 1])
survival_exp = [1.0]
time_points_exp = [0.0]
n_at_risk_exp = len(times_exp_sorted)

for t in unique_times_exp:
    d = np.sum((times_exp_sorted == t) & (events_exp_sorted == 1))
    if len(time_points_exp) > 1:
        prev_t = time_points_exp[-1]
        lost = np.sum((times_exp_sorted > prev_t) & (times_exp_sorted < t))
        n_at_risk_exp -= lost
    if n_at_risk_exp > 0:
        s = survival_exp[-1] * (1 - d / n_at_risk_exp)
    else:
        s = survival_exp[-1]
    time_points_exp.append(t)
    survival_exp.append(s)
    n_at_risk_exp -= d

time_exp = np.array(time_points_exp)
surv_exp = np.array(survival_exp)

# Create step function data for pygal XY chart
step_std = []
for i in range(len(time_std)):
    if i > 0:
        step_std.append((float(time_std[i]), float(surv_std[i - 1])))
    step_std.append((float(time_std[i]), float(surv_std[i])))

step_exp = []
for i in range(len(time_exp)):
    if i > 0:
        step_exp.append((float(time_exp[i]), float(surv_exp[i - 1])))
    step_exp.append((float(time_exp[i]), float(surv_exp[i])))

# Calculate 95% confidence intervals using Greenwood's formula
# Standard treatment CI
var_std = []
n_risk_std = len(times_std_sorted)
cumvar_std = 0.0
for i in range(len(time_std)):
    if i == 0:
        var_std.append(0.0)
    else:
        mask = times_std_sorted == time_std[i]
        d = np.sum(mask & (events_std_sorted == 1))
        if n_risk_std > 0 and d > 0:
            cumvar_std += d / (n_risk_std * (n_risk_std - d + 0.001))
        var_std.append(cumvar_std)
        n_risk_std -= np.sum(mask)

se_std = surv_std * np.sqrt(var_std)
ci_upper_std = np.minimum(surv_std + 1.96 * se_std, 1.0)
ci_lower_std = np.maximum(surv_std - 1.96 * se_std, 0.0)

# Experimental treatment CI
var_exp = []
n_risk_exp = len(times_exp_sorted)
cumvar_exp = 0.0
for i in range(len(time_exp)):
    if i == 0:
        var_exp.append(0.0)
    else:
        mask = times_exp_sorted == time_exp[i]
        d = np.sum(mask & (events_exp_sorted == 1))
        if n_risk_exp > 0 and d > 0:
            cumvar_exp += d / (n_risk_exp * (n_risk_exp - d + 0.001))
        var_exp.append(cumvar_exp)
        n_risk_exp -= np.sum(mask)

se_exp = surv_exp * np.sqrt(var_exp)
ci_upper_exp = np.minimum(surv_exp + 1.96 * se_exp, 1.0)
ci_lower_exp = np.maximum(surv_exp - 1.96 * se_exp, 0.0)

# Create CI step function data - combined for cleaner visual
ci_std_upper_step = []
ci_std_lower_step = []
for i in range(len(time_std)):
    if i > 0:
        ci_std_upper_step.append((float(time_std[i]), float(ci_upper_std[i - 1])))
        ci_std_lower_step.append((float(time_std[i]), float(ci_lower_std[i - 1])))
    ci_std_upper_step.append((float(time_std[i]), float(ci_upper_std[i])))
    ci_std_lower_step.append((float(time_std[i]), float(ci_lower_std[i])))

ci_exp_upper_step = []
ci_exp_lower_step = []
for i in range(len(time_exp)):
    if i > 0:
        ci_exp_upper_step.append((float(time_exp[i]), float(ci_upper_exp[i - 1])))
        ci_exp_lower_step.append((float(time_exp[i]), float(ci_lower_exp[i - 1])))
    ci_exp_upper_step.append((float(time_exp[i]), float(ci_upper_exp[i])))
    ci_exp_lower_step.append((float(time_exp[i]), float(ci_lower_exp[i])))

# Get censored observation points with survival values (as simple tuples for pygal XY)
censored_times_std = times_std_sorted[censored_std_sorted == 1]
censored_markers_std = []
for ct in censored_times_std:
    idx = np.searchsorted(time_std, ct, side="right") - 1
    idx = max(0, min(idx, len(surv_std) - 1))
    censored_markers_std.append((float(ct), float(surv_std[idx])))

censored_times_exp = times_exp_sorted[censored_exp_sorted == 1]
censored_markers_exp = []
for ct in censored_times_exp:
    idx = np.searchsorted(time_exp, ct, side="right") - 1
    idx = max(0, min(idx, len(surv_exp) - 1))
    censored_markers_exp.append((float(ct), float(surv_exp[idx])))

# Custom style for pyplots (4800x2700 canvas)
# Colorblind-safe blue/yellow palette
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#7BA3C9", "#FFE680", "#306998", "#FFD43B"),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=40,
    value_font_size=36,
    stroke_width=5,
    guide_stroke_dasharray="5,5",
    major_guide_stroke_dasharray="5,5",
    font_family="sans-serif",
    opacity=1.0,
    opacity_hover=1.0,
)

# Create XY chart for survival curves
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="survival-kaplan-meier · pygal · pyplots.ai",
    x_title="Time (Months)",
    y_title="Survival Probability",
    show_dots=False,
    stroke=True,
    fill=False,
    show_x_guides=True,
    show_y_guides=True,
    x_label_rotation=0,
    truncate_legend=-1,
    legend_at_bottom=True,
    legend_at_bottom_columns=3,
    show_legend=True,
    range=(0, 1.05),
    include_x_axis=True,
    margin=60,
    spacing=40,
    explicit_size=True,
)

# Add main survival curves first (these are the primary data)
chart.add("Standard Treatment", step_std, stroke_style={"width": 8})
chart.add("Experimental Treatment", step_exp, stroke_style={"width": 8})

# Add 95% CI bounds as thinner dashed lines (same colors, lighter)
chart.add("Standard 95% CI", ci_std_upper_step + ci_std_lower_step, stroke_style={"width": 3, "dasharray": "10,6"})
chart.add("Experimental 95% CI", ci_exp_upper_step + ci_exp_lower_step, stroke_style={"width": 3, "dasharray": "10,6"})

# Add censored observations as separate scatter series with visible markers
chart.add("Censored (Std)", censored_markers_std, stroke=False, show_dots=True, dots_size=15)
chart.add("Censored (Exp)", censored_markers_exp, stroke=False, show_dots=True, dots_size=15)

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
