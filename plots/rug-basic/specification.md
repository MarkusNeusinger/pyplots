# rug-basic: Basic Rug Plot

## Description

A rug plot displays individual data points as small tick marks along an axis, typically at the bottom or side of another plot. Unlike histograms or density plots that bin data, rug plots show the exact location of every observation. They reveal clustering patterns, gaps in data, and the precise distribution of values with minimal visual footprint.

## Applications

- Showing the underlying data points alongside a kernel density estimate or histogram
- Revealing gaps and clusters in continuous data that binning would hide
- Displaying marginal distributions along the axes of scatter plots
- Identifying potential outliers at the edges of a distribution

## Data

- `values` (numeric) - Continuous variable to display as tick marks
- Size: 5-1000+ observations (works well at any sample size)
- Example: Measurement data, response times, or any continuous variable

## Notes

- Use semi-transparency (alpha) when observations overlap
- Tick height should be consistent and small relative to the plot
- Position along x-axis by default, but can be placed on y-axis
- Works best as a complement to histograms, density plots, or scatter plots
