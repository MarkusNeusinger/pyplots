# Plot Types Catalog

A comprehensive catalog of plot types for the pyplots platform. Each plot is implemented across all 9 supported libraries (matplotlib, seaborn, plotly, bokeh, altair, plotnine, pygal, highcharts, lets-plot).

**Legend:** ✅ = implemented | 📋 = planned

---

## 1. Scatter Plots

### scatter-basic ✅
**Description:** A fundamental 2D scatter plot that displays the relationship between two numeric variables by plotting points on a Cartesian coordinate system.

### scatter-color-mapped 📋
**Description:** Scatter plot with a third variable encoded as color using a colormap. Includes colorbar for reference.

### scatter-size-mapped 📋
**Description:** Bubble chart where marker size represents a third variable. Semi-transparent markers reveal overlapping points.

### scatter-categorical 📋
**Description:** Scatter plot with points colored by category. Distinct colors for each group with legend.

### scatter-regression 📋
**Description:** Scatter plot with linear regression line and confidence interval band.

### scatter-marginal 📋
**Description:** Scatter plot with marginal histograms or KDE on axes showing distributions.

### scatter-3d 📋
**Description:** Three-dimensional scatter plot with rotation capability for exploring 3D relationships.

### scatter-matrix 📋
**Description:** Grid of scatter plots for all variable pairs in a dataset with histograms on diagonal.

---

## 2. Line Plots

### line-basic ✅
**Description:** A basic line plot connects data points with straight lines to show how a continuous variable changes over a sequence or time.

### line-multi 📋
**Description:** Multiple lines on the same axes for comparison with legend.

### line-styled 📋
**Description:** Line plot with different line styles (solid, dashed, dotted) for black-and-white printing.

### line-markers 📋
**Description:** Line plot with visible markers at data points, helpful for sparse data.

### line-timeseries 📋
**Description:** Line plot with datetime x-axis and proper date formatting.

### line-stepwise 📋
**Description:** Step function plot with horizontal then vertical transitions.

### step-basic ✅
**Description:** A step plot displays data using horizontal lines connected by vertical lines, creating a stair-step pattern that shows values as constant until the next change occurs.

### line-filled 📋
**Description:** Line plot with area filled to baseline, semi-transparent.

### line-confidence 📋
**Description:** Line plot with confidence interval band around the mean.

### line-interactive 📋
**Description:** Line plot with hover tooltips and zoom capability.

---

## 3. Bar Charts

### bar-basic ✅
**Description:** A vertical bar chart that displays categorical data with rectangular bars whose heights are proportional to the values they represent.

### bar-horizontal 📋
**Description:** Horizontal bars, useful for long category names.

### bar-grouped 📋
**Description:** Side-by-side bars for comparing groups within categories.

### bar-stacked 📋
**Description:** Bars stacked on top of each other showing composition.

### bar-stacked-percent 📋
**Description:** Stacked bars normalized to 100% showing proportions.

### bar-error 📋
**Description:** Bar chart with error bars showing uncertainty.

### bar-sorted 📋
**Description:** Bar chart with categories sorted by value.

### bar-categorical 📋
**Description:** Bar chart showing count of observations per category.

### bar-diverging 📋
**Description:** Bars extending from center, positive/negative values with different colors.

### lollipop-basic ✅
**Description:** A lollipop chart displays categorical data with thin lines (stems) extending from a baseline to circular markers (dots) at each data point.

### bar-interactive 📋
**Description:** Bar chart with hover details and click interactions.

---

## 4. Histograms

### histogram-basic ✅
**Description:** A histogram displays the distribution of a single continuous variable by dividing the data range into bins and showing the frequency of observations in each bin.

### histogram-normalized 📋
**Description:** Histogram normalized to show density instead of count.

### histogram-overlapping 📋
**Description:** Multiple overlapping histograms for comparison.

### histogram-stacked 📋
**Description:** Stacked histograms showing combined distribution.

### histogram-stepwise 📋
**Description:** Histogram with step outline only (no filled bars).

### histogram-kde 📋
**Description:** Histogram with kernel density estimate overlay.

