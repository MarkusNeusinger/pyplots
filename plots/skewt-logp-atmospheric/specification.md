# skewt-logp-atmospheric: Skew-T Log-P Atmospheric Diagram

## Description

A Skew-T Log-P diagram is a specialized thermodynamic chart used in meteorology to display vertical atmospheric profiles. It features a logarithmic pressure axis (inverted, with surface at bottom) and temperature isotherms skewed 45 degrees to the right, allowing simultaneous visualization of temperature, dewpoint, and derived stability parameters. This diagram is essential for analyzing atmospheric soundings and assessing weather conditions.

## Applications

- Analyzing weather balloon (radiosonde) sounding data to understand atmospheric structure
- Assessing atmospheric stability and convective potential for severe weather forecasting
- Evaluating lifting condensation level, convective available potential energy (CAPE), and convective inhibition (CIN)
- Teaching meteorology students about thermodynamic processes in the atmosphere

## Data

- `pressure` (numeric) - Atmospheric pressure levels in hectopascals (hPa), typically ranging from 1000 hPa (surface) to 100 hPa (stratosphere)
- `temperature` (numeric) - Air temperature in degrees Celsius at each pressure level
- `dewpoint` (numeric) - Dewpoint temperature in degrees Celsius at each pressure level
- `wind_speed` (numeric, optional) - Wind speed in knots for wind barb display
- `wind_direction` (numeric, optional) - Wind direction in degrees (0-360) for wind barb display
- Size: 20-100 vertical levels (typical radiosonde resolution)
- Example: Standard atmospheric sounding with surface to upper troposphere coverage

## Notes

- Pressure axis must be logarithmic and inverted (1000 hPa at bottom, decreasing upward)
- Temperature isotherms should be drawn at 45-degree angle (skewed to the right)
- Include reference lines: dry adiabats (potential temperature), moist adiabats (equivalent potential temperature), and mixing ratio lines
- Temperature profile typically shown as solid line, dewpoint as dashed line
- Wind barbs along right edge are optional but enhance the diagram's utility
- Color coding can distinguish different reference line types for clarity
