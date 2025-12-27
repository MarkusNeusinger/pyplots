"""pyplots.ai
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
    colors=(
        "#306998",  # Study markers (Python Blue)
        "#306998",  # CI lines
        "#4A4A4A",  # Null line
        "#CC6600",  # Pooled diamond (distinct orange)
        "#CC6600",  # Pooled CI
    ),
    title_font_size=56,
    label_font_size=32,
    major_label_font_size=28,
    legend_font_size=28,
    value_font_size=24,
    tooltip_font_size=28,
    stroke_width=4,
    font_family="Arial",
)

# Normalize weights to dot sizes (range 12-28 for visibility)
min_weight = min(w for _, _, _, _, w in studies)
max_weight = max(w for _, _, _, _, w in studies)
weight_range = max_weight - min_weight if max_weight > min_weight else 1


def get_dot_size(weight):
    """Scale weight to marker size between 12 and 28."""
    normalized = (weight - min_weight) / weight_range
    return int(12 + normalized * 16)


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
    dots_size=16,
    stroke=False,
    show_y_guides=False,
    show_x_guides=True,
    x_label_rotation=0,
    range=(-1.3, 0.4),
    margin=100,
    truncate_legend=-1,
)

# Add each study as separate series for weight-based sizing
for i, (study, effect, _ci_low, _ci_high, weight) in enumerate(studies):
    y_pos = len(studies) - i  # Position from top (10 down to 1)
    dot_size = get_dot_size(weight)

    # Add study point with weight-proportional size
    chart.add(study, [(effect, y_pos)], dots_size=dot_size, stroke=False, show_legend=False)

# Add CI whiskers as individual line segments (one series per study)
for i, (_study, _effect, ci_low, ci_high, _weight) in enumerate(studies):
    y_pos = len(studies) - i
    chart.add(
        None,  # No legend entry
        [(ci_low, y_pos), (ci_high, y_pos)],
        stroke=True,
        show_dots=False,
        stroke_style={"width": 4},
        show_legend=False,
    )

# Add vertical reference line at x=0 (null effect)
chart.add(
    "Null (x=0)",
    [(0, -0.5), (0, len(studies) + 0.5)],
    stroke=True,
    show_dots=False,
    stroke_style={"width": 3, "dasharray": "12, 6"},
)

# Add pooled estimate as a diamond shape using 4 points
# Diamond vertices: top, right, bottom, left
diamond_height = 0.4
diamond_width = 0.06
chart.add(
    "Pooled Estimate",
    [
        (pooled_effect, 0 + diamond_height / 2),  # Top
        (pooled_effect + diamond_width, 0),  # Right
        (pooled_effect, 0 - diamond_height / 2),  # Bottom
        (pooled_effect - diamond_width, 0),  # Left
        (pooled_effect, 0 + diamond_height / 2),  # Close diamond
    ],
    stroke=True,
    fill=True,
    show_dots=False,
    stroke_style={"width": 3},
)

# Add pooled CI whiskers
chart.add(
    "Pooled 95% CI",
    [(pooled_ci_lower, 0), (pooled_ci_upper, 0)],
    stroke=True,
    show_dots=False,
    stroke_style={"width": 5},
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
