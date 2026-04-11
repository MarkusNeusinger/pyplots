# dot-matrix-proportional: Dot Matrix Chart for Proportional Counts

## Description

A dot matrix chart displays proportions using a grid of equally-sized dots where filled or colored dots represent counts out of a total. Each dot corresponds to one unit, making it intuitive to read "X out of N" statistics at a glance. Unlike waffle charts that use percentage-based squares, dot matrix charts emphasize absolute counts with variable grid sizes, excelling at risk communication and survey result visualization.

## Applications

- Showing survey results where 47 out of 100 respondents agreed with a statement
- Visualizing medical risk such as 3 in 1,000 patients experiencing a side effect
- Displaying election or vote breakdowns across candidates or parties
- Communicating proportions in infographics and reports for general audiences

## Data

- `category` (str) - Group name identifying each segment (e.g., "Agreed", "Disagreed", "No opinion")
- `count` (int) - Number of units (dots) for that category
- `total` (int) - Total grid size representing the full population (e.g., 100, 500, 1000)
- Size: 2-5 categories, total between 50 and 1,000 dots

## Notes

- Grid layout should match the total (e.g., 10x10 for 100, 10x50 for 500)
- Each dot represents exactly one unit
- Dots are color-coded by category, filled left-to-right, top-to-bottom
- Include a legend with category labels and their counts
- Use uniform dot size and spacing for accurate visual comparison
- Consider adding count or percentage annotations alongside the legend
