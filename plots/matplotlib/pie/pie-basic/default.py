"""
pie-basic: Basic Pie Chart
Library: matplotlib
"""

from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import pandas as pd


if TYPE_CHECKING:
    from matplotlib.figure import Figure


# PyPlots.ai color palette
PYPLOTS_COLORS = [
    "#306998",  # Python Blue
    "#FFD43B",  # Python Yellow
    "#DC2626",  # Signal Red
    "#059669",  # Teal Green
    "#8B5CF6",  # Violet
    "#F97316",  # Orange
]


def create_plot(
    data: pd.DataFrame,
    category: str,
    value: str,
    figsize: tuple[float, float] = (10, 8),
    title: str | None = None,
    colors: list[str] | None = None,
    startangle: float = 90,
    autopct: str = "%1.1f%%",
    explode: list[float] | None = None,
    shadow: bool = False,
    labels: list[str] | None = None,
    legend: bool = True,
    legend_loc: str = "best",
    **kwargs,
) -> "Figure":
    """
    Create a basic pie chart showing proportions of categorical data.

    Args:
        data: Input DataFrame containing category and value columns.
        category: Column name for category labels.
        value: Column name for numeric values.
        figsize: Figure size as (width, height). Defaults to (10, 8).
        title: Plot title. Defaults to None.
        colors: Custom color palette for slices. Defaults to PyPlots palette.
        startangle: Starting angle for first slice in degrees. Defaults to 90.
        autopct: Format string for percentage labels. Defaults to '%1.1f%%'.
        explode: Offset distances for each slice. Defaults to None.
        shadow: Add shadow effect for 3D appearance. Defaults to False.
        labels: Custom labels for slices. Defaults to category values.
        legend: Display legend. Defaults to True.
        legend_loc: Legend location. Defaults to 'best'.
        **kwargs: Additional parameters passed to ax.pie().

    Returns:
        Matplotlib Figure object.

    Raises:
        ValueError: If data is empty or values contain negatives or sum to zero.
        KeyError: If required columns are not found in data.

    Example:
        >>> data = pd.DataFrame({
        ...     'category': ['A', 'B', 'C'],
        ...     'value': [30, 50, 20]
        ... })
        >>> fig = create_plot(data, 'category', 'value', title='Distribution')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    for col in [category, value]:
        if col not in data.columns:
            available = ", ".join(data.columns)
            raise KeyError(f"Column '{col}' not found. Available: {available}")

    values = data[value]
    if (values < 0).any():
        raise ValueError("Values cannot be negative for pie charts")

    if values.sum() == 0:
        raise ValueError("Values cannot all be zero")

    # Prepare data
    categories = data[category].tolist()
    pie_values = values.tolist()
    slice_labels = labels if labels is not None else categories

    # Use PyPlots colors if not provided
    if colors is None:
        n_slices = len(pie_values)
        colors = (PYPLOTS_COLORS * ((n_slices // len(PYPLOTS_COLORS)) + 1))[:n_slices]

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Configure text properties for style guide compliance
    textprops = {"fontsize": 14, "fontfamily": ["Inter", "DejaVu Sans", "Arial", "Helvetica", "sans-serif"]}

    # Plot pie chart
    wedges, texts, autotexts = ax.pie(
        pie_values,
        labels=slice_labels if not legend else None,
        colors=colors,
        startangle=startangle,
        autopct=autopct,
        explode=explode,
        shadow=shadow,
        textprops=textprops,
        **kwargs,
    )

    # Style percentage labels
    for autotext in autotexts:
        autotext.set_fontsize(14)
        autotext.set_fontweight("bold")

    # Ensure circular shape (equal aspect ratio)
    ax.set_aspect("equal")

    # Add title if provided
    if title:
        ax.set_title(
            title,
            fontsize=20,
            fontweight="semibold",
            fontfamily=["Inter", "DejaVu Sans", "Arial", "Helvetica", "sans-serif"],
            pad=20,
        )

    # Add legend if requested
    if legend:
        ax.legend(
            wedges,
            slice_labels,
            loc=legend_loc,
            fontsize=16,
            frameon=True,
            facecolor="white",
            edgecolor="black",
            framealpha=1.0,
        )

    # Tight layout
    plt.tight_layout()

    return fig


if __name__ == "__main__":
    # Sample data for testing
    sample_data = pd.DataFrame(
        {"category": ["Product A", "Product B", "Product C", "Product D", "Other"], "value": [35, 25, 20, 15, 5]}
    )

    # Create plot
    fig = create_plot(sample_data, "category", "value", title="Market Share Distribution")

    # Save - ALWAYS use 'plot.png'!
    plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
    print("Plot saved to plot.png")