### density-basic ✅
**Description:** A density plot (Kernel Density Estimation) visualizes the distribution of a continuous variable by smoothing the data into a continuous probability density curve.

### histogram-2d 📋
**Description:** Two-dimensional histogram as heatmap.

### histogram-cumulative 📋
**Description:** Cumulative distribution function as histogram.

---

## 5. Pie & Donut Charts

### pie-basic ✅
**Description:** A pie chart showing proportions of categorical data as slices of a circle. Each slice represents a category's contribution to the whole.

### pie-exploded 📋
**Description:** Pie chart with one or more slices pulled out to highlight.

### donut-basic ✅
**Description:** A donut chart (ring chart) showing proportions of categorical data as segments of a ring, with a hollow center.

### donut-nested 📋
**Description:** Multiple concentric donut rings showing hierarchical data.

### sunburst-basic ✅
**Description:** A sunburst chart displays hierarchical data as concentric rings, where each ring represents a level in the hierarchy.

---

## 6. Box Plots & Distributions

### box-basic ✅
**Description:** A box plot (box-and-whisker plot) showing the distribution of numerical data through quartiles. Displays the median, first and third quartiles as a box, with whiskers extending to show the data range.

### box-grouped 📋
**Description:** Multiple box plots grouped by category.

### box-horizontal 📋
**Description:** Horizontal box plot orientation.

### box-notched 📋
**Description:** Box plot with notches indicating median confidence.

### violin-basic ✅
**Description:** A violin plot combining a box plot with a kernel density estimation on each side, showing the distribution shape of numerical data.

### violin-split 📋
**Description:** Half-violins comparing two groups.

### violin-box 📋
**Description:** Violin plot with embedded box plot.

### strip-basic ✅
**Description:** A strip plot displays individual data points for each category along a single axis, with random horizontal jitter applied to reduce overplotting.

### swarm-basic ✅
**Description:** A swarm plot (beeswarm plot) displays individual data points for categorical comparisons, with points spread horizontally to avoid overlap.

### ridgeline-basic ✅
**Description:** A ridgeline plot displays the distribution of multiple groups by stacking partially overlapping density curves vertically, creating a mountain ridge appearance.

### ecdf-basic ✅
**Description:** An ECDF (Empirical Cumulative Distribution Function) plot displays a step function that shows the proportion of observations less than or equal to each value.

### rug-basic ✅
**Description:** A rug plot displays individual data points as small tick marks along an axis, typically at the bottom or side of another plot.

---

## 7. Heatmaps

### heatmap-basic ✅
**Description:** A heatmap displaying values in a matrix format using color intensity. Each cell's color represents the magnitude of the value.

### heatmap-annotated 📋
**Description:** Heatmap with values displayed in cells.

### heatmap-correlation 📋
**Description:** Correlation matrix visualization with diverging colormap.

### heatmap-clustered 📋
**Description:** Heatmap with hierarchical clustering dendrograms.

### heatmap-calendar ✅
**Description:** A calendar heatmap visualizes time-series data on a calendar grid, where each day is represented as a cell and color intensity indicates the value magnitude.

### heatmap-interactive 📋
**Description:** Heatmap with hover values and zoom.

---

## 8. Area Charts

### area-basic ✅
**Description:** An area chart showing quantitative data over a continuous axis with the area below the line filled.

### area-stacked 📋
**Description:** Multiple areas stacked showing cumulative total.

### area-stacked-percent 📋
**Description:** Stacked areas normalized to 100%.

### streamgraph-basic ✅
**Description:** A streamgraph (stacked area chart with centered baseline) displaying the composition of multiple categories over time with smooth, flowing curves.

### band-basic ✅
**Description:** A band plot displays a filled region between two boundary lines, commonly used to show confidence intervals or prediction intervals.

---

## 9. Polar & Radar Charts

### polar-basic ✅
**Description:** A polar chart displays data points on a circular coordinate system where position is determined by angle (theta) and distance from center (radius).

### polar-scatter 📋
**Description:** Scatter plot in polar coordinates.

### polar-line 📋
**Description:** Line plot in polar coordinates.

### polar-bar 📋
**Description:** Bar chart arranged in a circle (wind rose).

