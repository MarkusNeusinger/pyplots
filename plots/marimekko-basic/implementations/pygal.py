"""
marimekko-basic: Basic Marimekko Chart
Library: pygal
"""

import sys


# Temporarily remove current directory from path to avoid name collision
_cwd = sys.path[0] if sys.path[0] else "."
if _cwd in sys.path:
    sys.path.remove(_cwd)

from pygal.graph.graph import Graph  # noqa: E402
from pygal.style import Style  # noqa: E402


# Restore path
sys.path.insert(0, _cwd)


class Marimekko(Graph):
    """Custom Marimekko chart for pygal - stacked bars with variable widths."""

    _serie_margin = 0

    def __init__(self, *args, **kwargs):
        self.gap = kwargs.pop("gap", 0.02)  # Gap between bars as fraction of width
        super().__init__(*args, **kwargs)

    def _compute_x_labels(self):
        """Override to skip standard x-label computation - we draw our own."""
        pass

    def _compute_y_labels(self):
        """Override to skip standard y-label computation."""
        pass

    def _plot(self):
        """Draw the marimekko chart."""
        if not self.series:
            return

        # Calculate column totals (determines bar widths)
        num_cols = len(self.series[0].values) if self.series else 0
        col_totals = [0] * num_cols

        for serie in self.series:
            for i, val in enumerate(serie.values):
                if val is not None:
                    col_totals[i] += val

        grand_total = sum(col_totals)
        if grand_total == 0:
            return

        # Get plot area dimensions
        plot_width = self.view.width
        plot_height = self.view.height

        # Calculate gap and usable width
        total_gap = self.gap * plot_width * (num_cols - 1)
        usable_width = plot_width - total_gap
        gap_px = self.gap * plot_width

        # Get coordinates
        x_start = self.view.x(0)
        y_bottom = self.view.y(0)  # Bottom of plot area

        # Create group for the marimekko chart
        plot_node = self.nodes["plot"]
        mekko_group = self.svg.node(plot_node, class_="marimekko-chart")

        # Draw bars column by column
        x_pos = x_start

        for col_idx in range(num_cols):
            col_total = col_totals[col_idx]
            if col_total == 0:
                continue

            # Bar width proportional to column total
            bar_width = (col_total / grand_total) * usable_width

            # Stack segments within this column
            y_offset = 0

            for serie_idx, serie in enumerate(self.series):
                val = serie.values[col_idx] if col_idx < len(serie.values) else None
                if val is None or val == 0:
                    continue

                # Segment height proportional to value within column
                segment_height = (val / col_total) * plot_height
                color = self.style.colors[serie_idx % len(self.style.colors)]

                # Draw rectangle (y increases downward in SVG)
                y_pos = y_bottom - y_offset - segment_height

                # Create series group if needed
                serie_group = self.svg.node(mekko_group, class_="series serie-%d color-%d" % (serie_idx, serie_idx))

                self.svg.node(
                    serie_group,
                    "rect",
                    x=x_pos,
                    y=y_pos,
                    width=bar_width,
                    height=segment_height,
                    fill=color,
                    stroke="white",
                    **{"stroke-width": "2", "class": "rect reactive tooltip-trigger"},
                )

                # Add value label if segment is large enough
                if segment_height > 80 and bar_width > 100:
                    pct = (val / col_total) * 100
                    label_y = y_pos + segment_height / 2
                    label_x = x_pos + bar_width / 2

                    self.svg.node(
                        serie_group,
                        "text",
                        x=label_x,
                        y=label_y,
                        fill="white",
                        **{
                            "text-anchor": "middle",
                            "dominant-baseline": "middle",
                            "font-size": "32",
                            "font-weight": "bold",
                        },
                    ).text = f"{pct:.0f}%"

                y_offset += segment_height

            x_pos += bar_width + gap_px

        # Draw x-axis labels (column labels)
        if hasattr(self, "x_labels") and self.x_labels:
            x_pos = x_start
            for col_idx in range(num_cols):
                col_total = col_totals[col_idx]
                if col_total == 0:
                    continue

                bar_width = (col_total / grand_total) * usable_width
                label_x = x_pos + bar_width / 2
                label_y = y_bottom + 60

                label_group = self.svg.node(mekko_group, class_="x-labels")

                # Category label
                self.svg.node(
                    label_group,
                    "text",
                    x=label_x,
                    y=label_y,
                    fill="#333",
                    **{"text-anchor": "middle", "font-size": "38", "font-weight": "normal"},
                ).text = str(self.x_labels[col_idx]) if col_idx < len(self.x_labels) else ""

                # Width percentage label
                width_pct = (col_total / grand_total) * 100
                self.svg.node(
                    label_group,
                    "text",
                    x=label_x,
                    y=label_y + 50,
                    fill="#666",
                    **{"text-anchor": "middle", "font-size": "32", "font-style": "italic"},
                ).text = f"({width_pct:.0f}%)"

                x_pos += bar_width + gap_px

    def _compute(self):
        """Compute the box for rendering."""
        self._box.xmin = 0
        self._box.xmax = 1
        self._box.ymin = 0
        self._box.ymax = 1


# Custom style for 4800x2700 canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#4ECDC4", "#FF6B6B", "#9B59B6"),
    title_font_size=72,
    legend_font_size=48,
    label_font_size=38,
    value_font_size=36,
    font_family="sans-serif",
)

# Data - Market share by region and product line
# Regions (x-categories) with different market sizes
regions = ["North America", "Europe", "Asia Pacific", "Latin America", "MEA"]
# Total market size per region (determines bar width)
market_sizes = [450, 380, 520, 180, 120]

# Product lines (y-categories) and their share within each region
# Each list represents [NA, EU, APAC, LATAM, MEA] values
products = {
    "Enterprise": [180, 140, 200, 60, 40],
    "Consumer": [120, 130, 180, 70, 45],
    "SMB": [90, 70, 90, 35, 25],
    "Government": [60, 40, 50, 15, 10],
}

# Create marimekko chart
chart = Marimekko(
    width=4800,
    height=2700,
    gap=0.015,
    style=custom_style,
    title="Market Share by Region · marimekko-basic · pygal · pyplots.ai",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=4,
    margin=80,
    margin_bottom=300,
    show_x_labels=False,
    show_y_labels=False,
)

chart.x_labels = regions

# Add data series for each product line
for product_name, values in products.items():
    chart.add(product_name, values)

# Save outputs
chart.render_to_file("plot.svg")
chart.render_to_png("plot.png")

# Also save HTML for interactive viewing
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>marimekko-basic · pygal · pyplots.ai</title>
    <style>
        body {{ margin: 0; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 100%; margin: 0 auto; }}
        svg {{ max-width: 100%; height: auto; }}
    </style>
</head>
<body>
    <div class="container">
        {chart.render(is_unicode=True)}
    </div>
</body>
</html>"""

with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)
