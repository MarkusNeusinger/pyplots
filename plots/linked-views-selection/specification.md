# linked-views-selection: Multiple Linked Views with Selection Sync

## Description

Multiple coordinated plots where selecting data in one view automatically highlights or filters corresponding data points in all other views. This brushing-and-linking interaction pattern is fundamental for exploratory data analysis, allowing users to discover relationships across different visual representations of the same dataset. By selecting a cluster in a scatter plot, for example, users can instantly see how those points distribute in histograms, how they appear in parallel coordinates, or which categories they belong to.

## Applications

- Exploratory data analysis dashboards where analysts investigate multivariate datasets by brushing across scatter plots, histograms, and categorical views
- Customer segmentation tools where selecting a group in one dimension reveals their characteristics across demographics, behavior, and transactions
- Scientific data exploration comparing different measurements or experimental conditions with synchronized highlighting
- Financial portfolio analysis linking asset allocation views with performance metrics and risk indicators

## Data

- `x` (numeric) - Values for scatter plot horizontal axis
- `y` (numeric) - Values for scatter plot vertical axis
- `category` (categorical) - Group labels for bar chart or color encoding
- `value` (numeric) - Additional numeric dimension for histogram or secondary visualizations
- Size: 100-1000 points (interactivity works best with moderate dataset sizes)
- Example: Iris dataset or simulated multivariate data with numeric and categorical columns

## Notes

- Implement at least 2-3 coordinated views (e.g., scatter plot + histogram + bar chart)
- Selection in any view should highlight corresponding points in all other views
- Use consistent color encoding across all views for the same data points
- Unselected points should be visually de-emphasized (reduced opacity or gray)
- Include a clear selection mechanism (brush, click, or lasso)
- Provide a reset/clear selection button to restore full view
- Consider showing selection count or summary statistics
- Libraries with native linked selection support (Altair, Bokeh, Plotly) should leverage those features
