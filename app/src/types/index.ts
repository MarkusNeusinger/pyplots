// Types for pyplots.ai frontend

export interface PlotImage {
  library: string;
  url: string;
  thumb?: string;
  html?: string;
  code?: string;
  spec_id?: string;
}

// Filter system types
export type FilterCategory = 'lib' | 'spec' | 'plot' | 'data' | 'dom' | 'feat';

// Display labels for filter categories
export const FILTER_LABELS: Record<FilterCategory, string> = {
  lib: 'library',
  spec: 'spec',
  plot: 'plot type',
  data: 'data type',
  dom: 'domain',
  feat: 'features',
};

// All filter categories in display order
export const FILTER_CATEGORIES: FilterCategory[] = ['lib', 'spec', 'plot', 'data', 'dom', 'feat'];

// A single filter group (one chip) - values within are OR-linked
export interface FilterGroup {
  category: FilterCategory;
  values: string[];
}

// Active filters: array of filter groups - groups are AND-linked
export type ActiveFilters = FilterGroup[];

// Counts per filter value
export type FilterCounts = Record<FilterCategory, Record<string, number>>;

// API response for filtered plots
export interface FilteredPlotsResponse {
  total: number;
  images: PlotImage[];
  counts: FilterCounts;  // Contextual counts (for AND additions)
  globalCounts: FilterCounts;  // Global counts (for reference)
  orCounts: Record<string, number>[];  // Per-group counts for OR additions
}

export interface LibraryInfo {
  id: string;
  name: string;
  version?: string;
  documentation_url?: string;
  description?: string;
}

export interface SpecInfo {
  id: string;
  title: string;
  description?: string;
}

// Plausible analytics (only in production)
declare global {
  interface Window {
    plausible?: (event: string, options?: { url?: string; props?: Record<string, string> }) => void;
  }
}
