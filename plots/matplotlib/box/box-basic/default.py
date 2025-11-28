"""
box-basic: Basic Box Plot
Implementation for: matplotlib
Variant: default
Python: 3.10+
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from matplotlib.figure import Figure


def create_plot(
    data: pd.DataFrame,
    values: str,
    groups: str,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    colors: Optional[list] = None,
    figsize: tuple[float, float] = (10, 6),
    **kwargs
) -> Figure:
    """
    Create a basic box plot showing statistical distribution of multiple groups.

    Args:
        data: Input DataFrame with required columns
        values: Column name containing numeric values
        groups: Column name containing group categories
        title: Plot title (optional)
        xlabel: Custom x-axis label (optional, defaults to groups column name)
        ylabel: Custom y-axis label (optional, defaults to values column name)
        colors: List of colors for each box (optional)
        figsize: Figure size as (width, height) in inches (default: (10, 6))
        **kwargs: Additional parameters passed to boxplot function

    Returns:
        Matplotlib Figure object

    Raises:
        ValueError: If data is empty
        KeyError: If required columns not found

    Example:
        >>> data = pd.DataFrame({
        ...     'Group': ['A', 'A', 'B', 'B', 'C', 'C'],
        ...     'Value': [1, 2, 2, 3, 3, 4]
        ... })
        >>> fig = create_plot(data, values='Value', groups='Group')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    # Check required columns
    for col in [values, groups]:
        if col not in data.columns:
            available = ", ".join(data.columns)
            raise KeyError(f"Column '{col}' not found. Available columns: {available}")

    # Prepare data for boxplot
    grouped_data = [group[values].dropna().values for name, group in data.groupby(groups)]
    group_names = data[groups].unique()

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Create boxplot
    bp = ax.boxplot(
        grouped_data,
        labels=group_names,
        patch_artist=True,  # Enable filling boxes with colors
        showmeans=False,
        notch=False,
        widths=0.7,
        **kwargs
    )

    # Apply colors if provided
    if colors:
        for patch, color in zip(bp['boxes'], colors * len(bp['boxes'])):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
    else:
        # Use a default color scheme
        default_colors = plt.cm.Set2(np.linspace(0, 1, len(bp['boxes'])))
        for patch, color in zip(bp['boxes'], default_colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)

    # Customize whiskers, caps, medians, and outliers
    for whisker in bp['whiskers']:
        whisker.set(color='#8B8B8B', linewidth=1.5, linestyle='-')

    for cap in bp['caps']:
        cap.set(color='#8B8B8B', linewidth=2)

    for median in bp['medians']:
        median.set(color='#FF0000', linewidth=2)

    for flier in bp['fliers']:
        flier.set(marker='o', markerfacecolor='#FF0000', markersize=8,
                  alpha=0.5, markeredgecolor='#8B8B8B')

    # Labels and title
    ax.set_xlabel(xlabel or groups)
    ax.set_ylabel(ylabel or values)

    if title:
        ax.set_title(title, fontsize=14, fontweight='bold')

    # Grid for better readability
    ax.grid(True, axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)

    # Rotate x-axis labels if there are many groups
    if len(group_names) > 5:
        plt.xticks(rotation=45, ha='right')

    # Layout
    plt.tight_layout()

    return fig


if __name__ == '__main__':
    # Sample data for testing with different distributions per group
    np.random.seed(42)  # For reproducibility

    # Generate sample data with 4 groups
    group_names = ['Group A', 'Group B', 'Group C', 'Group D']
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
    fig = create_plot(
        data,
        values='Value',
        groups='Group',
        title='Statistical Distribution Comparison Across Groups',
        ylabel='Measurement Value',
        xlabel='Groups'
    )

    # Save for inspection
    plt.savefig('plot.png', dpi=300, bbox_inches='tight')
    print("Plot saved to plot.png")