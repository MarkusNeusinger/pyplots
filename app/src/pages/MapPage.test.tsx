import { describe, it, expect, vi, beforeEach } from 'vitest';

import { render, screen, waitFor } from '../test-utils';
import { MapPage } from './MapPage';


vi.mock('react-helmet-async', () => ({
  Helmet: ({ children }: { children: React.ReactNode }) => <>{children}</>,
}));

vi.mock('../hooks', () => ({
  useAnalytics: () => ({
    trackPageview: vi.fn(),
    trackEvent: vi.fn(),
  }),
}));

vi.mock('../hooks/useLayoutContext', () => ({
  useTheme: () => ({ isDark: false }),
}));

// Stub ForceGraph2D to a marker div so we can assert wiring without rendering canvas.
vi.mock('react-force-graph-2d', () => ({
  default: (props: { graphData: { nodes: { id: string }[]; links: unknown[] } }) => (
    <div
      data-testid="force-graph-2d"
      data-node-count={props.graphData.nodes.length}
      data-link-count={props.graphData.links.length}
    />
  ),
}));


const mockSpecs = [
  {
    id: 'scatter-basic',
    title: 'Basic Scatter Plot',
    preview_url_light: 'https://example.com/scatter-basic-light.png',
    preview_url_dark: 'https://example.com/scatter-basic-dark.png',
    quality_score: 90,
    tags: { plot_type: ['scatter'], data_type: ['numeric'], features: ['basic'] },
    impl_tags: { dependencies: ['scipy'] },
  },
  {
    id: 'scatter-color-mapped',
    title: 'Scatter with Color Mapping',
    preview_url_light: 'https://example.com/scatter-color-light.png',
    preview_url_dark: 'https://example.com/scatter-color-dark.png',
    quality_score: 88,
    tags: { plot_type: ['scatter'], data_type: ['numeric'], features: ['color-mapped'] },
    impl_tags: { dependencies: ['scipy'] },
  },
  {
    id: 'line-basic',
    title: 'Basic Line Chart',
    preview_url_light: 'https://example.com/line-basic-light.png',
    preview_url_dark: 'https://example.com/line-basic-dark.png',
    quality_score: 92,
    tags: { plot_type: ['line'], data_type: ['numeric'], features: ['basic'] },
    impl_tags: null,
  },
];


function mockFetchSuccess() {
  vi.stubGlobal(
    'fetch',
    vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockSpecs),
    }),
  );
}


// jsdom doesn't ship ResizeObserver; stub it so the page's useEffect doesn't crash.
class MockResizeObserver {
  observe(target: Element) {
    // Trigger a single layout callback so size > 0 and the canvas mounts.
    Object.defineProperty(target, 'contentRect', { value: { width: 800, height: 600 }, configurable: true });
  }
  unobserve() {}
  disconnect() {}
}


describe('MapPage', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
    vi.stubGlobal('ResizeObserver', MockResizeObserver);
  });

  it('renders the spec/edge count meta after fetch', async () => {
    mockFetchSuccess();
    render(<MapPage />);
    await waitFor(() => {
      expect(screen.getByText(/3 specs/)).toBeInTheDocument();
    });
  });

  it('renders an a11y fallback list of every spec as anchor links', async () => {
    mockFetchSuccess();
    render(<MapPage />);
    await waitFor(() => {
      expect(screen.getByRole('link', { name: 'Basic Scatter Plot' })).toBeInTheDocument();
      expect(screen.getByRole('link', { name: 'Basic Line Chart' })).toBeInTheDocument();
      expect(screen.getByRole('link', { name: 'Scatter with Color Mapping' })).toBeInTheDocument();
    });
  });

  it('shows an error message when the fetch fails', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: false, status: 500 }));
    render(<MapPage />);
    await waitFor(() => {
      expect(screen.getByText(/Failed to load map/)).toBeInTheDocument();
    });
  });
});
