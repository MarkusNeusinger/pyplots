"""
step-basic: Basic Step Plot
Implementation for: matplotlib
Variant: default
Python: 3.10+
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from matplotlib.figure import Figure


def create_plot(
    data: pd.DataFrame,
    x: str,
    y: str,
    where: str = "pre",
    color: str = "steelblue",
    linewidth: float = 2.0,
    alpha: float = 0.9,
    linestyle: str = "-",
    marker: str | None = None,
    markersize: float = 6,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    figsize: tuple[float, float] = (10, 6),
    **kwargs
) -> "Figure":
    """
    Create a basic step plot showing discrete changes in values.

    Step plots display data as a series of horizontal and vertical lines,
    showing discrete changes between values. Ideal for visualizing data that
    changes at specific intervals.

    Args:
        data: Input DataFrame with required columns
        x: Column name for x-axis values (sequential or time-based)
        y: Column name for y-axis values (numeric levels)
        where: Position of steps - "pre", "post", or "mid" (default: "pre")
        color: Line color (default: "steelblue")
        linewidth: Line width (default: 2.0)
        alpha: Transparency level 0.0-1.0 (default: 0.9)
        linestyle: Line style - "-", "--", "-.", or ":" (default: "-")
        marker: Optional marker style for data points (default: None)
        markersize: Size of markers if used (default: 6)
        title: Optional plot title (default: None)
        xlabel: Custom x-axis label (default: column name)
        ylabel: Custom y-axis label (default: column name)
        figsize: Figure size in inches (default: (10, 6))
        **kwargs: Additional parameters passed to step function

    Returns:
        Matplotlib Figure object

    Raises:
        ValueError: If data is empty or 'where' parameter is invalid
        KeyError: If required columns not found

    Example:
        >>> import pandas as pd
        >>> data = pd.DataFrame({
        ...     'time': [1, 2, 3, 4, 5],
        ...     'level': [10, 15, 12, 18, 14]
        ... })
        >>> fig = create_plot(data, 'time', 'level')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    # Check required columns
    required_columns = [x, y]
    missing_columns = []
    for col in required_columns:
        if col not in data.columns:
            missing_columns.append(col)

    if missing_columns:
        available = ", ".join(data.columns)
        missing = ", ".join(missing_columns)
        raise KeyError(f"Column(s) '{missing}' not found. Available columns: {available}")

    # Validate 'where' parameter
    if where not in ["pre", "post", "mid"]:
        raise ValueError(f"'where' parameter must be 'pre', 'post', or 'mid', got '{where}'")

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Sort data by x values to ensure proper step plot
    plot_data = data[[x, y]].copy()
    plot_data = plot_data.sort_values(by=x)

    # Plot step lines
    ax.step(plot_data[x], plot_data[y],
            where=where,
            color=color,
            linewidth=linewidth,
            alpha=alpha,
            linestyle=linestyle,
            **kwargs)

    # Add markers if specified
    if marker:
        ax.plot(plot_data[x], plot_data[y],
                marker=marker,
                markersize=markersize,
                color=color,
                alpha=alpha,
                linestyle='None')  # Only markers, no line

    # Apply styling
    ax.set_xlabel(xlabel or x, fontsize=12)
    ax.set_ylabel(ylabel or y, fontsize=12)

    # Add title if provided
    if title:
        ax.set_title(title, fontsize=14, fontweight='bold')

    # Add subtle grid
    ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)

    # Ensure no overlapping labels
    fig.autofmt_xdate()  # Automatically format date labels if x is datetime

    # Layout
    plt.tight_layout()

    return fig


if __name__ == '__main__':
    # Sample data for testing
    np.random.seed(42)  # For reproducibility

    # Create sample data representing interest rate changes over time
    data = pd.DataFrame({
        'month': range(1, 13),
        'rate': [2.0, 2.0, 2.25, 2.25, 2.25, 2.5, 2.5, 2.75, 2.75, 2.75, 3.0, 3.0]
    })

    # Create plot
    fig = create_plot(
        data,
        x='month',
        y='rate',
        title='Interest Rate Changes Over Time',
        xlabel='Month',
        ylabel='Interest Rate (%)',
        where='post',  # Step occurs after the data point
        marker='o',  # Show actual data points
        markersize=4
    )

    # Save for inspection - ALWAYS use 'plot.png' as filename
    plt.savefig('plot.png', dpi=300, bbox_inches='tight')
    print("Plot saved to plot.png")