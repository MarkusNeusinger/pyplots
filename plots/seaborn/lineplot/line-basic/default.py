"""
line-basic: Basic Line Plot
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
    x: str,
    y: str,
    figsize: tuple[float, float] = (16, 9),
    color: str = "steelblue",
    linewidth: float = 2.0,
    linestyle: str = "-",
    marker: str | None = None,
    markersize: float = 6,
    alpha: float = 1.0,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    **kwargs,
) -> "Figure":
    """
    Create a basic line plot for visualizing trends and changes in data.

    Args:
        data: Input DataFrame containing the data to plot
        x: Column name for x-axis values (numeric, datetime, or ordered categorical)
        y: Column name for y-axis values (numeric)
        figsize: Figure size as (width, height) tuple
        color: Line color
        linewidth: Width of the line
        linestyle: Line style ('-', '--', '-.', ':')
        marker: Marker style for data points (None for no markers)
        markersize: Size of markers if marker is specified
        alpha: Transparency level (0 to 1)
        title: Plot title (optional)
        xlabel: X-axis label (defaults to column name)
        ylabel: Y-axis label (defaults to column name)
        **kwargs: Additional parameters passed to seaborn lineplot

    Returns:
        Matplotlib Figure object

    Raises:
        ValueError: If data is empty or y column is not numeric
        KeyError: If required columns are not found in data

    Example:
        >>> data = pd.DataFrame({'time': [1, 2, 3, 4, 5], 'value': [2, 4, 3, 5, 6]})
        >>> fig = create_plot(data, 'time', 'value')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    for col in [x, y]:
        if col not in data.columns:
            available = ", ".join(data.columns)
            raise KeyError(f"Column '{col}' not found. Available: {available}")

    if not pd.api.types.is_numeric_dtype(data[y]):
        raise ValueError(f"Column '{y}' must be numeric, got {data[y].dtype}")

    # Sort data by x-axis for proper line rendering
    plot_data = data.sort_values(by=x).copy()

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

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

    # Labels
    ax.set_xlabel(xlabel if xlabel is not None else x, fontsize=12)
    ax.set_ylabel(ylabel if ylabel is not None else y, fontsize=12)

    # Title
    if title is not None:
        ax.set_title(title, fontsize=14, fontweight="bold")

    # Grid
    ax.grid(True, alpha=0.3)

    # Layout
    fig.tight_layout()

    return fig


if __name__ == "__main__":
    # Sample data for testing
    sample_data = pd.DataFrame(
        {"time": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "value": [2.3, 4.1, 3.5, 5.2, 6.1, 5.8, 7.2, 8.0, 7.5, 9.3]}
    )

    # Create plot
    fig = create_plot(
        sample_data,
        "time",
        "value",
        color="steelblue",
        linewidth=2.5,
        marker="o",
        markersize=8,
        title="Basic Line Plot Example",
        xlabel="Time (s)",
        ylabel="Value",
    )

    # Save
    plt.savefig("plot.png", dpi=300, bbox_inches="tight")
    print("Plot saved to plot.png")
