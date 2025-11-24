"""
scatter-basic-006: 3 scatter plots
Implementation for: seaborn
Variant: default
Python: 3.10+
"""

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import seaborn as sns
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
    palette: list[str] | None = None,
    alpha: float = 0.8,
    size: float = 50,
    style: str | None = None,
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
        palette: List of three colors for the series (default: seaborn tab10 colors)
        alpha: Transparency of points (default: 0.8)
        size: Size of points (default: 50)
        style: Seaborn style to apply (default: None, uses current style)
        **kwargs: Additional parameters passed to scatterplot function

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
    if palette is None:
        palette = sns.color_palette("tab10", n_colors=3)
    elif len(palette) < 3:
        raise ValueError("palette list must contain at least 3 colors")
    else:
        palette = palette[:3]

    if title is None:
        title = "Three Scatter Plots"
    if xlabel is None:
        xlabel = x
    if ylabel is None:
        ylabel = "Y Values"

    # Apply style if specified
    if style:
        sns.set_style(style)

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot data using seaborn
    sns.scatterplot(data=data, x=x, y=y1, ax=ax, s=size, alpha=alpha,
                   color=palette[0], label=y1, **kwargs)
    sns.scatterplot(data=data, x=x, y=y2, ax=ax, s=size, alpha=alpha,
                   color=palette[1], label=y2, **kwargs)
    sns.scatterplot(data=data, x=x, y=y3, ax=ax, s=size, alpha=alpha,
                   color=palette[2], label=y3, **kwargs)

    # Apply styling
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')

    # Add grid with seaborn style
    ax.grid(True, alpha=0.3, linestyle='--')

    # Ensure legend is properly positioned
    ax.legend(loc='best', framealpha=0.9)

    # Layout
    plt.tight_layout()

    # Reset style if it was changed
    if style:
        sns.reset_defaults()

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

    # Create plot with seaborn style
    fig = create_plot(
        data,
        x='x',
        y1='y1',
        y2='y2',
        y3='y3',
        title='Sample Three Scatter Plots (Seaborn)',
        xlabel='X Values',
        ylabel='Y Values',
        style='whitegrid'
    )

    # Save for inspection
    plt.savefig('test_output_seaborn.png', dpi=150, bbox_inches='tight')
    print("Plot saved to test_output_seaborn.png")
    plt.show()