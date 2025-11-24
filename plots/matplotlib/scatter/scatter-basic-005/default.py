"""
scatter-basic-005: Regression Line Scatter Plot
Implementation for: matplotlib
Variant: default
Python: 3.10+
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import TYPE_CHECKING, Optional, Tuple

if TYPE_CHECKING:
    from matplotlib.figure import Figure


def create_plot(
    data: pd.DataFrame,
    x: str,
    y: str,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    marker_color: str = "blue",
    line_color: str = "red",
    marker_size: float = 50,
    alpha: float = 0.6,
    show_confidence: bool = True,
    confidence_level: float = 0.95,
    show_equation: bool = True,
    show_r_squared: bool = True,
    figsize: Tuple[float, float] = (10, 6),
    **kwargs
) -> "Figure":
    """
    Create a scatter plot with fitted regression line and regression quality metrics.

    Args:
        data: Input DataFrame with required columns
        x: Column name for x-axis values
        y: Column name for y-axis values
        title: Plot title (optional, defaults to descriptive title)
        xlabel: X-axis label (optional, defaults to column name)
        ylabel: Y-axis label (optional, defaults to column name)
        marker_color: Color for scatter points (default: "blue")
        line_color: Color for regression line (default: "red")
        marker_size: Size of scatter points (default: 50)
        alpha: Transparency for points (default: 0.6)
        show_confidence: Whether to show confidence interval (default: True)
        confidence_level: Confidence level for interval (default: 0.95)
        show_equation: Whether to show regression equation (default: True)
        show_r_squared: Whether to show R² value (default: True)
        figsize: Figure size as (width, height) tuple (default: (10, 6))
        **kwargs: Additional parameters passed to scatter function

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
    for col in [x, y]:
        if col not in data.columns:
            available = ", ".join(data.columns)
            raise KeyError(f"Column '{col}' not found. Available columns: {available}")

    # Remove any rows with NaN values in x or y columns
    clean_data = data[[x, y]].dropna()

    if len(clean_data) < 2:
        raise ValueError("Need at least 2 non-null data points for regression")

    # Extract data
    x_data = clean_data[x].values
    y_data = clean_data[y].values

    # Calculate regression
    coefficients = np.polyfit(x_data, y_data, 1)
    slope, intercept = coefficients
    poly_fn = np.poly1d(coefficients)

    # Calculate R-squared
    y_pred = poly_fn(x_data)
    ss_res = np.sum((y_data - y_pred) ** 2)
    ss_tot = np.sum((y_data - np.mean(y_data)) ** 2)
    r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Plot scatter points
    scatter = ax.scatter(x_data, y_data, s=marker_size, alpha=alpha,
                        color=marker_color, label='Data points', **kwargs)

    # Plot regression line
    x_range = np.linspace(x_data.min(), x_data.max(), 100)
    y_regression = poly_fn(x_range)
    ax.plot(x_range, y_regression, color=line_color, linewidth=2,
            label='Regression line', zorder=5)

    # Add confidence interval if requested
    if show_confidence and len(x_data) > 2:
        # Calculate standard error
        n = len(x_data)
        se = np.sqrt(ss_res / (n - 2))

        # Calculate confidence interval
        from scipy import stats
        t_val = stats.t.ppf((1 + confidence_level) / 2, n - 2)

        # Simplified confidence band (approximate)
        x_mean = np.mean(x_data)
        sx = np.sqrt(np.sum((x_data - x_mean) ** 2) / (n - 1))

        confidence_margin = t_val * se * np.sqrt(1/n + (x_range - x_mean)**2 / ((n-1) * sx**2))

        ax.fill_between(x_range,
                        y_regression - confidence_margin,
                        y_regression + confidence_margin,
                        alpha=0.2, color=line_color,
                        label=f'{int(confidence_level*100)}% Confidence interval')

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
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    # Styling
    ax.set_xlabel(xlabel or x, fontsize=12)
    ax.set_ylabel(ylabel or y, fontsize=12)

    if title:
        ax.set_title(title, fontsize=14, fontweight='bold')
    else:
        ax.set_title(f"Regression Analysis: {y} vs {x}", fontsize=14, fontweight='bold')

    # Add grid
    ax.grid(True, alpha=0.3, linestyle='--')

    # Add legend
    ax.legend(loc='lower right', framealpha=0.9)

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

    # Create DataFrame
    sample_data = pd.DataFrame({
        'Temperature (°C)': x_values,
        'Sales (units)': y_values
    })

    # Create plot
    fig = create_plot(
        sample_data,
        x='Temperature (°C)',
        y='Sales (units)',
        title='Ice Cream Sales vs Temperature',
        xlabel='Temperature (°C)',
        ylabel='Sales (units)',
        marker_color='dodgerblue',
        line_color='crimson'
    )

    # Save for inspection
    plt.savefig('test_output.png', dpi=150, bbox_inches='tight')
    print("Plot saved to test_output.png")
    print(f"Sample data shape: {sample_data.shape}")
    print(f"Correlation coefficient: {sample_data.corr().iloc[0, 1]:.4f}")

    # Show plot (optional)
    plt.show()