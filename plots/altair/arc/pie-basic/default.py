"""
pie-basic: Basic Pie Chart
Library: altair
"""

import altair as alt
import pandas as pd


# PyPlots.ai default color palette
PYPLOTS_COLORS = ["#306998", "#FFD43B", "#DC2626", "#059669", "#8B5CF6", "#F97316"]


def create_plot(
    data: pd.DataFrame,
    category: str,
    value: str,
    *,
    title: str | None = None,
    colors: list[str] | None = None,
    startangle: float = 90,
    show_labels: bool = True,
    label_format: str = ".1%",
    legend: bool = True,
    legend_loc: str = "right",
    inner_radius: float = 0,
    outer_radius: float = 150,
    **kwargs,
) -> alt.Chart:
    """
    Create a basic pie chart visualizing proportions of categorical data.

    A fundamental pie chart where each slice represents a category's share of the whole,
    ideal for showing composition and distribution across a small number of categories.

    Args:
        data: Input DataFrame containing the data to plot.
        category: Column name for category labels (slice names).
        value: Column name for numeric values (slice sizes).
        title: Plot title. Defaults to None.
        colors: Custom color palette for slices. Defaults to PyPlots.ai palette.
        startangle: Starting angle for first slice in degrees. Defaults to 90.
        show_labels: Whether to show percentage labels on slices. Defaults to True.
        label_format: Format string for percentage labels. Defaults to ".1%".
        legend: Whether to display legend. Defaults to True.
        legend_loc: Legend location ('right', 'left', 'top', 'bottom'). Defaults to 'right'.
        inner_radius: Inner radius for donut style (0 for solid pie). Defaults to 0.
        outer_radius: Outer radius of the pie. Defaults to 150.
        **kwargs: Additional parameters.

    Returns:
        Altair Chart object.

    Raises:
        ValueError: If data is empty or values contain negative numbers.
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

    # Validate non-negative values
    if (data[value] < 0).any():
        raise ValueError("Pie chart values must be non-negative")

    # Handle case where all values are zero
    total = data[value].sum()
    if total == 0:
        raise ValueError("Sum of values cannot be zero")

    # Use custom colors or default palette
    color_palette = colors if colors is not None else PYPLOTS_COLORS

    # Calculate the starting angle in radians (Altair uses radians, offset from 12 o'clock)
    # Altair's theta starts from 3 o'clock (0 degrees), so we need to adjust
    # To start from 12 o'clock (90 degrees from 3 o'clock), we use theta2Offset
    start_offset = (startangle - 90) * 3.14159 / 180

    # Create base chart with arc mark
    base = alt.Chart(data).encode(
        theta=alt.Theta(f"{value}:Q", stack=True),
        color=alt.Color(
            f"{category}:N",
            scale=alt.Scale(range=color_palette),
            legend=alt.Legend(title=category, orient=legend_loc, labelFontSize=16, titleFontSize=16)
            if legend
            else None,
        ),
        tooltip=[alt.Tooltip(f"{category}:N", title="Category"), alt.Tooltip(f"{value}:Q", title="Value")],
    )

    # Create the pie/arc chart
    pie = base.mark_arc(
        innerRadius=inner_radius,
        outerRadius=outer_radius,
        stroke="#ffffff",
        strokeWidth=2,
        theta2Offset=start_offset,
        thetaOffset=start_offset,
    )

    # Add percentage labels if requested
    if show_labels:
        # Calculate percentage for labels
        data_with_pct = data.copy()
        data_with_pct["_percentage"] = data_with_pct[value] / total

        # Create text labels positioned at the middle of each arc
        text = (
            alt.Chart(data_with_pct)
            .mark_text(radius=outer_radius * 0.7, fontSize=14, fontWeight="bold", color="#FFFFFF")
            .encode(theta=alt.Theta(f"{value}:Q", stack=True), text=alt.Text("_percentage:Q", format=label_format))
            .transform_calculate(theta2Offset=str(start_offset), thetaOffset=str(start_offset))
        )

        # Layer pie and text
        chart = alt.layer(pie, text)
    else:
        chart = pie

    # Set chart dimensions and title
    chart = chart.properties(width=400, height=400)

    if title is not None:
        chart = chart.properties(title=alt.TitleParams(text=title, fontSize=20, anchor="middle", fontWeight=600))

    # Configure chart appearance
    chart = chart.configure_view(strokeWidth=0).configure_legend(
        labelFontSize=16, titleFontSize=16, symbolSize=200, padding=10
    )

    return chart


if __name__ == "__main__":
    # Sample data for testing
    sample_data = pd.DataFrame(
        {"category": ["Product A", "Product B", "Product C", "Product D", "Other"], "value": [35, 25, 20, 15, 5]}
    )

    # Create plot
    fig = create_plot(sample_data, "category", "value", title="Market Share Distribution")

    # Save
    fig.save("plot.png", scale_factor=2.0)
    print("Plot saved to plot.png")
