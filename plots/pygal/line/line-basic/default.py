"""
line-basic: Basic Line Chart
Library: pygal
"""

from typing import TYPE_CHECKING

import pandas as pd
import pygal
from pygal.style import Style


if TYPE_CHECKING:
    pass


def create_plot(
    data: pd.DataFrame,
    x: str,
    y: str,
    color: str = "#306998",
    linewidth: float = 2,
    marker: bool = False,
    marker_size: float = 4,
    alpha: float = 1.0,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    linestyle: str = "solid",
    **kwargs,
) -> pygal.Line:
    """
    Create a basic line chart using pygal.

    Args:
        data: Input DataFrame
        x: Column name for x-axis values
        y: Column name for y-axis values
        color: Line color (default: "#306998" Python Blue)
        linewidth: Width of the line (default: 2)
        marker: Whether to show markers at data points (default: False)
        marker_size: Size of markers if enabled (default: 4)
        alpha: Transparency level for the line (default: 1.0)
        title: Plot title (default: None)
        xlabel: X-axis label (default: uses column name)
        ylabel: Y-axis label (default: uses column name)
        linestyle: Line style - solid, dashed, dotted (default: "solid")
        **kwargs: Additional parameters passed to pygal.Line

    Returns:
        pygal.Line chart object

    Raises:
        ValueError: If data is empty
        KeyError: If required columns not found

    Example:
        >>> data = pd.DataFrame({'month': [1, 2, 3], 'sales': [100, 150, 130]})
        >>> chart = create_plot(data, 'month', 'sales')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    for col in [x, y]:
        if col not in data.columns:
            available = ", ".join(data.columns)
            raise KeyError(f"Column '{col}' not found. Available: {available}")

    # Sort data by x-axis values
    plot_data = data.copy().sort_values(by=x)

    # Handle NaN values
    plot_data = plot_data.dropna(subset=[x, y])

    # Use column names as default labels
    x_label = xlabel if xlabel is not None else x
    y_label = ylabel if ylabel is not None else y

    # Define custom style with PyPlots color palette
    custom_style = Style(
        background="white",
        plot_background="white",
        foreground="#333333",
        foreground_strong="#333333",
        foreground_subtle="#666666",
        colors=(color,),
        opacity=alpha,
        opacity_hover=min(alpha + 0.1, 1.0),
        title_font_size=56,
        label_font_size=44,
        major_label_font_size=44,
        legend_font_size=44,
        tooltip_font_size=40,
    )

    # Map linestyle to pygal stroke style
    stroke_style = {"solid": None, "dashed": "5,5", "dotted": "2,2"}
    dash_style = stroke_style.get(linestyle, None)

    # Build stroke style dict
    stroke_opts: dict = {"width": linewidth}
    if dash_style:
        stroke_opts["dasharray"] = dash_style

    # Create chart with target dimensions 4800 x 2700 px
    chart = pygal.Line(
        width=4800,
        height=2700,
        title=title,
        x_title=x_label,
        y_title=y_label,
        style=custom_style,
        show_x_guides=False,
        show_y_guides=True,
        show_dots=marker,
        dots_size=marker_size,
        stroke_style=stroke_opts,
        show_legend=False,
        margin=50,
        **kwargs,
    )

    # Set x-axis labels
    chart.x_labels = [str(val) for val in plot_data[x].tolist()]

    # Add data series
    chart.add(y_label, plot_data[y].tolist())

    return chart


if __name__ == "__main__":
    # Sample data for testing
    sample_data = pd.DataFrame(
        {
            "month": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            "sales": [100, 150, 130, 180, 200, 190, 220, 240, 210, 250, 280, 300],
        }
    )

    # Create plot
    chart = create_plot(
        sample_data, "month", "sales", title="Monthly Sales Trend", xlabel="Month", ylabel="Sales ($)", marker=True
    )

    # Save
    chart.render_to_png("plot.png")
    print("Plot saved to plot.png")
