# map-animated-temporal: Animated Map over Time

## Description

An animated geographic map visualization that displays point data changing over time, with interactive play controls and a time slider for navigation. Each frame shows the spatial distribution of data at a specific timestamp, with smooth transitions between frames revealing temporal patterns and movement. This visualization is ideal for storytelling with geospatial data, allowing viewers to observe how geographic phenomena evolve, spread, or shift across locations over time.

## Applications

- Visualizing disease spread patterns across regions, showing how an outbreak expands geographically over days or weeks
- Tracking historical boundary changes or migration patterns, revealing temporal shifts in population or territorial control
- Displaying temporal sequences of events like earthquake aftershocks, crime incidents, or social media activity hotspots
- Animating weather pattern movement such as storm tracks, temperature changes, or air quality measurements across a geographic area

## Data

- `lat` (numeric) - Latitude coordinate for each point (-90 to 90)
- `lon` (numeric) - Longitude coordinate for each point (-180 to 180)
- `timestamp` (datetime) - Time dimension that drives the animation frames
- `value` (numeric, optional) - Data value for color or size encoding at each point
- `label` (string, optional) - Point label or identifier for tooltips
- Size: 50-500 points across 10-50 time steps recommended for smooth, comprehensible animation
- Example: Daily COVID case locations over a month, hourly earthquake aftershock sequences, weekly crime incident reports

## Notes

- Include play/pause controls that are prominently visible and intuitive to use
- Provide a time slider for manual navigation to any point in the animation sequence
- Display the current timestamp clearly during animation (as title, subtitle, or overlay text)
- Use smooth transitions between frames to enhance the visual narrative
- Include a basemap with geographic context (country boundaries, coastlines, or terrain)
- Animation speed should be configurable or use a sensible default duration
- For libraries without animation support, implement a small multiples grid showing key time snapshots
- Consider adding optional point trails to show movement paths over recent frames
