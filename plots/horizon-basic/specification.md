# horizon-basic: Horizon Chart

## Description

A horizon chart displays many time series compactly by folding values into color-coded bands, preserving local resolution while minimizing vertical space. It divides the y-axis into bands and uses color intensity to encode magnitude, allowing dozens of series to be compared in limited space. This technique is particularly effective when monitoring many metrics simultaneously where traditional line charts would become unreadable.

## Applications

- Dashboard monitoring displaying 50+ system metrics (CPU, memory, network) in a compact panel
- Stock market sector analysis comparing performance of multiple securities over time
- Environmental monitoring showing temperature, humidity, and other readings from multiple sensors

## Data

- `date` (datetime) - Time points for the x-axis, typically evenly spaced
- `value` (numeric) - The measured value at each time point
- `series` (categorical) - Identifier for each time series when displaying multiple
- Size: 100-1000 time points per series, 5-50 series for effective comparison
- Example: Server metrics over 24 hours, stock prices over trading days

## Notes

- Typically uses 2-4 bands with mirrored positive/negative coloring (e.g., blue for positive, red for negative)
- Color intensity increases with magnitude within each band
- Baseline should be meaningful (often zero or mean value)
- Works best with normalized or similarly-scaled data across series
