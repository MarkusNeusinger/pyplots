"""
pie-basic: Basic Pie Chart
Library: bokeh
"""

import math
from typing import TYPE_CHECKING

import pandas as pd
from bokeh.models import ColumnDataSource, Label, Legend, LegendItem
from bokeh.plotting import figure


if TYPE_CHECKING:
    from bokeh.plotting import figure as Figure

# PyPlots.ai style colors
PYPLOTS_COLORS = [
    "#306998",  # Python Blue
    "#FFD43B",  # Python Yellow
    "#DC2626",  # Signal Red
    "#059669",  # Teal Green
    "#8B5CF6",  # Violet
    "#F97316",  # Orange
]


def create_plot(
    data: pd.DataFrame,
    category: str,
    value: str,
    title: str | None = None,
    colors: list[str] | None = None,
    startangle: float = 90,
    legend: bool = True,
    legend_loc: str = "right",
    **kwargs,
) -> "Figure":
    """
    Create a basic pie chart using Bokeh wedge glyphs.

    Bokeh does not have a native pie chart method, so this implementation
    uses wedge glyphs to construct the pie chart manually.

    Args:
        data: Input DataFrame containing category and value columns
        category: Column name for category labels (slice names)
        value: Column name for numeric values (slice sizes)
        title: Plot title (optional)
        colors: Custom color palette for slices (defaults to PyPlots colors)
        startangle: Starting angle for first slice in degrees (default: 90)
        legend: Whether to display legend (default: True)
        legend_loc: Legend location - 'right', 'left', 'above', 'below' (default: 'right')
        **kwargs: Additional parameters passed to figure

    Returns:
        Bokeh figure object

    Raises:
        ValueError: If data is empty or values are all zero/negative
        KeyError: If required columns not found in data

    Example:
        >>> data = pd.DataFrame({
        ...     'category': ['A', 'B', 'C'],
        ...     'value': [30, 50, 20]
        ... })
        >>> fig = create_plot(data, 'category', 'value', title='Distribution')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    for col in [category, value]:
        if col not in data.columns:
            available = ", ".join(data.columns)
            raise KeyError(f"Column '{col}' not found. Available: {available}")

    # Validate numeric values
    if not pd.api.types.is_numeric_dtype(data[value]):
        raise ValueError(f"Column '{value}' must contain numeric values")

    if (data[value] < 0).any():
        raise ValueError("Pie chart values must be non-negative")

    total = data[value].sum()
    if total == 0:
        raise ValueError("Sum of values cannot be zero")

    # Prepare data
    plot_data = data.copy()
    plot_data["angle"] = plot_data[value] / total * 2 * math.pi
    plot_data["percentage"] = plot_data[value] / total * 100

    # Calculate cumulative angles for wedge positioning
    plot_data["end_angle"] = plot_data["angle"].cumsum()
    plot_data["start_angle"] = plot_data["end_angle"] - plot_data["angle"]

    # Apply start angle offset (convert degrees to radians, adjust for Bokeh's coordinate system)
    start_rad = math.radians(startangle - 90)
    plot_data["start_angle"] = plot_data["start_angle"] + start_rad
    plot_data["end_angle"] = plot_data["end_angle"] + start_rad

    # Assign colors
    if colors is None:
        colors = PYPLOTS_COLORS
    # Cycle through colors if more categories than colors
    num_categories = len(plot_data)
    plot_data["color"] = [colors[i % len(colors)] for i in range(num_categories)]

    # Create ColumnDataSource
    source = ColumnDataSource(plot_data)

    # Create figure - use range to ensure circular aspect ratio
    # Set frame dimensions to maintain 16:9 overall but circular pie
    fig_width = kwargs.get("width", 1600)
    fig_height = kwargs.get("height", 900)

    p = figure(
        width=fig_width,
        height=fig_height,
        title=title,
        tools="hover",
        tooltips=[(category.capitalize(), f"@{category}"), ("Value", f"@{value}"), ("Percentage", "@percentage{0.1}%")],
        x_range=(-1.2, 2.0 if legend else 1.2),
        y_range=(-1.2, 1.2),
    )

    # Draw wedges (pie slices)
    renderers = p.wedge(
        x=0,
        y=0,
        radius=0.9,
        start_angle="start_angle",
        end_angle="end_angle",
        line_color="white",
        line_width=2,
        fill_color="color",
        source=source,
    )

    # Add percentage labels inside slices
    for _, row in plot_data.iterrows():
        # Calculate label position at middle of wedge, 60% from center
        mid_angle = (row["start_angle"] + row["end_angle"]) / 2
        label_radius = 0.55

        x = label_radius * math.cos(mid_angle)
        y = label_radius * math.sin(mid_angle)

        # Only show percentage label if slice is large enough
        if row["percentage"] >= 5:
            label = Label(
                x=x,
                y=y,
                text=f"{row['percentage']:.1f}%",
                text_font_size="14pt",
                text_align="center",
                text_baseline="middle",
                text_color="white" if row["percentage"] >= 10 else "black",
            )
            p.add_layout(label)

    # Configure legend
    if legend:
        legend_items = []
        for i, cat in enumerate(plot_data[category]):
            legend_items.append(LegendItem(label=str(cat), renderers=[renderers], index=i))

        leg = Legend(
            items=legend_items,
            location="center",
            label_text_font_size="16pt",
            background_fill_color="white",
            background_fill_alpha=1.0,
            border_line_color="black",
            border_line_width=1,
        )

        p.add_layout(leg, legend_loc)

    # Style configuration
    p.axis.visible = False
    p.grid.visible = False
    p.outline_line_color = None

    # Title styling
    if title:
        p.title.text_font_size = "20pt"
        p.title.align = "center"

    # Background
    p.background_fill_color = "white"

    return p


if __name__ == "__main__":
    # Sample data for testing
    sample_data = pd.DataFrame(
        {"category": ["Product A", "Product B", "Product C", "Product D", "Other"], "value": [35, 25, 20, 15, 5]}
    )

    # Create plot
    fig = create_plot(sample_data, "category", "value", title="Market Share Distribution")

    # Save - try PNG first, fall back to HTML if selenium not available
    try:
        from bokeh.io import export_png

        export_png(fig, filename="plot.png")
        print("Plot saved to plot.png")
    except RuntimeError as e:
        if "selenium" in str(e).lower():
            from bokeh.io import output_file, save

            output_file("plot.html")
            save(fig)
            print("Plot saved to plot.html (selenium not available for PNG export)")
        else:
            raise
