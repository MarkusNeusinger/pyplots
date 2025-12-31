# pdp-basic: Partial Dependence Plot

## Description

A partial dependence plot (PDP) showing the marginal effect of one feature on the predicted outcome of a machine learning model. The plot displays how predictions change as a feature varies across its range, while averaging over the effects of all other features. This visualization is essential for understanding the relationship between individual features and model predictions in interpretable machine learning.

## Applications

- Interpreting complex models like gradient boosting or random forests by revealing how features influence predictions
- Validating that learned relationships align with domain knowledge (e.g., higher prices lead to lower demand)
- Communicating model behavior to non-technical stakeholders by showing intuitive feature-response curves

## Data

- `feature_values` (numeric) - The range of values for the feature being analyzed on the x-axis
- `partial_dependence` (numeric) - The average predicted outcome for each feature value on the y-axis
- `confidence_interval` (numeric, optional) - Upper and lower bounds showing prediction variability across samples
- Size: 50-100 grid points along feature range recommended for smooth curves
- Example: PDP from sklearn's `PartialDependenceDisplay` for a feature in a GradientBoostingRegressor

## Notes

- The y-axis represents partial dependence (average prediction), not probability
- Include a confidence band or individual conditional expectation (ICE) lines for uncertainty visualization
- A rug plot along the x-axis can show the distribution of training data values
- Consider centering the partial dependence at zero for easier interpretation of relative effects
- For categorical features, use a bar or step plot instead of a continuous line
