# Plot Types Catalog

A comprehensive catalog of plot types for the pyplots platform. Each entry includes the recommended library, a brief description of a basic implementation, and a suggested spec ID.

## Supported Libraries

| Library | Strength | Best For |
|---------|----------|----------|
| **Matplotlib** | Flexibility, customization | Static plots, publication-quality figures, custom layouts |
| **Seaborn** | Statistical visualization | Distributions, relationships, categorical data |
| **Plotly** | Interactivity, web | Dashboards, 3D plots, animations |
| **Bokeh** | Large datasets, streaming | Real-time data, big data visualization |
| **Altair** | Declarative, exploratory | Quick exploration, academic use |
| **Plotnine** | ggplot2 syntax | R users, grammar of graphics |
| **Pygal** | SVG output, minimalistic | Embeddable SVG charts, simple dashboards |
| **Highcharts** | Professional web charts | Stock charts, drilldown, enterprise dashboards |

---

## 1. Scatter Plots

### scatter-basic
**Best Library:** Matplotlib
**Description:** Simple 2D scatter plot showing relationship between two numeric variables. X-axis and Y-axis with circular markers.
**Basic Chart:** 50-100 random points, default blue color, no legend needed.

### scatter-color-mapped
**Best Library:** Matplotlib
**Description:** Scatter plot with a third variable encoded as color using a colormap. Includes colorbar.
**Basic Chart:** Points colored by a continuous variable (e.g., temperature), viridis colormap.

### scatter-size-mapped
**Best Library:** Matplotlib
**Description:** Bubble chart where marker size represents a third variable.
**Basic Chart:** Points with varying sizes based on a value column, semi-transparent markers.

### scatter-categorical
**Best Library:** Seaborn
**Description:** Scatter plot with points colored by category.
**Basic Chart:** Two categories (A, B) with distinct colors, legend included.

### scatter-regression
**Best Library:** Seaborn
**Description:** Scatter plot with linear regression line and confidence interval.
**Basic Chart:** Points with fitted line, shaded 95% CI region.

### scatter-marginal
**Best Library:** Seaborn (jointplot)
**Description:** Scatter plot with marginal histograms or KDE on axes.
**Basic Chart:** Central scatter with histogram distributions on top and right margins.

### scatter-3d
**Best Library:** Plotly
**Description:** Three-dimensional scatter plot with rotation capability.
**Basic Chart:** Points in 3D space, interactive rotation, basic axis labels.

### scatter-matrix
**Best Library:** Seaborn (pairplot)
**Description:** Grid of scatter plots for all variable pairs in a dataset.
**Basic Chart:** 3-4 variables, diagonal shows histograms, off-diagonal shows scatter.

---

## 2. Line Plots

### line-basic
**Best Library:** Matplotlib
**Description:** Simple line connecting data points in order.
**Basic Chart:** Single line, 20-30 points, solid line style.

### line-multi
**Best Library:** Matplotlib
**Description:** Multiple lines on the same axes for comparison.
**Basic Chart:** 3 lines with different colors, legend included.

### line-styled
**Best Library:** Matplotlib
**Description:** Line plot with different line styles (solid, dashed, dotted).
**Basic Chart:** 3 lines with distinct styles, useful for black-and-white printing.

### line-markers
**Best Library:** Matplotlib
**Description:** Line plot with visible markers at data points.
**Basic Chart:** Line with circular markers, helpful for sparse data.

### line-timeseries
**Best Library:** Matplotlib
**Description:** Line plot with datetime x-axis and proper date formatting.
**Basic Chart:** 12 months of data, month labels on x-axis.

### line-stepwise
**Best Library:** Matplotlib
**Description:** Step function plot (horizontal then vertical transitions).
**Basic Chart:** Step plot showing discrete changes, common for cumulative data.

### line-filled
**Best Library:** Matplotlib
**Description:** Line plot with area filled to baseline.
**Basic Chart:** Single line with shaded area below, semi-transparent fill.

### line-confidence
**Best Library:** Seaborn (lineplot)
**Description:** Line plot with confidence interval band.
**Basic Chart:** Mean line with shaded 95% CI, common for aggregated data.

### line-interactive
**Best Library:** Plotly
**Description:** Line plot with hover tooltips and zoom.
**Basic Chart:** Interactive line with data point details on hover.

---

## 3. Bar Charts

### bar-basic
**Best Library:** Matplotlib
**Description:** Vertical bars representing categorical values.
**Basic Chart:** 5-7 categories, single color, value labels optional.

### bar-horizontal
**Best Library:** Matplotlib
**Description:** Horizontal bars, useful for long category names.
**Basic Chart:** 5-7 categories with readable labels on y-axis.

