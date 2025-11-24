"""
scatter-basic-006: Multiple Scatter Plots in Single Figure
Implementation for: seaborn
Variant: default
Python: 3.10+
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from matplotlib.figure import Figure


def create_plot(
    data: pd.DataFrame,
    x: str,
    y1: str,
    y2: str,
    y3: str,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    figsize: tuple[float, float] = (10, 6),
    point_size: float = 50,
    alpha: float = 0.7,
    colors: list[str] | None = None,
    grid: bool = True,
    grid_alpha: float = 0.3,
    legend_loc: str = "upper right",
    style: str = "whitegrid",
    **kwargs
) -> Figure:
    """
    Create a figure with three scatter plots showing x vs y1, y2, and y3 using seaborn.

    Args:
        data: Input DataFrame with required columns
        x: Column name for x-axis values
        y1: Column name for first y-axis series
        y2: Column name for second y-axis series
        y3: Column name for third y-axis series
        title: Plot title (default: "Multiple Scatter Plots: x vs y1, y2, y3")
        xlabel: X-axis label (default: "X Values")
        ylabel: Y-axis label (default: "Y Values")
        figsize: Figure size in inches (default: (10, 6))
        point_size: Size of scatter points (default: 50)
        alpha: Transparency of points (default: 0.7)
        colors: List of colors for each series (default: ["blue", "orange", "green"])
        grid: Whether to show grid (default: True)
        grid_alpha: Grid transparency (default: 0.3)
        legend_loc: Legend location (default: "upper right")
        style: Seaborn style (default: "whitegrid")
        **kwargs: Additional parameters passed to scatterplot function

    Returns:
        Matplotlib Figure object

    Raises:
        ValueError: If data is empty
        KeyError: If required columns not found in data

    Example:
        >>> np.random.seed(42)
        >>> data = pd.DataFrame({
        ...     'x': np.arange(20),
        ...     'y1': np.random.randn(20) * 2 + 10,
        ...     'y2': np.random.randn(20) * 3 + 15,
        ...     'y3': np.random.randn(20) * 2.5 + 20
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
        colors = ["blue", "orange", "green"]
    if title is None:
        title = "Multiple Scatter Plots: x vs y1, y2, y3"
    if xlabel is None:
        xlabel = "X Values"
    if ylabel is None:
        ylabel = "Y Values"

    # Set seaborn style
    sns.set_style(style)

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Plot data - three scatter plots with different colors using seaborn
    sns.scatterplot(
        data=data,
        x=x,
        y=y1,
        s=point_size,
        alpha=alpha,
        color=colors[0],
        label=y1,
        ax=ax,
        **kwargs
    )

    sns.scatterplot(
        data=data,
        x=x,
        y=y2,
        s=point_size,
        alpha=alpha,
        color=colors[1],
        label=y2,
        ax=ax,
        **kwargs
    )

    sns.scatterplot(
        data=data,
        x=x,
        y=y3,
        s=point_size,
        alpha=alpha,
        color=colors[2],
        label=y3,
        ax=ax,
        **kwargs
    )

    # Apply styling
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')

    # Customize grid if needed (seaborn already adds grid with whitegrid style)
    if grid:
        ax.grid(True, alpha=grid_alpha, linestyle='--')
    else:
        ax.grid(False)

    # Ensure legend is properly positioned
    ax.legend(loc=legend_loc, framealpha=0.9)

    # Ensure layout doesn't cut off labels
    plt.tight_layout()

    # Reset seaborn style to avoid affecting other plots
    sns.reset_orig()

    return fig


if __name__ == '__main__':
    # Sample data for testing
    np.random.seed(42)

    # Generate sample data with three y variables
    n_points = 30
    x_values = np.linspace(0, 10, n_points)

    sample_data = pd.DataFrame({
        'x': x_values,
        'y1': 2 * x_values + np.random.randn(n_points) * 2 + 5,      # Linear with noise
        'y2': x_values ** 1.5 + np.random.randn(n_points) * 3,        # Power relationship
        'y3': 10 * np.sin(x_values * 0.5) + np.random.randn(n_points) * 1.5 + 20  # Sinusoidal
    })

    # Create plot
    fig = create_plot(
        sample_data,
        x='x',
        y1='y1',
        y2='y2',
        y3='y3'
    )

    # Save for inspection
    plt.savefig('test_output_seaborn.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("Plot saved to test_output_seaborn.png")