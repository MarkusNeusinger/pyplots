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
    figsize: tuple[int, int] = (10, 6),
    color: str = "#306998",
    linewidth: float = 2.0,
    marker: str | None = None,
    marker_size: int = 6,
    alpha: float = 1.0,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    linestyle: str = "solid",
    **kwargs,
) -> go.Figure:
    """
    Create a basic line chart showing trends over a sequence using plotly.

    A fundamental line chart that visualizes trends and patterns in data over
    a continuous axis, typically time or sequential values.

    Args:
        data: Input DataFrame with required columns.
        x: Column name for x-axis values (numeric or temporal).
        y: Column name for y-axis (numeric) values.
        figsize: Figure size as (width, height) tuple (default: (10, 6)).
            Note: This is scaled to achieve 4800x2700 px output.
        color: Line color (default: "#306998" - Python Blue).
        linewidth: Width of the line (default: 2.0).
        marker: Marker style for data points (default: None).
            Valid values: "circle", "square", "diamond", "cross", "x", etc.
        marker_size: Size of markers if enabled (default: 6).
        alpha: Transparency level for the line (default: 1.0).
        title: Plot title (default: None).
        xlabel: Custom x-axis label (default: uses column name).
        ylabel: Custom y-axis label (default: uses column name).
        linestyle: Line style (default: "solid").
            Valid values: "solid", "dash", "dot", "dashdot".
        **kwargs: Additional parameters passed to plotly trace.

    Returns:
        Plotly Figure object.

    Raises:
        ValueError: If data is empty.
        KeyError: If required columns not found.

    Example:
        >>> data = pd.DataFrame({
        ...     'month': [1, 2, 3, 4, 5, 6],
        ...     'sales': [100, 150, 130, 180, 200, 190]
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

    # Sort data by x-axis to ensure proper line connections
    plot_data = data.copy()
    try:
        plot_data = plot_data.sort_values(by=x)
    except TypeError:
        # If x column is not sortable (e.g., categorical), keep original order
        pass

    # Map linestyle to plotly dash format
    dash_map = {"solid": "solid", "dash": "dash", "dashed": "dash", "dot": "dot", "dotted": "dot", "dashdot": "dashdot"}
    dash_style = dash_map.get(linestyle, "solid")

    # Determine mode based on marker parameter
    mode = "lines+markers" if marker else "lines"

    # Figure dimensions for 4800x2700 output (scaled by 3)
    base_width = 1600
    base_height = 900

    # Create figure
    fig = go.Figure()

    # Build trace configuration
    trace_kwargs = {
        "x": plot_data[x],
        "y": plot_data[y],
        "mode": mode,
        "name": y,
        "line": {"color": color, "width": linewidth, "dash": dash_style},
        "opacity": alpha,
    }

    # Add marker configuration if enabled
    if marker:
        trace_kwargs["marker"] = {
            "symbol": marker,
            "size": marker_size,
            "color": color,
            "line": {"width": 1, "color": "white"},
        }

    # Merge with additional kwargs
    trace_kwargs.update(kwargs)

    fig.add_trace(go.Scatter(**trace_kwargs))

    # Set axis labels
    x_label = xlabel if xlabel is not None else x
    y_label = ylabel if ylabel is not None else y

    # Update layout with clean styling
    # Font sizes scaled for 4800x2700 output (scale=3)
    title_font_size = 60  # 20pt * 3
    axis_label_font_size = 60  # 20pt * 3
    tick_font_size = 48  # 16pt * 3

    fig.update_layout(
        title={
            "text": title,
            "font": {"size": title_font_size, "family": "Arial, sans-serif"},
            "x": 0.5,
            "xanchor": "center",
        }
        if title
        else None,
        xaxis={
            "title": {"text": x_label, "font": {"size": axis_label_font_size}},
            "tickfont": {"size": tick_font_size},
            "gridcolor": "rgba(128, 128, 128, 0.3)",
            "gridwidth": 1,
            "showgrid": True,
            "zeroline": False,
            "showline": True,
            "linewidth": 1,
            "linecolor": "lightgray",
        },
        yaxis={
            "title": {"text": y_label, "font": {"size": axis_label_font_size}},
            "tickfont": {"size": tick_font_size},
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
        width=base_width,
        height=base_height,
        showlegend=False,
        hovermode="x unified",
        hoverlabel={"bgcolor": "white", "font_size": tick_font_size, "font_family": "Arial, sans-serif"},
        margin={"l": 120, "r": 60, "t": 100 if title else 60, "b": 100},
    )

    # Update hover template for better information display
    fig.update_traces(hovertemplate=f"<b>{x}</b>: %{{x}}<br><b>{y}</b>: %{{y}}<extra></extra>")

    return fig


if __name__ == "__main__":
    # Sample data for testing - monthly sales data
    sample_data = pd.DataFrame(
        {
            "month": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            "sales": [120, 135, 125, 148, 162, 178, 195, 188, 172, 158, 145, 165],
        }
    )

    # Create plot with default settings
    fig = create_plot(
        sample_data,
        x="month",
        y="sales",
        title="Monthly Sales Trend",
        xlabel="Month",
        ylabel="Sales ($)",
        marker="circle",
        marker_size=10,
    )

    # Save as PNG - 4800x2700 px (1600x900 * scale=3)
    fig.write_image("plot.png", width=1600, height=900, scale=3)
    print("Plot saved to plot.png")
