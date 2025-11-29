"""
heatmap-correlation: Correlation Heatmap
Library: altair
"""

import altair as alt
import pandas as pd
import numpy as np
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from altair import Chart


def create_plot(
    data: pd.DataFrame,
    numeric_cols: Optional[List[str]] = None,
    method: str = 'pearson',
    cmap: str = 'blueorange',
    annot: bool = True,
    fmt: str = '.2f',
    vmin: float = -1,
    vmax: float = 1,
    mask_upper: bool = False,
    title: Optional[str] = None,
    **kwargs
) -> alt.Chart:
    """
    Create a correlation heatmap displaying the correlation matrix between numeric variables.

    Args:
        data: Input DataFrame with numeric columns to correlate
        numeric_cols: List of numeric columns to include. If None, all numeric columns are used
        method: Correlation method ('pearson', 'spearman', 'kendall'). Default: 'pearson'
        cmap: Colormap for the heatmap. Default: 'blueorange'
        annot: Whether to annotate cells with correlation values. Default: True
        fmt: Format string for annotations. Default: '.2f'
        vmin: Minimum value for colormap scale. Default: -1
        vmax: Maximum value for colormap scale. Default: 1
        mask_upper: Whether to mask the upper triangle. Default: False
        title: Optional title for the plot
        **kwargs: Additional parameters

    Returns:
        Altair Chart object

    Raises:
        ValueError: If data is empty or has insufficient numeric columns
        KeyError: If specified columns not found in DataFrame

    Example:
        >>> data = pd.DataFrame({
        ...     'A': np.random.randn(100),
        ...     'B': np.random.randn(100),
        ...     'C': np.random.randn(100)
        ... })
        >>> chart = create_plot(data, method='pearson')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    # Determine numeric columns to use
    if numeric_cols is None:
        numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    else:
        # Validate specified columns exist
        missing_cols = [col for col in numeric_cols if col not in data.columns]
        if missing_cols:
            available = ", ".join(data.columns)
            raise KeyError(f"Columns not found: {missing_cols}. Available: {available}")

        # Ensure specified columns are numeric
        non_numeric = []
        for col in numeric_cols:
            if not pd.api.types.is_numeric_dtype(data[col]):
                non_numeric.append(col)
        if non_numeric:
            raise ValueError(f"Non-numeric columns specified: {non_numeric}")

    # Check minimum requirements
    if len(numeric_cols) < 2:
        raise ValueError(f"At least 2 numeric columns required, found {len(numeric_cols)}")

    if len(data) < 3:
        import warnings
        warnings.warn("DataFrame has fewer than 3 rows - correlation may be unreliable")

    # Calculate correlation matrix
    corr_matrix = data[numeric_cols].corr(method=method)

    # Convert correlation matrix to long format for Altair
    corr_df = corr_matrix.reset_index()
    corr_df = corr_df.melt(id_vars='index', var_name='variable2', value_name='correlation')
    corr_df.rename(columns={'index': 'variable1'}, inplace=True)

    # Apply upper triangle mask if requested
    if mask_upper:
        # Create mask for upper triangle
        mask = []
        vars_list = numeric_cols
        for i, var1 in enumerate(vars_list):
            for j, var2 in enumerate(vars_list):
                mask.append(j >= i)  # Keep lower triangle and diagonal
        corr_df['mask'] = mask
        corr_df = corr_df[corr_df['mask']].drop(columns=['mask'])

    # Format correlation values for display
    corr_df['correlation_text'] = corr_df['correlation'].apply(lambda x: f"{x:{fmt}}")

    # Create base heatmap
    base = alt.Chart(corr_df).encode(
        x=alt.X('variable2:N', title=None, axis=alt.Axis(labelAngle=-45)),
        y=alt.Y('variable1:N', title=None)
    )

    # Create rect marks for heatmap
    heatmap = base.mark_rect().encode(
        color=alt.Color('correlation:Q',
                       scale=alt.Scale(scheme=cmap, domain=[vmin, vmax]),
                       legend=alt.Legend(title='Correlation'))
    )

    # Add text annotations if requested
    if annot:
        text = base.mark_text(baseline='middle').encode(
            text='correlation_text:N',
            color=alt.condition(
                alt.datum.correlation > 0.5,
                alt.value('white'),
                alt.value('black')
            )
        )
        chart = heatmap + text
    else:
        chart = heatmap

    # Set properties
    chart = chart.properties(
        width=800,
        height=800,  # Square aspect for correlation matrix
        title=title if title else f"Correlation Matrix ({method.capitalize()})"
    ).configure_axis(
        grid=False,
        labelFontSize=11,
        titleFontSize=12
    ).configure_legend(
        labelFontSize=10,
        titleFontSize=11
    )

    return chart


if __name__ == '__main__':
    # Sample data for testing
    np.random.seed(42)
    n_samples = 100

    # Create correlated data
    data = pd.DataFrame({
        'temperature': np.random.normal(20, 5, n_samples),
        'humidity': np.random.normal(60, 10, n_samples),
        'pressure': np.random.normal(1013, 20, n_samples),
        'wind_speed': np.random.normal(10, 3, n_samples),
        'rainfall': np.random.normal(50, 15, n_samples)
    })

    # Add some correlations
    data['humidity'] += 0.5 * data['temperature'] + np.random.normal(0, 2, n_samples)
    data['pressure'] -= 0.3 * data['temperature'] + np.random.normal(0, 5, n_samples)
    data['rainfall'] += 0.4 * data['humidity'] + np.random.normal(0, 3, n_samples)

    # Create plot
    chart = create_plot(
        data,
        method='pearson',
        annot=True,
        fmt='.2f'
    )

    # Save - ALWAYS use 'plot.png'!
    chart.save('plot.png', scale_factor=2.0)
    print("Plot saved to plot.png")