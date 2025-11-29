"""
box-basic: Basic Box Plot
Implementation for: bokeh
Variant: default
Python: 3.10+
"""

from typing import TYPE_CHECKING, Optional

import numpy as np
import pandas as pd
from bokeh.models import ColumnDataSource, FixedTicker, Label, Whisker
from bokeh.plotting import figure


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
    width: int = 1600,
    height: int = 900,
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
        width: Figure width in pixels (default: 1600)
        height: Figure height in pixels (default: 900)
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
    n_groups = len(group_names)

    # Prepare data for box plot
    stats = {"x": [], "q1": [], "q2": [], "q3": [], "upper": [], "lower": [], "group": []}
    outliers = {"x": [], "y": []}

    for i, group in enumerate(group_names):
        group_data = data[data[groups] == group][values].dropna()

        q1 = group_data.quantile(0.25)
        q2 = group_data.quantile(0.5)
        q3 = group_data.quantile(0.75)
        iqr = q3 - q1
        upper = min(group_data.max(), q3 + 1.5 * iqr)
        lower = max(group_data.min(), q1 - 1.5 * iqr)

        stats["x"].append(i)
        stats["q1"].append(q1)
        stats["q2"].append(q2)
        stats["q3"].append(q3)
        stats["upper"].append(upper)
        stats["lower"].append(lower)
        stats["group"].append(group)

        # Find outliers
        outlier_data = group_data[(group_data < lower) | (group_data > upper)]
        for val in outlier_data:
            outliers["x"].append(i)
            outliers["y"].append(val)

    # Set colors
    if not colors:
        from bokeh.palettes import Set2_8

        colors = Set2_8[:n_groups]

    # Create figure with numeric x-axis
    p = figure(
        width=width,
        height=height,
        title=title or "Box Plot Distribution",
        toolbar_location="above",
        tools="pan,wheel_zoom,box_zoom,reset,save",
    )

    source = ColumnDataSource(data=stats)

    # Draw boxes (Q1 to Q3)
    box_width = 0.5
    for i, color in enumerate(colors):
        p.vbar(
            x=i,
            width=box_width,
            bottom=stats["q1"][i],
            top=stats["q3"][i],
            fill_color=color,
            line_color="black",
            alpha=0.7,
        )

    # Draw median lines
    for i in range(n_groups):
        p.segment(
            x0=i - box_width / 2,
            y0=stats["q2"][i],
            x1=i + box_width / 2,
            y1=stats["q2"][i],
            line_color="red",
            line_width=2,
        )

    # Draw whiskers
    upper_whisker = Whisker(base="x", upper="upper", lower="q3", source=source, line_color="black")
    upper_whisker.upper_head.size = 10
    upper_whisker.lower_head.size = 0
    p.add_layout(upper_whisker)

    lower_whisker = Whisker(base="x", upper="q1", lower="lower", source=source, line_color="black")
    lower_whisker.upper_head.size = 0
    lower_whisker.lower_head.size = 10
    p.add_layout(lower_whisker)

    # Draw outliers
    if outliers["x"]:
        outlier_source = ColumnDataSource(data=outliers)
        p.scatter(x="x", y="y", source=outlier_source, size=8, color="red", alpha=0.5, line_color="black", line_width=1)

    # Set x-axis to show group names
    p.xaxis.ticker = FixedTicker(ticks=list(range(n_groups)))
    p.xaxis.major_label_overrides = dict(enumerate(group_names))

    # Labels
    p.xaxis.axis_label = xlabel or groups
    p.yaxis.axis_label = ylabel or values

    # Styling
    p.title.text_font_size = "14pt"
    p.title.align = "center"
    p.ygrid.grid_line_alpha = 0.3
    p.ygrid.grid_line_dash = [6, 4]
    p.xgrid.visible = False

    # Add sample size annotations
    group_counts = data.groupby(groups)[values].count()
    y_min = data[values].min()
    y_range = data[values].max() - y_min
    for i, group in enumerate(group_names):
        count = group_counts[group]
        label = Label(
            x=i, y=y_min - y_range * 0.08, text=f"n={count}", text_align="center", text_font_size="9pt", text_alpha=0.7
        )
        p.add_layout(label)

    return p


if __name__ == "__main__":
    # Sample data for testing with different distributions per group
    np.random.seed(42)

    data_dict = {"Group": [], "Value": []}

    # Group A: Normal distribution
    group_a_data = np.random.normal(50, 10, 40)
    group_a_data = np.append(group_a_data, [80, 85, 15])

    # Group B: Normal distribution
    group_b_data = np.random.normal(60, 15, 35)
    group_b_data = np.append(group_b_data, [100, 10])

    # Group C: Normal distribution
    group_c_data = np.random.normal(45, 8, 45)

    # Group D: Skewed distribution
    group_d_data = np.random.gamma(2, 2, 30) + 40
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

    # Save as PNG using webdriver-manager for automatic chromedriver
    from bokeh.io import export_png
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    export_png(fig, filename="plot.png", webdriver=driver)
    driver.quit()
    print("Plot saved to plot.png")
