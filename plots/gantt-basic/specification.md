# gantt-basic: Basic Gantt Chart

## Description

A Gantt chart is a horizontal bar chart that visualizes project schedules and timelines. Each task is represented as a horizontal bar spanning from its start date to end date, making it easy to see task durations, overlaps, and the overall project timeline at a glance. Gantt charts are essential for project management, helping teams understand task sequences and identify scheduling conflicts.

## Applications

- Project management and planning to track task progress and deadlines
- Resource allocation visualization showing when different resources are committed
- Manufacturing and production scheduling to coordinate sequential operations
- Event planning timelines to coordinate multiple parallel activities

## Data

- `task` (str) - Name or description of the task
- `start` (datetime) - Start date/time of the task
- `end` (datetime) - End date/time of the task
- `category` (str, optional) - Category or group for color coding tasks
- Size: 5-30 tasks for optimal readability
- Example: Project milestone data with phases like "Design", "Development", "Testing"

## Notes

- Horizontal bars should be clearly visible on a time axis (x-axis)
- Use clear date formatting on the x-axis (consider date range when choosing format)
- Consider color coding by category or status for better visual grouping
- Tasks should be ordered logically (by start date or category)
- Add a vertical line to indicate the current date when applicable
- Ensure adequate spacing between task bars for readability