### bar-grouped
**Best Library:** Matplotlib
**Description:** Side-by-side bars for comparing groups within categories.
**Basic Chart:** 4 categories, 2 groups each, legend for group names.

### bar-stacked
**Best Library:** Matplotlib
**Description:** Bars stacked on top of each other showing composition.
**Basic Chart:** 4 categories, 3 components stacked, legend included.

### bar-stacked-percent
**Best Library:** Matplotlib
**Description:** Stacked bars normalized to 100% showing proportions.
**Basic Chart:** Each bar totals 100%, shows relative composition.

### bar-error
**Best Library:** Matplotlib
**Description:** Bar chart with error bars showing uncertainty.
**Basic Chart:** Bars with symmetric error bars, cap lines.

### bar-sorted
**Best Library:** Seaborn
**Description:** Bar chart with categories sorted by value.
**Basic Chart:** Descending order, highlights ranking.

### bar-categorical
**Best Library:** Seaborn (countplot)
**Description:** Bar chart showing count of observations per category.
**Basic Chart:** Counts of categorical variable, no aggregation needed.

### bar-diverging
**Best Library:** Matplotlib
**Description:** Bars extending from center, positive/negative values.
**Basic Chart:** Centered at zero, different colors for positive/negative.

### bar-lollipop
**Best Library:** Matplotlib
**Description:** Minimalist bar chart with line and dot instead of full bar.
**Basic Chart:** Vertical lines with circular markers at top.

### bar-interactive
**Best Library:** Plotly
**Description:** Bar chart with hover details and click interactions.
**Basic Chart:** Hoverable bars showing exact values.

---

## 4. Histograms

### histogram-basic
**Best Library:** Matplotlib
**Description:** Frequency distribution of a single numeric variable.
**Basic Chart:** 20-30 bins, single color, y-axis shows count.

### histogram-normalized
**Best Library:** Matplotlib
**Description:** Histogram normalized to show density instead of count.
**Basic Chart:** Area sums to 1, suitable for probability comparison.

### histogram-overlapping
**Best Library:** Matplotlib
**Description:** Multiple overlapping histograms for comparison.
**Basic Chart:** 2 distributions, semi-transparent, different colors.

### histogram-stacked
**Best Library:** Matplotlib
**Description:** Stacked histograms showing combined distribution.
**Basic Chart:** 2-3 groups stacked, shows total and composition.

### histogram-stepwise
**Best Library:** Matplotlib
**Description:** Histogram with step outline only (no filled bars).
**Basic Chart:** Unfilled steps, good for overlapping distributions.

### histogram-kde
**Best Library:** Seaborn
**Description:** Histogram with kernel density estimate overlay.
**Basic Chart:** Bars with smooth KDE curve on top.

### histogram-2d
**Best Library:** Matplotlib
**Description:** Two-dimensional histogram as heatmap.
**Basic Chart:** Grid of bins colored by count, colorbar included.

### histogram-cumulative
**Best Library:** Matplotlib
**Description:** Cumulative distribution function as histogram.
**Basic Chart:** Step histogram showing cumulative proportion.

---

## 5. Pie & Donut Charts

### pie-basic
**Best Library:** Matplotlib
**Description:** Circular chart divided into proportional slices.
**Basic Chart:** 4-6 slices, percentage labels, legend.

### pie-exploded
**Best Library:** Matplotlib
**Description:** Pie chart with one or more slices pulled out.
**Basic Chart:** One slice offset to highlight, shadow optional.

### donut-basic
**Best Library:** Matplotlib
**Description:** Pie chart with hollow center.
**Basic Chart:** Ring chart, can display total in center.

### donut-nested
**Best Library:** Matplotlib
**Description:** Multiple concentric donut rings.
**Basic Chart:** 2 rings showing hierarchical data.

### sunburst
**Best Library:** Plotly
**Description:** Multi-level hierarchical pie chart.
**Basic Chart:** 2-3 levels of hierarchy, interactive drill-down.

---

## 6. Box Plots & Distributions

### box-basic
**Best Library:** Matplotlib
**Description:** Box and whisker plot showing distribution summary.
**Basic Chart:** Single box showing median, quartiles, whiskers, outliers.

### box-grouped
**Best Library:** Seaborn
**Description:** Multiple box plots grouped by category.
**Basic Chart:** 3-4 categories, boxes side by side.

### box-horizontal
**Best Library:** Matplotlib
**Description:** Horizontal box plot orientation.
**Basic Chart:** Boxes extending left to right.

### box-notched
**Best Library:** Matplotlib
**Description:** Box plot with notches indicating median confidence.
**Basic Chart:** Notched boxes, overlapping notches suggest similar medians.

