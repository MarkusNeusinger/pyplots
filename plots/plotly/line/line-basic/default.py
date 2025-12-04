"""
line-basic: Basic Line Chart
Library: plotly
"""

from typing import TYPE_CHECKING

import pandas as pd
import plotly.graph_objects as go


if TYPE_CHECKING:
    pass


def create_plot(
    data: pd.DataFrame,
    x: str,
    y: str,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    color: str = "steelblue",
    linewidth: float = 2.0,
    marker: str | None = "circle",
    markersize: int = 6,
    alpha: float = 1.0,
    width: int = 1600,
    height: int = 900,
    **kwargs,
) -> go.Figure:
    """
    Create a basic line chart showing trends over a sequence using plotly.

    Args:
        data: Input DataFrame with required columns
        x: Column name for x-axis values
        y: Column name for y-axis (numeric) values
        title: Plot title (optional)
        xlabel: Custom x-axis label (optional, defaults to x column name)
        ylabel: Custom y-axis label (optional, defaults to y column name)
        color: Line color (default: "steelblue")
        linewidth: Width of the line (default: 2.0)
        marker: Marker style for data points (default: "circle", set None to hide)
        markersize: Size of markers (default: 6)
        alpha: Transparency level (default: 1.0)
        width: Figure width in pixels (default: 1600)
        height: Figure height in pixels (default: 900)
        **kwargs: Additional parameters passed to plotly trace

    Returns:
        Plotly Figure object

    Raises:
        ValueError: If data is empty
        KeyError: If required columns not found

    Example:
        >>> data = pd.DataFrame({
        ...     'month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
        ...     'sales': [100, 120, 90, 140, 160]
        ... })
        >>> fig = create_plot(data, x='month', y='sales')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    for col in [x, y]:
        if col not in data.columns:
            available = ", ".join(data.columns)
            raise KeyError(f"Column '{col}' not found. Available columns: {available}")

    # Determine mode based on marker parameter
    mode = "lines+markers" if marker else "lines"

    # Create figure
    fig = go.Figure()

    # Build trace configuration
    trace_kwargs = {
        "x": data[x],
        "y": data[y],
        "mode": mode,
        "name": y,
        "line": {"color": color, "width": linewidth},
        "opacity": alpha,
    }

    # Add marker configuration if enabled
    if marker:
        trace_kwargs["marker"] = {
            "symbol": marker,
            "size": markersize,
            "color": color,
            "line": {"width": 1, "color": "white"},
        }

    # Merge with additional kwargs
    trace_kwargs.update(kwargs)

    fig.add_trace(go.Scatter(**trace_kwargs))

    # Update layout with clean styling
    fig.update_layout(
        title={"text": title, "font": {"size": 16, "family": "Arial, sans-serif"}, "x": 0.5, "xanchor": "center"}
        if title
        else None,
        xaxis={
            "title": {"text": xlabel or x, "font": {"size": 12}},
            "gridcolor": "rgba(128, 128, 128, 0.3)",
            "gridwidth": 1,
            "showgrid": True,
            "zeroline": False,
            "showline": True,
            "linewidth": 1,
            "linecolor": "lightgray",
        },
        yaxis={
            "title": {"text": ylabel or y, "font": {"size": 12}},
            "gridcolor": "rgba(128, 128, 128, 0.3)",
            "gridwidth": 1,
            "showgrid": True,
            "zeroline": True,
            "zerolinewidth": 1,
            "zerolinecolor": "lightgray",
            "showline": True,
            "linewidth": 1,
            "linecolor": "lightgray",
        },
        plot_bgcolor="white",
        paper_bgcolor="white",
        width=width,
        height=height,
        showlegend=False,
        hovermode="x unified",
        hoverlabel={"bgcolor": "white", "font_size": 12, "font_family": "Arial, sans-serif"},
    )

    # Update hover template for better information display
    fig.update_traces(hovertemplate=f"<b>{x}</b>: %{{x}}<br><b>{y}</b>: %{{y}}<extra></extra>")

    return fig


if __name__ == "__main__":
    # Sample data for testing - monthly sales data
    sample_data = pd.DataFrame(
        {
            "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            "Sales": [120, 135, 125, 148, 162, 178, 195, 188, 172, 158, 145, 165],
        }
    )

    # Create plot with default settings
    fig = create_plot(
        sample_data,
        x="Month",
        y="Sales",
        title="Monthly Sales Trend",
        xlabel="Month",
        ylabel="Sales ($)",
        color="steelblue",
        linewidth=2.5,
        marker="circle",
        markersize=10,
    )

    # Save as PNG
    fig.write_image("plot.png", width=1600, height=900, scale=2)
    print("Plot saved to plot.png")
