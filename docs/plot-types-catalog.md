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

## Summary by Library Recommendation

| Library | Primary Strengths | Recommended Plot Types |
|---------|-------------------|------------------------|
| **Matplotlib** | Flexibility, static plots | Line, bar, scatter, histogram, polar, 3D wireframe, annotations |
| **Seaborn** | Statistical, beautiful defaults | Distributions, regression, heatmaps, categorical, pair plots |
| **Plotly** | Interactivity, web, 3D | Interactive plots, maps, 3D surfaces, animations, sankey, treemap |
| **Bokeh** | Streaming, large data | Linked views, brush/zoom, real-time dashboards |
| **Altair** | Declarative, quick exploration | Exploratory analysis, faceted plots, academic visualizations |
| **Plotnine** | ggplot2 syntax | Users from R, grammar of graphics approach |

---

## Next Steps

Each plot type in this catalog can become a spec file. Priority order suggestion:

1. **Essential basics** (scatter-basic, line-basic, bar-basic, histogram-basic, pie-basic, box-basic)
2. **Statistical** (heatmap-correlation, violin-basic, regression-linear)
3. **Interactive** (scatter-3d, timeseries-candlestick, map-choropleth)
4. **Specialized** (sankey-basic, treemap-basic, radar-basic)

To create a spec, use the format: `specs/{spec-id}.md`
