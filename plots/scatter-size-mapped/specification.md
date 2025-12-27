# scatter-size-mapped: Bubble Chart

## Description

A bubble chart where marker size represents a third variable. Semi-transparent markers reveal overlapping points and enable comparison of three dimensions simultaneously on a 2D plane.

## Applications

- **Economic analysis**: Comparing countries by GDP, population, and area
- **Business metrics**: Visualizing market segments by revenue, growth, and market share
- **Scientific data**: Showing measurements with intensity or magnitude values
- **Social sciences**: Displaying demographic data across multiple variables

## Data

Generate synthetic data representing country economic indicators:
- 30-50 data points representing different entities
- X-axis: GDP per capita (continuous, 1,000-80,000 range)
- Y-axis: Life expectancy (continuous, 50-85 range)
- Bubble size: Population (log scale recommended for better visibility)
- Optional: Category for coloring by region/continent

Example structure:
```
country      | gdp_per_capita | life_expectancy | population  | region
USA          | 63000          | 78.5           | 330000000   | Americas
Germany      | 51000          | 81.2           | 83000000    | Europe
Japan        | 42000          | 84.3           | 126000000   | Asia
```

## Notes

- Use semi-transparent markers (alpha 0.5-0.7) to reveal overlapping bubbles
- Scale bubble sizes appropriately - largest should not overwhelm the plot
- Consider log scaling for size variable if data spans multiple orders of magnitude
- Include size legend showing what bubble sizes represent
- Add axis labels with units
- Use colormap if including category dimension
- Consider adding annotations for notable data points