### violin-basic
**Best Library:** Seaborn
**Description:** Distribution plot showing density shape.
**Basic Chart:** Symmetric violin shape, wider where more data.

### violin-split
**Best Library:** Seaborn
**Description:** Half-violins comparing two groups.
**Basic Chart:** Two halves showing different categories.

### violin-box
**Best Library:** Seaborn
**Description:** Violin plot with embedded box plot.
**Basic Chart:** Violin with mini box inside showing quartiles.

### strip-basic
**Best Library:** Seaborn
**Description:** Individual points plotted along category axis.
**Basic Chart:** Jittered points showing actual data distribution.

### swarm-basic
**Best Library:** Seaborn
**Description:** Non-overlapping point distribution plot.
**Basic Chart:** Points arranged to avoid overlap, shows density.

### ridge-basic
**Best Library:** Seaborn (ridgeplot via kdeplot)
**Description:** Overlapping density plots for multiple categories.
**Basic Chart:** Staggered KDE curves, mountain range appearance.

### ecdf-basic
**Best Library:** Seaborn
**Description:** Empirical cumulative distribution function.
**Basic Chart:** Step function from 0 to 1, shows data percentiles.

---

## 7. Heatmaps

### heatmap-basic
**Best Library:** Seaborn
**Description:** 2D matrix visualization with color encoding.
**Basic Chart:** Grid of colored cells, colorbar, axis labels.

### heatmap-annotated
**Best Library:** Seaborn
**Description:** Heatmap with values displayed in cells.
**Basic Chart:** Numbers overlaid on colored cells.

### heatmap-correlation
**Best Library:** Seaborn
**Description:** Correlation matrix visualization.
**Basic Chart:** Symmetric matrix, diverging colormap, -1 to 1 range.

### heatmap-clustered
**Best Library:** Seaborn (clustermap)
**Description:** Heatmap with hierarchical clustering dendrograms.
**Basic Chart:** Reordered rows/columns, dendrograms on sides.

### heatmap-calendar
**Best Library:** Matplotlib
**Description:** Calendar-style heatmap for daily data.
**Basic Chart:** Weeks as rows, days as columns, GitHub-style.

### heatmap-interactive
**Best Library:** Plotly
**Description:** Heatmap with hover values and zoom.
**Basic Chart:** Interactive cells showing exact values.

---

## 8. Area Charts

### area-basic
**Best Library:** Matplotlib
**Description:** Filled area under a line.
**Basic Chart:** Single series, solid fill to baseline.

### area-stacked
**Best Library:** Matplotlib
**Description:** Multiple areas stacked showing cumulative total.
**Basic Chart:** 3-4 series, areas on top of each other.

### area-stacked-percent
**Best Library:** Matplotlib
**Description:** Stacked areas normalized to 100%.
**Basic Chart:** Shows proportion changes over time.

### area-stream
**Best Library:** Matplotlib
**Description:** Streamgraph with symmetric baseline.
**Basic Chart:** Flowing organic shapes, centered around middle.

### area-between
**Best Library:** Matplotlib
**Description:** Filled area between two lines.
**Basic Chart:** Upper and lower bounds with fill between.

---

## 9. Polar & Radar Charts

### polar-scatter
**Best Library:** Matplotlib
**Description:** Scatter plot in polar coordinates.
**Basic Chart:** Points plotted by angle and radius.

### polar-line
**Best Library:** Matplotlib
**Description:** Line plot in polar coordinates.
**Basic Chart:** Closed or open curve around center.

### polar-bar
**Best Library:** Matplotlib
**Description:** Bar chart arranged in a circle.
**Basic Chart:** Bars radiating from center, also called wind rose.

### radar-basic
**Best Library:** Matplotlib
**Description:** Multi-axis chart for comparing across dimensions.
**Basic Chart:** 5-6 axes, single polygon, filled area.

### radar-multi
**Best Library:** Matplotlib
**Description:** Multiple overlapping radar polygons.
**Basic Chart:** 2-3 subjects compared, semi-transparent fills.

---

## 10. Statistical Plots

### regression-linear
**Best Library:** Seaborn
**Description:** Scatter with linear regression fit.
**Basic Chart:** Points, fitted line, confidence band.

### regression-polynomial
**Best Library:** Seaborn
**Description:** Non-linear regression curve fit.
**Basic Chart:** Points with curved fit line.

### regression-lowess
**Best Library:** Seaborn
**Description:** Locally weighted regression smoothing.
**Basic Chart:** Smooth non-parametric curve through points.

### residual-basic
**Best Library:** Seaborn (residplot)
**Description:** Residual plot for regression diagnostics.
**Basic Chart:** Residuals vs fitted values, centered at zero.

