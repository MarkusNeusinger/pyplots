"""
scatter-basic-005: Regression Line Scatter Plot
Implementation for: seaborn
Variant: default
Python: 3.10+
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from typing import TYPE_CHECKING, Optional, Tuple

if TYPE_CHECKING:
    from matplotlib.figure import Figure

# Set seaborn style
sns.set_style("whitegrid")


def create_plot(
    data: pd.DataFrame,
    x: str,
    y: str,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    marker_color: str = "dodgerblue",
    line_color: str = "crimson",
    marker_size: float = 100,
    alpha: float = 0.7,
    show_confidence: bool = True,
    confidence_level: int = 95,
    show_equation: bool = True,
    show_r_squared: bool = True,
    figsize: Tuple[float, float] = (10, 6),
    style: Optional[str] = None,
    **kwargs
) -> "Figure":
    """
    Create a scatter plot with fitted regression line and regression quality metrics using seaborn.

    Args:
        data: Input DataFrame with required columns
        x: Column name for x-axis values
        y: Column name for y-axis values
        title: Plot title (optional, defaults to descriptive title)
        xlabel: X-axis label (optional, defaults to column name)
        ylabel: Y-axis label (optional, defaults to column name)
        marker_color: Color for scatter points (default: "dodgerblue")
        line_color: Color for regression line (default: "crimson")
        marker_size: Size of scatter points (default: 100)
        alpha: Transparency for points (default: 0.7)
        show_confidence: Whether to show confidence interval (default: True)
        confidence_level: Confidence level percentage (default: 95)
        show_equation: Whether to show regression equation (default: True)
        show_r_squared: Whether to show R² value (default: True)
        figsize: Figure size as (width, height) tuple (default: (10, 6))
        style: Optional style parameter for different marker styles per group
        **kwargs: Additional parameters passed to seaborn functions

    Returns:
        Matplotlib Figure object

    Raises:
        ValueError: If data is empty or has insufficient points
        KeyError: If required columns not found

    Example:
        >>> data = pd.DataFrame({
        ...     'height': [165, 170, 175, 180, 185],
        ...     'weight': [60, 65, 70, 75, 80]
        ... })
        >>> fig = create_plot(data, 'height', 'weight')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    if len(data) < 2:
        raise ValueError("Need at least 2 data points for regression")

    # Check required columns
    required_cols = [x, y]
    if style and style in data.columns:
        required_cols.append(style)

    for col in required_cols:
        if col not in data.columns:
            available = ", ".join(data.columns)
            raise KeyError(f"Column '{col}' not found. Available columns: {available}")

    # Remove any rows with NaN values in x or y columns
    clean_data = data[required_cols].dropna()

    if len(clean_data) < 2:
        raise ValueError("Need at least 2 non-null data points for regression")

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Create the regression plot using seaborn
    # This combines scatter plot with regression line
    sns.regplot(
        data=clean_data,
        x=x,
        y=y,
        scatter_kws={
            's': marker_size,
            'alpha': alpha,
            'color': marker_color,
            'label': 'Data points'
        },
        line_kws={
            'color': line_color,
            'linewidth': 2,
            'label': 'Regression line'
        },
        ci=confidence_level if show_confidence else None,
        ax=ax,
        **kwargs
    )

    # If style parameter is provided, overlay styled scatter plot
    if style and style in data.columns:
        # Clear the legend from regplot to avoid duplicates
        ax.legend().set_visible(False)

        # Create styled scatter plot
        sns.scatterplot(
            data=clean_data,
            x=x,
            y=y,
            style=style,
            s=marker_size,
            alpha=alpha,
            color=marker_color,
            ax=ax,
            legend='brief'
        )

    # Calculate regression statistics for display
    x_data = clean_data[x].values
    y_data = clean_data[y].values

    # Calculate regression coefficients
    coefficients = np.polyfit(x_data, y_data, 1)
    slope, intercept = coefficients
    poly_fn = np.poly1d(coefficients)

    # Calculate R-squared
    y_pred = poly_fn(x_data)
    ss_res = np.sum((y_data - y_pred) ** 2)
    ss_tot = np.sum((y_data - np.mean(y_data)) ** 2)
    r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0

    # Add equation and R² to plot
    equation_text = ""
    if show_equation:
        sign = "+" if intercept >= 0 else "-"
        equation_text = f"y = {slope:.3f}x {sign} {abs(intercept):.3f}"

    if show_r_squared:
        if equation_text:
            equation_text += f"\n"
        equation_text += f"R² = {r_squared:.4f}"

    if equation_text:
        # Position text in upper left with some padding
        ax.text(0.05, 0.95, equation_text,
               transform=ax.transAxes,
               fontsize=11,
               verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='gray'))

    # Styling
    ax.set_xlabel(xlabel or x, fontsize=12)
    ax.set_ylabel(ylabel or y, fontsize=12)

    if title:
        ax.set_title(title, fontsize=14, fontweight='bold')
    else:
        ax.set_title(f"Regression Analysis: {y} vs {x}", fontsize=14, fontweight='bold')

    # Enhance grid appearance (seaborn style)
    ax.grid(True, alpha=0.3, linestyle='--')

    # Add legend if not already visible
    if not (style and style in data.columns):
        # Custom legend with regression info
        handles, labels = ax.get_legend_handles_labels()
        if handles:
            ax.legend(handles[:2], ['Data points', 'Regression line'],
                     loc='lower right', framealpha=0.9)

    # Ensure axis labels don't overlap
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=0, ha='center')

    # Adjust layout
    plt.tight_layout()

    return fig


if __name__ == '__main__':
    # Sample data for testing - synthetic data with linear relationship
    np.random.seed(42)

    # Generate correlated data
    n_points = 50
    x_values = np.random.uniform(10, 100, n_points)
    # Create y values with linear relationship plus noise
    true_slope = 2.5
    true_intercept = 10
    noise = np.random.normal(0, 10, n_points)
    y_values = true_slope * x_values + true_intercept + noise

    # Add a categorical variable for demonstrating style parameter
    categories = np.random.choice(['Type A', 'Type B', 'Type C'], n_points)

    # Create DataFrame
    sample_data = pd.DataFrame({
        'Temperature (°C)': x_values,
        'Sales (units)': y_values,
        'Product Type': categories
    })

    # Create basic plot
    fig = create_plot(
        sample_data,
        x='Temperature (°C)',
        y='Sales (units)',
        title='Ice Cream Sales vs Temperature',
        xlabel='Temperature (°C)',
        ylabel='Sales (units)',
        marker_color='steelblue',
        line_color='darkred'
    )

    # Save for inspection
    plt.savefig('test_output_seaborn.png', dpi=150, bbox_inches='tight')
    print("Plot saved to test_output_seaborn.png")
    print(f"Sample data shape: {sample_data.shape}")

    # Calculate and display correlation
    correlation = sample_data[['Temperature (°C)', 'Sales (units)']].corr().iloc[0, 1]
    print(f"Correlation coefficient: {correlation:.4f}")

    # Create a second plot with style parameter
    fig2 = create_plot(
        sample_data,
        x='Temperature (°C)',
        y='Sales (units)',
        title='Ice Cream Sales vs Temperature (by Product Type)',
        style='Product Type',
        marker_color='navy',
        line_color='firebrick'
    )

    # Save second plot
    plt.savefig('test_output_seaborn_styled.png', dpi=150, bbox_inches='tight')
    print("Styled plot saved to test_output_seaborn_styled.png")

    # Show plots (optional)
    plt.show()