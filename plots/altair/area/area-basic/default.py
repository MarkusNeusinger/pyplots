"""
area-basic: Basic Area Chart
Implementation for: altair
Variant: default
Python: 3.10+
"""

from typing import TYPE_CHECKING, Optional

import altair as alt
import pandas as pd


if TYPE_CHECKING:
    from altair import LayerChart


def create_plot(
    data: pd.DataFrame,
    x: str,
    y: str,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    color: str = "steelblue",
    alpha: float = 0.7,
    line_color: Optional[str] = None,
    line_width: float = 2,
    show_line: bool = True,
    width: int = 800,
    height: int = 450,
    **kwargs,
) -> "LayerChart":
    """
    Create a basic filled area chart showing a single data series using altair.

    Args:
        data: Input DataFrame with required columns
        x: Column name for x-axis values (numeric or datetime)
        y: Column name for y-axis values (numeric)
        title: Plot title (optional)
        xlabel: Custom x-axis label (optional, defaults to x column name)
        ylabel: Custom y-axis label (optional, defaults to y column name)
        color: Fill color for the area (default: 'steelblue')
        alpha: Transparency level for the fill (default: 0.7)
        line_color: Color of the line at the top (default: same as fill color)
        line_width: Width of the top line (default: 2)
        show_line: Whether to show the line at the top (default: True)
        width: Figure width in pixels (default: 800)
        height: Figure height in pixels (default: 450)
        **kwargs: Additional parameters for altair chart configuration

    Returns:
        Altair LayerChart object

    Raises:
        ValueError: If data is empty
        KeyError: If required columns not found

    Example:
        >>> data = pd.DataFrame({
        ...     'month': [1, 2, 3, 4, 5, 6],
        ...     'sales': [100, 150, 200, 180, 220, 250]
        ... })
        >>> chart = create_plot(data, x='month', y='sales')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    # Check required columns
    for col in [x, y]:
        if col not in data.columns:
            available = ", ".join(data.columns)
            raise KeyError(f"Column '{col}' not found. Available columns: {available}")

    # Determine encoding type for x-axis
    x_dtype = data[x].dtype
    if pd.api.types.is_datetime64_any_dtype(x_dtype):
        x_encoding = f"{x}:T"
    elif pd.api.types.is_numeric_dtype(x_dtype):
        x_encoding = f"{x}:Q"
    else:
        x_encoding = f"{x}:O"

    # Use provided line_color or default to fill color
    actual_line_color = line_color if line_color is not None else color

    # Create the area chart
    area = (
        alt.Chart(data)
        .mark_area(
            color=color,
            opacity=alpha,
            line={"color": actual_line_color, "strokeWidth": line_width} if show_line else False,
        )
        .encode(
            x=alt.X(
                x_encoding,
                title=xlabel or x,
                axis=alt.Axis(labelAngle=0 if len(data) <= 12 else -45, labelLimit=200),
            ),
            y=alt.Y(
                f"{y}:Q",
                title=ylabel or y,
                scale=alt.Scale(domain=[0, data[y].max() * 1.1]),
            ),
            tooltip=[
                alt.Tooltip(x_encoding, title=xlabel or x),
                alt.Tooltip(f"{y}:Q", title=ylabel or y, format=",.2f"),
            ],
        )
    )

    # Configure the chart with title and styling
    chart = area.properties(
        width=width,
        height=height,
        title=alt.TitleParams(
            text=title or "Area Chart",
            fontSize=16,
            anchor="middle",
        ),
    ).configure_view(
        strokeWidth=0,
    ).configure_axis(
        grid=True,
        gridOpacity=0.3,
        gridDash=[3, 3],
        domainWidth=1,
        tickWidth=1,
    )

    return chart


if __name__ == "__main__":
    # Sample data for testing - monthly sales data
    sample_data = pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        "Sales": [120, 150, 180, 165, 200, 230, 250, 245, 220, 195, 170, 210],
    })

    # Create plot with ordinal x-axis
    chart = create_plot(
        sample_data,
        x="Month",
        y="Sales",
        title="Monthly Sales Trend",
        xlabel="Month",
        ylabel="Sales ($K)",
        color="steelblue",
        alpha=0.7,
    )

    # Save as PNG
    chart.save("plot.png", scale_factor=2.0)
    print("Plot saved to plot.png")
