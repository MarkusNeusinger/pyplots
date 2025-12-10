# violin-basic: Basic Violin Plot

## Description

A violin plot combines a box plot with a kernel density estimation, displaying the full distribution shape of numerical data across different categories. The symmetric curves show probability density, while inner markers indicate quartiles or median. Ideal for comparing distributions where shape matters as much as summary statistics.

## Applications

- Comparing salary distributions across departments to reveal bimodal patterns
- Analyzing test score distributions by class to identify performance clusters
- Visualizing response time distributions per server to detect latency patterns
- Examining customer satisfaction scores across product lines

## Data

- `category` (categorical) - group labels for each violin
- `value` (numeric) - values for distribution visualization
- Size: 3-6 groups, 50-200 values per group
- Example: performance metrics grouped by team or region

## Notes

- Kernel bandwidth affects smoothness - use library defaults for consistency
- Include inner quartile markers or mini box plot for reference statistics
- Ensure sufficient data points per group for meaningful density estimation
- Horizontal orientation is useful when category names are long, improving readability
- Both vertical (default) and horizontal orientations are valid implementations
