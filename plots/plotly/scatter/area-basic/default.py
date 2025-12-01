"""
area-basic: Basic Area Chart
Implementation for: plotly
Variant: default
Python: 3.10+
"""

from typing import TYPE_CHECKING, Optional

import pandas as pd
import plotly.graph_objects as go


if TYPE_CHECKING:
    pass


def create_plot(
    data: pd.DataFrame,
    x: str,
    y: str,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    color: str = "rgba(99, 110, 250, 0.5)",
    line_color: Optional[str] = None,
    line_width: float = 2.0,
    fill_to: str = "tozeroy",
    height: int = 900,
    width: int = 1600,
    **kwargs,
) -> go.Figure:
    """
    Create a basic area chart showing quantitative data over a continuous interval.

    The area between the line and the x-axis is filled with color, emphasizing
    the magnitude of values. Ideal for showing trends and cumulative totals.

    Args:
        data: Input DataFrame with required columns
        x: Column name for x-axis values (typically time or sequential data)
        y: Column name for y-axis values (numeric)
        title: Plot title (optional)
        xlabel: Custom x-axis label (optional, defaults to column name)
        ylabel: Custom y-axis label (optional, defaults to column name)
        color: Fill color for the area with alpha (default: semi-transparent blue)
        line_color: Color of the line at top of area (default: derived from fill color)
        line_width: Width of the line (default: 2.0)
        fill_to: Fill mode - 'tozeroy', 'tonexty', 'none' (default: 'tozeroy')
        height: Figure height in pixels (default: 900)
        width: Figure width in pixels (default: 1600)
        **kwargs: Additional parameters passed to plotly Scatter trace

    Returns:
        Plotly Figure object

    Raises:
        ValueError: If data is empty
        KeyError: If required columns not found

    Example:
        >>> data = pd.DataFrame({
        ...     'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
        ...     'Sales': [100, 150, 130, 180, 200]
        ... })
        >>> fig = create_plot(data, x='Month', y='Sales', title='Monthly Sales')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    # Check required columns
    for col in [x, y]:
        if col not in data.columns:
            available = ", ".join(data.columns)
            raise KeyError(f"Column '{col}' not found. Available columns: {available}")

    # Derive line color from fill color if not provided
    if line_color is None:
        # Use a solid version of the fill color (darker)
        line_color = "rgb(99, 110, 250)"

    # Create the figure
    fig = go.Figure()

    # Add the area trace
    fig.add_trace(
        go.Scatter(
            x=data[x],
            y=data[y],
            mode="lines",
            fill=fill_to,
            fillcolor=color,
            line={"color": line_color, "width": line_width},
            name=y,
            hovertemplate=f"<b>{x}</b>: %{{x}}<br><b>{y}</b>: %{{y:,.2f}}<extra></extra>",
            **kwargs,
        )
    )

    # Update layout for professional appearance
    fig.update_layout(
        title={
            "text": title or "Area Chart",
            "font": {"size": 18, "family": "Arial, sans-serif"},
            "x": 0.5,
            "xanchor": "center",
        },
        xaxis={
            "title": {"text": xlabel or x, "font": {"size": 14}},
            "showgrid": True,
            "gridcolor": "rgba(128, 128, 128, 0.3)",
            "gridwidth": 1,
            "zeroline": False,
            "showline": True,
            "linewidth": 1,
            "linecolor": "rgba(128, 128, 128, 0.5)",
        },
        yaxis={
            "title": {"text": ylabel or y, "font": {"size": 14}},
            "showgrid": True,
            "gridcolor": "rgba(128, 128, 128, 0.3)",
            "gridwidth": 1,
            "zeroline": True,
            "zerolinewidth": 1,
            "zerolinecolor": "rgba(128, 128, 128, 0.5)",
            "showline": True,
            "linewidth": 1,
            "linecolor": "rgba(128, 128, 128, 0.5)",
        },
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=height,
        width=width,
        showlegend=False,
        hovermode="x unified",
        hoverlabel={"bgcolor": "white", "font_size": 12, "font_family": "Arial, sans-serif"},
        margin={"l": 80, "r": 40, "t": 80, "b": 60},
    )

    return fig


if __name__ == "__main__":
    import numpy as np

    # Sample data: Monthly website traffic over a year
    np.random.seed(42)

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    # Generate realistic traffic pattern with seasonal variation
    base_traffic = 10000
    seasonal_factor = [0.8, 0.85, 0.95, 1.0, 1.1, 1.15, 1.2, 1.25, 1.1, 1.0, 0.9, 0.95]
    noise = np.random.normal(0, 500, 12)

    traffic = [int(base_traffic * sf + n) for sf, n in zip(seasonal_factor, noise, strict=False)]

    data = pd.DataFrame({"Month": months, "Visitors": traffic})

    # Create the area chart
    fig = create_plot(
        data,
        x="Month",
        y="Visitors",
        title="Monthly Website Visitors (2024)",
        xlabel="Month",
        ylabel="Number of Visitors",
        color="rgba(99, 110, 250, 0.4)",
        line_color="rgb(99, 110, 250)",
        line_width=2.5,
    )

    # Save as PNG
    fig.write_image("plot.png", width=1600, height=900, scale=2)
    print("Plot saved to plot.png")
