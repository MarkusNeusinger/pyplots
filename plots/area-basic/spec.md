# area-basic: Basic Area Chart

## Description

An area chart displaying a single data series as a filled region under a line. The filled area emphasizes magnitude and cumulative values over a sequence, making trends more visually impactful than simple line plots. Best suited for time series data where you want to highlight volume or accumulated quantities.

## Data

**Required columns:**
- `x` (numeric/datetime) - sequential values for the horizontal axis (typically time)
- `y` (numeric) - values for the vertical axis representing magnitude

**Example:**
```python
import pandas as pd
data = pd.DataFrame({
    'month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    'sales': [120, 135, 148, 162, 175, 195, 210, 198, 185, 170, 158, 190]
})
```

## Tags

area, trend, timeseries, basic, 2d

## Use Cases

- Visualizing website traffic volume over time
- Showing cumulative sales or revenue trends across quarters
- Tracking system resource usage (CPU, memory) over time
- Displaying temperature variations throughout a day
