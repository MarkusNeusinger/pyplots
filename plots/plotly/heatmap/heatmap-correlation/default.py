"""
heatmap-correlation: Correlation Matrix Heatmap
Library: plotly
"""

import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import TYPE_CHECKING, Optional, Tuple

if TYPE_CHECKING:
    from plotly.graph_objects import Figure


def create_plot(
    data: pd.DataFrame,
    figsize: Optional[Tuple[float, float]] = None,
    cmap: Optional[str] = None,
    annot: bool = True,
    fmt: str = '.2f',
    mask_upper: bool = False,
    vmin: float = -1.0,
    vmax: float = 1.0,
    title: str = 'Correlation Matrix',
    **kwargs
) -> go.Figure:
    """
    Create a heatmap visualization of the correlation matrix for numerical columns in a dataset.

    Args:
        data: Input DataFrame with at least 2 numeric columns
        figsize: Figure size in inches (converted to pixels for plotly)
        cmap: Color map for the heatmap (plotly uses colorscale)
        annot: Show correlation values in cells
        fmt: Format string for annotations
        mask_upper: Mask the upper triangle for cleaner display
        vmin: Minimum value for color scale
        vmax: Maximum value for color scale
        title: Plot title
        **kwargs: Additional parameters

    Returns:
        Plotly Figure object

    Raises:
        ValueError: If data is empty or has fewer than 2 numeric columns

    Example:
        >>> data = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6], 'C': [7, 8, 9]})
        >>> fig = create_plot(data)
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    # Select only numeric columns
    numeric_data = data.select_dtypes(include=[np.number])

    if numeric_data.shape[1] < 2:
        raise ValueError(f"Data must have at least 2 numeric columns. Found: {numeric_data.shape[1]}")

    # Calculate correlation matrix
    corr_matrix = numeric_data.corr()

    # Apply upper triangle mask if requested
    if mask_upper:
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
        corr_display = corr_matrix.copy()
        corr_display[mask] = np.nan
    else:
        corr_display = corr_matrix

    # Prepare text annotations
    if annot:
        # Format correlation values for display
        text_values = []
        for i in range(len(corr_display)):
            row_text = []
            for j in range(len(corr_display.columns)):
                if pd.isna(corr_display.iloc[i, j]):
                    row_text.append('')
                else:
                    row_text.append(f'{corr_display.iloc[i, j]:{fmt}}')
            text_values.append(row_text)
    else:
        text_values = None

    # Set colorscale (default to RdBu_r which is similar to coolwarm)
    if cmap is None:
        colorscale = 'RdBu'
    else:
        # Map common matplotlib/seaborn colormap names to plotly equivalents
        colormap_mapping = {
            'coolwarm': 'RdBu',
            'seismic': 'RdBu',
            'bwr': 'RdBu',
            'viridis': 'Viridis',
            'plasma': 'Plasma',
            'inferno': 'Inferno',
            'magma': 'Magma',
            'cividis': 'Cividis',
            'turbo': 'Turbo',
            'twilight': 'Twilight'
        }
        colorscale = colormap_mapping.get(cmap, cmap)

    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=corr_display.values,
        x=corr_display.columns.tolist(),
        y=corr_display.index.tolist(),
        text=text_values,
        texttemplate='%{text}' if annot else None,
        textfont={'size': 10},
        colorscale=colorscale,
        zmin=vmin,
        zmax=vmax,
        colorbar=dict(
            title='Correlation',
            tickmode='linear',
            tick0=vmin,
            dtick=0.5,
            len=0.87,
            thickness=15
        ),
        hoverongaps=False,
        hovertemplate='%{x} - %{y}<br>Correlation: %{z:.2f}<extra></extra>'
    ))

    # Set figure size
    if figsize is not None:
        width = int(figsize[0] * 100)  # Convert inches to pixels (roughly)
        height = int(figsize[1] * 100)
    else:
        width = 1000  # Default width
        height = 800  # Default height

    # Update layout
    fig.update_layout(
        title=dict(
            text=title,
            x=0.5,
            xanchor='center',
            font=dict(size=16)
        ),
        xaxis=dict(
            title='',
            tickangle=45,
            side='bottom',
            showgrid=False,
            tickfont=dict(size=11)
        ),
        yaxis=dict(
            title='',
            showgrid=False,
            tickfont=dict(size=11),
            autorange='reversed'  # To match typical correlation matrix orientation
        ),
        width=width,
        height=height,
        template='plotly_white',
        margin=dict(l=100, r=100, t=100, b=100)
    )

    return fig


if __name__ == '__main__':
    # Sample data for testing
    np.random.seed(42)
    n_samples = 100

    # Create sample data with some correlations
    data = pd.DataFrame({
        'Temperature': np.random.normal(25, 5, n_samples),
        'Humidity': np.random.normal(60, 10, n_samples),
        'Pressure': np.random.normal(1013, 20, n_samples),
        'Wind_Speed': np.random.normal(10, 3, n_samples),
        'Rainfall': np.random.exponential(5, n_samples)
    })

    # Add some correlations
    data['Solar_Radiation'] = data['Temperature'] * 1.5 + np.random.normal(0, 2, n_samples)
    data['Heat_Index'] = data['Temperature'] * 0.8 + data['Humidity'] * 0.3 + np.random.normal(0, 3, n_samples)

    # Create plot
    fig = create_plot(
        data,
        figsize=(10, 8),
        cmap='coolwarm',
        annot=True,
        fmt='.2f',
        title='Weather Variables Correlation Matrix'
    )

    # Save - ALWAYS use 'plot.png'!
    fig.write_image('plot.png', width=1600, height=900, scale=2)
    print("Plot saved to plot.png")