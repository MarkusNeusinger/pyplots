# scatter-animated-controls: Animated Scatter Plot with Play Controls

## Description

An animated scatter plot that displays data points changing over time, inspired by Hans Rosling's Gapminder visualizations. This plot includes interactive play/pause controls and a timeline slider, allowing users to explore temporal patterns, observe how data evolves across time periods, and pause at specific moments for detailed analysis. Ideal for storytelling with data and revealing trends that unfold over time.

## Applications

- Visualizing country-level metrics (GDP, life expectancy, population) evolving over decades like Gapminder
- Tracking product performance metrics across multiple quarters or years
- Exploring how scientific measurements or experimental results change through sequential observations

## Data

- `x` (numeric) - Variable plotted on the horizontal axis, changing over time
- `y` (numeric) - Variable plotted on the vertical axis, changing over time
- `time` (numeric or datetime) - Time dimension that drives the animation frames
- `size` (numeric, optional) - Point size encoding for a third variable
- `color` (categorical, optional) - Category for color-coding different groups/entities
- `label` (string, optional) - Entity labels for identification
- Size: 10-100 entities tracked across 10-50 time periods recommended
- Example: Simulated country data with GDP per capita, life expectancy, and population over 20 years

## Notes

- Play/pause button should be prominently visible and intuitive
- Timeline slider enables jumping to any point in the animation
- Current time/year should be displayed clearly (often as large text in background or corner)
- Smooth transitions between frames enhance the storytelling effect
- Optional trails can show the path of entities over time
- Libraries without animation support should implement a static faceted version showing key time points
