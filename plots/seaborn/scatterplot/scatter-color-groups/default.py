"""
scatter-color-groups: Scatter Plot with Color Groups
Implementation for: seaborn
Variant: default
Python: 3.10+
"""

from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

if TYPE_CHECKING:
    from matplotlib.figure import Figure


def create_plot(
    data: pd.DataFrame,
    x: str,
    y: str,
    group: str,
    figsize: tuple[float, float] = (16, 9),
    alpha: float = 0.7,
    size: float = 100,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    palette: str = "Set1",
    **kwargs
) -> "Figure":
    """
    Create a scatter plot with points colored by categorical groups using seaborn.

    Visualizes data points in a 2D x-y space with distinct colors for each
    categorical group, showing separate "color clouds" for different categories.

    Args:
        data: Input DataFrame with required columns
        x: Column name for x-axis values
        y: Column name for y-axis values
        group: Column name for categorical grouping and coloring
        figsize: Figure size as (width, height) tuple (default: (16, 9))
        alpha: Transparency level for points (default: 0.7)
        size: Point size (default: 100)
        title: Plot title (default: None)
        xlabel: Custom x-axis label (default: uses column name)
        ylabel: Custom y-axis label (default: uses column name)
        palette: Seaborn palette name (default: "Set1")
        **kwargs: Additional parameters passed to scatterplot

    Returns:
        Matplotlib Figure object

    Raises:
        ValueError: If data is empty
        KeyError: If required columns not found in data

    Example:
        >>> import pandas as pd
        >>> data = pd.DataFrame({
        ...     'x': [1, 2, 3, 4, 5, 6],
        ...     'y': [2, 4, 3, 5, 6, 4],
        ...     'group': ['A', 'A', 'B', 'B', 'C', 'C']
        ... })
        >>> fig = create_plot(data, 'x', 'y', 'group')
        >>> plt.savefig('plot.png')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    # Check required columns
    required_cols = [x, y, group]
    for col in required_cols:
        if col not in data.columns:
            available = ", ".join(data.columns)
            raise KeyError(
                f"Column '{col}' not found in data. Available columns: {available}"
            )

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Create scatter plot with hue for grouping
    sns.scatterplot(
        data=data,
        x=x,
        y=y,
        hue=group,
        palette=palette,
        alpha=alpha,
        s=size,
        ax=ax,
        **kwargs
    )

    # Set labels
    ax.set_xlabel(xlabel or x, fontsize=11)
    ax.set_ylabel(ylabel or y, fontsize=11)

    # Add title if provided
    if title:
        ax.set_title(title, fontsize=12, fontweight="bold", pad=15)

    # Customize legend
    ax.legend(title=group, loc="best", framealpha=0.9)

    # Add subtle grid
    ax.grid(True, alpha=0.3, linestyle="--")

    # Layout
    plt.tight_layout()

    return fig


if __name__ == "__main__":
    # Sample data for testing
    data = pd.DataFrame({
        "x": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5],
        "y": [2, 4, 3, 5, 6, 4, 7, 8, 9, 10, 3, 5, 4, 6, 7, 5],
        "group": [
            "A", "A", "A", "A", "A", "A",
            "B", "B", "B", "B",
            "C", "C", "C", "C", "C", "C"
        ]
    })

    # Create plot
    fig = create_plot(data, "x", "y", "group", title="Scatter Plot with Color Groups")

    # Save for inspection
    plt.savefig("plot.png", dpi=300, bbox_inches="tight")
    print("Plot saved to plot.png")
