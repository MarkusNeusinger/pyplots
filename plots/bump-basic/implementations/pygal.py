"""pyplots.ai
bump-basic: Basic Bump Chart
Library: pygal 3.1.0 | Python 3.13.11
Quality: 94/100 | Created: 2025-12-17
"""

import pygal
from pygal.style import Style


# Data - Sports league standings over a season
entities = ["Team Alpha", "Team Beta", "Team Gamma", "Team Delta", "Team Epsilon"]
periods = ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5", "Week 6"]

# Rankings for each team across periods (1 = best)
rankings = {
    "Team Alpha": [3, 2, 1, 1, 2, 1],
    "Team Beta": [1, 1, 2, 3, 3, 2],
    "Team Gamma": [2, 3, 3, 2, 1, 3],
    "Team Delta": [4, 4, 5, 4, 4, 4],
    "Team Epsilon": [5, 5, 4, 5, 5, 5],
}

# Custom style for pyplots (4800 × 2700 px target)
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333",
    foreground_strong="#333",
    foreground_subtle="#666",
    colors=("#306998", "#FFD43B", "#2ecc71", "#e74c3c", "#9b59b6"),
    title_font_size=64,
    label_font_size=42,
    major_label_font_size=38,
    legend_font_size=38,
    value_font_size=32,
    stroke_width=6,
    opacity=0.9,
)

# Create bump chart - invert rankings to show rank 1 at top
# Transform: rank -> (max_rank + 1 - rank) so rank 1 becomes 5, rank 5 becomes 1
max_rank = len(entities)
inverted_rankings = {entity: [max_rank + 1 - r for r in ranks] for entity, ranks in rankings.items()}

# Create chart using Line
chart = pygal.Line(
    width=4800,
    height=2700,
    style=custom_style,
    title="bump-basic · pygal · pyplots.ai",
    x_title="Period",
    y_title="Rank",
    show_dots=True,
    dots_size=12,
    show_x_guides=True,
    show_y_guides=True,
    x_label_rotation=0,
    legend_at_bottom=False,
    truncate_legend=-1,
    show_legend=True,
    interpolate=None,
    min_scale=1,
    max_scale=max_rank,
)

# Set x-axis labels
chart.x_labels = periods

# Custom y-axis labels (inverted: 5 displays as 1, 1 displays as 5)
chart.y_labels = [{"value": max_rank + 1 - i, "label": str(i)} for i in range(1, max_rank + 1)]

# Add each team's inverted ranking as a series
for entity in entities:
    chart.add(entity, inverted_rankings[entity])

# Save as PNG
chart.render_to_png("plot.png")

# Save interactive HTML version
chart.render_to_file("plot.html")
