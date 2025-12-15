# stem-basic: Basic Stem Plot

## Description

A stem plot displays data points as markers connected to a baseline by vertical lines (stems). Each data point is represented by a marker at the data value with a thin line extending down to a baseline, making it ideal for visualizing discrete or sequential data where individual values matter. This plot type is particularly useful in signal processing and scientific applications where the discrete nature of measurements needs emphasis.

## Applications

- Visualizing impulse responses and discrete-time signals in signal processing
- Displaying discrete probability distributions where individual probabilities need highlighting
- Showing time series with discrete events or measurements
- Scientific data visualization emphasizing individual measurement points

## Data

- `x` (numeric) - Position along horizontal axis (sequence index or time)
- `y` (numeric) - Value determining stem height from baseline
- Size: 10-100 data points for optimal clarity
- Example: Discrete signal samples, probability mass function values

## Notes

- Stems should be thin vertical lines from baseline (typically y=0) to data points
- Markers should be clearly visible circles at the top of each stem
- Baseline position at y=0 unless data requires different baseline
- Consistent marker size and stem width throughout the plot
