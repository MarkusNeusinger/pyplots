# andrews-curves: Andrews Curves for Multivariate Data

## Description

Andrews curves visualization transforms multivariate observations into smooth Fourier series curves. Each data point is represented as a continuous function where variable values become coefficients in a Fourier expansion, producing distinctive wave patterns. This technique enables visual comparison of multivariate patterns, cluster identification, and outlier detection—observations with similar values across variables produce similar curves, while outliers appear as distinctly different patterns.

## Applications

- Comparing iris flower species across sepal/petal measurements to visualize natural clustering in botanical data
- Detecting anomalous network traffic patterns by transforming connection metrics into curves and identifying outliers
- Analyzing wine quality factors (acidity, sugar, alcohol, pH) to reveal how different quality grades separate visually

## Data

- `variable_1` through `variable_n` (numeric) - Multiple numeric attributes for each observation
- `category` (categorical, optional) - Group identifier for color coding curves
- Size: 30-150 observations with 4-8 dimensions recommended
- Example: Iris dataset with sepal length, sepal width, petal length, petal width by species

## Notes

- Normalize variables to similar scales before transformation to prevent dominant variables
- Use transparency (alpha < 0.5) when plotting many curves to reveal density patterns
- Color by category to highlight cluster separation between groups
- The parameter t typically ranges from -π to π for the Fourier expansion