### qq-plot
**Best Library:** Matplotlib (scipy.stats)
**Description:** Quantile-quantile plot for distribution comparison.
**Basic Chart:** Points along diagonal if normal distribution.

### bland-altman
**Best Library:** Matplotlib
**Description:** Agreement plot between two measurements.
**Basic Chart:** Difference vs mean, with limits of agreement.

### error-bar
**Best Library:** Matplotlib
**Description:** Points with error bars showing uncertainty.
**Basic Chart:** Central values with symmetric error bars.

### error-asymmetric
**Best Library:** Matplotlib
**Description:** Error bars with different upper/lower bounds.
**Basic Chart:** Asymmetric error bars, common for log-scale data.

---

## 11. Categorical Plots

### count-basic
**Best Library:** Seaborn
**Description:** Bar chart of category counts.
**Basic Chart:** Automatic counting of categorical variable.

### point-basic
**Best Library:** Seaborn (pointplot)
**Description:** Point estimates with confidence intervals.
**Basic Chart:** Points with error bars, connected by lines.

### cat-strip
**Best Library:** Seaborn
**Description:** Categorical scatter plot.
**Basic Chart:** Points distributed along category axis.

### cat-box-strip
**Best Library:** Seaborn
**Description:** Combined box plot with overlaid strip plot.
**Basic Chart:** Box shows summary, points show individual data.

---

## 12. Matrix & Grid Plots

### facet-grid
**Best Library:** Seaborn (FacetGrid)
**Description:** Grid of plots split by categorical variables.
**Basic Chart:** 2x2 grid of scatter plots by category.

### pair-plot
**Best Library:** Seaborn
**Description:** All pairwise relationships in dataset.
**Basic Chart:** Scatter matrix with histograms on diagonal.

### subplot-grid
**Best Library:** Matplotlib
**Description:** Custom grid of different plot types.
**Basic Chart:** 2x2 grid with varied content.

### mosaic-layout
**Best Library:** Matplotlib
**Description:** Complex subplot layout with varying sizes.
**Basic Chart:** Mix of large and small panels.

---

## 13. Time Series Plots

### timeseries-single
**Best Library:** Matplotlib
**Description:** Single time series with proper date axis.
**Basic Chart:** Line plot with datetime x-axis.

### timeseries-multi
**Best Library:** Matplotlib
**Description:** Multiple time series for comparison.
**Basic Chart:** Several lines with shared time axis.

### timeseries-decomposition
**Best Library:** Matplotlib
**Description:** Trend, seasonal, residual components.
**Basic Chart:** Stacked subplots showing decomposition.

### timeseries-rolling
**Best Library:** Matplotlib
**Description:** Time series with rolling average overlay.
**Basic Chart:** Raw data with smoothed line.

### timeseries-candlestick
**Best Library:** Plotly
**Description:** OHLC candlestick chart for financial data.
**Basic Chart:** Candlesticks showing open, high, low, close.

### timeseries-ohlc
**Best Library:** Plotly
**Description:** Open-high-low-close bar chart.
**Basic Chart:** Vertical bars with tick marks for OHLC.

### timeseries-forecast
**Best Library:** Matplotlib
**Description:** Historical data with forecast and uncertainty.
**Basic Chart:** Solid history, dashed forecast, shaded prediction interval.

---

## 14. Geographic & Spatial

### map-choropleth
**Best Library:** Plotly
**Description:** Map with regions colored by value.
**Basic Chart:** Country or state map with color scale.

### map-scatter
**Best Library:** Plotly
**Description:** Points plotted on geographic map.
**Basic Chart:** Markers at lat/lon coordinates.

### map-bubble
**Best Library:** Plotly
**Description:** Map with sized circles at locations.
**Basic Chart:** Bubble size represents value.

### map-heatmap
**Best Library:** Plotly
**Description:** Density heatmap on geographic background.
**Basic Chart:** Color intensity shows point density.

### map-lines
**Best Library:** Plotly
**Description:** Connection lines between locations.
**Basic Chart:** Great circle arcs connecting points.

---

## 15. 3D Plots

### surface-3d
**Best Library:** Plotly
**Description:** 3D surface plot from grid data.
**Basic Chart:** Wireframe or solid surface, colormap.

### wireframe-3d
**Best Library:** Matplotlib
**Description:** 3D wireframe mesh plot.
**Basic Chart:** Grid lines forming surface shape.

### contour-3d
**Best Library:** Matplotlib
**Description:** 3D contour plot.
**Basic Chart:** Stacked contour lines in 3D space.

