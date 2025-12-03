"""
pie-basic: Basic Pie Chart
Library: pygal
"""

import pandas as pd
import pygal
from pygal.style import Style


# PyPlots.ai color palette
PYPLOTS_COLORS = (
    "#306998",  # Python Blue (Primary)
    "#FFD43B",  # Python Yellow
    "#DC2626",  # Signal Red
    "#059669",  # Teal Green
    "#8B5CF6",  # Violet
    "#F97316",  # Orange
)


def create_plot(
    data: pd.DataFrame,
    category: str,
    value: str,
    figsize: tuple[int, int] = (1600, 900),
    title: str | None = None,
    colors: list[str] | None = None,
    startangle: float = 90,
    legend: bool = True,
    legend_loc: str = "right",
    inner_radius: float = 0,
    **kwargs,
) -> pygal.Pie:
    """
    Create a basic pie chart for visualizing proportions of categorical data.

    Args:
        data: Input DataFrame containing the data to plot.
        category: Column name for category labels.
        value: Column name for numeric values representing each slice's proportion.
        figsize: Figure size as (width, height) in pixels.
        title: Optional plot title.
        colors: Custom color palette for slices (defaults to PyPlots palette).
        startangle: Starting angle for first slice in degrees (not used in pygal).
        legend: Whether to display legend.
        legend_loc: Legend location ('right', 'bottom', or 'top').
        inner_radius: Inner radius for donut chart (0-1, 0 for solid pie).
        **kwargs: Additional parameters passed to pygal.Pie.

    Returns:
        pygal.Pie chart object.

    Raises:
        ValueError: If data is empty or contains negative values.
        KeyError: If required columns are not found in data.

    Example:
        >>> data = pd.DataFrame({
        ...     'category': ['Product A', 'Product B', 'Product C'],
        ...     'value': [35, 25, 40]
        ... })
        >>> chart = create_plot(data, 'category', 'value', title='Market Share')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    for col in [category, value]:
        if col not in data.columns:
            available = ", ".join(data.columns)
            raise KeyError(f"Column '{col}' not found. Available: {available}")

    # Handle missing values
    clean_data = data[[category, value]].dropna()

    if clean_data.empty:
        raise ValueError("Data cannot be empty after removing missing values")

    # Validate non-negative values
    if (clean_data[value] < 0).any():
        raise ValueError("Pie chart values must be non-negative")

    # Check if all values sum to zero
    total = clean_data[value].sum()
    if total == 0:
        raise ValueError("Values sum to zero; cannot create pie chart")

    # Use provided colors or default PyPlots palette
    chart_colors = tuple(colors) if colors else PYPLOTS_COLORS

    # Create custom style
    custom_style = Style(
        background="white",
        plot_background="white",
        foreground="#333333",
        foreground_strong="#333333",
        foreground_subtle="#666666",
        colors=chart_colors,
        font_family="Inter, DejaVu Sans, Arial, Helvetica, sans-serif",
        title_font_size=20,
        legend_font_size=16,
        value_font_size=14,
        tooltip_font_size=14,
    )

    # Determine legend position
    legend_at_bottom = legend_loc == "bottom"
    legend_box_size = 16 if legend else 0

    # Create chart
    chart = pygal.Pie(
        width=figsize[0],
        height=figsize[1],
        title=title,
        style=custom_style,
        show_legend=legend,
        legend_at_bottom=legend_at_bottom,
        legend_box_size=legend_box_size,
        inner_radius=inner_radius,
        print_values=True,
        value_formatter=lambda x: f"{x:.1f}%",
        **kwargs,
    )

    # Add each category as a separate slice with percentage value
    for _, row in clean_data.iterrows():
        cat_name = str(row[category])
        cat_value = float(row[value])
        percentage = (cat_value / total) * 100
        chart.add(cat_name, [{"value": percentage, "label": cat_name}])

    return chart


if __name__ == "__main__":
    # Sample data for testing
    sample_data = pd.DataFrame(
        {"category": ["Product A", "Product B", "Product C", "Product D", "Other"], "value": [35, 25, 20, 15, 5]}
    )

    # Create plot
    chart = create_plot(sample_data, "category", "value", title="Market Share Distribution")

    # Save to PNG
    chart.render_to_png("plot.png")
    print("Plot saved to plot.png")
