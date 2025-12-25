# heatmap-clustered: Clustered Heatmap

## Description

A heatmap with hierarchical clustering dendrograms on rows and/or columns, showing both data values and their hierarchical relationships. Rows and columns are automatically reordered based on clustering results to reveal natural groupings in the data. Essential for discovering patterns in high-dimensional data where similar observations or variables should be visually grouped together.

## Applications

- Gene expression analysis identifying co-expressed genes and sample clusters
- Customer segmentation revealing behavioral patterns and market segments
- Feature correlation analysis with automatic grouping of related variables
- Biological pathway analysis clustering related proteins or metabolites

## Data

- `matrix` (numeric) - 2D matrix of values for heatmap cells
- `row_labels` (string) - labels for matrix rows
- `column_labels` (string) - labels for matrix columns
- Size: 10-100 rows, 10-50 columns (larger matrices may have readability issues)

## Notes

- Display dendrograms on both rows and columns (clustermap style)
- Reorder rows and columns according to hierarchical clustering results
- Use a diverging colormap for data centered around zero
- Include a colorbar legend showing the value scale
- Consider adding row/column color bars for group annotations
- Ward's method with Euclidean distance is a common default for clustering
