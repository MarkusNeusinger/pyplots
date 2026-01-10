# scatter-matrix-interactive: Interactive Scatter Plot Matrix (SPLOM)

## Description

An interactive scatter plot matrix (SPLOM) for exploring relationships between multiple variables with full interactivity. Users can brush to select points in one subplot and see corresponding points highlighted across all other subplots, enabling discovery of patterns that span multiple dimensions. Supports zooming, panning, and linked selection across the entire matrix, making it a powerful tool for multivariate exploratory data analysis.

## Applications

- Interactive exploration of multivariate datasets where analysts brush regions to identify clusters and correlations across multiple variable pairs simultaneously
- Feature engineering in machine learning workflows where data scientists interactively select subgroups to understand their distribution across all features
- Quality control analysis where engineers select outlier regions in one measurement and instantly see how those points behave across all other measurements

## Data

- `variables` (list of numeric columns) - Multiple continuous variables to compare pairwise
- Variables: 3-5 recommended for usability (grid grows quadratically)
- Size: 50-500 points recommended for responsive interactions
- Example: Iris dataset, mtcars, or similar multivariate numeric data

## Notes

- Brushing/selection in any subplot must highlight corresponding points in all other subplots
- Support for box selection or lasso selection across scatter plots
- Diagonal cells should show univariate distributions (histograms or KDE) that update or highlight based on selection
- Include zoom and pan functionality for detailed inspection
- Unselected points should be visually de-emphasized (reduced opacity or gray)
- Provide a clear way to reset/clear selection
- Use consistent color encoding across all subplots
- Libraries without native linked selection (matplotlib, seaborn, plotnine) may need alternative approaches or should note limitations
- Interactive libraries (Plotly, Bokeh, Altair) should leverage their built-in linked brushing capabilities
