"""
scatter-basic-006: 3 scatter plots
Implementation for: matplotlib
Variant: default
Python: 3.10+
"""

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import pandas as pd
import numpy as np


def create_plot(
    data: pd.DataFrame,
    x: str,
    y1: str,
    y2: str,
    y3: str,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    colors: list[str] | None = None,
    alpha: float = 0.8,
    size: float = 50,
    **kwargs
) -> Figure:
    """
    Display three scatter plots in a single figure showing three different y-series against a common x-axis.

    Args:
        data: Input DataFrame with required columns
        x: Column name for x-axis values
        y1: Column name for first y-series
        y2: Column name for second y-series
        y3: Column name for third y-series
        title: Title for the plot (default: "Three Scatter Plots")
        xlabel: Label for x-axis (default: column name)
        ylabel: Label for y-axis (default: "Y Values")
        colors: List of three colors for the series (default: ['#1f77b4', '#ff7f0e', '#2ca02c'])
        alpha: Transparency of points (default: 0.8)
        size: Size of points (default: 50)
        **kwargs: Additional parameters passed to scatter function

    Returns:
        Matplotlib Figure object

    Raises:
        ValueError: If data is empty
        KeyError: If required columns not found in data

    Example:
        >>> data = pd.DataFrame({
        ...     'x': [1, 2, 3, 4, 5],
        ...     'y1': [2, 4, 6, 8, 10],
        ...     'y2': [1, 3, 5, 7, 9],
        ...     'y3': [3, 3, 6, 6, 9]
        ... })
        >>> fig = create_plot(data, 'x', 'y1', 'y2', 'y3')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    # Check required columns
    required_columns = [x, y1, y2, y3]
    for col in required_columns:
        if col not in data.columns:
            available = ", ".join(data.columns)
            raise KeyError(f"Column '{col}' not found. Available columns: {available}")

    # Set defaults
    if colors is None:
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    if len(colors) < 3:
        raise ValueError("colors list must contain at least 3 colors")

    if title is None:
        title = "Three Scatter Plots"
    if xlabel is None:
        xlabel = x
    if ylabel is None:
        ylabel = "Y Values"

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot data
    scatter1 = ax.scatter(data[x], data[y1], c=colors[0], s=size, alpha=alpha,
                         label=y1, **kwargs)
    scatter2 = ax.scatter(data[x], data[y2], c=colors[1], s=size, alpha=alpha,
                         label=y2, **kwargs)
    scatter3 = ax.scatter(data[x], data[y3], c=colors[2], s=size, alpha=alpha,
                         label=y3, **kwargs)

    # Apply styling
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')

    # Add grid
    ax.grid(True, alpha=0.3, linestyle='--')

    # Add legend
    ax.legend(loc='best', framealpha=0.9)

    # Layout
    plt.tight_layout()

    return fig


if __name__ == '__main__':
    # Sample data for testing
    np.random.seed(42)
    n_points = 30

    data = pd.DataFrame({
        'x': np.linspace(1, 10, n_points),
        'y1': np.linspace(1, 10, n_points) + np.random.normal(0, 0.5, n_points),
        'y2': np.linspace(2, 12, n_points) + np.random.normal(0, 0.7, n_points),
        'y3': np.linspace(0, 8, n_points) + np.random.normal(0, 0.6, n_points)
    })

    # Create plot
    fig = create_plot(
        data,
        x='x',
        y1='y1',
        y2='y2',
        y3='y3',
        title='Sample Three Scatter Plots',
        xlabel='X Values',
        ylabel='Y Values'
    )

    # Save for inspection
    plt.savefig('test_output.png', dpi=150, bbox_inches='tight')
    print("Plot saved to test_output.png")
    plt.show()