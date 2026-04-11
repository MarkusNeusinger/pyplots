# shap-waterfall: SHAP Waterfall Plot for Feature Attribution

## Description

A waterfall-style chart showing how each feature contributes to pushing a model prediction from a base value (expected model output) to the final predicted value. Horizontal bar segments extend right for positive SHAP values and left for negative SHAP values, stacking cumulatively so the viewer can trace the path from baseline to prediction. This is a core ML explainability visualization for explaining individual predictions, complementing the SHAP summary plot which shows feature effects across many samples.

## Applications

- Explaining individual predictions in credit scoring models to auditors or loan applicants
- Debugging unexpected model outputs in healthcare ML by identifying which features drove the prediction
- Communicating feature impact to non-technical stakeholders in business decision-making
- Satisfying regulatory compliance requirements for model explainability (e.g., GDPR right to explanation)

## Data

- `feature` (str) - Feature names (e.g., "Age", "Income", "Credit Score")
- `shap_value` (float) - SHAP contribution value per feature (positive pushes prediction up, negative pushes down)
- `base_value` (float) - Expected model output (mean prediction across training data), single scalar
- `final_value` (float) - Actual model prediction for this instance (base_value + sum of SHAP values), single scalar
- Size: 10-20 features typical; show top features by absolute SHAP magnitude

## Notes

- Order features by absolute SHAP value magnitude (largest contribution at top)
- Cumulative bar segments flow from base_value to final_value
- Color bars red/pink for positive SHAP contributions and blue for negative contributions
- Display base value and final prediction value as labeled reference lines or annotations
- Show numeric SHAP values on or beside each bar segment
- Use a horizontal layout with feature names on the y-axis for readability
- Consider a connector line between segments to emphasize the cumulative flow
