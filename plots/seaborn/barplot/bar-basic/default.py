"""
bar-basic: Basic Bar Chart
Implementation for: seaborn
Variant: default
Python: 3.10+
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from matplotlib.figure import Figure


def create_plot(
    data: pd.DataFrame,
    x: str,
    y: str,
    color: Optional[str] = None,
    alpha: float = 0.8,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    figsize: tuple[float, float] = (10, 6),
    **kwargs
) -> "Figure":
    """
    Create a basic bar chart showing values for different categories using seaborn.

    Args:
        data: Input DataFrame with required columns
        x: Column name for category labels (x-axis)
        y: Column name for numeric values (y-axis)
        color: Bar color or column name for color mapping (default: "steelblue")
        alpha: Transparency level 0.0-1.0 (default: 0.8)
        title: Plot title (default: None)
        xlabel: Custom x-axis label (default: column name)
        ylabel: Custom y-axis label (default: column name)
        figsize: Figure size as (width, height) (default: (10, 6))
        **kwargs: Additional parameters passed to sns.barplot()

    Returns:
        Matplotlib Figure object

    Raises:
        ValueError: If data is empty
        KeyError: If required columns not found

    Example:
        >>> data = pd.DataFrame({'Category': ['A', 'B', 'C'], 'Value': [10, 20, 15]})
        >>> fig = create_plot(data, x='Category', y='Value')
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

    # Prepare parameters for seaborn barplot
    plot_kwargs = kwargs.copy()

    # Determine if color is a column or a direct value
    if color and color in data.columns:
        # Color mapping from column
        sns.barplot(
            data=data,
            x=x,
            y=y,
            hue=color,
            ax=ax,
            alpha=alpha,
            **plot_kwargs
        )
        # Legend is automatically created by seaborn with hue
        ax.legend(title=color, loc="best")
    else:
        # Direct color value
        bar_color = color or "steelblue"
        sns.barplot(
            data=data,
            x=x,
            y=y,
            color=bar_color,
            ax=ax,
            alpha=alpha,
            **plot_kwargs
        )

    # Apply styling
    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel or y)
    ax.grid(True, axis="y", alpha=0.3, linestyle="--")

    # Title
    if title:
        ax.set_title(title, fontsize=14, fontweight="bold")

    # Tight layout to avoid label clipping
    plt.tight_layout()

    return fig


if __name__ == "__main__":
    # Sample data for testing
    data = pd.DataFrame({
        "Category": ["Product A", "Product B", "Product C", "Product D", "Product E"],
        "Sales": [23000, 17500, 21000, 19500, 25000]
    })

    # Create plot
    fig = create_plot(data, x="Category", y="Sales", title="Product Sales Comparison")

    # Save for inspection
    plt.savefig("test_output_seaborn.png", dpi=150, bbox_inches="tight")
    print("Plot saved to test_output_seaborn.png")
    plt.show()
