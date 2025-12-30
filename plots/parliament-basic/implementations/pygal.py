""" pyplots.ai
parliament-basic: Parliament Seat Chart
Library: pygal 3.1.0 | Python 3.13.11
Quality: 72/100 | Created: 2025-12-30
"""

import pygal
from pygal.style import Style


# Data - Parliament composition by party (fictional neutral parties)
parties = ["Progressive Alliance", "Centrist Union", "Reform Party", "Green Coalition", "Independent"]
seats = [145, 98, 72, 35, 15]
total_seats = sum(seats)
majority_threshold = total_seats // 2 + 1  # 183 seats needed for majority

# Custom colors (colorblind-safe, politically neutral)
party_colors = ("#306998", "#FFD43B", "#4ECDC4", "#45B7D1", "#96CEB4")

# Custom style for 4800x2700 px canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#1a1a1a",
    foreground_subtle="#666666",
    colors=party_colors,
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=48,
    legend_font_size=42,
    value_font_size=48,
    tooltip_font_size=36,
)

# Create half-pie chart for parliament visualization
# Half-pie creates a semicircular chart representing the parliament chamber
chart = pygal.Pie(
    width=4800,
    height=2700,
    style=custom_style,
    title=f"Parliament Composition ({total_seats} seats, {majority_threshold} for majority) · parliament-basic · pygal · pyplots.ai",
    inner_radius=0.35,
    half_pie=True,
    show_legend=True,
    legend_at_bottom=True,
    legend_box_size=36,
    print_values=True,
    print_values_position="call",
    value_formatter=lambda x: f"{x} seats",
)

# Add each party as a pie segment
# Parties arranged from left to right in semicircle
for party, seat_count in zip(parties, seats, strict=True):
    chart.add(f"{party} ({seat_count})", seat_count)

# Save outputs
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