### rose-basic ✅
**Description:** A rose chart (Nightingale diagram) displays categorical data in a circular format where segments have equal angles but radius proportional to value.

### radar-basic ✅
**Description:** A radar chart (spider/web chart) displays multivariate data on axes starting from a common center point, with values connected to form a polygon.

### radar-multi 📋
**Description:** Multiple overlapping radar polygons for comparison.

---

## 10. Statistical Plots

### regression-linear 📋
**Description:** Scatter with linear regression fit and confidence band.

### regression-polynomial 📋
**Description:** Non-linear regression curve fit.

### regression-lowess 📋
**Description:** Locally weighted regression smoothing.

### residual-basic 📋
**Description:** Residual plot for regression diagnostics.

### qq-basic ✅
**Description:** A Q-Q (Quantile-Quantile) plot compares the distribution of a dataset against a theoretical distribution. Points along a diagonal reference line indicate perfect distribution match.

### bland-altman 📋
**Description:** Agreement plot between two measurements with limits of agreement.

### errorbar-basic ✅
**Description:** An error bar plot displays data points with associated uncertainty or variability represented by bars extending above and below each point.

### error-asymmetric 📋
**Description:** Error bars with different upper/lower bounds.

---

## 11. Categorical Plots

### count-basic 📋
**Description:** Bar chart of category counts.

### point-basic 📋
**Description:** Point estimates with confidence intervals.

### cat-strip 📋
**Description:** Categorical scatter plot.

### cat-box-strip 📋
**Description:** Combined box plot with overlaid strip plot.

---

## 12. Matrix & Grid Plots

### facet-grid 📋
**Description:** Grid of plots split by categorical variables.

### pair-plot 📋
**Description:** All pairwise relationships in dataset.

### subplot-grid 📋
**Description:** Custom grid of different plot types.

### mosaic-layout 📋
**Description:** Complex subplot layout with varying sizes.

---

## 13. Time Series Plots

### timeseries-single 📋
**Description:** Single time series with proper date axis.

### timeseries-multi 📋
**Description:** Multiple time series for comparison.

### timeseries-decomposition 📋
**Description:** Trend, seasonal, residual components.

### timeseries-rolling 📋
**Description:** Time series with rolling average overlay.

### candlestick-basic ✅
**Description:** A candlestick chart displays open, high, low, and close (OHLC) price data for financial instruments over time.

### timeseries-ohlc 📋
**Description:** Open-high-low-close bar chart.

### timeseries-forecast 📋
**Description:** Historical data with forecast and uncertainty.

### sparkline-basic ✅
**Description:** A sparkline is a small, condensed line chart designed to be embedded inline with text or in dashboard cells. Pure data visualization in minimal space.

---

## 14. Geographic & Spatial

### map-choropleth 📋
**Description:** Map with regions colored by value.

### map-scatter 📋
**Description:** Points plotted on geographic map.

### map-bubble 📋
**Description:** Map with sized circles at locations.

### map-heatmap 📋
**Description:** Density heatmap on geographic background.

### map-lines 📋
**Description:** Connection lines between locations.

---

## 15. 3D Plots

### surface-basic ✅
**Description:** A 3D surface plot visualizes a function of two variables as a continuous surface in three-dimensional space.

### wireframe-3d-basic ✅
**Description:** A 3D wireframe plot displays a mathematical surface as a mesh of lines connecting grid points, creating a see-through visualization.

### contour-3d 📋
**Description:** 3D contour plot.

### bar-3d 📋
**Description:** 3D bar chart.

### line-3d 📋
**Description:** 3D line plot or trajectory.

---

## 16. Contour Plots

### contour-basic ✅
**Description:** A contour plot displays isolines (level curves) of a 2D scalar field, connecting points of equal value across a surface.

### contour-filled 📋
**Description:** Filled contour regions.

### contour-density 📋
**Description:** Contour plot from point density.

### hexbin-basic ✅
**Description:** A hexagonal binning plot that visualizes the density of 2D point data by aggregating points into hexagonal bins.

---

## 17. Network & Graph Plots

