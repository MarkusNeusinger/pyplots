"""
scatter-basic: Basic Scatter Plot
Implementation for: matplotlib
Variant: default
Python: 3.10+
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from matplotlib.figure import Figure


def create_plot(
    data: pd.DataFrame,
    x: str,
    y: str,
    figsize: tuple[float, float] = (10, 6),
    alpha: float = 0.6,
    size: float = 30,
    color: str = "steelblue",
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    edgecolors: Optional[str] = None,
    linewidth: float = 0,
    **kwargs
) -> "Figure":
    """
    Create a basic scatter plot visualizing the relationship between two continuous variables.

    Args:
        data: Input DataFrame with required columns
        x: Column name for x-axis values
        y: Column name for y-axis values
        figsize: Figure size as (width, height) tuple (default: (10, 6))
        alpha: Transparency level for points (default: 0.6 for better visibility with many points)
        size: Point size (default: 30)
        color: Point color (default: "steelblue")
        title: Plot title (default: None)
        xlabel: X-axis label (default: uses column name)
        ylabel: Y-axis label (default: uses column name)
        edgecolors: Edge color for points (default: None)
        linewidth: Width of edge lines (default: 0)
        **kwargs: Additional parameters passed to scatter function

    Returns:
        Matplotlib Figure object

    Raises:
        ValueError: If data is empty
        KeyError: If required columns not found
        TypeError: If x or y columns contain non-numeric data

    Example:
        >>> data = pd.DataFrame({'x': [1, 2, 3], 'y': [2, 4, 3]})
        >>> fig = create_plot(data, 'x', 'y')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    # Check required columns
    for col in [x, y]:
        if col not in data.columns:
            available = ", ".join(data.columns)
            raise KeyError(f"Column '{col}' not found. Available columns: {available}")

    # Check if columns are numeric
    if not pd.api.types.is_numeric_dtype(data[x]):
        raise TypeError(f"Column '{x}' must contain numeric data")
    if not pd.api.types.is_numeric_dtype(data[y]):
        raise TypeError(f"Column '{y}' must contain numeric data")

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Plot data
    scatter = ax.scatter(
        data[x],
        data[y],
        s=size,
        alpha=alpha,
        c=color,
        edgecolors=edgecolors,
        linewidth=linewidth,
        **kwargs
    )

    # Labels and title
    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel or y)

    if title:
        ax.set_title(title)

    # Apply styling
    ax.grid(True, alpha=0.3)

    # Layout
    plt.tight_layout()

    return fig


if __name__ == '__main__':
    # Sample data for testing - many points to demonstrate basic scatter
    np.random.seed(42)
    n_points = 500

    data = pd.DataFrame({
        'x': np.random.randn(n_points) * 2 + 10,
        'y': np.random.randn(n_points) * 3 + 15 + np.random.randn(n_points) * 0.5
    })

    # Create plot
    fig = create_plot(
        data,
        'x',
        'y',
        title='Basic Scatter Plot Example',
        xlabel='X Value',
        ylabel='Y Value'
    )

    # Save for inspection - ALWAYS use 'plot.png' as filename
    plt.savefig('plot.png', dpi=200, bbox_inches='tight')
    print("Plot saved to plot.png")