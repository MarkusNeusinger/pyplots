# smith-chart-basic: Smith Chart for RF/Impedance

## Description

A Smith chart is a specialized circular diagram used in RF engineering to display complex impedance and reflection coefficients on a normalized polar grid. The chart features constant resistance circles (centered along the horizontal axis) and constant reactance arcs (curving from the right edge), enabling engineers to visualize impedance matching, transmission line behavior, and antenna characteristics. It reveals relationships between impedance, admittance, and reflection coefficient that would be difficult to interpret in Cartesian coordinates.

## Applications

- Designing impedance matching networks for RF circuits and antennas
- Analyzing transmission line impedance transformations along electrical length
- Visualizing complex S-parameters and reflection coefficients in microwave circuits
- Optimizing antenna feed point matching to minimize VSWR

## Data

- `frequency` (numeric) - Frequency points in Hz for impedance measurements
- `z_real` (numeric) - Real part of complex impedance (resistance in ohms)
- `z_imag` (numeric) - Imaginary part of complex impedance (reactance in ohms)
- `z0` (numeric, optional) - Reference impedance for normalization (default: 50 ohms)
- Size: 10-200 frequency points recommended for smooth impedance locus curves
- Example: S11 measurements from a vector network analyzer across 1-6 GHz

## Notes

- Draw standard Smith chart grid with constant resistance circles and constant reactance arcs
- Normalize impedance values to reference impedance (Z/Z0) before plotting
- Plot impedance locus as a connected curve showing frequency sweep trajectory
- Add frequency labels at key points along the impedance curve
- Optional: Include VSWR circles (constant reflection coefficient magnitude)
- Chart boundary represents |gamma| = 1 (total reflection)
- Center of chart is matched condition (Z = Z0, gamma = 0)
