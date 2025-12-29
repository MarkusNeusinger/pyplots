"""pyplots.ai
survival-kaplan-meier: Kaplan-Meier Survival Plot
Library: pygal | Python 3.13
Quality: pending | Created: 2025-12-29
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
    [
        np.random.exponential(scale=18, size=50),  # Most patients
        np.random.exponential(scale=8, size=30),  # Higher risk subset
    ]
)
censored_standard = np.random.binomial(1, 0.25, size=n_per_group)  # 25% censored
event_standard = 1 - censored_standard

# Experimental treatment group - longer median survival
survival_times_experimental = np.concatenate(
    [
        np.random.exponential(scale=28, size=55),  # Most patients - better response
        np.random.exponential(scale=12, size=25),  # Some non-responders
    ]
)
censored_experimental = np.random.binomial(1, 0.30, size=n_per_group)  # 30% censored
event_experimental = 1 - censored_experimental


# Kaplan-Meier estimator function
def kaplan_meier(times, events):
    """Calculate Kaplan-Meier survival curve."""
    # Sort by time
    order = np.argsort(times)
    times = times[order]
    events = events[order]

    # Get unique event times
    unique_times = np.unique(times[events == 1])

    survival = [1.0]
    time_points = [0.0]

    n_at_risk = len(times)

    for t in unique_times:
        # Number of events at time t
        d = np.sum((times == t) & (events == 1))

        # Adjust at-risk count for those lost between previous time and current
        if len(time_points) > 1:
            prev_t = time_points[-1]
            lost = np.sum((times > prev_t) & (times < t))
            n_at_risk -= lost

        # Survival probability
        if n_at_risk > 0:
            s = survival[-1] * (1 - d / n_at_risk)
        else:
            s = survival[-1]

        time_points.append(t)
        survival.append(s)

        # Update at-risk for next iteration
        n_at_risk -= d

    return np.array(time_points), np.array(survival)


# Calculate Kaplan-Meier curves
time_std, surv_std = kaplan_meier(survival_times_standard, event_standard)
time_exp, surv_exp = kaplan_meier(survival_times_experimental, event_experimental)


# Create step function data for pygal XY chart
def create_step_data(times, survival):
    """Convert survival data to step function points for pygal."""
    points = []
    for i in range(len(times)):
        if i > 0:
            # Horizontal line from previous time to current time at previous survival level
            points.append((times[i], survival[i - 1]))
        # Vertical drop (or initial point)
        points.append((times[i], survival[i]))
    return points


step_std = create_step_data(time_std, surv_std)
step_exp = create_step_data(time_exp, surv_exp)

# Custom style for pyplots (4800x2700 canvas)
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#E15759", "#76B7B2"),  # Python Blue first, then Yellow
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=42,
    value_font_size=36,
    stroke_width=6,
    guide_stroke_dasharray="5,5",
    major_guide_stroke_dasharray="5,5",
    font_family="sans-serif",
    opacity=0.9,
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
    show_dots=False,  # Step function without dots at each point
    stroke=True,
    fill=False,
    show_x_guides=True,
    show_y_guides=True,
    x_label_rotation=0,
    truncate_legend=-1,
    legend_at_bottom=False,
    show_legend=True,
    range=(0, 1.05),  # Y-axis range for survival probability
    include_x_axis=True,
    margin=50,
    spacing=30,
)

# Add survival curves
chart.add("Standard Treatment", step_std, stroke_style={"width": 6})
chart.add("Experimental Treatment", step_exp, stroke_style={"width": 6})

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
