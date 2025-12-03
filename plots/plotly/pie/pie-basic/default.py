"""
pie-basic: Basic Pie Chart
Library: plotly
"""

from typing import TYPE_CHECKING

import pandas as pd
import plotly.graph_objects as go


if TYPE_CHECKING:
    pass

# PyPlots.ai color palette
PYPLOTS_COLORS = [
    "#306998",  # Python Blue
    "#FFD43B",  # Python Yellow
    "#DC2626",  # Signal Red
    "#059669",  # Teal Green
    "#8B5CF6",  # Violet
    "#F97316",  # Orange
]


def create_plot(
    data: pd.DataFrame,
    category: str,
    value: str,
    figsize: tuple[int, int] = (1600, 900),
    title: str | None = None,
    colors: list[str] | None = None,
    startangle: float = 90,
    autopct: str = "%1.1f%%",
    explode: list[float] | None = None,
    shadow: bool = False,
    labels: list[str] | None = None,
    legend: bool = True,
    legend_loc: str = "best",
    **kwargs,
) -> go.Figure:
    """
    Create a basic pie chart for categorical data composition.

    A fundamental pie chart that visualizes proportions and percentages of
    categorical data as slices of a circular chart. Each slice represents
    a category's share of the whole, making it ideal for showing composition
    and distribution across a small number of categories.

    Args:
        data: Input DataFrame containing the data to plot.
        category: Column name for category names (slice labels).
        value: Column name for numeric values (slice sizes).
        figsize: Figure size as (width, height) in pixels. Defaults to (1600, 900).
        title: Plot title. Defaults to None.
        colors: Custom color palette for slices. Defaults to PyPlots palette.
        startangle: Starting angle for first slice in degrees. Defaults to 90.
        autopct: Format string for percentage labels. Defaults to '%1.1f%%'.
        explode: Offset distances for each slice (0-0.1 typical). Defaults to None.
        shadow: Add shadow effect (not fully supported in Plotly). Defaults to False.
        labels: Custom labels (defaults to category names). Defaults to None.
        legend: Display legend. Defaults to True.
        legend_loc: Legend location (Plotly uses different positioning). Defaults to 'best'.
        **kwargs: Additional parameters passed to go.Pie.

    Returns:
        Plotly Figure object containing the pie chart.

    Raises:
        ValueError: If data is empty or contains negative values.
        KeyError: If required columns are not found in data.

    Example:
        >>> data = pd.DataFrame({
        ...     'category': ['Product A', 'Product B', 'Product C', 'Product D'],
        ...     'value': [35, 25, 20, 20]
        ... })
        >>> fig = create_plot(data, 'category', 'value', title='Market Share')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    for col in [category, value]:
        if col not in data.columns:
            available = ", ".join(data.columns)
            raise KeyError(f"Column '{col}' not found. Available: {available}")

    # Validate non-negative values
    if (data[value] < 0).any():
        raise ValueError("Pie chart values must be non-negative")

    # Handle case where all values sum to zero
    if data[value].sum() == 0:
        raise ValueError("Pie chart values cannot all be zero")

    # Get data values
    categories = labels if labels is not None else data[category].tolist()
    values = data[value].tolist()

    # Set colors - use custom colors or default PyPlots palette
    color_sequence = colors if colors is not None else PYPLOTS_COLORS
    # Extend colors if needed
    while len(color_sequence) < len(values):
        color_sequence = color_sequence + PYPLOTS_COLORS
    slice_colors = color_sequence[: len(values)]

    # Handle explode/pull parameter
    pull_values = explode if explode is not None else [0] * len(values)
    # Ensure pull_values has correct length
    if len(pull_values) < len(values):
        pull_values = list(pull_values) + [0] * (len(values) - len(pull_values))

    # Create figure
    fig = go.Figure()

    # Build texttemplate from autopct format
    # Convert matplotlib format to plotly format
    if "%%" in autopct:
        # Parse the format string - e.g., '%1.1f%%' -> '%{percent:.1%}'
        try:
            # Extract precision from format like '%1.1f%%'
            import re

            match = re.search(r"%(\d+)\.(\d+)f%%", autopct)
            if match:
                precision = int(match.group(2))
                text_template = f"%{{percent:.{precision}%}}"
            else:
                text_template = "%{percent:.1%}"
        except Exception:
            text_template = "%{percent:.1%}"
    else:
        text_template = "%{percent:.1%}"

    # Add pie trace
    fig.add_trace(
        go.Pie(
            labels=categories,
            values=values,
            marker={"colors": slice_colors, "line": {"color": "white", "width": 2}},
            textinfo="percent",
            texttemplate=text_template,
            textfont={"size": 14, "family": "Inter, DejaVu Sans, Arial, sans-serif"},
            textposition="inside",
            insidetextorientation="horizontal",
            pull=pull_values,
            rotation=startangle,
            showlegend=legend,
            hovertemplate="<b>%{label}</b><br>Value: %{value}<br>Percentage: %{percent}<extra></extra>",
            **kwargs,
        )
    )

    # Configure legend position based on legend_loc
    legend_config = {
        "font": {"size": 16, "family": "Inter, DejaVu Sans, Arial, sans-serif"},
        "bgcolor": "rgba(255, 255, 255, 1)",
        "bordercolor": "rgba(0, 0, 0, 0.3)",
        "borderwidth": 1,
    }

    # Map matplotlib legend locations to Plotly positions
    if legend_loc in ["right", "center right"]:
        legend_config.update({"x": 1.02, "y": 0.5, "xanchor": "left", "yanchor": "middle"})
    elif legend_loc in ["left", "center left"]:
        legend_config.update({"x": -0.15, "y": 0.5, "xanchor": "right", "yanchor": "middle"})
    elif legend_loc in ["upper right"]:
        legend_config.update({"x": 1.02, "y": 1, "xanchor": "left", "yanchor": "top"})
    elif legend_loc in ["upper left"]:
        legend_config.update({"x": -0.15, "y": 1, "xanchor": "right", "yanchor": "top"})
    elif legend_loc in ["lower right"]:
        legend_config.update({"x": 1.02, "y": 0, "xanchor": "left", "yanchor": "bottom"})
    elif legend_loc in ["lower left"]:
        legend_config.update({"x": -0.15, "y": 0, "xanchor": "right", "yanchor": "bottom"})
    else:
        # Default 'best' - place on the right
        legend_config.update({"x": 1.02, "y": 0.5, "xanchor": "left", "yanchor": "middle"})

    # Update layout with styling
    fig.update_layout(
        title={
            "text": title,
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 20, "family": "Inter, DejaVu Sans, Arial, sans-serif", "weight": 600},
        }
        if title
        else None,
        template="plotly_white",
        width=figsize[0],
        height=figsize[1],
        showlegend=legend,
        legend=legend_config if legend else None,
        margin={"l": 40, "r": 150 if legend else 40, "t": 80 if title else 40, "b": 40},
        paper_bgcolor="white",
        plot_bgcolor="white",
    )

    # Ensure pie chart is circular (equal aspect ratio)
    fig.update_layout(yaxis={"scaleanchor": "x", "scaleratio": 1})

    return fig


if __name__ == "__main__":
    # Sample data for testing
    sample_data = pd.DataFrame(
        {"category": ["Product A", "Product B", "Product C", "Product D", "Other"], "value": [35, 25, 20, 15, 5]}
    )

    # Create plot
    fig = create_plot(sample_data, "category", "value", title="Market Share Distribution")

    # Save
    fig.write_image("plot.png", width=1600, height=900, scale=2)
    print("Plot saved to plot.png")
