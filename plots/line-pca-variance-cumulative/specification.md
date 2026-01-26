# line-pca-variance-cumulative: Cumulative Explained Variance for PCA Component Selection

## Description

A line plot showing the cumulative proportion of explained variance as a function of the number of Principal Component Analysis (PCA) components. This visualization helps determine the optimal number of components to retain by displaying the trade-off between dimensionality reduction and information preservation. The cumulative curve typically exhibits an elbow pattern where additional components yield diminishing returns, and horizontal threshold lines (e.g., 90%, 95%) guide component selection decisions.

## Applications

- Dimensionality reduction: choosing how many PCA components to retain for downstream machine learning tasks
- Feature engineering: determining the optimal reduced feature space size while preserving target variance thresholds
- Data compression: evaluating information loss vs. computational efficiency trade-offs in high-dimensional data
- Exploratory data analysis: understanding the intrinsic dimensionality and complexity of multivariate datasets

## Data

- `explained_variance_ratio` (numeric array) - proportion of variance explained by each individual component (sums to 1.0)
- `n_components` (integer) - number of PCA components (x-axis values from 1 to total components)
- Size: typically 5-50 components depending on original feature count
- Example: scikit-learn's `PCA.explained_variance_ratio_` attribute

## Notes

- Display cumulative sum on y-axis, not individual variance per component
- Y-axis should show percentage (0-100%) or proportion (0.0-1.0)
- Add horizontal dashed reference lines at common thresholds: 90%, 95%, and optionally 99%
- Mark or annotate the elbow point if automatically detectable
- Use clear markers at each component count to show discrete values
- Consider including individual variance ratios as a secondary bar plot overlay (optional enhancement)
- X-axis should start at 1 (first component), not 0
