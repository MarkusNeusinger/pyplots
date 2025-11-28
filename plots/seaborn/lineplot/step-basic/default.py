"""
step-basic: Basic Step Plot
Implementation for: seaborn
Variant: default
Python: 3.10+
"""

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from matplotlib.figure import Figure


def create_plot(
    data: pd.DataFrame,
    x: str,
    y: str,
    where: str = "pre",
    color: str = "steelblue",
    linewidth: float = 2.0,
    alpha: float = 0.9,
    linestyle: str = "-",
    marker: str | None = None,
    markersize: float = 6,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    figsize: tuple[float, float] = (10, 6),
    **kwargs
) -> "Figure":
    """
    Create a basic step plot showing discrete changes in values using seaborn styling.

    Step plots display data as a series of horizontal and vertical lines,
    showing discrete changes between values. This implementation uses matplotlib's
    step function with seaborn's aesthetic styling for better visual appeal.

    Args:
        data: Input DataFrame with required columns
        x: Column name for x-axis values (sequential or time-based)
        y: Column name for y-axis values (numeric levels)
        where: Position of steps - "pre", "post", or "mid" (default: "pre")
        color: Line color (default: "steelblue")
        linewidth: Line width (default: 2.0)
        alpha: Transparency level 0.0-1.0 (default: 0.9)
        linestyle: Line style - "-", "--", "-.", or ":" (default: "-")
        marker: Optional marker style for data points (default: None)
        markersize: Size of markers if used (default: 6)
        title: Optional plot title (default: None)
        xlabel: Custom x-axis label (default: column name)
        ylabel: Custom y-axis label (default: column name)
        figsize: Figure size in inches (default: (10, 6))
        **kwargs: Additional parameters passed to step function

    Returns:
        Matplotlib Figure object with seaborn styling

    Raises:
        ValueError: If data is empty or 'where' parameter is invalid
        KeyError: If required columns not found

    Example:
        >>> import pandas as pd
        >>> data = pd.DataFrame({
        ...     'quarter': ['Q1', 'Q2', 'Q3', 'Q4'],
        ...     'revenue': [100, 120, 115, 140]
        ... })
        >>> fig = create_plot(data, 'quarter', 'revenue')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    # Check required columns
    required_columns = [x, y]
    missing_columns = []
    for col in required_columns:
        if col not in data.columns:
            missing_columns.append(col)

    if missing_columns:
        available = ", ".join(data.columns)
        missing = ", ".join(missing_columns)
        raise KeyError(f"Column(s) '{missing}' not found. Available columns: {available}")

    # Validate 'where' parameter
    if where not in ["pre", "post", "mid"]:
        raise ValueError(f"'where' parameter must be 'pre', 'post', or 'mid', got '{where}'")

    # Set seaborn style
    sns.set_style("whitegrid")

    # Create figure with seaborn context
    with sns.plotting_context("notebook", font_scale=1.1):
        fig, ax = plt.subplots(figsize=figsize)

        # Prepare data - ensure it's sorted
        plot_data = data[[x, y]].copy()

        # Handle categorical x-axis by converting to numeric positions
        if plot_data[x].dtype == 'object' or pd.api.types.is_categorical_dtype(plot_data[x]):
            x_labels = plot_data[x].unique()
            x_positions = np.arange(len(plot_data[x]))
            plot_x = x_positions
            use_categorical = True
        else:
            plot_data = plot_data.sort_values(by=x)
            plot_x = plot_data[x]
            use_categorical = False

        # Plot step lines
        ax.step(plot_x, plot_data[y],
                where=where,
                color=color,
                linewidth=linewidth,
                alpha=alpha,
                linestyle=linestyle,
                **kwargs)

        # Add markers if specified
        if marker:
            ax.plot(plot_x, plot_data[y],
                    marker=marker,
                    markersize=markersize,
                    color=color,
                    alpha=alpha,
                    linestyle='None')  # Only markers, no line

        # Handle categorical x-axis labels
        if use_categorical:
            ax.set_xticks(x_positions)
            ax.set_xticklabels(x_labels)

        # Apply labels with seaborn styling
        ax.set_xlabel(xlabel or x, fontsize=12, fontweight='medium')
        ax.set_ylabel(ylabel or y, fontsize=12, fontweight='medium')

        # Add title if provided
        if title:
            ax.set_title(title, fontsize=14, fontweight='bold', pad=20)

        # Customize grid for better visibility
        ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
        ax.set_axisbelow(True)  # Grid behind data

        # Remove top and right spines for cleaner look
        sns.despine()

        # Ensure no overlapping labels
        fig.autofmt_xdate()  # Automatically format date labels if x is datetime

        # Adjust layout
        plt.tight_layout()

    # Reset seaborn defaults to avoid affecting other plots
    sns.reset_defaults()

    return fig


if __name__ == '__main__':
    # Sample data for testing
    np.random.seed(42)  # For reproducibility

    # Create sample data representing quarterly sales performance
    data = pd.DataFrame({
        'quarter': ['Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023',
                    'Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024'],
        'sales': [45, 48, 48, 52, 55, 55, 58, 62]
    })

    # Create plot with seaborn styling
    fig = create_plot(
        data,
        x='quarter',
        y='sales',
        title='Quarterly Sales Performance',
        xlabel='Quarter',
        ylabel='Sales (in millions)',
        where='post',  # Step occurs after the data point
        color='#2E86AB',  # Nice blue color
        marker='o',  # Show actual data points
        markersize=5
    )

    # Save for inspection - ALWAYS use 'plot.png' as filename
    plt.savefig('plot.png', dpi=300, bbox_inches='tight')
    print("Plot saved to plot.png")