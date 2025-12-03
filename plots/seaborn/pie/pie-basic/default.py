"""
pie-basic: Basic Pie Chart
Library: seaborn

Note: Seaborn does not have a native pie chart function. This implementation uses
matplotlib's pie chart with seaborn's styling context for consistent aesthetics.
"""

from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


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
    Create a basic pie chart visualizing proportions of categorical data.

    A fundamental pie chart where each slice represents a category's share of the
    whole, ideal for showing composition and distribution across a small number
    of categories.

    Note: Seaborn does not have a native pie chart function. This implementation
    uses matplotlib's pie chart with seaborn's styling context.

    Args:
        data: Input DataFrame containing category and value columns
        category: Column name for category labels
        value: Column name for numeric values (proportions)
        figsize: Figure size as (width, height) in inches
        title: Plot title (optional)
        colors: Custom color palette for slices (uses PyPlots.ai palette if None)
        startangle: Starting angle for first slice in degrees from positive x-axis
        autopct: Format string for percentage labels
        explode: Offset distances for each slice (0-0.1 typical)
        shadow: Add shadow effect for 3D appearance
        labels: Custom labels (defaults to category names if None)
        legend: Whether to display legend
        legend_loc: Legend location
        **kwargs: Additional parameters passed to ax.pie()

    Returns:
        Matplotlib Figure object

    Raises:
        ValueError: If data is empty or contains negative values
        KeyError: If required columns not found in data

    Example:
        >>> data = pd.DataFrame({
        ...     'category': ['Product A', 'Product B', 'Product C'],
        ...     'value': [35, 40, 25]
        ... })
        >>> fig = create_plot(data, 'category', 'value', title='Market Share')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    for col in [category, value]:
        if col not in data.columns:
            available = ", ".join(data.columns)
            raise KeyError(f"Column '{col}' not found. Available: {available}")

    # Extract values and validate
    values = data[value].values
    categories = data[category].values

    if (values < 0).any():
        raise ValueError("Pie chart values cannot be negative")

    if values.sum() == 0:
        raise ValueError("Sum of values cannot be zero")

    # Set seaborn style context for consistent aesthetics
    sns.set_theme(style="white")

    # Create figure with equal aspect ratio to prevent elliptical distortion
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_aspect("equal")

    # Determine colors
    if colors is None:
        # Extend palette if needed for more categories
        n_categories = len(categories)
        if n_categories <= len(PYPLOTS_COLORS):
            pie_colors = PYPLOTS_COLORS[:n_categories]
        else:
            # Use seaborn color palette for many categories
            pie_colors = sns.color_palette("husl", n_categories)
    else:
        pie_colors = colors

    # Determine labels
    pie_labels = labels if labels is not None else categories

    # Create pie chart
    wedges, texts, autotexts = ax.pie(
        values,
        labels=pie_labels if not legend else None,
        autopct=autopct,
        startangle=startangle,
        explode=explode,
        shadow=shadow,
        colors=pie_colors,
        wedgeprops={"edgecolor": "white", "linewidth": 1.5},
        textprops={"fontsize": 12},
        pctdistance=0.75,
        **kwargs,
    )

    # Style percentage labels
    for autotext in autotexts:
        autotext.set_fontsize(11)
        autotext.set_fontweight("bold")
        autotext.set_color("white")

    # Add legend if requested
    if legend:
        ax.legend(
            wedges,
            pie_labels,
            title=category,
            loc=legend_loc,
            bbox_to_anchor=(1, 0, 0.5, 1),
            frameon=True,
            facecolor="white",
            edgecolor="gray",
            fontsize=11,
        )

    # Set title if provided
    if title is not None:
        ax.set_title(title, fontsize=16, fontweight="semibold", pad=20)

    # Layout adjustment
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
    plt.savefig("plot.png", dpi=300, bbox_inches="tight")
    print("Plot saved to plot.png")
