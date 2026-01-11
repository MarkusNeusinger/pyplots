# bar-race-animated: Animated Bar Chart Race

## Description

An animated horizontal bar chart that visualizes how rankings and values change over time. Bars smoothly transition positions as their values update, with the chart reordering to maintain a sorted ranking at each time step. This dynamic visualization format is highly engaging for storytelling with time-series data, making it popular for showing the rise and fall of entities like countries, companies, or products over extended periods.

## Applications

- Visualizing how country GDP rankings have shifted over decades, with bars racing as economies grow and overtake one another
- Tracking brand market share evolution throughout the year, showing competitive dynamics in an engaging animated format
- Displaying historical sports team standings or player statistics over multiple seasons, revealing dynasty periods and surprising reversals

## Data

- `entity` (categorical) - The items being compared and ranked (countries, companies, teams, products)
- `time` (datetime or numeric) - Time points for each snapshot, driving the animation sequence
- `value` (numeric) - The metric determining bar length and ranking at each time point
- `color` (categorical, optional) - Category or group for coloring bars consistently
- Size: 10-20 entities with 20-100 time points recommended for smooth, comprehensible animation
- Example: Country GDP by year, streaming platform subscribers by month, brand revenue by quarter

## Notes

- Bars should be sorted by value at each frame, with smooth transitions for position changes
- Entity labels should remain attached to their bars throughout the animation
- A visible time indicator (counter, axis label, or title) should update during playback
- Animation speed should be configurable or use a reasonable default duration
- For static output or libraries without animation support, show a small multiples grid of key time snapshots
- Consider including play/pause controls and a timeline scrubber for interactive versions
- Color should remain consistent for each entity across all frames for tracking
