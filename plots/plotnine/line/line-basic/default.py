"""
line-basic: Basic Line Chart
Library: plotnine

A fundamental line chart that visualizes trends and patterns in data over a continuous axis.
"""

import pandas as pd
from plotnine import aes, geom_line, geom_point, ggplot, labs, theme, theme_minimal
from plotnine.ggplot import ggplot as ggplot_type
from plotnine.themes.elements import element_line, element_text


# Style guide colors (PyPlots default palette)
PYPLOTS_COLORS = ["#306998", "#FFD43B", "#DC2626", "#059669", "#8B5CF6", "#F97316"]
DEFAULT_COLOR = "#306998"  # Python Blue


def create_plot(
    data: pd.DataFrame,
    x: str,
    y: str,
    color: str = DEFAULT_COLOR,
    linewidth: float = 2.0,
    marker: str | None = None,
    marker_size: float = 4.0,
    alpha: float = 1.0,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    linestyle: str = "solid",
    **kwargs,
) -> ggplot_type:
    """
    Create a basic line chart to visualize trends and patterns in data.

    Args:
        data: Input DataFrame containing the data to plot
        x: Column name for x-axis values (typically time or sequence)
        y: Column name for y-axis values
        color: Line color (default: "#306998" - Python Blue)
        linewidth: Width of the line (default: 2.0)
        marker: Marker style for data points (default: None)
        marker_size: Size of markers if enabled (default: 4.0)
        alpha: Transparency level for the line (default: 1.0)
        title: Plot title (default: None)
        xlabel: X-axis label (default: uses column name)
        ylabel: Y-axis label (default: uses column name)
        linestyle: Line style - "solid", "dashed", "dotted", "dashdot" (default: "solid")
        **kwargs: Additional parameters passed to geom_line

    Returns:
        plotnine ggplot object

    Raises:
        ValueError: If data is empty
        KeyError: If required columns not found in data

    Example:
        >>> data = pd.DataFrame({'month': [1, 2, 3], 'sales': [100, 150, 130]})
        >>> fig = create_plot(data, 'month', 'sales')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    for col in [x, y]:
        if col not in data.columns:
            available = ", ".join(data.columns)
            raise KeyError(f"Column '{col}' not found. Available: {available}")

    # Create a copy and sort by x-axis values for proper line connections
    plot_data = data.copy()
    plot_data = plot_data.sort_values(by=x)

    # Handle NaN values - drop rows with NaN in x or y columns
    plot_data = plot_data.dropna(subset=[x, y])

    # Set labels
    x_label = xlabel if xlabel is not None else x
    y_label = ylabel if ylabel is not None else y

    # Map linestyle to plotnine compatible format
    linetype_map = {
        "solid": "solid",
        "-": "solid",
        "dashed": "dashed",
        "--": "dashed",
        "dotted": "dotted",
        ":": "dotted",
        "dashdot": "dashdot",
        "-.": "dashdot",
    }
    linetype = linetype_map.get(linestyle, "solid")

    # Create base plot with line
    plot = (
        ggplot(plot_data, aes(x=x, y=y))
        + geom_line(color=color, size=linewidth, alpha=alpha, linetype=linetype, **kwargs)
        + labs(x=x_label, y=y_label, title=title if title else "")
        + theme_minimal()
        + theme(
            # Figure size: 4800x2700 px at 300 dpi = 16x9 inches
            figure_size=(16, 9),
            # Typography per style guide
            plot_title=element_text(size=20, ha="center"),
            axis_title=element_text(size=20),
            axis_text=element_text(size=16),
            legend_text=element_text(size=16),
            # Grid styling - subtle per spec (alpha <= 0.3)
            panel_grid_major=element_line(color="#E5E5E5", size=0.5, alpha=0.3),
            panel_grid_minor=element_line(color="#F0F0F0", size=0.25, alpha=0.2),
        )
    )

    # Add markers if specified
    if marker is not None:
        plot = plot + geom_point(color=color, size=marker_size, alpha=alpha)

    return plot


if __name__ == "__main__":
    # Sample data for testing - monthly sales trend
    sample_data = pd.DataFrame(
        {
            "month": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            "sales": [100, 150, 130, 180, 200, 190, 220, 240, 210, 250, 280, 300],
        }
    )

    # Create plot with custom styling
    fig = create_plot(
        sample_data,
        x="month",
        y="sales",
        title="Monthly Sales Trend",
        xlabel="Month",
        ylabel="Sales ($)",
        linewidth=2.5,
        marker="o",
        marker_size=4,
    )

    # Save - ALWAYS use 'plot.png'!
    fig.save("plot.png", dpi=300, width=16, height=9)
    print("Plot saved to plot.png")
