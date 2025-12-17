"""
heatmap-calendar: Basic Calendar Heatmap
Library: pygal
"""

import sys
from datetime import datetime, timedelta

import numpy as np


# Temporarily remove current directory from path to avoid name collision
_cwd = sys.path[0] if sys.path[0] else "."
if _cwd in sys.path:
    sys.path.remove(_cwd)

from pygal.graph.graph import Graph  # noqa: E402
from pygal.style import Style  # noqa: E402


# Restore path
sys.path.insert(0, _cwd)


class CalendarHeatmap(Graph):
    """Custom Calendar Heatmap for pygal - displays daily values in a calendar grid."""

    def __init__(self, *args, **kwargs):
        self.dates = kwargs.pop("dates", [])
        self.values = kwargs.pop("values", [])
        self.weekday_labels = kwargs.pop("weekday_labels", ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
        self.cell_colors = kwargs.pop("cell_colors", ["#ebedf0", "#9be9a8", "#40c463", "#30a14e", "#216e39"])
        super().__init__(*args, **kwargs)

    def _get_color(self, value, min_val, max_val):
        """Get color based on value intensity."""
        if value is None or value == 0:
            return self.cell_colors[0]
        if max_val == min_val:
            return self.cell_colors[-1]
        # Normalize value to 0-1 range
        normalized = (value - min_val) / (max_val - min_val)
        # Map to color index (1-4, skip 0 which is for empty)
        idx = min(int(normalized * 4) + 1, len(self.cell_colors) - 1)
        return self.cell_colors[idx]

    def _plot(self):
        """Draw the calendar heatmap."""
        if not self.dates or not self.values:
            return

        # Create date-value mapping
        date_values = dict(zip(self.dates, self.values, strict=True))

        # Find date range
        min_date = min(self.dates)
        max_date = max(self.dates)

        # Calculate value range (excluding zeros)
        non_zero_values = [v for v in self.values if v and v > 0]
        min_val = min(non_zero_values) if non_zero_values else 0
        max_val = max(non_zero_values) if non_zero_values else 1

        # Get plot dimensions
        plot_width = self.view.width
        plot_height = self.view.height

        # Calculate weeks and dimensions
        # Adjust start to first day of the week containing min_date
        days_from_monday = min_date.weekday()
        start_date = min_date - timedelta(days=days_from_monday)

        # Calculate total weeks
        total_days = (max_date - start_date).days + 1
        total_weeks = (total_days + 6) // 7 + 1

        # Calculate cell size - leave space for labels
        label_margin_left = 280
        label_margin_top = 120
        available_width = plot_width - label_margin_left - 100
        available_height = plot_height - label_margin_top - 200

        cell_size = min(available_width / total_weeks, available_height / 7) * 0.88
        gap = cell_size * 0.12

        # Center the grid
        grid_width = total_weeks * (cell_size + gap)
        grid_height = 7 * (cell_size + gap)

        x_offset = self.view.x(0) + label_margin_left + (available_width - grid_width) / 2
        y_offset = self.view.y(7) + label_margin_top + (available_height - grid_height) / 2

        # Create group for the calendar
        plot_node = self.nodes["plot"]
        cal_group = self.svg.node(plot_node, class_="calendar-heatmap")

        # Draw weekday labels on the left - ensure large readable size
        weekday_font_size = max(cell_size * 1.0, 48)
        for i, label in enumerate(self.weekday_labels):
            y = y_offset + i * (cell_size + gap) + cell_size / 2
            self.svg.node(
                cal_group,
                "text",
                x=x_offset - 50,
                y=y + weekday_font_size * 0.35,
                text_anchor="end",
                fill="#333333",
                font_size=weekday_font_size,
                font_weight="bold",
            ).text = label

        # Track months for labels
        month_positions = {}

        # Draw cells
        current_date = start_date
        week = 0
        while current_date <= max_date:
            weekday = current_date.weekday()

            # Track month positions
            if current_date.day <= 7 and current_date >= min_date:
                month_key = (current_date.year, current_date.month)
                if month_key not in month_positions:
                    month_positions[month_key] = week

            # Get value and color
            value = date_values.get(current_date, 0)
            color = self._get_color(value, min_val, max_val)

            # Calculate position
            x = x_offset + week * (cell_size + gap)
            y = y_offset + weekday * (cell_size + gap)

            # Draw cell
            if current_date >= min_date:
                self.svg.node(
                    cal_group,
                    "rect",
                    x=x,
                    y=y,
                    width=cell_size,
                    height=cell_size,
                    fill=color,
                    rx=cell_size * 0.1,
                    ry=cell_size * 0.1,
                    class_="calendar-cell reactive",
                )

            # Move to next day
            if weekday == 6:
                week += 1
            current_date += timedelta(days=1)

        # Draw month labels at the top
        month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        for (_year, month), week_pos in month_positions.items():
            x = x_offset + week_pos * (cell_size + gap)
            y = y_offset - 30
            self.svg.node(cal_group, "text", x=x, y=y, fill="#666666", font_size=cell_size * 0.65).text = month_names[
                month - 1
            ]

        # Draw color scale legend at bottom
        legend_y = y_offset + 7 * (cell_size + gap) + 60
        legend_cell_size = cell_size * 0.9
        legend_x = x_offset + grid_width / 2 - (len(self.cell_colors) * (legend_cell_size + 8)) / 2
        legend_label_size = cell_size * 0.55

        self.svg.node(
            cal_group,
            "text",
            x=legend_x - 20,
            y=legend_y + legend_cell_size * 0.7,
            text_anchor="end",
            fill="#666",
            font_size=legend_label_size,
        ).text = "Less"

        for i, color in enumerate(self.cell_colors):
            self.svg.node(
                cal_group,
                "rect",
                x=legend_x + i * (legend_cell_size + 8),
                y=legend_y,
                width=legend_cell_size,
                height=legend_cell_size,
                fill=color,
                rx=legend_cell_size * 0.1,
                ry=legend_cell_size * 0.1,
            )

        self.svg.node(
            cal_group,
            "text",
            x=legend_x + len(self.cell_colors) * (legend_cell_size + 8) + 15,
            y=legend_y + legend_cell_size * 0.7,
            fill="#666",
            font_size=legend_label_size,
        ).text = "More"

    def _compute(self):
        """Compute the box for rendering."""
        self._box.xmin = 0
        self._box.xmax = 53  # Max weeks in a year
        self._box.ymin = 0
        self._box.ymax = 7  # Days in a week


# Generate data - GitHub-style contribution data for a year
np.random.seed(42)
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)

