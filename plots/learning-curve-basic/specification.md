# learning-curve-basic: Model Learning Curve

## Description

A learning curve visualizes model performance (training and validation scores) as a function of training set size. It is essential for diagnosing bias vs variance tradeoffs, determining whether collecting more data would improve model performance, and guiding model selection decisions. The plot typically shows two lines with shaded confidence bands representing variability across cross-validation folds.

## Applications

- Diagnosing underfitting (high bias) when both training and validation scores are low
- Diagnosing overfitting (high variance) when training score is high but validation score is low with a large gap
- Determining if collecting more training data would improve model performance
- Comparing learning characteristics across different model architectures

## Data

- `train_sizes` (numeric) - Array of training set sizes used for evaluation
- `train_scores` (numeric) - Training scores at each sample size (2D: folds × sizes)
- `validation_scores` (numeric) - Validation scores at each sample size (2D: folds × sizes)
- Size: 5-20 different training set sizes, typically with 5-10 cross-validation folds
- Example: Scikit-learn's `learning_curve` function output

## Notes

- Use shaded regions to show confidence bands (e.g., ±1 standard deviation across folds)
- Clearly label the y-axis with the metric being evaluated (accuracy, F1, MSE, etc.)
- Include a legend distinguishing training from validation curves
- X-axis should show actual sample sizes or percentages of total training data
- Consider using distinct colors (e.g., blue for training, orange for validation) for clarity
