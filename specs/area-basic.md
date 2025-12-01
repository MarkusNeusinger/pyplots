# area-basic: Basic Area Chart

**Spec Version:** 1.0.0

## Description

A basic area chart displays a single data series as a filled area under a line, connecting data points in sequence. This visualization is ideal for showing trends over time while emphasizing the magnitude of values through the filled region beneath the line.

## Data Requirements

- **x**: Sequential values for the x-axis (numeric or categorical representing order/time)
- **y**: Numeric values for the y-axis representing the magnitude at each point

## Optional Parameters

- `title`: Chart title (type: str, default: None)
- `xlabel`: X-axis label (type: str, default: column name)
- `ylabel`: Y-axis label (type: str, default: column name)
- `fill_alpha`: Transparency of the filled area (type: float, default: 0.5)
- `color`: Color for the line and fill (type: str, default: library default)
- `show_line`: Whether to show the line on top of fill (type: bool, default: True)

## Quality Criteria

- [ ] X and Y axes are labeled with meaningful descriptions
- [ ] The filled area is clearly visible with appropriate transparency (alpha ~0.5)
- [ ] The line connecting data points is visible on top of the fill
- [ ] Grid is present but subtle (alpha ≤ 0.5)
- [ ] No overlapping axis labels or tick marks
- [ ] Fill extends from the line to the baseline (y=0 or bottom axis)
- [ ] Data points are accurately represented without distortion

## Expected Output

A single area chart showing one data series with a filled region beneath the line. The line should be clearly visible on top of the semi-transparent fill. The fill should extend from the data line down to the x-axis baseline. The chart should include proper axis labels, a subtle grid for readability, and optionally a title. The overall appearance should be clean and professional, suitable for showing trends or cumulative data over a sequence.

## Tags

area, trend, timeseries, basic, 2d, composition

## Use Cases

- Visualizing website traffic over time with emphasis on volume
- Showing cumulative sales or revenue trends over months/quarters
- Displaying temperature variations throughout a day
- Tracking stock price movements with visual volume emphasis
- Monitoring system resource usage (CPU, memory) over time
- Illustrating population growth or decline over years
