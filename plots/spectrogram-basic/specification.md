# spectrogram-basic: Spectrogram Time-Frequency Heatmap

## Description

A spectrogram displaying time-frequency representation of a signal as a heatmap. It shows how the frequency content of a signal changes over time, with color intensity representing the amplitude or power at each time-frequency point. Essential for analyzing non-stationary signals where frequency characteristics vary, revealing patterns invisible in time-domain or frequency-domain views alone.

## Applications

- Audio analysis including speech recognition and music processing
- Vibration monitoring for machinery health and fault detection
- Seismic data analysis for earthquake and geological studies
- Biomedical signal processing such as EEG and ECG analysis

## Data

- `signal` (numeric array) - time-domain signal values
- `sample_rate` (numeric) - sampling frequency in Hz
- Size: 1000-50000 samples for clear visualization
- Example: chirp signal with increasing frequency, audio waveform, or vibration data

## Notes

- Use a perceptually uniform colormap (viridis, inferno) for accurate magnitude representation
- Include colorbar with power/amplitude units (dB scale often preferred)
- Label axes clearly: time (seconds) on x-axis, frequency (Hz) on y-axis
- Consider log scale for frequency axis when spanning multiple octaves
- Window size and overlap affect time-frequency resolution trade-off
