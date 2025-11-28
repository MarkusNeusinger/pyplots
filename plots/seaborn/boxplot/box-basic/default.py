"""
box-basic: Basic Box Plot
Implementation for: seaborn
Variant: default
Python: 3.10+
"""

import matplotlib.pyplot as plt
import seaborn as sns
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
    palette: Optional[str] = 'Set2',
    figsize: tuple[float, float] = (10, 6),
    showfliers: bool = True,
    **kwargs
) -> Figure:
    """
    Create a basic box plot showing statistical distribution of multiple groups using seaborn.

    Args:
        data: Input DataFrame with required columns
        values: Column name containing numeric values
        groups: Column name containing group categories
        title: Plot title (optional)
        xlabel: Custom x-axis label (optional, defaults to groups column name)
        ylabel: Custom y-axis label (optional, defaults to values column name)
        palette: Color palette name for boxes (default: 'Set2')
        figsize: Figure size as (width, height) in inches (default: (10, 6))
        showfliers: Whether to show outliers (default: True)
        **kwargs: Additional parameters passed to seaborn boxplot function

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

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Create boxplot with seaborn
    sns.boxplot(
        data=data,
        x=groups,
        y=values,
        palette=palette,
        ax=ax,
        showfliers=showfliers,
        width=0.7,
        linewidth=1.5,
        fliersize=6,
        **kwargs
    )

    # Customize the appearance
    # Set median line color to be more visible
    for patch in ax.artists:
        # Get the current face color
        r, g, b, a = patch.get_facecolor()
        # Set the box face color with some transparency
        patch.set_facecolor((r, g, b, 0.7))
        # Set edge color
        patch.set_edgecolor('black')
        patch.set_linewidth(1.2)

    # Style the median lines
    for line in ax.lines:
        # Median lines are the ones inside the boxes
        if line.get_linestyle() == '-' and line.get_marker() == 'None':
            line.set_color('red')
            line.set_linewidth(2)

    # Labels and title
    ax.set_xlabel(xlabel or groups)
    ax.set_ylabel(ylabel or values)

    if title:
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)

    # Grid for better readability
    ax.grid(True, axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)

    # Rotate x-axis labels if there are many groups
    unique_groups = data[groups].nunique()
    if unique_groups > 5:
        plt.xticks(rotation=45, ha='right')

    # Add some statistical annotations
    # Calculate and display the number of data points per group
    group_counts = data.groupby(groups)[values].count()
    y_bottom = ax.get_ylim()[0]
    for i, (group_name, count) in enumerate(group_counts.items()):
        ax.text(i, y_bottom, f'n={count}', ha='center', va='top', fontsize=9, alpha=0.7)

    # Apply seaborn style for better aesthetics
    sns.despine(ax=ax)

    # Layout
    plt.tight_layout()

    return fig


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
    fig = create_plot(
        data,
        values='Value',
        groups='Group',
        title='Statistical Distribution Comparison Across Groups',
        ylabel='Measurement Value',
        xlabel='Categories',
        palette='Set2'
    )

    # Save for inspection
    plt.savefig('plot.png', dpi=300, bbox_inches='tight')
    print("Plot saved to plot.png")