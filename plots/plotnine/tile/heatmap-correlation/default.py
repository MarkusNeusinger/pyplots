"""
heatmap-correlation: Correlation Matrix Heatmap
Library: plotnine
"""

import pandas as pd
import numpy as np
from plotnine import (
    ggplot, aes,
    geom_tile, geom_text,
    labs, theme, theme_minimal, element_text,
    scale_fill_gradient2
)
from typing import Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from plotnine import ggplot as PlotNineGGPlot


def create_plot(
    data: pd.DataFrame,
    variables: Optional[list] = None,
    title: str = "Correlation Matrix",
    figsize: Tuple[float, float] = (10, 8),
    cmap: str = "RdBu_r",
    vmin: float = -1,
    vmax: float = 1,
    annot: bool = True,
    fmt: str = ".2f",
    cbar: bool = True,
    **kwargs
) -> 'PlotNineGGPlot':
    """
    Create a correlation matrix heatmap showing pairwise correlations.

    Args:
        data: Input DataFrame with numeric columns
        variables: List of column names to include (None for all numeric)
        title: Title for the plot
        figsize: Figure size as (width, height) tuple
        cmap: Color scheme name (ignored, uses RdBu gradient)
        vmin: Minimum value for color scale
        vmax: Maximum value for color scale
        annot: Show values in cells
        fmt: Format string for annotations
        cbar: Show color bar (always True in plotnine)
        **kwargs: Additional parameters

    Returns:
        plotnine ggplot object

    Raises:
        ValueError: If data is empty or no numeric columns
        KeyError: If specified variables not found

    Example:
        >>> data = pd.DataFrame({'A': [1, 2, 3], 'B': [2, 4, 6], 'C': [3, 2, 1]})
        >>> plot = create_plot(data)
        >>> plot.save('plot.png')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    # Select variables
    if variables is None:
        # Use all numeric columns
        numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
        if not numeric_cols:
            raise ValueError("No numeric columns found in data")
        variables = numeric_cols
    else:
        # Validate specified variables
        for var in variables:
            if var not in data.columns:
                available = ", ".join(data.columns)
                raise KeyError(f"Column '{var}' not found. Available: {available}")

    # Calculate correlation matrix
    corr_matrix = data[variables].corr()

    # Prepare data for heatmap (long format)
    corr_long = corr_matrix.reset_index().melt(
        id_vars='index',
        var_name='variable',
        value_name='correlation'
    )
    corr_long.columns = ['var1', 'var2', 'correlation']

    # Create categorical ordering for proper axis display
    var_order = variables
    corr_long['var1'] = pd.Categorical(corr_long['var1'], categories=var_order, ordered=True)
    corr_long['var2'] = pd.Categorical(corr_long['var2'], categories=var_order[::-1], ordered=True)

    # Format correlation values for display
    if annot:
        corr_long['label'] = corr_long['correlation'].apply(lambda x: f"{x:{fmt}}")

    # Create heatmap
    plot = (
        ggplot(corr_long, aes(x='var1', y='var2', fill='correlation'))
        + geom_tile(color='white', size=0.5)
        + scale_fill_gradient2(
            low='#053061',  # Dark blue for -1
            mid='white',     # White for 0
            high='#67001f',  # Dark red for 1
            midpoint=0,
            limits=(vmin, vmax)
        )
        + labs(
            x='',
            y='',
            title=title,
            fill='Correlation'
        )
        + theme_minimal()
        + theme(
            figure_size=figsize,
            axis_text_x=element_text(angle=45, hjust=1),
            axis_text_y=element_text(hjust=1),
            panel_grid=None,  # Remove grid for cleaner look
            plot_title=element_text(size=14, weight='bold')
        )
    )

    # Add text annotations if requested
    if annot:
        plot = plot + geom_text(
            aes(label='label'),
            size=8,
            color='black'
        )

    return plot


if __name__ == '__main__':
    # Sample data for testing - create correlated variables
    np.random.seed(42)
    n = 100

    # Create correlated variables
    base = np.random.randn(n)
    data = pd.DataFrame({
        'Temperature': base + np.random.randn(n) * 0.5,
        'Sales': base * 2 + np.random.randn(n) * 0.8,
        'Marketing': base * 1.5 + np.random.randn(n) * 0.6,
        'Profit': base * 3 + np.random.randn(n) * 0.7,
        'Costs': -base * 1.2 + np.random.randn(n) * 0.4,
        'Quality': base * 0.8 + np.random.randn(n) * 0.9
    })

    # Create plot
    plot = create_plot(
        data,
        title="Variable Correlation Matrix"
    )

    # Save - ALWAYS use 'plot.png'!
    plot.save('plot.png', dpi=300)
    print("Plot saved to plot.png")