### network-basic ✅
**Description:** A network graph (node-link diagram) visualizes relationships between entities as nodes connected by edges.

### network-directed 📋
**Description:** Directed graph with arrows.

### network-weighted 📋
**Description:** Graph with edge thickness by weight.

### network-hierarchical 📋
**Description:** Tree or hierarchy layout.

### network-force-directed ✅
**Description:** A force-directed graph uses physics simulation to position nodes, where connected nodes attract each other and all nodes repel.

### chord-basic ✅
**Description:** A chord diagram displays relationships or flows between entities arranged around a circle's perimeter.

### arc-basic ✅
**Description:** An arc diagram arranges nodes along a single horizontal line and draws connections between them as curved arcs above the line.

### sankey-basic ✅
**Description:** A Sankey diagram visualizes flow or transfer between nodes using links with widths proportional to flow values.

---

## 18. Tree & Hierarchical

### treemap-basic ✅
**Description:** A treemap displaying hierarchical data as nested rectangles, where each rectangle's area is proportional to its value.

### dendrogram-basic ✅
**Description:** A dendrogram visualizes hierarchical clustering by showing how data points or clusters merge at different distance levels.

### icicle-basic 📋
**Description:** Rectangular hierarchy visualization with stacked rectangles.

### circle-packing 📋
**Description:** Nested circles showing hierarchy.

---

## 19. Part-to-Whole

### waffle-basic ✅
**Description:** A waffle chart displays proportions using a grid of equal-sized squares where colored squares represent parts of a whole.

### parliament-basic 📋
**Description:** Semicircular parliament seat chart.

### gauge-basic ✅
**Description:** A gauge chart (speedometer chart) displays a single value within a defined range using a semi-circular or circular dial.

### bullet-basic ✅
**Description:** A bullet chart displays a single measure against qualitative ranges and a target marker, designed as a space-efficient alternative to gauge charts.

### marimekko-basic ✅
**Description:** A Marimekko chart is a stacked bar chart where both the width and height of segments represent data values.

---

## 20. Animation & Interactive

### animation-line 📋
**Description:** Animated line plot building over time.

### animation-scatter 📋
**Description:** Animated scatter with play button.

### animation-bar 📋
**Description:** Bar chart race animation.

### slider-basic 📋
**Description:** Plot with slider control.

### brush-zoom 📋
**Description:** Plot with brush selection and zoom.

### linked-views 📋
**Description:** Multiple plots with linked selection.

---

## 21. Specialized Plots

### waterfall-basic ✅
**Description:** A waterfall chart visualizes how an initial value is affected by a series of intermediate positive or negative values, leading to a final value.

### funnel-basic ✅
**Description:** A funnel chart visualizes sequential stages of a process where values progressively decrease from one stage to the next.

### pyramid-basic ✅
**Description:** A pyramid chart displays two opposing horizontal bar charts that share a central axis, creating a pyramid or butterfly shape.

### slope-basic ✅
**Description:** A slope chart (slopegraph) visualizes changes between two or more time points by connecting values with lines across vertical axes.

### bump-basic ✅
**Description:** A bump chart visualizes how rankings change over time by plotting rank positions and connecting them with lines.

### dumbbell-basic ✅
**Description:** A dumbbell chart (connected dot plot) compares two values for each category by displaying two dots connected by a line.

### span-basic ✅
**Description:** A span plot highlights a specific region of interest on a chart using a shaded rectangular area that spans the full height or width.

### gantt-basic 📋
**Description:** Project timeline Gantt chart with horizontal task bars.

### timeline-basic 📋
**Description:** Zeitleiste mit Events und Zeitpunkten.

### venn-basic 📋
**Description:** Venn-Diagramm zeigt überlappende Mengen (2-3 Kreise).

---

## 22. Text & Annotation

### wordcloud-basic ✅
**Description:** A word cloud displays text data where word size represents frequency or importance.

### annotated-scatter 📋
**Description:** Scatter plot with text labels on points.

### annotated-line 📋
**Description:** Line plot with annotations at key points.

---

## 23. Comparison Plots

### parallel-basic ✅
**Description:** A parallel coordinates plot visualizes multivariate data by representing each variable as a vertical axis and each observation as a line connecting values across all axes.

