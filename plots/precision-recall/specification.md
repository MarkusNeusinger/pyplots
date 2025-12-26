# precision-recall: Precision-Recall Curve

## Description

A Precision-Recall curve plots precision (positive predictive value) against recall (sensitivity) at various classification thresholds. This visualization is essential for evaluating binary classifiers on imbalanced datasets where accuracy alone is misleading. The area under the curve (Average Precision) summarizes classifier performance, with higher values indicating better performance.

## Applications

- Evaluating fraud detection models where fraudulent transactions are rare compared to legitimate ones
- Assessing medical diagnostic systems where correctly identifying positive cases (high recall) is critical
- Comparing information retrieval systems for document search relevance ranking
- Optimizing spam filters to balance catching spam (recall) with minimizing false positives (precision)

## Data

- `y_true` (binary array) - Ground truth binary labels (0 or 1)
- `y_scores` (numeric array) - Predicted probabilities or decision function scores from classifier
- Size: 100-10000 samples typical for evaluation
- Example: Binary classification predictions from sklearn classifier with `predict_proba()` output

## Notes

- Display Average Precision (AP) score in legend or annotation
- Include baseline reference line showing random classifier performance (horizontal line at positive class ratio)
- Use stepped line style to accurately represent threshold-based curve
- Consider showing iso-F1 curves as contour lines for F1 score reference
- For multiple classifiers comparison, use distinct colors with clear legend
