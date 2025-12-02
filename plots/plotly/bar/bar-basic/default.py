"""
bar-basic: Basic Bar Chart
Library: plotly
"""

from typing import TYPE_CHECKING

import pandas as pd
import plotly.graph_objects as go


if TYPE_CHECKING:
    pass


def create_plot(
    data: pd.DataFrame,
    category: str,
    value: str,
    figsize: tuple[int, int] = (1600, 900),
    color: str = "steelblue",
    edgecolor: str = "black",
    alpha: float = 0.8,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    rotation: int = 0,
    **kwargs,
) -> go.Figure:
    """
    Create a basic vertical bar chart for categorical data comparison.

    A fundamental bar chart that displays rectangular bars with heights
    proportional to the values they represent. Each bar corresponds to
    a category, making it ideal for comparing quantities across discrete
    categories.

    Args:
        data: Input DataFrame containing the data to plot.
        category: Column name for category labels (x-axis).
        value: Column name for numeric values (bar heights).
        figsize: Figure size as (width, height) in pixels. Defaults to (1600, 900).
        color: Bar fill color. Defaults to "steelblue".
        edgecolor: Bar edge/outline color. Defaults to "black".
        alpha: Transparency level for bars (0-1). Defaults to 0.8.
        title: Plot title. Defaults to None.
        xlabel: X-axis label. Defaults to column name if None.
        ylabel: Y-axis label. Defaults to column name if None.
        rotation: Rotation angle for x-axis labels in degrees. Defaults to 0.
        **kwargs: Additional parameters passed to go.Bar.

    Returns:
        Plotly Figure object containing the bar chart.

    Raises:
        ValueError: If data is empty.
        KeyError: If required columns are not found in data.

    Example:
        >>> data = pd.DataFrame({
        ...     'category': ['A', 'B', 'C', 'D'],
        ...     'value': [45, 78, 52, 91]
        ... })
        >>> fig = create_plot(data, 'category', 'value', title='Sales by Product')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    for col in [category, value]:
        if col not in data.columns:
            available = ", ".join(data.columns)
            raise KeyError(f"Column '{col}' not found. Available: {available}")

    # Set default labels from column names
    x_label = xlabel if xlabel is not None else category
    y_label = ylabel if ylabel is not None else value

    # Create figure
    fig = go.Figure()

    # Add bar trace
    fig.add_trace(
        go.Bar(
            x=data[category],
            y=data[value],
            marker=dict(color=color, opacity=alpha, line=dict(color=edgecolor, width=1)),
            **kwargs,
        )
    )

    # Update layout with styling
    fig.update_layout(
        title=dict(text=title, x=0.5, xanchor="center") if title else None,
        xaxis=dict(title=dict(text=x_label, font=dict(size=14)), tickangle=-rotation, tickfont=dict(size=12)),
        yaxis=dict(
            title=dict(text=y_label, font=dict(size=14)),
            tickfont=dict(size=12),
            rangemode="tozero",
            showgrid=True,
            gridwidth=1,
            gridcolor="rgba(128, 128, 128, 0.3)",
        ),
        template="plotly_white",
        width=figsize[0],
        height=figsize[1],
        showlegend=False,
        margin=dict(l=80, r=40, t=80 if title else 40, b=80),
    )

    return fig


if __name__ == "__main__":
    # Sample data for testing
    sample_data = pd.DataFrame(
        {"category": ["Product A", "Product B", "Product C", "Product D", "Product E"], "value": [45, 78, 52, 91, 63]}
    )

    # Create plot
    fig = create_plot(sample_data, "category", "value", title="Sales by Product")

    # Save
    fig.write_image("plot.png", width=1600, height=900, scale=2)
    print("Plot saved to plot.png")
