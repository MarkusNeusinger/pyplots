# ternary-basic: Basic Ternary Plot

## Description

A ternary plot displays three-component compositional data on an equilateral triangle where each vertex represents 100% of one component. Points inside the triangle show compositions that sum to a constant total (usually 100%), with position indicating relative proportions. This visualization is essential for data where three variables are interdependent and constrained to sum to a fixed value.

## Applications

- Analyzing chemical or material compositions (e.g., alloy mixtures, cement formulations)
- Soil classification using sand, silt, and clay proportions
- Visualizing market share distribution among three competitors
- Studying color mixing with RGB or other three-component systems

## Data

- `component_a` (numeric) - Proportion of first component (0-100%)
- `component_b` (numeric) - Proportion of second component (0-100%)
- `component_c` (numeric) - Proportion of third component (0-100%)
- Size: 20-200 points work well; larger datasets may need density visualization
- Constraint: All three components must sum to 100% (or a constant total)

## Notes

- Grid lines should be drawn at regular intervals (typically 10% or 20%)
- Each vertex should be clearly labeled with component names
- Points should be visually distinct with appropriate marker size and color
- Consider adding tick marks along each edge to aid reading proportions
