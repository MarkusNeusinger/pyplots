"""
scatter-basic-007: Financial Categories Bar Chart
Implementation for: seaborn
Variant: default
Python: 3.10+
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Optional, Union, List
from matplotlib.figure import Figure


def create_plot(
    data: pd.DataFrame,
    categories: str,
    values: str,
    color: Optional[Union[str, List[str]]] = None,
    currency: str = "$",
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    orientation: str = "vertical",
    show_values: bool = True,
    **kwargs
) -> Figure:
    """
    Create a bar chart displaying financial categories with their corresponding values.

    This visualization is designed to show categorical financial data such as expense categories,
    revenue streams, budget allocations, or portfolio distributions. The chart provides clear
    visual comparison between different financial categories.

    Args:
        data: Input DataFrame with required columns
        categories: Column name containing category labels
        values: Column name containing monetary values
        color: Bar color or palette (default: "steelblue")
        currency: Currency symbol to display (default: "$")
        title: Chart title (default: "Financial Categories")
        xlabel: Custom x-axis label (default: "Categories")
        ylabel: Custom y-axis label (default: "Amount")
        orientation: Bar orientation ("vertical" or "horizontal", default: "vertical")
        show_values: Display values on bars (default: True)
        **kwargs: Additional parameters passed to seaborn barplot function

    Returns:
        Matplotlib Figure object

    Raises:
        ValueError: If data is empty
        KeyError: If required columns not found in data
        ValueError: If orientation is not "vertical" or "horizontal"

    Example:
        >>> data = pd.DataFrame({
        ...     'Category': ['Rent', 'Food', 'Transport', 'Entertainment'],
        ...     'Amount': [1500, 800, 300, 200]
        ... })
        >>> fig = create_plot(data, 'Category', 'Amount')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    # Check required columns
    required_columns = [categories, values]
    for col in required_columns:
        if col not in data.columns:
            available = ", ".join(data.columns)
            raise KeyError(f"Column '{col}' not found. Available columns: {available}")

    # Validate orientation
    if orientation not in ["vertical", "horizontal"]:
        raise ValueError(f"Orientation must be 'vertical' or 'horizontal', not '{orientation}'")

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Set style for professional financial charts
    sns.set_style("whitegrid")

    # Prepare data - ensure consistent ordering
    plot_data = data[[categories, values]].copy()
    plot_data[categories] = plot_data[categories].astype(str)

    # Handle colors - create palette if not specified
    if color is None:
        # Create custom palette based on positive/negative values
        unique_cats = plot_data[categories].unique()
        palette = {}
        for cat in unique_cats:
            val = plot_data[plot_data[categories] == cat][values].iloc[0]
            palette[cat] = '#ff4444' if val < 0 else '#4682b4'
    elif isinstance(color, list):
        unique_cats = plot_data[categories].unique()
        palette = dict(zip(unique_cats, color))
    else:
        palette = color

    # Plot bars based on orientation
    if orientation == "vertical":
        ax = sns.barplot(
            data=plot_data,
            x=categories,
            y=values,
            hue=categories,
            palette=palette,
            legend=False,
            ax=ax,
            **kwargs
        )

        # Rotate x labels if there are many categories
        if len(plot_data[categories].unique()) > 10:
            plt.xticks(rotation=45, ha='right')
        elif len(plot_data[categories].unique()) > 7:
            plt.xticks(rotation=30, ha='right')

        # Set labels
        ax.set_xlabel(xlabel or "Categories", fontsize=11)
        ax.set_ylabel(ylabel or "Amount", fontsize=11)

        # Format y-axis with currency
        ax.yaxis.set_major_formatter(plt.FuncFormatter(
            lambda x, p: f'{currency}{x:,.0f}' if abs(x) < 1000 else
                        f'{currency}{x/1000:.0f}K' if abs(x) < 1000000 else
                        f'{currency}{x/1000000:.1f}M'))
    else:  # horizontal
        # For horizontal, swap x and y
        ax = sns.barplot(
            data=plot_data,
            x=values,
            y=categories,
            hue=categories,
            orient='h',
            palette=palette,
            legend=False,
            ax=ax,
            **kwargs
        )

        # Set labels
        ax.set_xlabel(xlabel or "Amount", fontsize=11)
        ax.set_ylabel(ylabel or "Categories", fontsize=11)

        # Format x-axis with currency
        ax.xaxis.set_major_formatter(plt.FuncFormatter(
            lambda x, p: f'{currency}{x:,.0f}' if abs(x) < 1000 else
                        f'{currency}{x/1000:.0f}K' if abs(x) < 1000000 else
                        f'{currency}{x/1000000:.1f}M'))

    # Add value labels on bars if requested
    if show_values:
        containers = ax.containers if hasattr(ax, 'containers') else [ax.patches]
        for container in containers:
            # Get bar patches
            bars = container if hasattr(container, '__iter__') else ax.patches

            # Iterate through bars and add value labels
            for i, bar in enumerate(bars):
                # Get the height/width of the bar
                if orientation == "vertical":
                    height = bar.get_height()
                    if height != 0:  # Skip zero-height bars
                        # Format value with currency and appropriate scale
                        if abs(height) >= 1_000_000:
                            label = f"{currency}{height/1_000_000:.1f}M"
                        elif abs(height) >= 1_000:
                            label = f"{currency}{height/1_000:.1f}K"
                        else:
                            label = f"{currency}{height:,.0f}"

                        # Position label
                        va = 'bottom' if height >= 0 else 'top'
                        ax.text(bar.get_x() + bar.get_width()/2, height, label,
                               ha='center', va=va, fontsize=9, fontweight='bold')
                else:  # horizontal
                    width = bar.get_width()
                    if width != 0:  # Skip zero-width bars
                        # Format value with currency and appropriate scale
                        if abs(width) >= 1_000_000:
                            label = f"{currency}{width/1_000_000:.1f}M"
                        elif abs(width) >= 1_000:
                            label = f"{currency}{width/1_000:.1f}K"
                        else:
                            label = f"{currency}{width:,.0f}"

                        # Position label
                        ha = 'left' if width >= 0 else 'right'
                        ax.text(width, bar.get_y() + bar.get_height()/2, label,
                               ha=ha, va='center', fontsize=9, fontweight='bold')

    # Apply styling
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)

    # Add title
    if title:
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    else:
        ax.set_title("Financial Categories", fontsize=14, fontweight='bold', pad=20)

    # Add a subtle line at zero for reference
    if orientation == "vertical":
        ax.axhline(y=0, color='black', linewidth=0.5, alpha=0.3)
    else:
        ax.axvline(x=0, color='black', linewidth=0.5, alpha=0.3)

    # Reset style to default to not affect other plots
    sns.reset_orig()

    # Adjust layout to prevent label cutoff
    plt.tight_layout()

    return fig


if __name__ == '__main__':
    # Sample data for testing
    np.random.seed(42)

    # Create sample financial data with both positive and negative values
    categories = ['Rent', 'Food', 'Transport', 'Entertainment', 'Utilities',
                  'Insurance', 'Savings', 'Healthcare', 'Education', 'Returns']
    amounts = [1500, 800, 300, 200, 250, 180, 500, 150, 100, -200]  # Returns is negative

    data = pd.DataFrame({
        'Category': categories,
        'Amount': amounts
    })

    # Create plot
    fig = create_plot(
        data,
        categories='Category',
        values='Amount',
        title='Monthly Expense & Income Breakdown',
        ylabel='Amount (USD)'
    )

    # Save for inspection
    plt.savefig('test_output_seaborn.png', dpi=150, bbox_inches='tight')
    print("Plot saved to test_output_seaborn.png")

    total_expenses = sum([a for a in amounts if a > 0])
    total_income = sum([a for a in amounts if a < 0])
    print(f"Total expenses: ${total_expenses:,.2f}")
    print(f"Total income: ${abs(total_income):,.2f}")
    print(f"Net: ${total_expenses + total_income:,.2f}")