# spectrum-basic: Frequency Spectrum Plot

## Description

A frequency spectrum plot displays signal amplitude or power across a range of frequencies, showing the frequency domain representation of time-series data. This visualization reveals the frequency components present in a signal, making it essential for identifying dominant frequencies, harmonics, and noise characteristics. It is fundamental in signal processing, audio engineering, and vibration analysis.

## Applications

- Analyzing audio signals to identify frequency content such as musical notes, speech formants, or noise interference
- Detecting machinery vibration patterns and identifying potential mechanical faults based on characteristic frequencies
- Examining electrical signals to find interference frequencies or verify filter performance

## Data

- `frequency` (numeric) - frequency values in Hz, typically from FFT computation
- `amplitude` (numeric) - signal amplitude or magnitude at each frequency, often in dB or linear scale
- Size: 256-4096 frequency bins (typical FFT sizes)
- Example: FFT output of a synthetic signal with multiple frequency components

## Notes

- Use logarithmic scale for frequency axis when spanning wide frequency ranges
- Power spectral density (dB scale) is common for comparing signals with different amplitudes
- Include clear axis labels with units (Hz for frequency, dB or linear for amplitude)
- Consider highlighting peak frequencies or annotating dominant components
