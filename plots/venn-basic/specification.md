# venn-basic: Venn Diagram

## Description

A Venn diagram visualizes the logical relationships between two or three sets using overlapping circles. Each circle represents a set, and overlapping regions show elements shared between sets. This classic visualization is ideal for showing intersections, unions, and exclusive memberships, making abstract set relationships immediately intuitive.

## Applications

- Comparing feature overlap between product offerings or service tiers
- Analyzing survey responses where respondents may belong to multiple groups
- Visualizing gene expression overlap in biological research
- Illustrating shared and unique skills across team members or job candidates

## Data

- `set_labels` (list of strings) - Names for each set (2-3 sets)
- `set_sizes` (list of integers) - Total size of each set
- `intersections` (dict or list) - Sizes of pairwise and triple overlaps
- Size: 2-3 sets maximum for clarity
- Example: Three sets A, B, C with sizes 100, 80, 60 and overlaps AB=30, AC=20, BC=25, ABC=10

## Notes

- Limit to 2 or 3 circles for visual clarity (more circles become unreadable)
- Area proportional to size when possible (proportional Venn diagrams)
- Display counts or percentages in each region
- Use distinct colors with transparency to show overlapping areas clearly
- Ensure text labels are readable against all background colors
