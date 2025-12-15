# swarm-basic: Basic Swarm Plot

## Description

A swarm plot (beeswarm plot) displays individual data points for categorical comparisons, with points spread horizontally to avoid overlap. This reveals the full distribution shape and density while preserving exact values - combining the benefits of strip plots (individual points) and violin plots (density visualization). Ideal when you need to see every observation rather than just summary statistics.

## Applications

- Comparing response times across different experimental conditions in psychology research
- Visualizing patient biomarker levels across treatment groups in clinical trials
- Analyzing employee performance scores by department
- Displaying student test scores by classroom to identify patterns and outliers

## Data

- `category` (categorical) - Group labels for comparison on the categorical axis
- `value` (numeric) - Continuous variable values shown on the value axis
- Size: 20-300 observations total (swarm plots become cluttered with too many points)
- Example: Performance metrics across 3-5 groups with 30-60 observations per group

## Notes

- Points should be sized appropriately to show spread without excessive overlap
- Use consistent point sizes within the plot
- Consider adding a subtle mean or median marker for each category
- Color can distinguish categories or encode an additional variable
- Maintain clear spacing between category groups
