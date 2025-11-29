"""
heatmap-correlation: Correlation matrix heatmap showing pairwise correlations between variables
Library: matplotlib
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.figure import Figure
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from matplotlib.figure import Figure


def create_plot(
    data: pd.DataFrame,
    cmap: str = 'RdBu_r',
    annot: bool = True,
    fmt: str = '.2f',
    vmin: float = -1.0,
    vmax: float = 1.0,
    cbar_label: str = 'Correlation',
    title: Optional[str] = None,
    **kwargs
) -> Figure:
    """
    Create a correlation matrix heatmap showing pairwise correlations between variables.

    Args:
        data: Input DataFrame with numeric columns to correlate
        cmap: Colormap for the heatmap (diverging)
        annot: Whether to show values in cells
        fmt: Format for cell annotations
        vmin: Minimum value for color scale
        vmax: Maximum value for color scale
        cbar_label: Label for color bar
        title: Optional plot title
        **kwargs: Additional parameters

    Returns:
        Matplotlib Figure object

    Raises:
        ValueError: If data is empty or has no numeric columns
        KeyError: If required columns not found

    Example:
        >>> data = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6], 'C': [7, 8, 9]})
        >>> fig = create_plot(data, cmap='coolwarm')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    # Select only numeric columns
    numeric_data = data.select_dtypes(include=[np.number])

    if numeric_data.empty:
        raise ValueError("Data must contain at least one numeric column")

    if len(numeric_data.columns) < 2:
        raise ValueError("Data must contain at least 2 numeric columns for correlation")

    # Calculate correlation matrix
    corr_matrix = numeric_data.corr()

    # Create figure
    fig, ax = plt.subplots(figsize=(16, 9))

    # Create heatmap using imshow
    im = ax.imshow(corr_matrix.values, cmap=cmap, vmin=vmin, vmax=vmax, aspect='auto')

    # Set ticks and labels
    ax.set_xticks(np.arange(len(corr_matrix.columns)))
    ax.set_yticks(np.arange(len(corr_matrix.columns)))
    ax.set_xticklabels(corr_matrix.columns)
    ax.set_yticklabels(corr_matrix.columns)

    # Rotate the tick labels for better readability
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    # Add text annotations if requested
    if annot:
        for i in range(len(corr_matrix.columns)):
            for j in range(len(corr_matrix.columns)):
                value = corr_matrix.iloc[i, j]
                text = ax.text(j, i, format(value, fmt),
                             ha="center", va="center",
                             color="white" if abs(value) > 0.7 else "black",
                             fontsize=10)

    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label(cbar_label, rotation=270, labelpad=15)

    # Styling
    ax.set_xlabel('')
    ax.set_ylabel('')

    # Add title if provided
    if title:
        ax.set_title(title, pad=20)

    # Add subtle grid for cell boundaries
    ax.set_xticks(np.arange(len(corr_matrix.columns) + 1) - 0.5, minor=True)
    ax.set_yticks(np.arange(len(corr_matrix.columns) + 1) - 0.5, minor=True)
    ax.grid(which="minor", color="gray", linestyle='-', linewidth=0.3, alpha=0.3)
    ax.tick_params(which="minor", size=0)

    # Layout
    plt.tight_layout()

    return fig


if __name__ == '__main__':
    # Sample data for testing
    import numpy as np

    np.random.seed(42)
    n = 100

    data = pd.DataFrame({
        'Temperature': np.random.normal(20, 5, n),
        'Humidity': np.random.normal(60, 10, n),
        'Pressure': np.random.normal(1013, 10, n),
        'Wind Speed': np.random.normal(10, 3, n),
        'Rainfall': np.random.normal(5, 2, n)
    })

    # Add correlations
    data['Humidity'] = 100 - data['Temperature'] * 1.5 + np.random.normal(0, 5, n)
    data['Rainfall'] = data['Humidity'] * 0.1 + np.random.normal(0, 1, n)
    data['Wind Speed'] = 15 - data['Pressure'] * 0.01 + np.random.normal(0, 2, n)

    # Create plot
    fig = create_plot(data)

    # Save - ALWAYS use 'plot.png'!
    plt.savefig('plot.png', dpi=300, bbox_inches='tight')
    print("Plot saved to plot.png")