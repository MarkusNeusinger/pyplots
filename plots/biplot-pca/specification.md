# biplot-pca: PCA Biplot with Scores and Loading Vectors

## Description

A PCA biplot simultaneously displays both observation scores (as points) and variable loadings (as arrows) in the principal component space. This dual representation is essential for interpreting PCA results, revealing how observations relate to each other and which original variables drive the separation along each principal component. The length and direction of loading arrows indicate variable importance and correlation with the components.

## Applications

- Exploratory data analysis to understand which variables contribute most to data variance and how samples cluster in reduced dimensionality
- Quality control in manufacturing to visualize relationships between process variables and identify outliers in multivariate measurements
- Gene expression analysis to reveal sample groupings and identify which genes drive biological variation across conditions

## Data

- `features` (numeric matrix) - Multiple continuous variables for PCA decomposition (columns are features, rows are observations)
- `labels` (optional categorical) - Group labels for coloring observations
- Variables: 4-10 original features recommended for readable loading arrows
- Size: 30-200 observations for visual clarity
- Example: Iris dataset or similar multivariate numeric data

## Notes

- Display PC1 vs PC2 (the two components explaining most variance) as the default view
- Show observation scores as points, optionally colored by group labels
- Draw variable loadings as arrows originating from the origin
- Label each loading arrow with the corresponding variable name
- Scale loadings appropriately so arrows are visible alongside score points (often requires separate scaling)
- Include axis labels showing component name and variance explained percentage (e.g., "PC1 (45.2%)")
- Consider adding a unit circle as reference for loading magnitudes when using correlation biplot scaling