### parallel-categories 📋
**Description:** Parallel coordinates for categorical data.

### andrews-curves 📋
**Description:** Multivariate data as Fourier curves.

---

## 24. Financial Charts

### stock-candlestick 📋
**Description:** Professional candlestick chart for stock prices with volume.

### stock-area 📋
**Description:** Area chart for stock price history with range selector.

### stock-comparison 📋
**Description:** Multiple stock series normalized for comparison.

### stock-flags 📋
**Description:** Stock chart with event markers/annotations.

### stock-volume 📋
**Description:** Stock price with volume bars in synchronized panes.

### indicator-macd 📋
**Description:** MACD technical indicator chart.

### indicator-rsi 📋
**Description:** Relative Strength Index indicator.

### indicator-bollinger 📋
**Description:** Bollinger Bands overlay on price chart.

### indicator-sma 📋
**Description:** Simple Moving Average overlay.

### indicator-ema 📋
**Description:** Exponential Moving Average overlay.

### returns-histogram 📋
**Description:** Distribution of daily/monthly returns.

### drawdown-chart 📋
**Description:** Drawdown from peak visualization.

### correlation-returns 📋
**Description:** Correlation matrix of asset returns.

### portfolio-allocation 📋
**Description:** Interactive portfolio weight visualization.

### efficient-frontier 📋
**Description:** Portfolio risk-return optimization curve.

---

## 25. Extended Geographic & Maps

### map-tile 📋
**Description:** Map with OpenStreetMap or satellite tile background.

### map-density 📋
**Description:** Point density visualization on map.

### map-flow 📋
**Description:** Origin-destination flow map with curved lines.

### map-cluster 📋
**Description:** Clustered markers that expand on zoom.

### map-hexbin 📋
**Description:** Hexagonal binning on geographic data.

### map-route 📋
**Description:** Path/route visualization on map.

### map-animated 📋
**Description:** Animated map showing changes over time.

### map-drill 📋
**Description:** Drillable map (country → state → city).

### map-projection 📋
**Description:** Map with different geographic projections.

### map-contour 📋
**Description:** Contour lines on geographic background.

---

## 26. SVG & Minimal Charts

### svg-line 📋
**Description:** Clean SVG line chart for web embedding.

### svg-bar 📋
**Description:** SVG bar chart with smooth animations.

### svg-pie 📋
**Description:** Interactive SVG pie chart.

### svg-radar 📋
**Description:** SVG radar/spider chart.

### svg-dot 📋
**Description:** Dot matrix chart in SVG.

### svg-gauge 📋
**Description:** Gauge chart in SVG format.

### svg-funnel 📋
**Description:** SVG funnel chart.

### svg-box 📋
**Description:** SVG box plot.

### svg-treemap 📋
**Description:** SVG treemap visualization.

### svg-worldmap 📋
**Description:** Simple SVG world map.

---

## 27. Drilldown & Interactive

### drilldown-pie 📋
**Description:** Pie chart with click-to-drill functionality.

### drilldown-bar 📋
**Description:** Bar chart with drilldown to details.

### drilldown-column 📋
**Description:** Column chart with hierarchical drilling.

### synchronized-charts 📋
**Description:** Multiple charts with synchronized crosshairs.

### navigator-chart 📋
**Description:** Chart with mini navigator for range selection.

### range-selector 📋
**Description:** Chart with preset range buttons (1M, 3M, YTD, 1Y).

### export-chart 📋
**Description:** Chart with built-in export menu.

---

## 28. Real-Time & Streaming

### realtime-line 📋
**Description:** Line chart updating with live data.

### realtime-gauge 📋
**Description:** Gauge updating in real-time.

### realtime-bar 📋
**Description:** Bar chart with live updates.

### streaming-scatter 📋
**Description:** Scatter plot with streaming points.

### dashboard-tiles 📋
**Description:** Multiple real-time metrics in tiles.

---

## 29. Scientific & Domain-Specific

### spectrum-plot 📋
**Description:** Frequency spectrum visualization.

### spectrogram 📋
**Description:** Time-frequency heatmap for audio/signals.