### bar-3d
**Best Library:** Matplotlib
**Description:** 3D bar chart.
**Basic Chart:** Bars in 3D space, depth perspective.

### line-3d
**Best Library:** Matplotlib
**Description:** 3D line plot or trajectory.
**Basic Chart:** Line winding through 3D space.

---

## 16. Contour Plots

### contour-basic
**Best Library:** Matplotlib
**Description:** 2D contour lines showing elevation.
**Basic Chart:** Smooth curves of equal value, labeled.

### contour-filled
**Best Library:** Matplotlib
**Description:** Filled contour regions.
**Basic Chart:** Color-filled regions between contour levels.

### contour-density
**Best Library:** Seaborn (kdeplot)
**Description:** Contour plot from point density.
**Basic Chart:** KDE contours showing concentration.

---

## 17. Network & Graph Plots

### network-basic
**Best Library:** Matplotlib (networkx)
**Description:** Node-link diagram for graph data.
**Basic Chart:** Nodes as circles, edges as lines.

### network-directed
**Best Library:** Matplotlib (networkx)
**Description:** Directed graph with arrows.
**Basic Chart:** Arrows showing edge direction.

### network-weighted
**Best Library:** Matplotlib (networkx)
**Description:** Graph with edge thickness by weight.
**Basic Chart:** Varying line widths represent edge weights.

### network-hierarchical
**Best Library:** Matplotlib (networkx)
**Description:** Tree or hierarchy layout.
**Basic Chart:** Top-down or radial tree structure.

### chord-diagram
**Best Library:** Plotly
**Description:** Circular flow diagram between categories.
**Basic Chart:** Arcs connecting related categories.

### sankey-basic
**Best Library:** Plotly
**Description:** Flow diagram showing quantities between stages.
**Basic Chart:** Nodes with flowing connections.

---

## 18. Tree & Hierarchical

### treemap-basic
**Best Library:** Plotly
**Description:** Nested rectangles showing hierarchy.
**Basic Chart:** Rectangles sized by value, nested by category.

### dendrogram-basic
**Best Library:** Matplotlib (scipy)
**Description:** Tree diagram from hierarchical clustering.
**Basic Chart:** Branching tree structure.

### icicle-basic
**Best Library:** Plotly
**Description:** Rectangular hierarchy visualization.
**Basic Chart:** Stacked rectangles showing levels.

### circle-packing
**Best Library:** Matplotlib
**Description:** Nested circles showing hierarchy.
**Basic Chart:** Circles within circles by group.

---

## 19. Part-to-Whole

### waffle-basic
**Best Library:** Matplotlib
**Description:** Grid of squares showing proportions.
**Basic Chart:** 10x10 grid with colored squares.

### parliament-basic
**Best Library:** Matplotlib
**Description:** Semicircular parliament seat chart.
**Basic Chart:** Half-circle of seats colored by party.

### gauge-basic
**Best Library:** Plotly
**Description:** Speedometer-style gauge chart.
**Basic Chart:** Semicircle with needle indicator.

### bullet-basic
**Best Library:** Matplotlib
**Description:** Bullet graph for performance metrics.
**Basic Chart:** Bar with background ranges and target marker.

---

## 20. Animation & Interactive

### animation-line
**Best Library:** Matplotlib (FuncAnimation)
**Description:** Animated line plot building over time.
**Basic Chart:** Line drawing progressively.

### animation-scatter
**Best Library:** Plotly
**Description:** Animated scatter with play button.
**Basic Chart:** Points moving over time frames.

### animation-bar
**Best Library:** Plotly
**Description:** Bar chart race animation.
**Basic Chart:** Bars growing and reordering.

### slider-basic
**Best Library:** Plotly
**Description:** Plot with slider control.
**Basic Chart:** Slider adjusts displayed data range.

### brush-zoom
**Best Library:** Bokeh
**Description:** Plot with brush selection and zoom.
**Basic Chart:** Selectable and zoomable scatter plot.

### linked-views
**Best Library:** Bokeh
**Description:** Multiple plots with linked selection.
**Basic Chart:** Selecting points in one plot highlights in others.

---

## 21. Specialized Plots

### waterfall-basic
**Best Library:** Matplotlib
**Description:** Running total with positive/negative contributions.
**Basic Chart:** Floating bars showing incremental changes.

### funnel-basic
**Best Library:** Plotly
**Description:** Funnel chart for conversion stages.
**Basic Chart:** Progressively narrowing sections.

### pyramid-basic
**Best Library:** Matplotlib
**Description:** Population pyramid (back-to-back horizontal bars).
**Basic Chart:** Two groups extending from center.

### slope-basic
**Best Library:** Matplotlib
**Description:** Slope chart comparing two time points.
**Basic Chart:** Lines connecting start and end values.

