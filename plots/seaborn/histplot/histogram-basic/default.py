"""
histogram-basic: Basic Histogram
Implementation for: seaborn
Variant: default
Python: 3.10+
"""

from typing import TYPE_CHECKING, Optional

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

if TYPE_CHECKING:
    from matplotlib.figure import Figure


def create_plot(
    data: pd.DataFrame,
    column: str,
    bins: int = 30,
    color: str = "steelblue",
    alpha: float = 0.8,
    edgecolor: str = "black",
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    figsize: tuple[float, float] = (16, 9),
    **kwargs
) -> "Figure":
    """
    Create a basic histogram showing the distribution of numeric data using seaborn.

    Args:
        data: Input DataFrame with required column
        column: Column name for numeric values to visualize
        bins: Number of bins for histogram (default: 30)
        color: Bar color (default: "steelblue")
        alpha: Transparency level 0.0-1.0 (default: 0.8)
        edgecolor: Border color for bins (default: "black")
        title: Plot title (default: None)
        xlabel: Custom x-axis label (default: column name)
        ylabel: Custom y-axis label (default: "Frequency")
        figsize: Figure size as (width, height) (default: (16, 9))
        **kwargs: Additional parameters passed to sns.histplot()

    Returns:
        Matplotlib Figure object

    Raises:
        ValueError: If data is empty
        KeyError: If required column not found
        ValueError: If column contains no numeric values

    Example:
        >>> data = pd.DataFrame({'Values': [1.5, 2.1, 2.3, 3.2, 3.5, 4.1, 4.5]})
        >>> fig = create_plot(data, column='Values', bins=20)
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    # Check required column
    if column not in data.columns:
        available = ", ".join(data.columns)
        raise KeyError(f"Column '{column}' not found. Available: {available}")

    # Check if column has numeric data
    if not pd.api.types.is_numeric_dtype(data[column]):
        raise ValueError(f"Column '{column}' must contain numeric values")

    # Remove NaN values for histogram
    values = data[column].dropna()

    if len(values) == 0:
        raise ValueError(f"Column '{column}' contains no valid numeric values")

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Create histogram using seaborn
    sns.histplot(
        data=data,
        x=column,
        bins=bins,
        color=color,
        alpha=alpha,
        edgecolor=edgecolor,
        ax=ax,
        **kwargs
    )

    # Apply styling
    ax.set_xlabel(xlabel or column)
    ax.set_ylabel(ylabel or "Frequency")
    ax.grid(True, axis="y", alpha=0.3, linestyle="--")

    # Title
    if title:
        ax.set_title(title, fontsize=14, fontweight="bold")

    # Tight layout to avoid label clipping
    plt.tight_layout()

    return fig


if __name__ == "__main__":
    # Sample data for testing
    import numpy as np
    np.random.seed(42)
    data = pd.DataFrame({
        "Values": np.random.normal(loc=100, scale=15, size=1000)
    })

    # Create plot
    fig = create_plot(
        data,
        column="Values",
        bins=40,
        title="Distribution of Values"
    )

    # Save for inspection
    plt.savefig("plot.png", dpi=300, bbox_inches="tight")
    print("Plot saved to plot.png")
    plt.show()
