"""
line-basic: Basic Line Chart
Library: altair
"""

from typing import TYPE_CHECKING

import altair as alt
import pandas as pd


if TYPE_CHECKING:
    from altair import Chart

# Style guide colors
PYTHON_BLUE = "#306998"


def create_plot(
    data: pd.DataFrame,
    x: str,
    y: str,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    color: str = PYTHON_BLUE,
    linewidth: float = 2,
    marker: str | None = None,
    marker_size: int = 60,
    alpha: float = 1.0,
    linestyle: str = "solid",
    **kwargs,
) -> "Chart":
    """
    Create a basic line chart showing trends over a continuous axis.

    Args:
        data: Input DataFrame with required columns
        x: Column name for x-axis values (typically time or sequence)
        y: Column name for y-axis values
        title: Plot title (default: None)
        xlabel: Custom x-axis label (default: uses column name)
        ylabel: Custom y-axis label (default: uses column name)
        color: Line color (default: Python Blue #306998)
        linewidth: Width of the line (default: 2)
        marker: Marker style - 'circle', 'square', 'diamond', etc. (default: None)
        marker_size: Size of markers if enabled (default: 60)
        alpha: Transparency level for the line (default: 1.0)
        linestyle: Line style - 'solid', 'dashed', 'dotted' (default: 'solid')
        **kwargs: Additional parameters for altair chart configuration

    Returns:
        Altair Chart object

    Raises:
        ValueError: If data is empty
        KeyError: If required columns not found

    Example:
        >>> data = pd.DataFrame({
        ...     'month': [1, 2, 3, 4, 5, 6],
        ...     'sales': [100, 150, 130, 180, 200, 190]
        ... })
        >>> chart = create_plot(data, x='month', y='sales')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    for col in [x, y]:
        if col not in data.columns:
            available = ", ".join(data.columns)
            raise KeyError(f"Column '{col}' not found. Available columns: {available}")

    # Sort data by x-axis to ensure proper line connections
    plot_data = data.sort_values(by=x).copy()

    # Determine x encoding type based on data
    x_dtype = plot_data[x].dtype
    if pd.api.types.is_datetime64_any_dtype(x_dtype):
        x_encoding = f"{x}:T"
    else:
        x_encoding = f"{x}:Q"

    # Map linestyle to altair strokeDash
    stroke_dash_map = {"solid": [], "dashed": [8, 4], "dotted": [2, 2]}
    stroke_dash = stroke_dash_map.get(linestyle, [])

    # Create the line chart
    line = (
        alt.Chart(plot_data)
        .mark_line(color=color, strokeWidth=linewidth, opacity=alpha, strokeDash=stroke_dash)
        .encode(
            x=alt.X(
                x_encoding,
                title=xlabel or x,
                axis=alt.Axis(labelAngle=0, labelLimit=200, labelFontSize=16, titleFontSize=20),
            ),
            y=alt.Y(
                f"{y}:Q",
                title=ylabel or y,
                scale=alt.Scale(zero=False),
                axis=alt.Axis(labelFontSize=16, titleFontSize=20),
            ),
            tooltip=[
                alt.Tooltip(x_encoding, title=xlabel or x),
                alt.Tooltip(f"{y}:Q", title=ylabel or y, format=".2f"),
            ],
        )
    )

    # Add markers if specified
    if marker:
        points = (
            alt.Chart(plot_data)
            .mark_point(color=color, size=marker_size, filled=True, shape=marker, opacity=alpha)
            .encode(
                x=alt.X(x_encoding),
                y=alt.Y(f"{y}:Q"),
                tooltip=[
                    alt.Tooltip(x_encoding, title=xlabel or x),
                    alt.Tooltip(f"{y}:Q", title=ylabel or y, format=".2f"),
                ],
            )
        )
        chart_base = line + points
    else:
        chart_base = line

    # Apply properties and configuration
    # Target: 4800 × 2700 px with scale_factor=3.0 -> 1600 × 900 base
    title_config = alt.TitleParams(text=title, fontSize=20, anchor="middle") if title else None
    chart = (
        chart_base.properties(width=1600, height=900, title=title_config)
        .configure_view(strokeWidth=0)
        .configure_axis(grid=True, gridOpacity=0.3, gridDash=[3, 3], domainWidth=1, tickWidth=1)
    )

    return chart


if __name__ == "__main__":
    # Sample data for testing - monthly sales trend
    sample_data = pd.DataFrame(
        {
            "Month": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            "Sales": [120, 150, 170, 165, 180, 220, 250, 240, 210, 190, 180, 200],
        }
    )

    # Create plot with markers
    chart = create_plot(
        sample_data,
        x="Month",
        y="Sales",
        title="Monthly Sales Trend (2024)",
        xlabel="Month",
        ylabel="Sales (thousands)",
        linewidth=2.5,
        marker="circle",
        marker_size=80,
    )

    # Save as PNG - scale_factor=3.0 gives 4800 × 2700 px
    chart.save("plot.png", scale_factor=3.0)
    print("Plot saved to plot.png")
