# waterfall-basic: Basic Waterfall Chart

## Description

A waterfall chart visualizes how an initial value is affected by a series of intermediate positive or negative values, leading to a final value. Each bar represents a change from the previous cumulative total, with positive values extending upward and negative values extending downward. This chart type is essential for understanding cumulative effects and breaking down the components that contribute to a final result.

## Applications

- Financial analysis: breaking down revenue to net profit through costs, taxes, and adjustments
- Inventory management: tracking stock levels through additions and withdrawals over time
- Project cost tracking: visualizing budget changes through additions and reductions
- Sales pipeline progression: showing conversion rates and drop-offs through stages

## Data

- `category` (string) - step labels describing each change (e.g., "Starting Balance", "Sales", "Costs", "Taxes", "Net Profit")
- `value` (numeric) - change values (positive for increases, negative for decreases)
- Size: 5-15 steps
- Example: quarterly financial breakdown from revenue to net income

## Notes

- Color positive and negative changes differently (e.g., green for positive, red for negative)
- Show connecting lines between bars to emphasize the cumulative flow
- Include distinct start and end total bars (often in a different color like blue or gray)
- Display running total labels on or near bars for clarity
- First and last bars typically represent totals, middle bars represent changes