### bump-basic
**Best Library:** Matplotlib
**Description:** Ranking changes over time.
**Basic Chart:** Lines showing rank position changes.

### dumbbell-basic
**Best Library:** Matplotlib
**Description:** Two points connected by line for before/after.
**Basic Chart:** Dot-line-dot showing change.

### span-basic
**Best Library:** Matplotlib
**Description:** Horizontal spans showing ranges or durations.
**Basic Chart:** Horizontal bars with start/end, like Gantt.

### gantt-basic
**Best Library:** Matplotlib
**Description:** Project timeline Gantt chart.
**Basic Chart:** Horizontal task bars on timeline.

---

## 22. Text & Annotation

### wordcloud-basic
**Best Library:** Matplotlib (wordcloud)
**Description:** Word frequency visualization.
**Basic Chart:** Words sized by frequency.

### annotated-scatter
**Best Library:** Matplotlib
**Description:** Scatter plot with text labels on points.
**Basic Chart:** Points with nearby text annotations.

### annotated-line
**Best Library:** Matplotlib
**Description:** Line plot with annotations at key points.
**Basic Chart:** Arrows and text highlighting events.

---

## 23. Comparison Plots

### parallel-coordinates
**Best Library:** Plotly
**Description:** Multi-dimensional data as parallel axes.
**Basic Chart:** Vertical axes with lines connecting values.

### parallel-categories
**Best Library:** Plotly
**Description:** Parallel coordinates for categorical data.
**Basic Chart:** Ribbons flowing between category columns.

### andrews-curves
**Best Library:** Matplotlib (pandas)
**Description:** Multivariate data as Fourier curves.
**Basic Chart:** Smooth curves representing data points.

---

## 24. Financial Charts

### stock-candlestick
**Best Library:** Highcharts
**Description:** Professional candlestick chart for stock prices with volume.
**Basic Chart:** OHLC candles, volume bars below, date axis with trading days.

### stock-area
**Best Library:** Highcharts
**Description:** Area chart for stock price history with range selector.
**Basic Chart:** Filled area showing price, navigator at bottom, range buttons.

### stock-comparison
**Best Library:** Highcharts
**Description:** Multiple stock series normalized for comparison.
**Basic Chart:** 2-3 stocks rebased to 100%, percentage y-axis.

### stock-flags
**Best Library:** Highcharts
**Description:** Stock chart with event markers/annotations.
**Basic Chart:** Price line with flag icons marking dividends, splits, earnings.

### stock-volume
**Best Library:** Highcharts
**Description:** Stock price with volume bars in synchronized panes.
**Basic Chart:** Price in top pane, volume histogram below.

### indicator-macd
**Best Library:** Highcharts
**Description:** MACD technical indicator chart.
**Basic Chart:** Price chart with MACD line, signal line, histogram below.

### indicator-rsi
**Best Library:** Highcharts
**Description:** Relative Strength Index indicator.
**Basic Chart:** RSI oscillator with overbought/oversold zones (70/30).

### indicator-bollinger
**Best Library:** Highcharts
**Description:** Bollinger Bands overlay on price chart.
**Basic Chart:** Price with upper, middle, lower bands.

### indicator-sma
**Best Library:** Matplotlib
**Description:** Simple Moving Average overlay.
**Basic Chart:** Price line with 20-day and 50-day SMA lines.

### indicator-ema
**Best Library:** Matplotlib
**Description:** Exponential Moving Average overlay.
**Basic Chart:** Price line with EMA lines of different periods.

### returns-histogram
**Best Library:** Seaborn
**Description:** Distribution of daily/monthly returns.
**Basic Chart:** Histogram of percentage returns with normal curve overlay.

### drawdown-chart
**Best Library:** Matplotlib
**Description:** Drawdown from peak visualization.
**Basic Chart:** Area chart showing negative drawdown percentages over time.

### correlation-returns
**Best Library:** Seaborn
**Description:** Correlation matrix of asset returns.
**Basic Chart:** Heatmap of return correlations between assets.

### portfolio-allocation
**Best Library:** Plotly
**Description:** Interactive portfolio weight visualization.
**Basic Chart:** Pie or treemap showing asset allocation.

### efficient-frontier
**Best Library:** Matplotlib
**Description:** Portfolio risk-return optimization curve.
**Basic Chart:** Scatter of portfolios, efficient frontier line, risk vs return axes.

---

## 25. Extended Geographic & Maps

### map-tile
**Best Library:** Plotly
**Description:** Map with OpenStreetMap or satellite tile background.
**Basic Chart:** Zoomable tile map with markers.

