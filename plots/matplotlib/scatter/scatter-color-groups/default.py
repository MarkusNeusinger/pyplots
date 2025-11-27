"""
scatter-color-groups: Scatter Plot with Color Groups
Implementation for: matplotlib
Variant: default
Python: 3.10+
"""

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from matplotlib.figure import Figure


def create_plot(
    data: pd.DataFrame,
    x: str,
    y: str,
    group: str,
    figsize: tuple[float, float] = (10, 6),
    alpha: float = 0.7,
    size: float = 50,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    palette: str = "Set1",
    **kwargs
) -> "Figure":
    """
    Create a scatter plot with points colored by categorical groups.

    Visualizes data points in a 2D x-y space with distinct colors for each
    categorical group, showing separate "color clouds" for different categories.

    Args:
        data: Input DataFrame with required columns
        x: Column name for x-axis values
        y: Column name for y-axis values
        group: Column name for categorical grouping and coloring
        figsize: Figure size as (width, height) tuple (default: (10, 6))
        alpha: Transparency level for points (default: 0.7)
        size: Point size (default: 50)
        title: Plot title (default: None)
        xlabel: Custom x-axis label (default: uses column name)
        ylabel: Custom y-axis label (default: uses column name)
        palette: Matplotlib colormap or seaborn palette name (default: "Set1")
        **kwargs: Additional parameters passed to scatter plot

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
        >>> plt.savefig('scatter_groups.png')
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

    # Create figure and axis
    fig, ax = plt.subplots(figsize=figsize)

    # Get unique groups and create color mapping
    groups = data[group].unique()

    # Get colors from palette
    try:
        cmap = plt.get_cmap(palette)
        colors = [cmap(i / max(len(groups) - 1, 1)) for i in range(len(groups))]
    except (ValueError, AttributeError):
        # Fallback to tab10 if palette not found
        cmap = plt.get_cmap("tab10")
        colors = [cmap(i % 10) for i in range(len(groups))]

    # Plot each group with a different color
    for idx, group_val in enumerate(groups):
        group_data = data[data[group] == group_val]
        ax.scatter(
            group_data[x],
            group_data[y],
            label=str(group_val),
            alpha=alpha,
            s=size,
            color=colors[idx],
            **kwargs
        )

    # Set labels
    ax.set_xlabel(xlabel or x, fontsize=11)
    ax.set_ylabel(ylabel or y, fontsize=11)

    # Add title if provided
    if title:
        ax.set_title(title, fontsize=12, fontweight="bold", pad=15)

    # Add legend
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
    plt.savefig("test_output_matplotlib.png", dpi=150)
    print("Matplotlib plot saved to test_output_matplotlib.png")
