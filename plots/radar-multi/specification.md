# radar-multi: Multi-Series Radar Chart

## Description

A multi-series radar chart overlays multiple data polygons on shared axes radiating from a center point, enabling direct comparison across several entities or categories. Each series is rendered as a distinct colored polygon, making it easy to identify relative strengths and weaknesses at a glance. This visualization excels at comparative analysis where multiple subjects are evaluated across the same set of metrics.

## Applications

- Product feature comparison showing how competing products score across attributes like price, quality, durability, and support
- Employee or team skill assessments comparing individuals across competencies such as communication, technical skills, leadership, and creativity
- Sports player or team performance comparison across metrics like speed, accuracy, endurance, and teamwork
- Business competitor analysis across key performance indicators such as market share, customer satisfaction, and innovation

## Data

- `category` (string) - axis labels representing different variables/dimensions being compared
- `value` (numeric) - values for each axis per series (0-100 scale recommended for clarity)
- `series` (string) - identifier for each data series (e.g., product name, person name, team)
- Size: 5-8 axes, 2-5 series for optimal comparison clarity

## Notes

- Use filled polygons with transparency (alpha ~0.2-0.3) to allow visibility of overlapping areas
- Assign distinct, contrasting colors to each series for easy differentiation
- Include a legend identifying each series by color
- Add gridlines at regular intervals (e.g., 20, 40, 60, 80, 100) for value reference
- Label each axis clearly at the outer edge
- Close each polygon by connecting the last point back to the first
- Consider using both fill and outline for each polygon to enhance visibility
