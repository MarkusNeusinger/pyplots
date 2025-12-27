""" pyplots.ai
forest-basic: Meta-Analysis Forest Plot
Library: pygal 3.1.0 | Python 3.13.11
Quality: 58/100 | Created: 2025-12-27
"""

import pygal
from pygal.style import Style


# Data: Meta-analysis of treatment effect (mean difference)
# Format: (study_name, effect_size, ci_lower, ci_upper, weight)
studies = [
    ("Anderson 2023", -0.44, -0.82, -0.06, 12.8),
    ("Taylor 2022", -0.61, -1.08, -0.14, 7.6),
    ("Moore 2022", -0.38, -0.71, -0.05, 13.8),
    ("Wilson 2021", -0.55, -0.98, -0.12, 9.1),
    ("Miller 2021", -0.29, -0.65, 0.07, 11.7),
    ("Davis 2020", -0.41, -0.78, -0.04, 14.2),
    ("Brown 2020", -0.67, -1.15, -0.19, 10.3),
    ("Williams 2019", -0.18, -0.58, 0.22, 9.8),
    ("Johnson 2019", -0.52, -0.95, -0.09, 12.5),
    ("Smith 2018", -0.35, -0.72, 0.02, 8.2),
]

# Pooled estimate (diamond in traditional forest plots)
pooled_effect = -0.43
pooled_ci_lower = -0.58
pooled_ci_upper = -0.28

# Custom style for large canvas (4800 x 2700)
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#306998", "#FFD43B", "#FFD43B", "#666666"),
    title_font_size=56,
    label_font_size=32,
    major_label_font_size=28,
    legend_font_size=28,
    value_font_size=24,
    tooltip_font_size=28,
    stroke_width=4,
    font_family="Arial",
)

# Create XY chart for forest plot
chart = pygal.XY(
    width=4800,
    height=2700,
    title="forest-basic · pygal · pyplots.ai",
    x_title="Mean Difference (95% CI)",
    style=custom_style,
    show_legend=True,
    legend_at_bottom=True,
    legend_box_size=20,
    dots_size=18,
    stroke=False,
    show_y_guides=False,
    show_x_guides=True,
    x_label_rotation=0,
    range=(-1.3, 0.4),
    margin=100,
    truncate_legend=-1,
)

# Build data for each study
study_points = []
ci_lines = []
for i, (_study, effect, ci_low, ci_high, _weight) in enumerate(studies):
    y_pos = len(studies) - i  # Position from top (10 down to 1)
    study_points.append((effect, y_pos))
    # CI line segment with None break
    ci_lines.append((ci_low, y_pos))
    ci_lines.append((ci_high, y_pos))
    ci_lines.append((None, None))

# Add study effect points (Python Blue)
chart.add("Effect Size", study_points)

# Add CI lines (horizontal whiskers for each study)
chart.add("95% CI", ci_lines, stroke=True, show_dots=False, stroke_style={"width": 4})

# Add pooled estimate with its CI (Python Yellow for prominence)
chart.add("Pooled", [(pooled_effect, 0)], dots_size=28)
chart.add(
    "Pooled CI", [(pooled_ci_lower, 0), (pooled_ci_upper, 0)], stroke=True, show_dots=False, stroke_style={"width": 6}
)

# Add vertical reference line at x=0 (null effect)
chart.add(
    "Null (x=0)",
    [(0, -0.5), (0, len(studies) + 0.5)],
    stroke=True,
    show_dots=False,
    stroke_style={"width": 3, "dasharray": "12, 6"},
)

# Y-axis labels with study names and CIs
y_labels = []
for i, (study, _effect, ci_low, ci_high, _weight) in enumerate(studies):
    y_labels.append({"value": len(studies) - i, "label": f"{study} [{ci_low:.2f}, {ci_high:.2f}]"})
y_labels.append({"value": 0, "label": f"Pooled [{pooled_ci_lower:.2f}, {pooled_ci_upper:.2f}]"})

chart.y_labels = y_labels

# Save outputs
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
