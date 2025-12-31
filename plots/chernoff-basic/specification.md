# chernoff-basic: Chernoff Faces for Multivariate Data

## Description

Chernoff faces visualize multivariate data by mapping each variable to a facial feature (eye size, mouth curvature, face width, nose length, etc.), transforming each observation into a unique cartoon face. This technique leverages humans' innate ability to recognize and distinguish faces, making it easier to identify patterns, clusters, and outliers across multiple dimensions simultaneously.

## Applications

- Comparing financial health indicators across companies where each face represents a company's performance metrics
- Visualizing patient health profiles in medical research where facial features encode vital signs and lab results
- Analyzing customer segments in marketing where each face represents a customer profile with demographic and behavioral attributes

## Data

- `observation_id` (categorical) - Unique identifier for each observation/face
- `variable_1` through `variable_n` (numeric) - Continuous variables mapped to facial features (typically 5-15 variables)
- Size: 5-50 observations (faces become hard to compare with too many)
- Example: Iris dataset with 4 measurements per flower, or car ratings with multiple performance metrics

## Notes

- Each variable should be normalized to a common scale (0-1) before mapping to facial features
- Common feature mappings: face width, face height, eye size, eye spacing, eyebrow slant, nose length, mouth curvature, mouth width
- Grid layout recommended for comparing multiple faces side by side
- Consider colorizing faces by group membership if categorical grouping exists
