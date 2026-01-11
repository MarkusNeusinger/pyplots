# bar-realtime: Real-Time Updating Bar Chart

## Description

A bar chart that displays live-updating values with smooth animated transitions between states. This visualization is ideal for monitoring scenarios where categorical metrics change continuously and viewers need to observe comparative values as they evolve. Unlike static bar charts, real-time bar charts create the effect of streaming data through animated bar height changes, optional value label updates, and visual feedback on significant changes.

## Applications

- Displaying live voting or polling results as votes come in, with bars animating to reflect current standings
- Visualizing real-time leaderboard scores in gaming or competitive contexts, showing player rankings as they shift
- Monitoring live inventory levels across product categories, with color changes indicating low stock thresholds
- Streaming metrics comparison in dashboards showing concurrent users, active sessions, or throughput by service

## Data

- `category` (categorical) - Labels for each bar representing distinct groups or items being compared
- `value` (numeric) - The current measured quantity for each category, updated in real-time
- `color` (categorical, optional) - Category or status indicator for bar coloring, may change based on thresholds
- Size: 3-15 categories recommended for readability during updates
- Example: Live poll results with 5 candidates, inventory levels for 8 product categories, service metrics for 6 endpoints

## Notes

- Implement smooth animated transitions when bar heights change
- Value labels on or above bars should update smoothly alongside bar animations
- Consider optional auto-sorting by value to maintain ranking order
- Color changes can indicate significant updates (e.g., threshold crossings, positive/negative changes)
- For static image output, show a snapshot with visual indicators suggesting dynamic nature (e.g., motion blur effect, multiple ghosted positions)
- Simulated streaming data should use realistic update frequencies (1-5 second intervals)
- Update frequency should balance responsiveness with visual stability
