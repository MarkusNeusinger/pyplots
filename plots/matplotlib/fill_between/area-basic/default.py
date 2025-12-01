"""
area-basic: Basic Area Chart
Implementation for: matplotlib
Variant: default
Python: 3.10+
"""

from typing import TYPE_CHECKING, Optional

import matplotlib.pyplot as plt
import pandas as pd


if TYPE_CHECKING:
    from matplotlib.figure import Figure


def create_plot(
    data: pd.DataFrame,
    x: str,
    y: str,
    color: str = "steelblue",
    alpha: float = 0.4,
    line_color: Optional[str] = None,
    line_width: float = 2.0,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    figsize: tuple[float, float] = (16, 9),
    **kwargs,
) -> "Figure":
    """
    Create a basic area chart showing a filled region between the x-axis and a line.

    Args:
        data: Input DataFrame with required columns
        x: Column name for x-axis values (continuous sequence)
        y: Column name for y-axis values (numeric values)
        color: Fill color for the area (default: "steelblue")
        alpha: Transparency level for the filled area 0.0-1.0 (default: 0.4)
        line_color: Color of the top edge line (default: same as fill color)
        line_width: Width of the top edge line (default: 2.0)
        title: Plot title (default: None)
        xlabel: Custom x-axis label (default: column name)
        ylabel: Custom y-axis label (default: column name)
        figsize: Figure size as (width, height) (default: (16, 9))
        **kwargs: Additional parameters passed to ax.fill_between()

    Returns:
        Matplotlib Figure object

    Raises:
        ValueError: If data is empty
        KeyError: If required columns not found

    Example:
        >>> data = pd.DataFrame({'Time': [1, 2, 3, 4, 5], 'Value': [10, 25, 15, 30, 20]})
        >>> fig = create_plot(data, x='Time', y='Value')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    # Check required columns
    for col in [x, y]:
        if col not in data.columns:
            available = ", ".join(data.columns)
            raise KeyError(f"Column '{col}' not found. Available: {available}")

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Get data values
    x_values = data[x]
    y_values = data[y]

    # Determine line color (default to fill color if not specified)
    edge_color = line_color if line_color else color

    # Plot the filled area
    ax.fill_between(x_values, y_values, alpha=alpha, color=color, **kwargs)

    # Plot the top edge line for clarity
    ax.plot(x_values, y_values, color=edge_color, linewidth=line_width)

    # Apply styling
    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel or y)
    ax.grid(True, alpha=0.3, linestyle="--")

    # Title
    if title:
        ax.set_title(title, fontsize=14, fontweight="bold")

    # Tight layout to avoid label clipping
    plt.tight_layout()

    return fig


if __name__ == "__main__":
    # Sample data for testing - simulating monthly website traffic
    data = pd.DataFrame(
        {
            "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            "Visitors": [12000, 15000, 18000, 22000, 25000, 28000, 32000, 30000, 27000, 24000, 20000, 18000],
        }
    )

    # For a proper area chart, we need numeric x values
    # Convert month names to numeric positions for continuous x-axis
    data["Month_Num"] = range(1, 13)

    # Create plot
    fig = create_plot(
        data, x="Month_Num", y="Visitors", title="Monthly Website Traffic", xlabel="Month", ylabel="Number of Visitors"
    )

    # Customize x-ticks to show month names
    ax = fig.axes[0]
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(data["Month"])

    # Save for inspection
    plt.savefig("plot.png", dpi=300, bbox_inches="tight")
    print("Plot saved to plot.png")
