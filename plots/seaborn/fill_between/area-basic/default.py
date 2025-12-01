"""
area-basic: Basic Area Chart
Implementation for: seaborn
Variant: default
Python: 3.10+

Note: Seaborn does not have a native area chart function. This implementation
uses matplotlib's fill_between with seaborn's styling for a consistent look.
"""

from typing import TYPE_CHECKING, Optional

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


if TYPE_CHECKING:
    from matplotlib.figure import Figure


def create_plot(
    data: pd.DataFrame,
    x: str,
    y: str,
    color: str = "steelblue",
    alpha: float = 0.4,
    line_alpha: float = 1.0,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    figsize: tuple[float, float] = (16, 9),
    **kwargs,
) -> "Figure":
    """
    Create a basic filled area chart using seaborn styling with matplotlib.

    Args:
        data: Input DataFrame with required columns
        x: Column name for x-axis values (sequential: datetime, numeric, or categorical)
        y: Column name for y-axis values (numeric)
        color: Fill and line color (default: "steelblue")
        alpha: Transparency level for area fill 0.0-1.0 (default: 0.4)
        line_alpha: Transparency level for edge line 0.0-1.0 (default: 1.0)
        title: Plot title (default: None)
        xlabel: Custom x-axis label (default: column name)
        ylabel: Custom y-axis label (default: column name)
        figsize: Figure size as (width, height) (default: (16, 9))
        **kwargs: Additional parameters passed to fill_between()

    Returns:
        Matplotlib Figure object

    Raises:
        ValueError: If data is empty
        KeyError: If required columns not found

    Example:
        >>> data = pd.DataFrame({'Month': range(1, 13), 'Revenue': [10, 15, 13, 17, 20, 25, 22, 26, 24, 28, 30, 35]})
        >>> fig = create_plot(data, x='Month', y='Revenue')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    # Check required columns
    for col in [x, y]:
        if col not in data.columns:
            available = ", ".join(data.columns)
            raise KeyError(f"Column '{col}' not found. Available: {available}")

    # Set seaborn style for consistent appearance
    sns.set_theme(style="whitegrid")

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Get x and y values
    x_vals = data[x]
    y_vals = data[y]

    # Plot the edge line first
    ax.plot(x_vals, y_vals, color=color, alpha=line_alpha, linewidth=2)

    # Fill the area between the line and baseline (y=0)
    ax.fill_between(x_vals, y_vals, alpha=alpha, color=color, **kwargs)

    # Apply styling
    ax.set_xlabel(xlabel or x, fontsize=12)
    ax.set_ylabel(ylabel or y, fontsize=12)
    ax.grid(True, alpha=0.3, linestyle="--")

    # Set y-axis to start from 0 for area charts (standard practice)
    y_min = min(0, y_vals.min())
    y_max = y_vals.max()
    y_padding = (y_max - y_min) * 0.05
    ax.set_ylim(y_min, y_max + y_padding)

    # Title
    if title:
        ax.set_title(title, fontsize=14, fontweight="bold")

    # Tight layout to avoid label clipping
    plt.tight_layout()

    return fig


if __name__ == "__main__":
    # Sample data for testing - monthly revenue over a year
    data = pd.DataFrame(
        {
            "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            "Revenue": [12000, 15000, 13500, 17000, 20000, 25000, 22000, 26000, 24000, 28000, 30000, 35000],
        }
    )

    # Create plot
    fig = create_plot(data, x="Month", y="Revenue", title="Monthly Revenue Growth", ylabel="Revenue ($)")

    # Save for inspection
    plt.savefig("plot.png", dpi=300, bbox_inches="tight")
    print("Plot saved to plot.png")