### phase-diagram 📋
**Description:** Phase space plot (x vs dx/dt).

### quiver-basic ✅
**Description:** A quiver plot displays vector fields using arrows positioned at grid points. Each arrow represents a vector at that location, with direction indicating the vector's angle and length proportional to its magnitude.

### streamline-basic 📋
**Description:** Strömungslinien eines Vektorfelds als glatte Kurven.

### stem-basic ✅
**Description:** A stem plot displays data points as markers connected to a baseline by vertical lines (stems).

### ternary-basic ✅
**Description:** A ternary plot displays three-component compositional data on an equilateral triangle where each vertex represents 100% of one component.

### smith-chart 📋
**Description:** RF/microwave impedance chart.

### survival-curve 📋
**Description:** Kaplan-Meier survival analysis plot.

### forest-plot 📋
**Description:** Meta-analysis effect sizes with confidence intervals.

### volcano-plot 📋
**Description:** Statistical significance vs fold change.

### manhattan-plot 📋
**Description:** Genome-wide association study visualization.

### circos-plot 📋
**Description:** Circular genome or relationship visualization.

### phylogenetic-tree 📋
**Description:** Evolutionary tree diagram.

### bubble-basic ✅
**Description:** A bubble chart extending scatter plots by adding a third dimension through bubble size.

### bubble-packed ✅
**Description:** A packed bubble chart displays data as circles where size represents value, packed together without overlap using physics simulation.

---

## 30. Printable & Fun

Druckbare Vorlagen und spielerische Visualisierungen.

### Puzzles & Games

### sudoku-basic 📋
**Description:** Standard 9x9 Sudoku-Raster mit 3x3 Boxen. Dicke Linien für Regionen, dünne für Zellen. Leer oder mit Startzahlen zum Ausdrucken und Lösen.

### sudoku-filled 📋
**Description:** Sudoku-Rätsel mit vorgegebenen Zahlen und eindeutiger Lösung. Vorgegebene Zahlen optisch hervorgehoben.

### maze-basic 📋
**Description:** Rechteckiges Labyrinth mit Start und Ziel. Algorithmisch generiert mit genau einem Lösungsweg. Schwarz-weiß zum Ausdrucken.

### maze-circular 📋
**Description:** Rundes Labyrinth aus konzentrischen Ringen. Eingang außen, Ziel im Zentrum.

### chess-board 📋
**Description:** Klassisches 8x8 Schachbrett mit abwechselnd hellen und dunklen Feldern. Beschriftet mit a-h und 1-8.

### crossword-basic 📋
**Description:** Kreuzworträtsel-Gitter mit weißen Eingabe- und schwarzen Blockfeldern. Nummerierte Startfelder für Wörter.

### Codes & Identification

### qr-code 📋
**Description:** QR-Code generiert aus Text oder URL. Quadratisches Muster mit Positionsmarkierungen, scanbar mit Smartphone.

### barcode-ean 📋
**Description:** EAN-13 Barcode (europäischer Produktcode). Vertikale Striche mit 13 Ziffern darunter, scanbar im Einzelhandel.

### barcode-code128 📋
**Description:** Code 128 Barcode für alphanumerische Daten. Kompaktes Format für Logistik und Versand.

### datamatrix-basic 📋
**Description:** Data Matrix 2D-Barcode. Platzsparender als QR, L-förmiges Findermuster, für Industrie-Kennzeichnung.

---

## Statistics

- **Total Plot Types:** 210+
- **Implemented:** 58 ✅
- **Planned:** 150+ 📋
- **Categories:** 30

---

## Next Steps

Each plot type in this catalog can become a spec file. Priority order suggestion:

1. **Essential basics** - Complete the basic variants (scatter-regression, bar-grouped, histogram-kde)
2. **Statistical** - heatmap-correlation, violin-split, regression-linear
3. **Interactive** - scatter-3d, map-choropleth, drilldown-pie
4. **Financial** - stock-candlestick, indicator-macd, efficient-frontier
5. **Fun** - sudoku-basic, maze-basic, qr-code

To create a spec, use the format: `plots/{spec-id}/specification.md`
