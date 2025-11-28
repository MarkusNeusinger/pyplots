"""
box-basic: Basic Box Plot
Implementation for: altair
Variant: default
Python: 3.10+
"""

import altair as alt
import pandas as pd
import numpy as np
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from altair import Chart


def create_plot(
    data: pd.DataFrame,
    values: str,
    groups: str,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    color_scheme: str = 'set2',
    width: int = 600,
    height: int = 400,
    **kwargs
) -> Chart:
    """
    Create a basic box plot showing statistical distribution of multiple groups using altair.

    Args:
        data: Input DataFrame with required columns
        values: Column name containing numeric values
        groups: Column name containing group categories
        title: Plot title (optional)
        xlabel: Custom x-axis label (optional, defaults to groups column name)
        ylabel: Custom y-axis label (optional, defaults to values column name)
        color_scheme: Color scheme for boxes (default: 'set2')
        width: Figure width in pixels (default: 600)
        height: Figure height in pixels (default: 400)
        **kwargs: Additional parameters for altair chart configuration

    Returns:
        Altair Chart object

    Raises:
        ValueError: If data is empty
        KeyError: If required columns not found

    Example:
        >>> data = pd.DataFrame({
        ...     'Group': ['A', 'A', 'B', 'B', 'C', 'C'],
        ...     'Value': [1, 2, 2, 3, 3, 4]
        ... })
        >>> chart = create_plot(data, values='Value', groups='Group')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    # Check required columns
    for col in [values, groups]:
        if col not in data.columns:
            available = ", ".join(data.columns)
            raise KeyError(f"Column '{col}' not found. Available columns: {available}")

    # Create the box plot using Altair's mark_boxplot
    base = alt.Chart(data).mark_boxplot(
        extent=1.5,  # 1.5 * IQR for whiskers
        outliers=True,
        size=40,
        opacity=0.7
    ).encode(
        x=alt.X(
            f'{groups}:N',
            title=xlabel or groups,
            axis=alt.Axis(
                labelAngle=0 if data[groups].nunique() <= 5 else -45,
                labelLimit=200
            )
        ),
        y=alt.Y(
            f'{values}:Q',
            title=ylabel or values,
            scale=alt.Scale(zero=False)
        ),
        color=alt.Color(
            f'{groups}:N',
            scale=alt.Scale(scheme=color_scheme),
            legend=None  # Hide legend as it's redundant with x-axis
        ),
        tooltip=[
            alt.Tooltip(f'{groups}:N', title='Group'),
            alt.Tooltip(f'count({values}):Q', title='Count'),
            alt.Tooltip(f'min({values}):Q', title='Min', format='.2f'),
            alt.Tooltip(f'q1({values}):Q', title='Q1', format='.2f'),
            alt.Tooltip(f'median({values}):Q', title='Median', format='.2f'),
            alt.Tooltip(f'q3({values}):Q', title='Q3', format='.2f'),
            alt.Tooltip(f'max({values}):Q', title='Max', format='.2f')
        ]
    )

    # Add sample size annotations
    text = alt.Chart(data).mark_text(
        align='center',
        baseline='top',
        dy=10,
        fontSize=10,
        opacity=0.7
    ).encode(
        x=alt.X(f'{groups}:N'),
        y=alt.Y(f'min({values}):Q'),
        text=alt.Text('count():Q', format='d')
    ).transform_aggregate(
        count='count()',
        groupby=[groups]
    )

    # Combine box plot with annotations
    chart = (base + text).properties(
        width=width,
        height=height,
        title=alt.TitleParams(
            text=title or 'Box Plot Distribution',
            fontSize=16,
            anchor='middle'
        )
    ).configure_view(
        strokeWidth=0
    ).configure_axis(
        grid=True,
        gridOpacity=0.3,
        gridDash=[3, 3],
        domainWidth=1,
        tickWidth=1
    ).configure_boxplot(
        median=dict(color='red', strokeWidth=2),
        box=dict(strokeWidth=1.5),
        outliers=dict(fill='red', fillOpacity=0.5, size=50)
    )

    return chart


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
    chart = create_plot(
        data,
        values='Value',
        groups='Group',
        title='Statistical Distribution Comparison Across Groups',
        ylabel='Measurement Value',
        xlabel='Categories'
    )

    # Save for inspection
    chart.save('plot.html')
    print("Interactive plot saved to plot.html")

    # Also save as PNG
    chart.save('plot.png', scale_factor=2.0)
    print("Static plot saved to plot.png")