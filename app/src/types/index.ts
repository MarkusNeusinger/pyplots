// Types for pyplots.ai frontend

export interface PlotImage {
  library: string;
  url: string;
  thumb?: string;
  html?: string;
  code?: string;
  spec_id?: string;
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
    plausible?: (event: string, options?: { u?: string; props?: Record<string, string> }) => void;
  }
}
