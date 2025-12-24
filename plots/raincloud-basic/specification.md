# raincloud-basic: Basic Raincloud Plot

## Description

A raincloud plot combines three visualization elements—a half-violin (the "cloud"), jittered strip points (the "rain"), and a box plot—to provide a comprehensive view of data distribution. This hybrid approach shows distribution shape, summary statistics, and individual observations simultaneously, addressing the limitation of box plots that can hide multimodal distributions. Often called the "gold standard" for transparent statistical visualization in scientific publications.

## Applications

- Comparing treatment effects across experimental groups in clinical trials
- Visualizing response time distributions in psychology experiments
- Analyzing score distributions across different conditions in A/B testing
- Presenting survey response distributions by demographic groups

## Data

- `category` (categorical) - Group labels for comparison on the categorical axis
- `value` (numeric) - Continuous variable values shown on the value axis
- Size: 20-300 observations per category, 2-6 categories
- Example: Reaction times (ms) for control vs treatment groups

## Notes

- Position half-violin on one side, jittered points on the other, with box plot in between
- Use moderate jitter (0.05-0.1) to spread points without excessive overlap
- Apply transparency (alpha 0.5-0.7) to jittered points
- Include median and quartile markers in box plot
- Consider horizontal orientation for better label readability with many categories
