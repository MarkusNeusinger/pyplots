"""
box-basic: Basic Box Plot
Implementation for: pygal
Variant: default
Python: 3.10+
"""

from typing import TYPE_CHECKING, Optional

import numpy as np
import pandas as pd
import pygal
from pygal.style import Style


if TYPE_CHECKING:
    from pygal import Box


def create_plot(
    data: pd.DataFrame,
    values: str,
    groups: str,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    width: int = 800,
    height: int = 600,
    show_legend: bool = True,
    **kwargs,
) -> Box:
    """
    Create a basic box plot showing statistical distribution of multiple groups using pygal.

    Args:
        data: Input DataFrame with required columns
        values: Column name containing numeric values
        groups: Column name containing group categories
        title: Plot title (optional)
        xlabel: Custom x-axis label (optional, defaults to groups column name)
        ylabel: Custom y-axis label (optional, defaults to values column name)
        width: Figure width in pixels (default: 800)
        height: Figure height in pixels (default: 600)
        show_legend: Whether to show legend (default: True)
        **kwargs: Additional parameters for pygal configuration

    Returns:
        pygal Box chart object

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

    # Create custom style
    custom_style = Style(
        background="white",
        plot_background="white",
        foreground="#333",
        foreground_strong="#333",
        foreground_subtle="#555",
        opacity=0.7,
        opacity_hover=0.9,
        colors=("#66c2a5", "#fc8d62", "#8da0cb", "#e78ac3", "#a6d854", "#ffd92f", "#e5c494", "#b3b3b3"),
        font_family="Arial, sans-serif",
        major_guide_stroke_dasharray="3,3",
        guide_stroke_dasharray="1,1",
    )

    # Create box plot
    box_chart = pygal.Box(
        title=title or "Box Plot Distribution",
        x_title=xlabel or groups,
        y_title=ylabel or values,
        width=width,
        height=height,
        show_legend=show_legend,
        style=custom_style,
        box_mode="tukey",  # Use Tukey method (1.5 * IQR for whiskers)
        print_values=False,
        print_zeroes=False,
        **kwargs,
    )

    # Calculate box plot data for each group
    group_names = sorted(data[groups].unique())

    for group in group_names:
        group_data = data[data[groups] == group][values].dropna()

        # Pygal's Box chart expects data in a specific format:
        # [min, Q1, median, Q3, max] or the raw values (pygal will calculate)
        # We'll provide the raw values and let pygal handle the calculations
        values_list = group_data.tolist()

        # Add the series with label
        box_chart.add(f"{group} (n={len(values_list)})", values_list)

    return box_chart


if __name__ == "__main__":
    # Sample data for testing with different distributions per group
    np.random.seed(42)  # For reproducibility

    # Generate sample data with 4 groups
    data_dict = {"Group": [], "Value": []}

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
        ["Group A", "Group B", "Group C", "Group D"],
        [group_a_data, group_b_data, group_c_data, group_d_data],
        strict=False,
    ):
        data_dict["Group"].extend([group] * len(values))
        data_dict["Value"].extend(values)

    data = pd.DataFrame(data_dict)

    # Create plot
    chart = create_plot(
        data,
        values="Value",
        groups="Group",
        title="Statistical Distribution Comparison Across Groups",
        ylabel="Measurement Value",
        xlabel="Categories",
    )

    # Save as PNG
    chart.render_to_png("plot.png")
    print("Plot saved to plot.png")
