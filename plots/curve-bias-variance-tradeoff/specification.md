# curve-bias-variance-tradeoff: Bias-Variance Tradeoff Curve

## Description

A theoretical visualization of the bias-variance tradeoff showing how total prediction error decomposes into bias squared, variance, and irreducible noise as a function of model complexity. The plot displays multiple curves: bias squared (decreasing with complexity), variance (increasing with complexity), irreducible error (constant), and total error (U-shaped). This is one of the most fundamental conceptual plots in machine learning for understanding model selection, overfitting, and underfitting.

## Applications

- ML education: explaining the fundamental tradeoff between underfitting (high bias) and overfitting (high variance)
- Model selection: visualizing why more complex models are not always better
- Regularization justification: understanding why adding constraints to models improves generalization
- Algorithm comparison: explaining why ensemble methods work by reducing variance

## Data

- `model_complexity` (numeric) - x-axis representing model flexibility (e.g., polynomial degree, tree depth, number of parameters)
- Theoretical curves (generated, not empirical data):
  - `bias_squared` (numeric) - decreasing function of complexity (e.g., 1/(1 + complexity))
  - `variance` (numeric) - increasing function of complexity (e.g., complexity/scale)
  - `irreducible_error` (numeric) - constant horizontal line representing noise floor
  - `total_error` (numeric) - sum of bias_squared + variance + irreducible_error
- Size: 50-100 points for smooth curves

## Notes

- X-axis: Model Complexity (labeled from "Low" to "High" or with specific values)
- Y-axis: Prediction Error
- Display 4 curves with distinct colors and line styles: Bias squared, Variance, Total Error, Irreducible Error
- Mark the optimal complexity point where total error is minimized with a vertical line or annotation
- Use annotations to label each curve directly on the plot
- Include the formula: Total Error = Bias² + Variance + Irreducible Error
- Consider adding shaded regions to indicate underfitting zone (left) and overfitting zone (right)
