# area-basic: Basic Area Chart

**Spec Version:** 1.0.0

## Description

A simple filled area chart showing a single data series over time or sequential x-values. The area between the data line and the baseline (typically zero) is filled with a semi-transparent color to emphasize the magnitude of values.

## Data Requirements

- **x**: Sequential or time-series values for the x-axis (numeric or datetime)
- **y**: Numeric values to plot on the y-axis

## Optional Parameters

- `fill_alpha`: Transparency of the filled area (type: float, default: 0.5)
- `line_color`: Color of the line and fill (type: str, default: library default)
- `title`: Chart title (type: str, default: None)
- `x_label`: Label for x-axis (type: str, default: column name)
- `y_label`: Label for y-axis (type: str, default: column name)

## Quality Criteria

- [ ] X and Y axes are labeled with meaningful names
- [ ] Grid is visible but subtle (alpha <= 0.5)
- [ ] Area fill is semi-transparent (alpha between 0.3 and 0.7)
- [ ] Line on top of fill area is visible
- [ ] No overlapping axis labels or tick marks
- [ ] Data accurately represented without distortion
- [ ] Figure has appropriate size (16:9 aspect ratio)

## Expected Output

A clean area chart with a filled region between the data line and the x-axis baseline. The fill should be semi-transparent to allow grid lines to show through slightly. The line defining the top of the area should be clearly visible. Axes should be properly labeled, and a subtle grid should aid in reading values.

## Tags

area, trend, time-series, basic, 2d

## Use Cases

- Visualizing website traffic over time
- Showing cumulative sales or revenue trends
- Displaying stock price history with emphasis on magnitude
- Monitoring system resource usage over time
- Tracking temperature or weather data trends
