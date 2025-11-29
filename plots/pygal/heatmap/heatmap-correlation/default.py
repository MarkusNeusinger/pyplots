"""
heatmap-correlation: Correlation matrix heatmap
Library: pygal

IMPORTANT LIMITATION: pygal does not have native heatmap support. This implementation provides
an alternative visualization using a grouped bar chart where each bar represents a correlation value.
While this doesn't create a traditional heatmap grid, it does visualize the correlation data.

For true heatmap functionality, matplotlib, seaborn, plotly, or bokeh are recommended.
"""

import pygal
from pygal.style import Style
import pandas as pd
import numpy as np
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from pygal.graph.graph import Graph


def create_plot(
    data: pd.DataFrame,
    method: str = 'pearson',
    cmap: str = 'RdBu_r',
    vmin: float = -1,
    vmax: float = 1,
    show_values: bool = True,
    fmt: str = '.2f',
    title: Optional[str] = None,
    cbar_label: str = 'Correlation',
    **kwargs
) -> Graph:
    """
    Create a correlation matrix visualization using pygal bar chart.

    Since pygal doesn't support heatmaps natively, this creates a grouped bar chart
    where each group represents a variable and bars show correlations with other variables.

    Args:
        data: Input DataFrame with numeric columns
        method: Correlation method ('pearson', 'spearman', 'kendall')
        cmap: Color map (limited support - using custom pygal style)
        vmin: Minimum value for color scale
        vmax: Maximum value for color scale
        show_values: Display correlation values on bars
        fmt: Format string for values
        title: Optional plot title
        cbar_label: Label for correlation scale
        **kwargs: Additional parameters

    Returns:
        pygal Bar chart object

    Raises:
        ValueError: If data is empty or has no numeric columns

    Example:
        >>> data = pd.DataFrame({
        ...     'A': np.random.randn(50),
        ...     'B': np.random.randn(50),
        ...     'C': np.random.randn(50)
        ... })
        >>> chart = create_plot(data)
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    # Select only numeric columns
    numeric_data = data.select_dtypes(include=[np.number])
    if numeric_data.empty:
        raise ValueError("Data must contain at least one numeric column")

    # Calculate correlation matrix
    corr_matrix = numeric_data.corr(method=method)

    # Create custom style with diverging color scheme
    custom_style = Style(
        background='white',
        plot_background='white',
        foreground='#333',
        foreground_strong='#333',
        foreground_subtle='#666',
        opacity=0.8,
        transition='400ms',
        colors=('#d73027', '#f46d43', '#fdae61', '#fee08b',
                '#d9ef8b', '#a6d96a', '#66bd63', '#1a9850')
    )

    # Create a grouped bar chart to visualize correlations
    chart = pygal.Bar(
        width=1600,
        height=900,
        title=title or f'Correlation Matrix ({method.capitalize()})',
        x_title='Variables',
        y_title=cbar_label,
        style=custom_style,
        show_legend=True,
        x_label_rotation=45,
        print_values=show_values,
        print_values_position='top',
        print_zeroes=True,
        range=(vmin, vmax),
        show_x_guides=True,
        show_y_guides=True,
        value_formatter=lambda x: f'{x:{fmt}}' if x is not None else ''
    )

    # Add each variable's correlations as a series
    for i, var in enumerate(corr_matrix.columns):
        correlations = []
        for j, other_var in enumerate(corr_matrix.columns):
            corr_val = corr_matrix.loc[var, other_var]
            # Round to specified format
            correlations.append(float(f'{corr_val:{fmt}}'))

        chart.add(var, correlations)

    # Set x-axis labels
    chart.x_labels = list(corr_matrix.columns)

    return chart


if __name__ == '__main__':
    # Sample data for testing with known correlations
    np.random.seed(42)
    n_samples = 50

    # Create correlated data
    A = np.random.randn(n_samples)
    B = A + np.random.randn(n_samples) * 0.5  # Strong positive correlation with A
    C = -A + np.random.randn(n_samples) * 0.3  # Strong negative correlation with A
    D = np.random.randn(n_samples)  # Independent
    E = B * 0.5 + D * 0.5 + np.random.randn(n_samples) * 0.2  # Mixed correlations

    data = pd.DataFrame({
        'Variable_A': A,
        'Variable_B': B,
        'Variable_C': C,
        'Variable_D': D,
        'Variable_E': E
    })

    # Create plot
    chart = create_plot(
        data,
        method='pearson',
        title='Sample Correlation Matrix'
    )

    # Save - ALWAYS use 'plot.png'!
    try:
        # Try to render to PNG if cairosvg is available
        chart.render_to_png('plot.png')
        print("Plot saved to plot.png")
    except ImportError:
        # Fallback to SVG if PNG rendering not available
        chart.render_to_file('plot.svg')
        print("Plot saved to plot.svg (PNG rendering requires cairosvg)")
        print("To enable PNG output: pip install cairosvg")