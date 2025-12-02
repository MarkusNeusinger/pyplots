"""
bar-basic: Basic Bar Chart
Library: altair
"""

import altair as alt
import pandas as pd


def create_plot(
    data: pd.DataFrame,
    category: str,
    value: str,
    *,
    color: str = "steelblue",
    alpha: float = 0.8,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    rotation: int = 0,
    **kwargs,
) -> alt.Chart:
    """
    Create a basic vertical bar chart.

    A fundamental bar chart that visualizes categorical data with numeric values,
    ideal for comparing quantities across discrete categories.

    Args:
        data: Input DataFrame containing the data to plot.
        category: Column name for categorical x-axis values.
        value: Column name for numeric y-axis values.
        color: Bar fill color. Defaults to "steelblue".
        alpha: Transparency level for bars (0-1). Defaults to 0.8.
        title: Plot title. Defaults to None.
        xlabel: X-axis label. Defaults to column name if None.
        ylabel: Y-axis label. Defaults to column name if None.
        rotation: Rotation angle for x-axis labels. Defaults to 0.
        **kwargs: Additional parameters passed to chart properties.

    Returns:
        Altair Chart object.

    Raises:
        ValueError: If data is empty.
        KeyError: If required columns are not found in data.

    Example:
        >>> data = pd.DataFrame({
        ...     'category': ['A', 'B', 'C'],
        ...     'value': [10, 20, 15]
        ... })
        >>> chart = create_plot(data, 'category', 'value', title='Example')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    for col in [category, value]:
        if col not in data.columns:
            available = ", ".join(data.columns)
            raise KeyError(f"Column '{col}' not found. Available: {available}")

    # Determine axis labels
    x_label = xlabel if xlabel is not None else category
    y_label = ylabel if ylabel is not None else value

    # Build x-axis configuration
    x_axis = alt.Axis(title=x_label, labelAngle=-rotation if rotation != 0 else 0)

    # Build y-axis configuration with subtle grid
    y_axis = alt.Axis(title=y_label, grid=True, gridOpacity=0.3)

    # Create the bar chart
    chart = (
        alt.Chart(data)
        .mark_bar(color=color, opacity=alpha)
        .encode(
            x=alt.X(f"{category}:N", axis=x_axis, sort=None),
            y=alt.Y(f"{value}:Q", axis=y_axis, scale=alt.Scale(domain=[0, data[value].max() * 1.1])),
            tooltip=[alt.Tooltip(f"{category}:N", title=x_label), alt.Tooltip(f"{value}:Q", title=y_label)],
        )
        .properties(width=800, height=450)
    )

    # Add title if provided
    if title is not None:
        chart = chart.properties(title=title)

    # Configure chart appearance
    chart = chart.configure_axis(labelFontSize=12, titleFontSize=14).configure_title(fontSize=16, anchor="middle")

    return chart


if __name__ == "__main__":
    # Sample data for testing
    sample_data = pd.DataFrame(
        {"category": ["Product A", "Product B", "Product C", "Product D", "Product E"], "value": [45, 78, 52, 91, 63]}
    )

    # Create plot
    fig = create_plot(sample_data, "category", "value", title="Sales by Product")

    # Save
    fig.save("plot.png", scale_factor=2.0)
    print("Plot saved to plot.png")
