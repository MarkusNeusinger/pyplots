# roc-curve: ROC Curve with AUC

## Description

A Receiver Operating Characteristic (ROC) curve visualizes the performance of a binary classifier by plotting the True Positive Rate (TPR) against the False Positive Rate (FPR) at various classification thresholds. The Area Under the Curve (AUC) provides a single metric summarizing model performance, where 1.0 indicates perfect classification and 0.5 represents random guessing.

## Applications

- Evaluating binary classification model performance in machine learning pipelines
- Comparing multiple models to select the best classifier for production
- Selecting optimal classification thresholds based on sensitivity/specificity trade-offs
- Assessing diagnostic test accuracy in medical research

## Data

- `fpr` (numeric) - False Positive Rate values (0 to 1)
- `tpr` (numeric) - True Positive Rate values (0 to 1)
- `auc` (numeric) - Area Under the Curve score (0 to 1)
- Size: typically 100-1000 threshold points per curve
- Example: sklearn.metrics.roc_curve output from binary classification predictions

## Notes

- Include a diagonal reference line (y=x) representing random classifier performance
- Display AUC score in legend or annotation
- Use distinct colors/styles when comparing multiple models
- Axes should range from 0 to 1 with equal aspect ratio preferred
