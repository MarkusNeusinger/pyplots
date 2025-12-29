# timeline-basic: Event Timeline

## Description

A timeline visualization that displays events and milestones along a temporal axis. Events are represented as points or markers with accompanying labels, making it easy to understand the sequence and timing of events. This plot type excels at showing chronological progressions and is particularly effective for communicating project phases, historical events, or any time-ordered sequence of occurrences.

## Applications

- Tracking project milestones and deliverables in software development or construction projects
- Visualizing historical events for educational presentations or museum displays
- Presenting product roadmaps to stakeholders showing feature releases over time
- Displaying company history or biographical timelines for annual reports

## Data

- `date` (datetime) - The date or timestamp when the event occurred
- `event` (string) - The name or short description of the event
- `category` (string, optional) - A grouping category for color-coding related events
- Size: 5-50 events for readability
- Example: Project milestone data with dates, milestone names, and phase categories

## Notes

- Horizontal orientation is most common for reading left-to-right
- Alternate label positions above and below the axis to prevent text overlap
- Use clear date formatting appropriate to the time scale (days, months, years)
- Consider color-coding by category when multiple event types exist
- For dense timelines, ensure adequate spacing or implement zooming capabilities