### map-density
**Best Library:** Plotly
**Description:** Point density visualization on map.
**Basic Chart:** Heatmap-style density showing concentration.

### map-flow
**Best Library:** Plotly
**Description:** Origin-destination flow map with curved lines.
**Basic Chart:** Arcs showing movement between locations, width by volume.

### map-cluster
**Best Library:** Plotly
**Description:** Clustered markers that expand on zoom.
**Basic Chart:** Grouped markers with count badges.

### map-hexbin
**Best Library:** Plotly
**Description:** Hexagonal binning on geographic data.
**Basic Chart:** Hexagon grid colored by point count.

### map-route
**Best Library:** Plotly
**Description:** Path/route visualization on map.
**Basic Chart:** Connected waypoints showing journey.

### map-animated
**Best Library:** Plotly
**Description:** Animated map showing changes over time.
**Basic Chart:** Choropleth or scatter with time slider.

### map-drill
**Best Library:** Highcharts
**Description:** Drillable map (country → state → city).
**Basic Chart:** Click to zoom into sub-regions.

### map-projection
**Best Library:** Matplotlib (cartopy)
**Description:** Map with different geographic projections.
**Basic Chart:** Robinson, Mercator, or orthographic projection.

### map-contour
**Best Library:** Matplotlib (cartopy)
**Description:** Contour lines on geographic background.
**Basic Chart:** Elevation or weather contours on map.

---

## 26. SVG & Minimal Charts (Pygal)

### svg-line
**Best Library:** Pygal
**Description:** Clean SVG line chart for web embedding.
**Basic Chart:** Minimal line chart, hover tooltips, embeddable.

### svg-bar
**Best Library:** Pygal
**Description:** SVG bar chart with smooth animations.
**Basic Chart:** Animated bars on hover, clean design.

### svg-pie
**Best Library:** Pygal
**Description:** Interactive SVG pie chart.
**Basic Chart:** Slices with hover effects, legend.

### svg-radar
**Best Library:** Pygal
**Description:** SVG radar/spider chart.
**Basic Chart:** Clean polygonal radar with fill.

### svg-dot
**Best Library:** Pygal
**Description:** Dot matrix chart in SVG.
**Basic Chart:** Dots arranged in grid, sized by value.

### svg-gauge
**Best Library:** Pygal
**Description:** Gauge chart in SVG format.
**Basic Chart:** Semicircular gauge with needle.

### svg-funnel
**Best Library:** Pygal
**Description:** SVG funnel chart.
**Basic Chart:** Clean funnel with stage labels.

### svg-box
**Best Library:** Pygal
**Description:** SVG box plot.
**Basic Chart:** Clean box and whisker with tooltips.

### svg-treemap
**Best Library:** Pygal
**Description:** SVG treemap visualization.
**Basic Chart:** Nested rectangles with hover info.

### svg-worldmap
**Best Library:** Pygal
**Description:** Simple SVG world map.
**Basic Chart:** Countries colored by value, hover to show data.

---

## 27. Drilldown & Interactive (Highcharts)

### drilldown-pie
**Best Library:** Highcharts
**Description:** Pie chart with click-to-drill functionality.
**Basic Chart:** Click slice to see subcategory breakdown.

### drilldown-bar
**Best Library:** Highcharts
**Description:** Bar chart with drilldown to details.
**Basic Chart:** Click bar to see component breakdown.

### drilldown-column
**Best Library:** Highcharts
**Description:** Column chart with hierarchical drilling.
**Basic Chart:** Year → Quarter → Month drilldown.

### synchronized-charts
**Best Library:** Highcharts
**Description:** Multiple charts with synchronized crosshairs.
**Basic Chart:** Several charts, hover shows value across all.

### navigator-chart
**Best Library:** Highcharts
**Description:** Chart with mini navigator for range selection.
**Basic Chart:** Main chart with small overview below.

### range-selector
**Best Library:** Highcharts
**Description:** Chart with preset range buttons (1M, 3M, YTD, 1Y).
**Basic Chart:** Quick range selection buttons.

### export-chart
**Best Library:** Highcharts
**Description:** Chart with built-in export menu.
**Basic Chart:** Export to PNG, PDF, SVG, or print.

---

## 28. Real-Time & Streaming

### realtime-line
**Best Library:** Bokeh
**Description:** Line chart updating with live data.
**Basic Chart:** Auto-scrolling line with new points.

### realtime-gauge
**Best Library:** Plotly
**Description:** Gauge updating in real-time.
**Basic Chart:** Needle moving with live value.

### realtime-bar
**Best Library:** Bokeh
**Description:** Bar chart with live updates.
**Basic Chart:** Bars growing/shrinking with data.

