// Constants for pyplots.ai frontend

export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
export const GITHUB_URL = 'https://github.com/MarkusNeusinger/pyplots';
export const LIBRARIES = ['altair', 'bokeh', 'highcharts', 'letsplot', 'matplotlib', 'plotly', 'plotnine', 'pygal', 'seaborn'];
export const BATCH_SIZE = 15;

// Image size options for grid layout
// containerMax = maxCols * maxWidth + (maxCols - 1) * gap
export const IMAGE_SIZES = {
  L: { minWidth: 380, maxWidth: 520, maxCols: 5, containerMax: 2696 },  // 5*520+4*24
  M: { minWidth: 280, maxWidth: 400, maxCols: 7, containerMax: 2944 },  // 7*400+6*24
  S: { minWidth: 220, maxWidth: 320, maxCols: 9, containerMax: 3072 },  // 9*320+8*24
} as const;
export type ImageSize = keyof typeof IMAGE_SIZES;
