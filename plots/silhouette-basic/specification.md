# silhouette-basic: Silhouette Plot

## Description

A silhouette plot visualizes the quality of clustering results by showing the silhouette coefficient for each sample, grouped by cluster assignment. Each horizontal bar represents a sample's silhouette score (-1 to 1), where positive values indicate good cluster membership and negative values suggest potential misclassification. This visualization helps evaluate cluster cohesion (how similar samples are to their own cluster) and separation (how distinct they are from neighboring clusters).

## Applications

- Evaluating K-means, hierarchical, or other clustering algorithm results
- Comparing different numbers of clusters to find optimal k value
- Identifying poorly clustered or potentially misclassified samples
- Validating cluster assignments before downstream analysis

## Data

- `samples` (numeric) - feature vectors for each data point to be clustered
- `cluster_labels` (integer) - cluster assignment for each sample (0 to k-1)
- `silhouette_values` (numeric) - silhouette coefficient per sample (-1 to 1)
- Size: 50-500 samples with 2-10 clusters for readable visualization
- Example: clustering iris dataset into 3 species groups

## Notes

- Display horizontal bars for each sample's silhouette score, sorted within each cluster
- Group samples by cluster with distinct colors per cluster
- Include vertical line at average silhouette score for reference
- Annotate each cluster section with its average silhouette score
- Use sklearn.metrics.silhouette_samples for computing individual scores
- Clusters with consistently high scores (close to 1) indicate well-separated groups
