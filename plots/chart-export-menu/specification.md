# chart-export-menu: Chart with Built-in Export Menu

## Description

A chart with integrated export functionality that allows users to download the visualization in multiple formats (PNG, SVG, PDF) or extract the underlying data as CSV directly from an embedded menu control. The export menu appears as a hamburger icon or download button, providing a self-contained solution for sharing and documenting visualizations without requiring external tools or code modifications.

## Applications

- Report generation workflows where stakeholders need publication-ready chart images
- Presentation preparation requiring high-resolution vector exports for slides
- Data sharing scenarios where both visualization and raw data need to be distributed
- Documentation systems that embed charts with user-accessible download options

## Data

- `x` (numeric/categorical) - Independent variable or categories for the x-axis
- `y` (numeric) - Dependent variable or values to be plotted
- `series` (optional, categorical) - Group identifier for multiple data series
- Size: 10-500 data points (typical chart data)
- Example: Simple line chart or bar chart with sales data over time

## Notes

- Export menu button should be positioned in chart corner (typically top-right)
- Menu icon options: hamburger menu, download icon, or gear icon
- Supported formats: PNG (raster), SVG (vector), PDF (print), CSV (data)
- Include configurable export dimensions (width/height in pixels or inches)
- Option to include or exclude title and legend in exports
- Print-friendly preset with white background and optimized margins
- Interactive libraries (plotly, bokeh, highcharts, altair) have native export support
- Static libraries may require custom menu implementation or modebar configuration
