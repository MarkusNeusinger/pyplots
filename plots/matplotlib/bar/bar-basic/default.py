"""
bar-basic: Basic Bar Chart
Library: matplotlib
"""

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure


def create_plot(
    data: pd.DataFrame,
    category: str,
    value: str,
    figsize: tuple[float, float] = (10, 6),
    color: str = "steelblue",
    edgecolor: str = "black",
    alpha: float = 0.8,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    rotation: int = 0,
    **kwargs,
) -> Figure:
    """
    Create a basic vertical bar chart from a DataFrame.

    A fundamental bar chart that visualizes categorical data with numeric values,
    ideal for comparing quantities across discrete categories.

    Args:
        data: Input DataFrame containing the data to plot.
        category: Column name for category labels (x-axis).
        value: Column name for numeric values (bar heights).
        figsize: Figure size as (width, height) in inches.
        color: Bar fill color.
        edgecolor: Bar edge color.
        alpha: Transparency level for bars (0.0 to 1.0).
        title: Optional plot title.
        xlabel: X-axis label. Defaults to category column name if None.
        ylabel: Y-axis label. Defaults to value column name if None.
        rotation: Rotation angle for x-axis labels in degrees.
        **kwargs: Additional keyword arguments passed to ax.bar().

    Returns:
        Matplotlib Figure object containing the bar chart.

    Raises:
        ValueError: If data is empty.
        KeyError: If required columns are not found in the DataFrame.

    Example:
        >>> data = pd.DataFrame({
        ...     'category': ['A', 'B', 'C'],
        ...     'value': [10, 20, 15]
        ... })
        >>> fig = create_plot(data, 'category', 'value', title='Sample Chart')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    for col in [category, value]:
        if col not in data.columns:
            available = ", ".join(data.columns)
            raise KeyError(f"Column '{col}' not found. Available: {available}")

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Extract data
    categories = data[category]
    values = data[value]

    # Plot bars
    ax.bar(categories, values, color=color, edgecolor=edgecolor, alpha=alpha, **kwargs)

    # Set axis labels
    ax.set_xlabel(xlabel if xlabel is not None else category)
    ax.set_ylabel(ylabel if ylabel is not None else value)

    # Set title if provided
    if title is not None:
        ax.set_title(title)

    # Add subtle grid on y-axis only
    ax.yaxis.grid(True, alpha=0.3)
    ax.set_axisbelow(True)

    # Rotate x-axis labels if specified
    if rotation != 0:
        plt.xticks(rotation=rotation, ha="right" if rotation > 0 else "left")

    # Ensure y-axis starts at zero
    ax.set_ylim(bottom=0)

    # Adjust layout
    plt.tight_layout()

    return fig


if __name__ == "__main__":
    # Sample data for testing
    sample_data = pd.DataFrame(
        {"category": ["Product A", "Product B", "Product C", "Product D", "Product E"], "value": [45, 78, 52, 91, 63]}
    )

    # Create plot
    fig = create_plot(sample_data, "category", "value", title="Sales by Product", xlabel="Product", ylabel="Sales ($)")

    # Save
    plt.savefig("plot.png", dpi=300, bbox_inches="tight")
    print("Plot saved to plot.png")
