# elbow-curve: Elbow Curve for K-Means Clustering

## Description

An elbow curve visualizes the relationship between the number of clusters (k) and within-cluster sum of squares (inertia/distortion) in K-means clustering. The plot helps identify the optimal number of clusters by finding the "elbow point" where adding more clusters yields diminishing returns in reducing inertia. This is a fundamental diagnostic tool for unsupervised learning parameter selection.

## Applications

- Selecting the optimal number of clusters (k) in K-means clustering analysis
- Customer segmentation to determine natural groupings in behavioral data
- Image compression parameter selection for color quantization
- Document clustering to identify topic groupings in text corpora

## Data

- `k_values` (numeric) - Number of clusters tested (typically 1 to 10 or 15)
- `inertia` (numeric) - Within-cluster sum of squares for each k value
- Size: 8-15 different k values for clear elbow visualization
- Example: Scikit-learn's `KMeans.inertia_` attribute across multiple k values

## Notes

- X-axis shows number of clusters (k), y-axis shows inertia/distortion
- The elbow point is where the rate of decrease sharply changes
- Consider annotating or highlighting the optimal k value
- Use markers at each data point to show discrete k values tested
- A smooth connecting line helps visualize the curve shape
