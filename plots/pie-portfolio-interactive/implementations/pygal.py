"""pyplots.ai
pie-portfolio-interactive: Interactive Portfolio Allocation Chart
Library: pygal | Python 3.13
Quality: pending | Created: 2025-01-20
"""

import pygal
from pygal.style import Style


# Data - Investment portfolio allocation by asset class
categories = {
    "Equities": {"US Large Cap": 25.0, "US Mid Cap": 10.0, "International Developed": 12.0, "Emerging Markets": 8.0},
    "Fixed Income": {"US Treasury": 15.0, "Corporate Bonds": 8.0, "Municipal Bonds": 5.0},
    "Alternatives": {"Real Estate": 7.0, "Commodities": 5.0, "Private Equity": 5.0},
}

# Create category-level data for pie chart
category_totals = []
category_names = []
for category, holdings in categories.items():
    total = sum(holdings.values())
    category_totals.append(total)
    category_names.append(category)

# Custom style for large canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=(
        "#306998",
        "#FFD43B",
        "#E07C3E",
        "#4DAF4A",
        "#984EA3",
        "#FF7F00",
        "#A65628",
        "#F781BF",
        "#377EB8",
        "#66C2A5",
    ),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=42,
    value_font_size=36,
    tooltip_font_size=36,
)

# Create interactive pie chart
chart = pygal.Pie(
    width=4800,
    height=2700,
    style=custom_style,
    inner_radius=0.4,  # Donut style
    show_legend=True,
    legend_at_bottom=True,
    legend_box_size=36,
    title="pie-portfolio-interactive · pygal · pyplots.ai",
)

# Add category-level slices with detailed tooltips showing holdings
for category, holdings in categories.items():
    total = sum(holdings.values())
    # Build tooltip with breakdown
    holdings_breakdown = ", ".join([f"{name}: {pct:.1f}%" for name, pct in holdings.items()])
    tooltip = f"{category} ({total:.1f}%)\n{holdings_breakdown}"
    chart.add(f"{category} ({total:.0f}%)", [{"value": total, "label": tooltip}])

# Render to PNG and HTML for interactivity
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
