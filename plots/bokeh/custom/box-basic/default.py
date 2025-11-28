"""
box-basic: Basic Box Plot
Implementation for: bokeh
Variant: default
Python: 3.10+
"""

from typing import TYPE_CHECKING, Optional

import numpy as np
import pandas as pd
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, output_file, save


if TYPE_CHECKING:
    from bokeh.plotting import Figure


def create_plot(
    data: pd.DataFrame,
    values: str,
    groups: str,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    colors: Optional[list] = None,
    width: int = 1000,
    height: int = 600,
    **kwargs,
) -> Figure:
    """
    Create a basic box plot showing statistical distribution of multiple groups using bokeh.

    Args:
        data: Input DataFrame with required columns
        values: Column name containing numeric values
        groups: Column name containing group categories
        title: Plot title (optional)
        xlabel: Custom x-axis label (optional, defaults to groups column name)
        ylabel: Custom y-axis label (optional, defaults to values column name)
        colors: List of colors for each box (optional)
        width: Figure width in pixels (default: 1000)
        height: Figure height in pixels (default: 600)
        **kwargs: Additional parameters

    Returns:
        Bokeh Figure object

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

    # Calculate box plot statistics for each group
    group_names = sorted(data[groups].unique())

    # Prepare data structures for box plot components
    box_data = {
        "groups": [],
        "q1": [],
        "q2": [],
        "q3": [],
        "upper": [],
        "lower": [],
        "outliers_x": [],
        "outliers_y": [],
    }

    for group in group_names:
        group_data = data[data[groups] == group][values].dropna()

        q1 = group_data.quantile(0.25)
        q2 = group_data.quantile(0.5)  # median
        q3 = group_data.quantile(0.75)
        iqr = q3 - q1
        upper = min(group_data.max(), q3 + 1.5 * iqr)
        lower = max(group_data.min(), q1 - 1.5 * iqr)

        # Find outliers
        outliers = group_data[(group_data < lower) | (group_data > upper)]

        box_data["groups"].append(group)
        box_data["q1"].append(q1)
        box_data["q2"].append(q2)
        box_data["q3"].append(q3)
        box_data["upper"].append(upper)
        box_data["lower"].append(lower)

        # Add outliers
        for outlier in outliers:
            box_data["outliers_x"].append(group)
            box_data["outliers_y"].append(outlier)

    # Create figure
    p = figure(
        x_range=group_names,
        width=width,
        height=height,
        title=title or "Box Plot Distribution",
        toolbar_location="above",
        tools="pan,wheel_zoom,box_zoom,reset,save",
    )

    # Set colors
    if not colors:
        from bokeh.palettes import Set2_8

        colors = Set2_8[: len(group_names)]

    # Draw boxes (Q1 to Q3) for each group
    for i, group in enumerate(group_names):
        idx = box_data["groups"].index(group)

        # Box from Q1 to Q3
        p.vbar(
            x=group,
            width=0.5,
            bottom=box_data["q1"][idx],
            top=box_data["q3"][idx],
            fill_color=colors[i % len(colors)],
            line_color="black",
            alpha=0.7,
        )

        # Median line
        p.line(x=[i - 0.25, i + 0.25], y=[box_data["q2"][idx], box_data["q2"][idx]], line_color="red", line_width=2)

        # Upper whisker
        p.line(x=[i, i], y=[box_data["q3"][idx], box_data["upper"][idx]], line_color="black", line_width=1)

        # Upper whisker cap
        p.line(
            x=[i - 0.1, i + 0.1], y=[box_data["upper"][idx], box_data["upper"][idx]], line_color="black", line_width=1.5
        )

        # Lower whisker
        p.line(x=[i, i], y=[box_data["q1"][idx], box_data["lower"][idx]], line_color="black", line_width=1)

        # Lower whisker cap
        p.line(
            x=[i - 0.1, i + 0.1], y=[box_data["lower"][idx], box_data["lower"][idx]], line_color="black", line_width=1.5
        )

    # Draw outliers using ColumnDataSource (required for categorical x-axis)
    if box_data["outliers_x"]:
        outlier_source = ColumnDataSource(data={"x": box_data["outliers_x"], "y": box_data["outliers_y"]})
        p.scatter(x="x", y="y", source=outlier_source, size=8, color="red", alpha=0.5, line_color="black", line_width=1)

    # Styling
    p.xaxis.axis_label = xlabel or groups
    p.yaxis.axis_label = ylabel or values

    p.title.text_font_size = "14pt"
    p.title.align = "center"

    # Grid
    p.ygrid.grid_line_alpha = 0.3
    p.ygrid.grid_line_dash = [6, 4]
    p.xgrid.visible = False

    # Add sample size annotations
    group_counts = data.groupby(groups)[values].count()
    for i, (_group, count) in enumerate(group_counts.items()):
        y_position = data[values].min() - (data[values].max() - data[values].min()) * 0.05
        from bokeh.models import Label

        label = Label(x=i, y=y_position, text=f"n={count}", text_align="center", text_font_size="9pt", text_alpha=0.7)
        p.add_layout(label)

    return p


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
    fig = create_plot(
        data,
        values="Value",
        groups="Group",
        title="Statistical Distribution Comparison Across Groups",
        ylabel="Measurement Value",
        xlabel="Categories",
    )

    # Save for inspection
    output_file("plot.html")
    save(fig)
    print("Interactive plot saved to plot.html")

    # Also export as PNG if possible
    try:
        from bokeh.io import export_png

        export_png(fig, filename="plot.png")
        print("Static plot saved to plot.png")
    except ImportError:
        print("Note: Install 'selenium' and 'pillow' to export PNG images")
