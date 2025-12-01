"""
line-basic: Basic Line Plot
Implementation for: seaborn
Variant: default
Python: 3.10+
"""

from typing import TYPE_CHECKING, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


if TYPE_CHECKING:
    from matplotlib.figure import Figure


def create_plot(
    data: pd.DataFrame,
    x: str,
    y: str,
    figsize: tuple[float, float] = (16, 9),
    color: str = "steelblue",
    linewidth: float = 2.0,
    linestyle: str = "-",
    marker: Optional[str] = None,
    markersize: float = 6,
    alpha: float = 1.0,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    sort_data: bool = True,
    **kwargs,
) -> "Figure":
    """
    Create a basic line plot visualizing trends over a continuous or sequential axis.

    Args:
        data: Input DataFrame with required columns
        x: Column name for x-axis values
        y: Column name for y-axis values
        figsize: Figure size as (width, height) tuple (default: (16, 9))
        color: Line color (default: "steelblue")
        linewidth: Width of the line (default: 2.0)
        linestyle: Line style, e.g., '-', '--', '-.', ':' (default: '-')
        marker: Marker style for data points (default: None)
        markersize: Size of markers (default: 6)
        alpha: Transparency level (default: 1.0)
        title: Plot title (default: None)
        xlabel: X-axis label (default: uses column name)
        ylabel: Y-axis label (default: uses column name)
        sort_data: Whether to sort data by x-axis values (default: True)
        **kwargs: Additional parameters passed to seaborn lineplot function

    Returns:
        Matplotlib Figure object

    Raises:
        ValueError: If data is empty
        KeyError: If required columns not found
        TypeError: If y column contains non-numeric data

    Example:
        >>> data = pd.DataFrame({'time': [1, 2, 3], 'value': [2, 4, 3]})
        >>> fig = create_plot(data, 'time', 'value')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    # Check required columns
    for col in [x, y]:
        if col not in data.columns:
            available = ", ".join(data.columns)
            raise KeyError(f"Column '{col}' not found. Available columns: {available}")

    # Check if y column is numeric
    if not pd.api.types.is_numeric_dtype(data[y]):
        raise TypeError(f"Column '{y}' must contain numeric data")

    # Create a copy to avoid modifying original data
    plot_data = data.copy()

    # Sort data by x-axis for proper line rendering
    if sort_data:
        plot_data = plot_data.sort_values(by=x).reset_index(drop=True)

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Set seaborn style for clean appearance
    sns.set_style("whitegrid")

    # Plot data using seaborn lineplot
    sns.lineplot(
        data=plot_data,
        x=x,
        y=y,
        color=color,
        linewidth=linewidth,
        linestyle=linestyle,
        marker=marker,
        markersize=markersize,
        alpha=alpha,
        ax=ax,
        **kwargs,
    )

    # Labels and title
    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel or y)

    if title:
        ax.set_title(title)

    # Apply styling - make grid subtle
    ax.grid(True, alpha=0.3)

    # Reset seaborn style to avoid affecting other plots
    sns.set_style("ticks")

    # Layout
    plt.tight_layout()

    return fig


if __name__ == "__main__":
    # Sample data for testing - time series data
    np.random.seed(42)
    n_points = 50

    # Generate time series data with trend and noise
    time = np.arange(n_points)
    values = 10 + 0.5 * time + np.random.randn(n_points) * 2

    data = pd.DataFrame({"time": time, "value": values})

    # Create plot
    fig = create_plot(
        data, "time", "value", title="Basic Line Plot Example", xlabel="Time", ylabel="Value", marker="o", markersize=4
    )

    # Save for inspection - ALWAYS use 'plot.png' as filename
    plt.savefig("plot.png", dpi=300, bbox_inches="tight")
    print("Plot saved to plot.png")
