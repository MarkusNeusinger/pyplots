# bode-basic: Bode Plot for Frequency Response

## Description

A Bode plot displays a system's frequency response as two vertically aligned panels: magnitude (in decibels) on top and phase (in degrees) on the bottom, both plotted against frequency on a shared logarithmic scale. This visualization is fundamental in control systems engineering and signal processing for analyzing how a system responds to sinusoidal inputs across a range of frequencies, revealing stability characteristics, bandwidth, and resonance behavior.

## Applications

- Analyzing stability margins (gain margin and phase margin) of feedback control systems to ensure robust performance
- Designing and characterizing analog and digital filters in signal processing and audio engineering
- Evaluating amplifier frequency response and bandwidth limitations in electronics design
- Tuning PID controllers in industrial automation by examining open-loop transfer function behavior

## Data

- `frequency_hz` (numeric) - frequency values in Hz, logarithmically spaced (e.g., 0.01 to 10000 Hz)
- `magnitude_db` (numeric) - gain magnitude in decibels at each frequency point
- `phase_deg` (numeric) - phase shift in degrees at each frequency point
- Size: 100-1000 points (log-spaced for uniform coverage on logarithmic axis)
- Example: Second-order transfer function frequency response showing resonance peak and phase rolloff

## Notes

- Dual-panel layout with magnitude plot on top and phase plot on bottom, sharing a common logarithmic frequency axis
- Mark gain margin (dB above 0 dB at phase crossover frequency) and phase margin (degrees above -180 at gain crossover frequency) with annotations
- Draw reference lines at 0 dB on the magnitude plot and -180 on the phase plot
- Use logarithmic scale (log10) for the frequency axis in both panels
- Phase axis typically ranges from 0 to -180 (or -360 for higher-order systems)
- Consider using grid lines to aid reading of margin values
