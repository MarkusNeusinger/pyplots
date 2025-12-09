# line-basic: Basic Line Plot

## Description

A fundamental line plot visualizing trends and changes over a continuous or sequential axis. Data points are connected by lines, making it ideal for time series data and showing progression or trends. The continuous line helps viewers perceive patterns and changes over the ordered sequence.

## Data

**Required columns:**
- `x` (numeric/datetime) - values for the horizontal axis (typically time or sequence)
- `y` (numeric) - values for the vertical axis

**Example:**
```python
import pandas as pd
data = pd.DataFrame({
    'time': [1, 2, 3, 4, 5, 6, 7],
    'value': [10, 15, 13, 18, 22, 19, 25]
})
```

## Tags

line, trend, timeseries, basic, 2d

## Use Cases

- Time series visualization of stock prices over months
- Tracking website traffic over time
- Displaying temperature changes throughout a day
- Monitoring system performance metrics over time
