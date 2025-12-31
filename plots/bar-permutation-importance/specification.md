# bar-permutation-importance: Permutation Feature Importance Plot

## Description

A horizontal bar chart displaying permutation feature importance from machine learning models, showing the decrease in model score when each feature is randomly shuffled. Unlike model-specific feature importances, permutation importance is model-agnostic and measures how much the model's performance degrades when a feature's relationship with the target is broken. Error bars indicate variability across multiple shuffles, providing a confidence measure for each importance score.

## Applications

- Comparing feature importance across different model types (e.g., comparing a random forest vs neural network on the same dataset)
- Identifying features that may be redundant or have spurious correlations by examining importance variability
- Model validation by verifying that domain-expected important features rank highly in permutation importance

## Data

- `feature` (categorical) - Names of the model features displayed on the y-axis
- `importance_mean` (numeric) - Mean decrease in model score across permutation repetitions
- `importance_std` (numeric) - Standard deviation of the score decrease, displayed as error bars
- Size: 10-30 features recommended for readability
- Example: Output from sklearn.inspection.permutation_importance with n_repeats=10

## Notes

- Sort bars by mean importance (highest at top) for easy identification of key features
- Include horizontal error bars to show importance variability across shuffles
- Use a sequential color gradient mapped to importance values for visual emphasis
- Add a vertical reference line at x=0 to distinguish positive from negative importance values
- Consider showing only top N features if the model has many features
