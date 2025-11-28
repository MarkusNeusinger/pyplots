"""
box-basic: Basic Box Plot
Implementation for: plotnine
Variant: default
Python: 3.10+
"""

from plotnine import (
    ggplot, aes, geom_boxplot, theme, element_text, element_line,
    labs, theme_minimal, scale_fill_brewer, coord_cartesian
)
import pandas as pd
import numpy as np
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from plotnine import ggplot as GGPlot


def create_plot(
    data: pd.DataFrame,
    values: str,
    groups: str,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    fill_palette: str = 'Set2',
    width: int = 10,
    height: int = 6,
    show_outliers: bool = True,
    **kwargs
) -> GGPlot:
    """
    Create a basic box plot showing statistical distribution of multiple groups using plotnine (ggplot2 syntax).

    Args:
        data: Input DataFrame with required columns
        values: Column name containing numeric values
        groups: Column name containing group categories
        title: Plot title (optional)
        xlabel: Custom x-axis label (optional, defaults to groups column name)
        ylabel: Custom y-axis label (optional, defaults to values column name)
        fill_palette: Color palette for boxes (default: 'Set2')
        width: Figure width in inches (default: 10)
        height: Figure height in inches (default: 6)
        show_outliers: Whether to show outliers (default: True)
        **kwargs: Additional parameters for geom_boxplot

    Returns:
        plotnine ggplot object

    Raises:
        ValueError: If data is empty
        KeyError: If required columns not found

    Example:
        >>> data = pd.DataFrame({
        ...     'Group': ['A', 'A', 'B', 'B', 'C', 'C'],
        ...     'Value': [1, 2, 2, 3, 3, 4]
        ... })
        >>> plot = create_plot(data, values='Value', groups='Group')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    # Check required columns
    for col in [values, groups]:
        if col not in data.columns:
            available = ", ".join(data.columns)
            raise KeyError(f"Column '{col}' not found. Available columns: {available}")

    # Create the ggplot object
    plot = (
        ggplot(data, aes(x=groups, y=values, fill=groups))
        + geom_boxplot(
            alpha=0.7,
            outlier_alpha=0.5 if show_outliers else 0,
            outlier_size=2,
            outlier_color='red',
            width=0.6,
            **kwargs
        )
        + scale_fill_brewer(palette=fill_palette, guide=False)  # Hide legend
        + labs(
            title=title or 'Box Plot Distribution',
            x=xlabel or groups,
            y=ylabel or values
        )
        + theme_minimal()
        + theme(
            figure_size=(width, height),
            plot_title=element_text(size=14, weight='bold', ha='center'),
            axis_title=element_text(size=11),
            axis_text=element_text(size=10),
            panel_grid_major_x=element_line(alpha=0),
            panel_grid_major_y=element_line(alpha=0.3, linetype='dashed'),
            panel_grid_minor=element_line(alpha=0)
        )
    )

    # Rotate x-axis labels if there are many groups
    unique_groups = data[groups].nunique()
    if unique_groups > 5:
        plot = plot + theme(
            axis_text_x=element_text(angle=45, ha='right')
        )

    # Add sample size annotations
    # plotnine doesn't have easy text annotations like ggplot2's annotate,
    # but we can add them as a separate layer
    from plotnine import geom_text, stat_summary

    # Calculate group statistics for annotations
    group_stats = data.groupby(groups).agg(
        count=(values, 'count'),
        min_val=(values, 'min')
    ).reset_index()

    # Adjust y position for annotations
    y_range = data[values].max() - data[values].min()
    y_position = data[values].min() - y_range * 0.05

    group_stats['y_pos'] = y_position
    group_stats['label'] = 'n=' + group_stats['count'].astype(str)

    # Add annotations as a separate layer
    plot = plot + geom_text(
        aes(x=groups, y='y_pos', label='label'),
        data=group_stats,
        size=9,
        alpha=0.7,
        va='top',
        ha='center'
    )

    return plot


if __name__ == '__main__':
    # Sample data for testing with different distributions per group
    np.random.seed(42)  # For reproducibility

    # Generate sample data with 4 groups
    data_dict = {
        'Group': [],
        'Value': []
    }

    # Group A: Normal distribution, mean=50, std=10
    group_a_data = np.random.normal(50, 10, 40)
    # Add some outliers
    group_a_data = np.append(group_a_data, [80, 85, 15])

    # Group B: Normal distribution, mean=60, std=15
    group_b_data = np.random.normal(60, 15, 35)
    # Add outliers
    group_b_data = np.append(group_b_data, [100, 10])

    # Group C: Normal distribution, mean=45, std=8
    group_c_data = np.random.normal(45, 8, 45)

    # Group D: Skewed distribution
    group_d_data = np.random.gamma(2, 2, 30) + 40
    # Add outliers
    group_d_data = np.append(group_d_data, [75, 78, 20])

    # Combine all data
    for group, values in zip(
        ['Group A', 'Group B', 'Group C', 'Group D'],
        [group_a_data, group_b_data, group_c_data, group_d_data]
    ):
        data_dict['Group'].extend([group] * len(values))
        data_dict['Value'].extend(values)

    data = pd.DataFrame(data_dict)

    # Create plot
    plot = create_plot(
        data,
        values='Value',
        groups='Group',
        title='Statistical Distribution Comparison Across Groups',
        ylabel='Measurement Value',
        xlabel='Categories'
    )

    # Save for inspection
    plot.save('plot.png', dpi=300, verbose=False)
    print("Plot saved to plot.png")