# bubble-packed: Basic Packed Bubble Chart

## Description

A packed bubble chart displays data as circles where size represents value, and circles are packed together without overlap using physics simulation. Unlike scatter or traditional bubble charts, position has no meaning - only size and optional grouping matter. This visualization efficiently uses space for comparing values across many categories.

## Applications

- Budget and spending visualization: comparing department expenditures where circle size shows amount
- Market share comparison: visualizing competitor sizes within an industry
- Portfolio composition: displaying asset allocation or inventory breakdown
- Categorical value comparison: showing values across many categories where ranking and proportion matter

## Data

- `label` (categorical) - Category or item names
- `value` (numeric) - Size values determining circle area
- `group` (categorical, optional) - For clustering related items together
- Size: 10-100 items recommended for clear visualization
- Example: Synthetic data representing category values

## Notes

- Scale circle sizes by area (not radius) for accurate visual perception
- Use force simulation to pack circles without overlap
- Labels can be placed inside circles (if large enough) or as tooltips
- Color can encode category or group membership
- Optional grouping clusters related circles with spacing between groups
