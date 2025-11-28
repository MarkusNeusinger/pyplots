"""
box-basic: Basic Box Plot
Implementation for: plotly
Variant: default
Python: 3.10+
"""

from typing import TYPE_CHECKING, Optional

import numpy as np
import pandas as pd
import plotly.express as px


if TYPE_CHECKING:
    from plotly.graph_objects import Figure


def create_plot(
    data: pd.DataFrame,
    values: str,
    groups: str,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    color_discrete_sequence: Optional[list] = None,
    height: int = 600,
    width: int = 1000,
    showlegend: bool = False,
    **kwargs,
) -> Figure:
    """
    Create an interactive box plot showing statistical distribution of multiple groups using plotly.

    Args:
        data: Input DataFrame with required columns
        values: Column name containing numeric values
        groups: Column name containing group categories
        title: Plot title (optional)
        xlabel: Custom x-axis label (optional, defaults to groups column name)
        ylabel: Custom y-axis label (optional, defaults to values column name)
        color_discrete_sequence: List of colors for each box (optional)
        height: Figure height in pixels (default: 600)
        width: Figure width in pixels (default: 1000)
        showlegend: Whether to show legend (default: False)
        **kwargs: Additional parameters passed to plotly box trace

    Returns:
        Plotly Figure object

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

    # Use plotly.express for easier box plot creation
    fig = px.box(
        data,
        x=groups,
        y=values,
        color=groups,
        color_discrete_sequence=color_discrete_sequence or px.colors.qualitative.Set2,
        notched=False,
        points="outliers",  # Show only outliers as points
        **kwargs,
    )

    # Update traces for better styling
    fig.update_traces(
        boxmean="sd",  # Show mean and standard deviation
        marker={"size": 8, "opacity": 0.5, "line": {"width": 1}},
        line={"width": 1.5},
        fillcolor=None,
        opacity=0.7,
    )

    # Update layout
    fig.update_layout(
        title={
            "text": title or "Box Plot Distribution",
            "font": {"size": 16, "family": "Arial, sans-serif"},
            "x": 0.5,
            "xanchor": "center",
        },
        xaxis={
            "title": xlabel or groups,
            "gridcolor": "lightgray",
            "gridwidth": 0.5,
            "showgrid": False,
            "zeroline": False,
        },
        yaxis={
            "title": ylabel or values,
            "gridcolor": "lightgray",
            "gridwidth": 0.5,
            "showgrid": True,
            "zeroline": True,
            "zerolinewidth": 1,
            "zerolinecolor": "lightgray",
        },
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=height,
        width=width,
        showlegend=showlegend,
        hovermode="x unified",
        hoverlabel={"bgcolor": "white", "font_size": 12, "font_family": "Arial, sans-serif"},
    )

    # Add annotations with sample sizes
    group_counts = data.groupby(groups)[values].count()
    annotations = []
    for _i, (group_name, count) in enumerate(group_counts.items()):
        annotations.append(
            {
                "x": group_name,
                "y": data[data[groups] == group_name][values].min() - (data[values].max() - data[values].min()) * 0.05,
                "text": f"n={count}",
                "showarrow": False,
                "font": {"size": 10, "color": "gray"},
                "xanchor": "center",
                "yanchor": "top",
            }
        )

    fig.update_layout(annotations=annotations)

    # Update hover template for better information
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>"
        + "Max: %{y}<br>"
        + "Q3: %{upperfence}<br>"
        + "Median: %{median}<br>"
        + "Q1: %{lowerfence}<br>"
        + "Min: %{y}<br>"
        + "<extra></extra>"
    )

    return fig


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
    fig.write_html("plot.html")
    fig.write_image("plot.png", width=1000, height=600, scale=2)
    print("Interactive plot saved to plot.html")
    print("Static plot saved to plot.png")
