# line-animated-progressive: Animated Line Plot Over Time

## Description

An animated line plot that builds progressively over time, with the line drawing itself from left to right and revealing data points sequentially. This visualization technique transforms a standard time series into a dynamic storytelling element, ideal for presentations where the narrative unfolds as the line extends across the chart. The progressive reveal creates anticipation and helps audiences follow temporal patterns as they develop.

## Applications

- Presenting quarterly revenue growth in executive presentations, with the line building to show how performance evolved
- Telling the story of a scientific discovery or experiment by progressively revealing how measurements changed over time
- Creating engaging educational content that walks students through historical data trends, such as temperature records or population changes

## Data

- `time` (datetime or numeric) - The temporal dimension on the x-axis, driving the sequential reveal
- `value` (numeric) - The measurement or metric being visualized on the y-axis
- `series` (categorical, optional) - Multiple line series for comparing parallel trends
- Size: 20-200 data points recommended; enough for smooth animation but not overwhelming
- Example: Monthly stock prices over 5 years, daily temperature readings, or weekly sales figures

## Notes

- Animation should be smooth with configurable speed or duration
- Consider adding a trailing highlight or glow effect on the most recent point being drawn
- The current x-axis position or timestamp should be clearly indicated during playback
- For static output, show the complete line with a visual indicator (gradient or markers) suggesting the direction of progression
- Libraries without animation support should implement a small multiples version showing key stages of the line's progression
- Play/pause controls and speed adjustment enhance the presentation experience