dates = []
values = []
current = start_date

while current <= end_date:
    dates.append(current)

    # Simulate contribution pattern: weekdays more active, weekends less
    # Also add some randomness and occasional spikes
    weekday = current.weekday()
    base = 0 if weekday >= 5 else np.random.choice([0, 0, 1, 2, 3], p=[0.3, 0.2, 0.25, 0.15, 0.1])

    # Random spike days
    if np.random.random() < 0.05:
        base = np.random.randint(5, 15)

    # Some days have no activity
    if np.random.random() < 0.25:
        base = 0

    values.append(base)
    current += timedelta(days=1)

# Custom style for 4800x2700 canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998",),
    title_font_size=72,
    legend_font_size=48,
    label_font_size=42,
    value_font_size=36,
    font_family="sans-serif",
)

# GitHub-style green colors
github_colors = ["#ebedf0", "#9be9a8", "#40c463", "#30a14e", "#216e39"]

# Create calendar heatmap
chart = CalendarHeatmap(
    width=4800,
    height=2700,
    style=custom_style,
    title="heatmap-calendar · pygal · pyplots.ai",
    dates=dates,
    values=values,
    cell_colors=github_colors,
    show_legend=False,
    margin=100,
    margin_top=200,
    margin_bottom=250,
    show_x_labels=False,
    show_y_labels=False,
)

# Add a dummy series to trigger _plot (pygal requires at least one series)
chart.add("", [0])

# Save output
chart.render_to_png("plot.png")
