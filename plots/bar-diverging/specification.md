# bar-diverging: Diverging Bar Chart

## Description

A diverging bar chart displays bars extending in opposite directions from a central baseline, typically at zero. This visualization is ideal for comparing positive and negative values, showing responses above and below a neutral point, or contrasting opposing categories. Different colors distinguish positive from negative values, making it easy to identify magnitude and direction at a glance.

## Applications

- Visualizing survey responses (agree/disagree, satisfied/dissatisfied scales)
- Displaying net promoter scores or sentiment analysis results
- Comparing political polling data across ideological spectrums
- Showing profit/loss or growth/decline metrics across categories

## Data

- `category` (str) - Category label for each bar (e.g., product name, demographic group)
- `value` (float) - Numeric value that can be positive or negative
- Size: 5-30 categories works well; too many categories reduces readability
- Example: Survey responses with scores ranging from -100 to +100

## Notes

- Use contrasting colors for positive and negative values (e.g., blue/red, green/orange)
- Consider horizontal orientation for long category labels
- Add a vertical line or clear visual indicator at the zero baseline
- Sort bars by value to enhance pattern recognition
