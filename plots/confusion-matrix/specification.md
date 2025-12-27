# confusion-matrix: Confusion Matrix Heatmap

## Description

A specialized heatmap visualization for evaluating classification model performance, displaying the counts or proportions of predicted vs actual class labels. The confusion matrix reveals true positives, false positives, true negatives, and false negatives at a glance, making it essential for understanding model behavior, identifying class imbalances, and diagnosing specific misclassification patterns.

## Applications

- Binary classification model evaluation showing sensitivity and specificity
- Multi-class classifier performance analysis with per-class accuracy breakdown
- Model comparison to identify which classes are most often confused
- Error analysis to understand systematic misclassification patterns

## Data

- `true_labels` (categorical) - ground truth class labels for each sample
- `predicted_labels` (categorical) - model-predicted class labels for each sample
- `class_names` (string) - display names for each class on the axes
- Size: 2-20 classes (larger matrices may have readability issues)
- Example: Classification results from a trained model on test data

## Notes

- Label axes clearly: "True Label" (y-axis) and "Predicted Label" (x-axis)
- Annotate cells with counts or percentages for precise interpretation
- Support normalization options: none (raw counts), by row (recall), by column (precision), or by total
- Use sequential colormap (e.g., Blues) for count data
- Include colorbar showing the value scale
- Consider highlighting diagonal (correct predictions) for visual clarity
