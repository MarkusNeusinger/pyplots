"""
heatmap-correlation: Correlation Matrix Heatmap
Library: bokeh
"""

import numpy as np
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, LinearColorMapper, ColorBar, BasicTicker
from bokeh.models import Label
from bokeh.io import export_png
from bokeh.transform import transform
from bokeh.palettes import RdBu11
from typing import List, Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from bokeh.plotting import figure as FigureType


def create_plot(
    data: pd.DataFrame,
    columns: Optional[List[str]] = None,
    method: str = 'pearson',
    annot_format: str = '.2f',
    cmap: str = 'RdBu_r',
    vmin: float = -1,
    vmax: float = 1,
    center: float = 0,
    square: bool = True,
    linewidths: float = 0.5,
    linecolor: str = 'white',
    cbar_label: str = 'Correlation',
    title: Optional[str] = None,
    figsize: Tuple[int, int] = (10, 8),
    **kwargs
) -> 'FigureType':
    """
    Create a heatmap visualization showing pairwise correlations between multiple variables.

    Args:
        data: Input DataFrame
        columns: Specific columns to include in correlation. If None, use all numeric columns
        method: Correlation method ('pearson', 'spearman', 'kendall'). Default: 'pearson'
        annot_format: Format string for annotations. Default: '.2f'
        cmap: Colormap name. Default: 'RdBu_r' (diverging blue-white-red)
        vmin: Minimum value for color scale. Default: -1
        vmax: Maximum value for color scale. Default: 1
        center: Center value for diverging colormap. Default: 0
        square: Make cells square. Default: True
        linewidths: Width of lines between cells. Default: 0.5
        linecolor: Color of lines between cells. Default: 'white'
        cbar_label: Label for colorbar. Default: 'Correlation'
        title: Title for the plot. Default: None
        figsize: Figure size in inches. Default: (10, 8)
        **kwargs: Additional parameters

    Returns:
        bokeh Figure object

    Raises:
        ValueError: If data is empty
        KeyError: If specified columns not found

    Example:
        >>> data = pd.DataFrame({'A': [1, 2, 3], 'B': [2, 4, 6]})
        >>> fig = create_plot(data)
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    # Select columns for correlation
    if columns is not None:
        for col in columns:
            if col not in data.columns:
                available = ", ".join(data.columns)
                raise KeyError(f"Column '{col}' not found. Available: {available}")
        corr_data = data[columns]
    else:
        # Use all numeric columns
        corr_data = data.select_dtypes(include=[np.number])

    # Calculate correlation matrix
    corr_matrix = corr_data.corr(method=method)

    # Prepare data for bokeh
    var_names = list(corr_matrix.columns)
    n_vars = len(var_names)

    # Create x and y coordinates for rectangles
    x_coords = []
    y_coords = []
    colors = []
    values = []

    for i, row_name in enumerate(var_names):
        for j, col_name in enumerate(var_names):
            x_coords.append(col_name)
            y_coords.append(row_name)
            value = corr_matrix.iloc[i, j]
            values.append(value)

    # Create ColumnDataSource
    source = ColumnDataSource(data={
        'x': x_coords,
        'y': y_coords,
        'value': values,
        'formatted': [annot_format.format(v) for v in values]
    })

    # Convert figsize from inches to pixels (assuming 100 dpi for display)
    width_px = int(figsize[0] * 160)  # 16:9 aspect ratio adjustment
    height_px = int(figsize[1] * 100)

    # Create figure
    p = figure(
        width=width_px,
        height=height_px,
        title=title,
        x_range=var_names,
        y_range=list(reversed(var_names)),  # Reverse to match traditional matrix display
        toolbar_location="right",
        tools="hover,save,pan,box_zoom,reset,wheel_zoom"
    )

    # Create color mapper (using RdBu reversed palette)
    mapper = LinearColorMapper(
        palette=list(reversed(RdBu11)),
        low=vmin,
        high=vmax
    )

    # Add rectangles for heatmap
    p.rect(
        x='x',
        y='y',
        width=1,
        height=1,
        source=source,
        fill_color=transform('value', mapper),
        line_color=linecolor,
        line_width=linewidths
    )

    # Add text annotations
    from bokeh.models import Text
    text_glyph = Text(
        x='x',
        y='y',
        text='formatted',
        text_align='center',
        text_baseline='middle',
        text_font_size='10pt',
        text_color='black'
    )
    p.add_glyph(source, text_glyph)

    # Add color bar
    color_bar = ColorBar(
        color_mapper=mapper,
        ticker=BasicTicker(),
        label_standoff=12,
        border_line_color=None,
        location=(0, 0),
        title=cbar_label,
        title_text_font_size='10pt'
    )
    p.add_layout(color_bar, 'right')

    # Style the plot
    p.grid.visible = False
    p.axis.axis_line_color = None
    p.axis.major_tick_line_color = None
    p.axis.minor_tick_line_color = None
    p.xaxis.major_label_orientation = np.pi/4
    p.xaxis.axis_label = None
    p.yaxis.axis_label = None

    # Configure hover tool
    p.hover.tooltips = [
        ('Variables', '@x, @y'),
        ('Correlation', '@value{0.000}')
    ]

    return p


if __name__ == '__main__':
    # Sample data for testing
    np.random.seed(42)
    n = 100

    data = pd.DataFrame({
        'temperature': np.random.normal(20, 5, n),
        'humidity': np.random.normal(60, 10, n),
        'pressure': np.random.normal(1013, 20, n),
        'wind_speed': np.random.normal(10, 3, n)
    })

    # Add correlations
    data['humidity'] = 100 - 2 * data['temperature'] + np.random.normal(0, 5, n)
    data['wind_speed'] = 0.5 * data['temperature'] + np.random.normal(0, 2, n)

    # Create plot
    fig = create_plot(
        data,
        title='Correlation Matrix Heatmap'
    )

    # Save - ALWAYS use 'plot.png'!
    # Note: bokeh PNG export requires selenium and a webdriver
    # In CI/production environments, these should be pre-installed
    from bokeh.io import output_file, save

    # For development/testing: save HTML first
    output_file('plot.html')
    save(fig)

    try:
        # Try PNG export if dependencies are available
        export_png(fig, filename='plot.png')
        print("Plot saved to plot.png")
    except (ImportError, RuntimeError) as e:
        print("Note: PNG export requires selenium and a webdriver.")
        print("HTML version saved to plot.html")
        # In CI, this will be handled by the workflow