"""
pie-basic-labeled: Basic Pie Chart with Labels
Implementation for: seaborn
Variant: default
Python: 3.10+

Note: Seaborn does not have a native pie chart function.
This implementation uses matplotlib.pyplot.pie with seaborn styling for consistency.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from matplotlib.figure import Figure


def create_plot(
    data: pd.DataFrame,
    values: str,
    labels: str,
    colors: Optional[list | str] = None,
    autopct: str = "%1.1f%%",
    startangle: float = 0,
    explode: Optional[list] = None,
    title: Optional[str] = None,
    figsize: tuple = (8, 8),
    palette: str = "Set2",
    **kwargs
) -> "Figure":
    """
    Create a pie chart showing the composition of categorical data using seaborn styling.

    Args:
        data: Input DataFrame containing the data
        values: Column name containing numeric values for each slice
        labels: Column name containing category labels for each slice
        colors: List of colors for slices or column name for color mapping.
            If None, uses seaborn palette (default: None)
        autopct: String format for displaying percentages (default: "%1.1f%%")
        startangle: Starting angle for the pie chart in degrees (default: 0)
        explode: List of offset values for slices to separate them.
            Should have same length as values (default: None)
        title: Plot title (default: None)
        figsize: Figure size as tuple (width, height) in inches (default: (8, 8))
        palette: Seaborn color palette to use (default: "Set2")
        **kwargs: Additional parameters passed to plt.pie()

    Returns:
        Matplotlib Figure object

    Raises:
        ValueError: If data is empty or values/labels columns not found
        KeyError: If required columns are missing from data
        TypeError: If values column contains non-numeric data

    Example:
        >>> data = pd.DataFrame({
        ...     'category': ['A', 'B', 'C'],
        ...     'value': [30, 25, 45]
        ... })
        >>> fig = create_plot(data, values='value', labels='category')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    # Check required columns
    for col in [values, labels]:
        if col not in data.columns:
            available = ", ".join(data.columns)
            raise KeyError(f"Column '{col}' not found. Available columns: {available}")

    # Validate that values column contains numeric data
    try:
        numeric_values = pd.to_numeric(data[values], errors='coerce')
        if numeric_values.isna().all():
            raise TypeError(f"Column '{values}' contains non-numeric data")
    except Exception as e:
        raise TypeError(f"Column '{values}' must contain numeric data: {e}")

    # Extract data
    pie_values = data[values].values
    pie_labels = data[labels].values

    # Set seaborn style for consistent look
    sns.set_style("whitegrid")

    # Create figure with specified size
    fig, ax = plt.subplots(figsize=figsize)

    # Prepare colors
    if colors is not None:
        if isinstance(colors, str) and colors in data.columns:
            # Color mapping from column
            slice_colors = data[colors].values
        else:
            # Direct color list
            slice_colors = colors
    else:
        # Use seaborn palette for colorblind-safe colors
        slice_colors = sns.color_palette(palette, n_colors=len(pie_values))

    # Create pie chart
    wedges, texts, autotexts = ax.pie(
        pie_values,
        labels=pie_labels,
        colors=slice_colors,
        autopct=autopct,
        startangle=startangle,
        explode=explode,
        **kwargs
    )

    # Styling for readability
    for text in texts:
        text.set_fontsize(10)
        text.set_weight('normal')

    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(9)
        autotext.set_weight('bold')

    # Add title if provided
    if title:
        ax.set_title(title, fontsize=14, weight='bold', pad=20)

    plt.tight_layout()
    return fig


if __name__ == '__main__':
    # Sample data for testing
    data = pd.DataFrame({
        'category': ['Product A', 'Product B', 'Product C', 'Product D'],
        'sales': [35, 25, 20, 20]
    })

    # Create plot
    fig = create_plot(
        data,
        values='sales',
        labels='category',
        title='Sales Distribution by Product'
    )

    # Save for inspection
    plt.savefig('test_output_seaborn.png', dpi=150, bbox_inches='tight')
    print("Plot saved to test_output_seaborn.png")
