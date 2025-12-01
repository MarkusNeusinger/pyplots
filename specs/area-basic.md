# area-basic: Basic Area Chart

**Spec Version:** 1.0.0

## Description

A basic area chart that displays quantitative data over a continuous interval or time period. The area between the line and the axis is filled with color, emphasizing the magnitude of values. Ideal for showing trends and cumulative totals over time.

## Data Requirements

- **x**: Column for x-axis values (typically time or sequential data - numeric or datetime)
- **y**: Numeric column for y-axis values (the values to be plotted)

## Optional Parameters

- `title`: Plot title (default: None)
- `xlabel`: X-axis label (default: uses column name)
- `ylabel`: Y-axis label (default: uses column name)
- `color`: Fill color for the area (default: library-specific default)
- `alpha`: Transparency level for the fill (default: 0.5)
- `line_color`: Color of the line at the top of the area (default: same as color but darker)
- `line_width`: Width of the line (default: 2)
- `fill_to`: What to fill to - 'zero' or 'none' (default: 'zero')

## Quality Criteria

- [ ] X and Y axes are labeled with column names or custom labels
- [ ] Area fill is visible but not overwhelming (appropriate alpha)
- [ ] Line at top of area is clearly visible
- [ ] Grid is visible but subtle (alpha <= 0.3)
- [ ] No overlapping labels or tick marks
- [ ] Data accurately represented without distortion
- [ ] Appropriate figure size (16:9 aspect ratio)

## Expected Output

A filled area chart with:
- A colored area extending from the data line down to the x-axis (or zero line)
- A visible line tracing the top of the area
- Clear axis labels and optional title
- Subtle grid for readability
- Professional appearance suitable for presentations and reports

## Tags

area, line, trend, timeseries, basic, 2d

## Use Cases

- Visualizing stock price movements over time
- Displaying website traffic trends
- Showing cumulative sales or revenue over periods
- Tracking temperature changes throughout the day
- Monitoring resource usage (CPU, memory) over time
- Displaying population growth trends
