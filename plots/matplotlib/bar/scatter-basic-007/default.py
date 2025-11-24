"""
scatter-basic-007: Financial Categories Bar Chart
Implementation for: matplotlib
Variant: default
Python: 3.10+
"""

import matplotlib.pyplot as plt
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
        color: Bar color or list of colors (default: "steelblue")
        currency: Currency symbol to display (default: "$")
        title: Chart title (default: "Financial Categories")
        xlabel: Custom x-axis label (default: "Categories")
        ylabel: Custom y-axis label (default: "Amount")
        orientation: Bar orientation ("vertical" or "horizontal", default: "vertical")
        show_values: Display values on bars (default: True)
        **kwargs: Additional parameters passed to bar plotting function

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

    # Prepare data
    x_data = data[categories].astype(str)
    y_data = data[values]

    # Handle colors
    if color is None:
        # Use different colors for positive and negative values
        colors = ['#ff4444' if v < 0 else '#4682b4' for v in y_data]
    elif isinstance(color, list):
        colors = color
    else:
        colors = color

    # Plot bars based on orientation
    if orientation == "vertical":
        bars = ax.bar(x_data, y_data, color=colors, **kwargs)

        # Rotate x labels if there are many categories
        if len(x_data) > 10:
            plt.xticks(rotation=45, ha='right')
        elif len(x_data) > 7:
            plt.xticks(rotation=30, ha='right')
    else:  # horizontal
        bars = ax.barh(x_data, y_data, color=colors, **kwargs)

    # Add value labels on bars if requested
    if show_values:
        for bar, value in zip(bars, y_data):
            # Format value with currency and appropriate scale
            if abs(value) >= 1_000_000:
                label = f"{currency}{value/1_000_000:.1f}M"
            elif abs(value) >= 1_000:
                label = f"{currency}{value/1_000:.1f}K"
            else:
                label = f"{currency}{value:,.0f}"

            if orientation == "vertical":
                # Position label above positive bars, below negative bars
                if value >= 0:
                    va = 'bottom'
                    y_pos = value
                else:
                    va = 'top'
                    y_pos = value
                ax.text(bar.get_x() + bar.get_width()/2, y_pos, label,
                       ha='center', va=va, fontsize=9, fontweight='bold')
            else:  # horizontal
                # Position label to the right of positive bars, left of negative bars
                if value >= 0:
                    ha = 'left'
                    x_pos = value
                else:
                    ha = 'right'
                    x_pos = value
                ax.text(x_pos, bar.get_y() + bar.get_height()/2, label,
                       ha=ha, va='center', fontsize=9, fontweight='bold')

    # Apply styling
    if orientation == "vertical":
        ax.set_xlabel(xlabel or "Categories", fontsize=11)
        ax.set_ylabel(ylabel or "Amount", fontsize=11)
        # Add horizontal grid for vertical bars
        ax.grid(True, axis='y', alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)

        # Format y-axis with currency
        ax.yaxis.set_major_formatter(plt.FuncFormatter(
            lambda x, p: f'{currency}{x:,.0f}' if abs(x) < 1000 else
                        f'{currency}{x/1000:.0f}K' if abs(x) < 1000000 else
                        f'{currency}{x/1000000:.1f}M'))
    else:  # horizontal
        ax.set_xlabel(xlabel or "Amount", fontsize=11)
        ax.set_ylabel(ylabel or "Categories", fontsize=11)
        # Add vertical grid for horizontal bars
        ax.grid(True, axis='x', alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)

        # Format x-axis with currency
        ax.xaxis.set_major_formatter(plt.FuncFormatter(
            lambda x, p: f'{currency}{x:,.0f}' if abs(x) < 1000 else
                        f'{currency}{x/1000:.0f}K' if abs(x) < 1000000 else
                        f'{currency}{x/1000000:.1f}M'))

    # Add title
    if title:
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    else:
        ax.set_title("Financial Categories", fontsize=14, fontweight='bold', pad=20)

    # Add a subtle line at y=0 for reference
    if orientation == "vertical":
        ax.axhline(y=0, color='black', linewidth=0.5, alpha=0.3)
    else:
        ax.axvline(x=0, color='black', linewidth=0.5, alpha=0.3)

    # Adjust layout to prevent label cutoff
    plt.tight_layout()

    return fig


if __name__ == '__main__':
    # Sample data for testing
    np.random.seed(42)

    # Create sample financial data
    categories = ['Rent', 'Food', 'Transport', 'Entertainment', 'Utilities',
                  'Insurance', 'Savings', 'Healthcare', 'Education', 'Misc']
    amounts = [1500, 800, 300, 200, 250, 180, 500, 150, 100, 120]

    data = pd.DataFrame({
        'Category': categories,
        'Amount': amounts
    })

    # Create plot
    fig = create_plot(
        data,
        categories='Category',
        values='Amount',
        title='Monthly Expense Breakdown',
        ylabel='Amount (USD)'
    )

    # Save for inspection
    plt.savefig('test_output.png', dpi=150, bbox_inches='tight')
    print("Plot saved to test_output.png")
    print(f"Total expenses: ${sum(amounts):,.2f}")