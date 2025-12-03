"""
pie-basic: Basic Pie Chart
Library: plotnine

A fundamental pie chart that visualizes proportions and percentages of categorical data
as slices of a circular chart.

Note: plotnine (ggplot2 for Python) does not support coord_polar() as of version 0.15.x,
which is required for true pie charts in the grammar of graphics. This implementation
uses matplotlib directly (plotnine's underlying engine) to create the pie chart while
maintaining a compatible interface and following PyPlots.ai style guidelines.
"""

from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import pandas as pd


if TYPE_CHECKING:
    from matplotlib.figure import Figure

# PyPlots.ai color palette
PYPLOTS_COLORS = [
    "#306998",  # Python Blue (Primary)
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
    Create a basic pie chart.

    Note: plotnine does not support polar coordinates (coord_polar), so this
    implementation uses matplotlib directly while maintaining a compatible interface.

    Args:
        data: Input DataFrame containing category and value columns
        category: Column name for category names (slice labels)
        value: Column name for numeric values (slice proportions)
        figsize: Figure size as (width, height)
        title: Plot title (optional)
        colors: Custom color palette for slices (defaults to PyPlots palette)
        startangle: Starting angle for first slice in degrees (default 90 = top)
        autopct: Format string for percentage labels
        explode: Offset distances for each slice (0-0.1 typical)
        shadow: Add shadow effect for 3D appearance
        labels: Custom labels (defaults to category names)
        legend: Display legend
        legend_loc: Legend location ('best', 'upper right', 'lower left', etc.)
        **kwargs: Additional parameters passed to matplotlib pie()

    Returns:
        matplotlib Figure object

    Raises:
        ValueError: If data is empty or values contain negative numbers
        KeyError: If required columns are not found in data

    Example:
        >>> data = pd.DataFrame({
        ...     'category': ['A', 'B', 'C', 'D'],
        ...     'value': [35, 25, 20, 20]
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

    # Validate non-negative values
    if (data[value] < 0).any():
        raise ValueError("Pie chart values must be non-negative")

    # Handle case where all values sum to zero
    total = data[value].sum()
    if total == 0:
        raise ValueError("Total of values cannot be zero")

    # Prepare data
    values = data[value].tolist()
    category_labels = labels if labels is not None else data[category].astype(str).tolist()

    # Validate labels length if custom labels provided
    if labels is not None and len(labels) != len(data):
        raise ValueError(f"Labels length ({len(labels)}) must match data length ({len(data)})")

    # Set up colors
    n_categories = len(data)
    if colors is None:
        # Extend palette if more categories than colors
        plot_colors = (PYPLOTS_COLORS * ((n_categories // len(PYPLOTS_COLORS)) + 1))[:n_categories]
    else:
        if len(colors) < n_categories:
            plot_colors = (colors * ((n_categories // len(colors)) + 1))[:n_categories]
        else:
            plot_colors = colors[:n_categories]

    # Create figure with white background
    fig, ax = plt.subplots(figsize=figsize, facecolor="white")
    ax.set_facecolor("white")

    # Configure explode
    pie_explode = explode if explode is not None else None
    if pie_explode is not None and len(pie_explode) != n_categories:
        raise ValueError(f"Explode length ({len(pie_explode)}) must match data length ({n_categories})")

    # Configure text properties for percentage labels
    textprops = {"fontsize": 14, "fontweight": "bold", "color": "white"}

    # Create pie chart - hide labels on the pie itself since we'll use legend
    wedges, texts, autotexts = ax.pie(
        values,
        labels=None if legend else category_labels,  # Labels on pie only if no legend
        autopct=autopct if autopct else None,
        startangle=startangle,
        colors=plot_colors,
        explode=pie_explode,
        shadow=shadow,
        textprops=textprops,
        wedgeprops={"linewidth": 1, "edgecolor": "white"},
        **kwargs,
    )

    # Style the percentage labels with better contrast
    for autotext in autotexts:
        autotext.set_fontsize(14)
        autotext.set_fontweight("bold")
        # Use white for darker colors, dark for lighter colors
        autotext.set_color("white")

    # Add legend if requested
    if legend:
        ax.legend(
            wedges,
            category_labels,
            title=category,
            loc=legend_loc,
            fontsize=14,
            title_fontsize=16,
            frameon=True,
            facecolor="white",
            edgecolor="gray",
            framealpha=1.0,
        )

    # Add title if provided
    if title:
        ax.set_title(title, fontsize=20, fontweight="semibold", pad=20)

    # Ensure equal aspect ratio for circular pie
    ax.set_aspect("equal")

    # Adjust layout
    fig.tight_layout()

    return fig


if __name__ == "__main__":
    # Sample data for testing
    sample_data = pd.DataFrame(
        {"category": ["Product A", "Product B", "Product C", "Product D", "Other"], "value": [35, 25, 20, 15, 5]}
    )

    # Create plot
    fig = create_plot(sample_data, "category", "value", title="Market Share Distribution")

    # Save
    fig.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
    print("Plot saved to plot.png")
