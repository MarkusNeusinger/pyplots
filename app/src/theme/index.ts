/**
 * Theme constants for pyplots frontend.
 *
 * Centralized styling values to avoid hardcoded repetition.
 */

export const typography = {
  // MonoLisa with system mono fallback (size-adjusted to prevent CLS)
  fontFamily: '"MonoLisa", "MonoLisa Fallback", Consolas, Menlo, Monaco, "DejaVu Sans Mono", monospace',
} as const;

export const colors = {
  // Brand colors
  primary: '#3776AB', // Python blue
  accent: '#FFD43B', // Python yellow

  // Gray scale
  gray: {
    50: '#f9fafb',
    100: '#f3f4f6',
    200: '#e5e7eb',
    300: '#d1d5db',
    400: '#9ca3af',
    500: '#6b7280',
    600: '#4b5563',
    700: '#374151',
    800: '#1f2937',
    900: '#111827',
  },

  // Semantic colors
  success: '#22c55e',
  error: '#ef4444',
  warning: '#f59e0b',
  info: '#3b82f6',

  // Background
  background: '#fafafa',
} as const;

export const fontSize = {
  xs: '0.65rem',
  sm: '0.75rem',
  md: '0.8rem',
  base: '0.85rem',
  lg: '0.9rem',
  xl: '1rem',
} as const;

export const spacing = {
  xs: 0.5,
  sm: 1,
  md: 1.5,
  lg: 2,
  xl: 3,
} as const;

// Common style patterns
export const monoText = {
  fontFamily: typography.fontFamily,
} as const;

export const labelStyle = {
  fontFamily: typography.fontFamily,
  fontSize: fontSize.md,
  color: colors.gray[400],
} as const;