### streaming-scatter
**Best Library:** Bokeh
**Description:** Scatter plot with streaming points.
**Basic Chart:** New points appearing, old fading.

### dashboard-tiles
**Best Library:** Bokeh
**Description:** Multiple real-time metrics in tiles.
**Basic Chart:** KPI tiles with sparklines.

---

## 29. Scientific & Domain-Specific

### spectrum-plot
**Best Library:** Matplotlib
**Description:** Frequency spectrum visualization.
**Basic Chart:** Amplitude vs frequency, peaks labeled.

### spectrogram
**Best Library:** Matplotlib
**Description:** Time-frequency heatmap for audio/signals.
**Basic Chart:** Time on x, frequency on y, color for intensity.

### phase-diagram
**Best Library:** Matplotlib
**Description:** Phase space plot (x vs dx/dt).
**Basic Chart:** Trajectory in phase space, attractor patterns.

### vector-field
**Best Library:** Matplotlib
**Description:** 2D vector field with arrows.
**Basic Chart:** Grid of arrows showing direction and magnitude.

### streamline-plot
**Best Library:** Matplotlib
**Description:** Streamlines of a vector field.
**Basic Chart:** Smooth curves following flow direction.

### quiver-plot
**Best Library:** Matplotlib
**Description:** Arrow plot for velocity or gradient fields.
**Basic Chart:** Arrows at grid points showing vectors.

### ternary-plot
**Best Library:** Plotly
**Description:** Three-component composition diagram.
**Basic Chart:** Triangle with points showing 3-part ratios.

### smith-chart
**Best Library:** Matplotlib
**Description:** RF/microwave impedance chart.
**Basic Chart:** Circular chart for complex impedance.

### survival-curve
**Best Library:** Matplotlib
**Description:** Kaplan-Meier survival analysis plot.
**Basic Chart:** Step function showing survival probability over time.

### forest-plot
**Best Library:** Matplotlib
**Description:** Meta-analysis effect sizes with confidence intervals.
**Basic Chart:** Horizontal lines with diamonds showing effects.

### volcano-plot
**Best Library:** Matplotlib
**Description:** Statistical significance vs fold change.
**Basic Chart:** -log10(p) vs log2(fold change), highlighted significant points.

### manhattan-plot
**Best Library:** Matplotlib
**Description:** Genome-wide association study visualization.
**Basic Chart:** Chromosomes on x-axis, -log10(p) on y, significance line.

### circos-plot
**Best Library:** Matplotlib
**Description:** Circular genome or relationship visualization.
**Basic Chart:** Circular tracks with connections between regions.

### phylogenetic-tree
**Best Library:** Matplotlib
**Description:** Evolutionary tree diagram.
**Basic Chart:** Branching tree with species at leaves.

---

## Summary by Library Recommendation

| Library | Primary Strengths | Recommended Plot Types |
|---------|-------------------|------------------------|
| **Matplotlib** | Flexibility, static plots | Line, bar, scatter, histogram, polar, 3D wireframe, annotations, scientific |
| **Seaborn** | Statistical, beautiful defaults | Distributions, regression, heatmaps, categorical, pair plots |
| **Plotly** | Interactivity, web, 3D | Interactive plots, maps, 3D surfaces, animations, sankey, treemap, ternary |
| **Bokeh** | Streaming, large data | Linked views, brush/zoom, real-time dashboards, streaming data |
| **Altair** | Declarative, quick exploration | Exploratory analysis, faceted plots, academic visualizations |
| **Plotnine** | ggplot2 syntax | Users from R, grammar of graphics approach |
| **Pygal** | SVG, minimalistic, embeddable | Simple web charts, SVG export, lightweight dashboards |
| **Highcharts** | Professional, financial, drilldown | Stock charts, technical indicators, enterprise dashboards, drilldown |

---

## Next Steps

Each plot type in this catalog can become a spec file. Priority order suggestion:

1. **Essential basics** (scatter-basic, line-basic, bar-basic, histogram-basic, pie-basic, box-basic)
2. **Statistical** (heatmap-correlation, violin-basic, regression-linear)
3. **Interactive** (scatter-3d, map-choropleth, drilldown-pie)
4. **Financial** (stock-candlestick, indicator-macd, efficient-frontier)
5. **SVG/Minimal** (svg-line, svg-radar, svg-worldmap)
6. **Scientific** (spectrum-plot, survival-curve, forest-plot)

To create a spec, use the format: `plots/{spec-id}/spec.md`

---

## Statistics

- **Total Plot Types:** 170+
- **Categories:** 29
- **Libraries Covered:** 8 (Matplotlib, Seaborn, Plotly, Bokeh, Altair, Plotnine, Pygal, Highcharts)
