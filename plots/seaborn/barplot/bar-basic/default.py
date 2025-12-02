"""
bar-basic: Basic Bar Chart
Library: seaborn
"""

from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


if TYPE_CHECKING:
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
) -> "Figure":
    """
    Create a basic vertical bar chart for categorical data comparison.

    A fundamental bar chart displaying rectangular bars with heights proportional
    to their numeric values, ideal for comparing quantities across categories.

    Args:
        data: Input DataFrame containing the data to plot
        category: Column name for category labels (x-axis)
        value: Column name for numeric values (bar heights)
        figsize: Figure size as (width, height) in inches
        color: Bar fill color
        edgecolor: Bar edge color
        alpha: Transparency level for bars (0-1)
        title: Plot title (optional)
        xlabel: X-axis label (defaults to column name if None)
        ylabel: Y-axis label (defaults to column name if None)
        rotation: Rotation angle for x-axis labels in degrees
        **kwargs: Additional parameters passed to seaborn.barplot

    Returns:
        Matplotlib Figure object

    Raises:
        ValueError: If data is empty
        KeyError: If required columns not found in data

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

    # Plot data using seaborn barplot
    sns.barplot(data=data, x=category, y=value, color=color, edgecolor=edgecolor, alpha=alpha, ax=ax, **kwargs)

    # Set y-axis to start at zero for accurate visual comparison
    ax.set_ylim(bottom=0)

    # Add subtle grid on y-axis only
    ax.yaxis.grid(True, alpha=0.3)
    ax.set_axisbelow(True)

    # Labels
    ax.set_xlabel(xlabel if xlabel is not None else category)
    ax.set_ylabel(ylabel if ylabel is not None else value)

    # Title
    if title is not None:
        ax.set_title(title)

    # Rotate x-axis labels if specified
    if rotation != 0:
        plt.xticks(rotation=rotation, ha="right")

    # Layout
    plt.tight_layout()

    return fig


if __name__ == "__main__":
    # Sample data for testing
    sample_data = pd.DataFrame(
        {"category": ["Product A", "Product B", "Product C", "Product D", "Product E"], "value": [45, 78, 52, 91, 63]}
    )

    # Create plot
    fig = create_plot(sample_data, "category", "value", title="Sales by Product", xlabel="Product", ylabel="Sales ($)")

    # Save - ALWAYS use 'plot.png'!
    plt.savefig("plot.png", dpi=300, bbox_inches="tight")
    print("Plot saved to plot.png")
