"""
scatter-basic-001: Basic 2D Scatter Plot
Implementation for: seaborn
Variant: default
Python: 3.10+
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from matplotlib.figure import Figure


def create_plot(
    data: pd.DataFrame,
    x: str,
    y: str,
    color: str | None = None,
    size: str | int | float | None = None,
    alpha: float = 0.8,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    **kwargs
) -> "Figure":
    """
    Create a simple scatter plot showing the relationship between two numeric variables.

    Args:
        data: Input DataFrame with required columns
        x: Column name for x-axis values
        y: Column name for y-axis values
        color: Column name for color mapping or color value (default: None)
        size: Column name for size mapping or numeric size value (default: None)
        alpha: Transparency level from 0.0 to 1.0 (default: 0.8)
        title: Plot title (default: None)
        xlabel: Custom x-axis label (default: column name)
        ylabel: Custom y-axis label (default: column name)
        **kwargs: Additional parameters passed to sns.scatterplot()

    Returns:
        Matplotlib Figure object

    Raises:
        ValueError: If data is empty
        KeyError: If required columns not found in data

    Example:
        >>> data = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
        >>> fig = create_plot(data, x="x", y="y")
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    # Check required columns
    for col in [x, y]:
        if col not in data.columns:
            available = ", ".join(data.columns)
            raise KeyError(f"Column '{col}' not found. Available columns: {available}")

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Prepare scatterplot arguments
    plot_kwargs = {
        "data": data,
        "x": x,
        "y": y,
        "alpha": alpha,
        "ax": ax,
        **kwargs
    }

    # Add color mapping if specified
    if color:
        if color in data.columns:
            plot_kwargs["hue"] = color
            plot_kwargs["palette"] = "viridis"
        else:
            plot_kwargs["color"] = color

    # Add size mapping if specified
    if size:
        if isinstance(size, str) and size in data.columns:
            plot_kwargs["size"] = size
        elif isinstance(size, (int, float)):
            plot_kwargs["s"] = size
        else:
            plot_kwargs["s"] = 50

    # Default size if not specified
    if "s" not in plot_kwargs and "size" not in plot_kwargs:
        plot_kwargs["s"] = 50

    # Create scatter plot
    sns.scatterplot(**plot_kwargs)

    # Apply styling
    ax.grid(True, alpha=0.3, linestyle="--")

    # Labels and title
    ax.set_xlabel(xlabel or x, fontsize=11)
    ax.set_ylabel(ylabel or y, fontsize=11)

    if title:
        ax.set_title(title, fontsize=14, fontweight="bold")

    # Layout
    plt.tight_layout()

    return fig


if __name__ == "__main__":
    # Sample data for testing
    import numpy as np

    np.random.seed(42)
    data = pd.DataFrame({
        "x": np.random.randn(100) * 10 + 50,
        "y": np.random.randn(100) * 10 + 50,
        "category": np.random.choice(["A", "B", "C"], 100)
    })

    # Create plot
    fig = create_plot(data, x="x", y="y", title="Basic Scatter Plot (Seaborn)")

    # Save for inspection
    plt.savefig("test_output_seaborn.png", dpi=150)
    print("Plot saved to test_output_seaborn.png")
