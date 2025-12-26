// Constants for pyplots.ai frontend

export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
export const GITHUB_URL = 'https://github.com/MarkusNeusinger/pyplots';
export const LIBRARIES = ['altair', 'bokeh', 'highcharts', 'letsplot', 'matplotlib', 'plotly', 'plotnine', 'pygal', 'seaborn'];
export const BATCH_SIZE = 15;

// Image size: 'normal' or 'compact' (half size)
export type ImageSize = 'normal' | 'compact';
