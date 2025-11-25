"""
scatter-basic-001: Basic 2D Scatter Plot
Implementation for: matplotlib
Variant: default
Python: 3.10+
"""

import matplotlib.pyplot as plt
import pandas as pd
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from matplotlib.figure import Figure


def create_plot(
    data: pd.DataFrame,
    x: str,
    y: str,
    color: str | None = "steelblue",
    size: float = 50,
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
        color: Point color or column name for color mapping (default: "steelblue")
        size: Point size in pixels or column name for size mapping (default: 50)
        alpha: Transparency level from 0.0 to 1.0 (default: 0.8)
        title: Plot title (default: None)
        xlabel: Custom x-axis label (default: column name)
        ylabel: Custom y-axis label (default: column name)
        **kwargs: Additional parameters passed to ax.scatter()

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

    # Determine if color is a column or a direct value
    if color and color in data.columns:
        # Color mapping
        scatter = ax.scatter(
            data[x],
            data[y],
            c=data[color],
            s=size if isinstance(size, (int, float)) else data[size],
            alpha=alpha,
            cmap="viridis",
            edgecolors="none",
            **kwargs
        )
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label(color, fontsize=10)
    else:
        # Direct color
        scatter = ax.scatter(
            data[x],
            data[y],
            color=color or "steelblue",
            s=size if isinstance(size, (int, float)) else data[size],
            alpha=alpha,
            edgecolors="none",
            **kwargs
        )

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
    fig = create_plot(data, x="x", y="y", title="Basic Scatter Plot")

    # Save for inspection
    plt.savefig("test_output.png", dpi=150)
    print("Plot saved to test_output.png")
