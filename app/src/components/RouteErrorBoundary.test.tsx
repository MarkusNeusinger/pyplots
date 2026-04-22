import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { createMemoryRouter, RouterProvider } from 'react-router-dom';
import { RouteErrorBoundary } from './RouteErrorBoundary';

vi.mock('react-helmet-async', () => ({
  Helmet: ({ children }: { children: React.ReactNode }) => <>{children}</>,
}));

const theme = createTheme();

function renderWithRouter(thrown: unknown) {
  const router = createMemoryRouter(
    [
      {
        path: '/',
        errorElement: <RouteErrorBoundary />,
        loader: () => {
          throw thrown;
        },
        element: <div>never rendered</div>,
      },
    ],
    { initialEntries: ['/'] }
  );
  return render(
    <ThemeProvider theme={theme}>
      <RouterProvider router={router} />
    </ThemeProvider>
  );
}

describe('RouteErrorBoundary', () => {
  const originalLocation = window.location;

  beforeEach(() => {
    sessionStorage.clear();
    // Replace window.location so we can spy on reload without jsdom errors.
    Object.defineProperty(window, 'location', {
      configurable: true,
      value: { ...originalLocation, reload: vi.fn() },
    });
    vi.spyOn(console, 'error').mockImplementation(() => {});
    vi.spyOn(console, 'warn').mockImplementation(() => {});
  });

  afterEach(() => {
    Object.defineProperty(window, 'location', {
      configurable: true,
      value: originalLocation,
    });
    vi.restoreAllMocks();
  });

  it('renders generic error UI for unknown errors', async () => {
    renderWithRouter(new Error('boom'));
    expect(await screen.findByText('Something went wrong')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /reload page/i })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /go home/i })).toBeInTheDocument();
  });

  it('renders 404 page for route 404 responses', async () => {
    const router = createMemoryRouter(
      [
        {
          path: '/',
          errorElement: <RouteErrorBoundary />,
          loader: () => {
            throw new Response('Not Found', { status: 404 });
          },
          element: <div>never</div>,
        },
      ],
      { initialEntries: ['/'] }
    );
    render(
      <ThemeProvider theme={theme}>
        <RouterProvider router={router} />
      </ThemeProvider>
    );
    expect(await screen.findByText('404')).toBeInTheDocument();
    expect(screen.getByText('page not found')).toBeInTheDocument();
  });

  it('auto-reloads once on chunk load errors', async () => {
    renderWithRouter(new Error('Failed to fetch dynamically imported module: https://example.com/x.js'));
    await waitFor(() => expect(window.location.reload).toHaveBeenCalledTimes(1));
    expect(sessionStorage.getItem('anyplot:chunk-reload-attempt')).not.toBeNull();
  });

  it('does not reload loop — shows recovery UI after a prior attempt', async () => {
    sessionStorage.setItem('anyplot:chunk-reload-attempt', String(Date.now()));
    renderWithRouter(new Error('Failed to fetch dynamically imported module: https://example.com/x.js'));
    expect(await screen.findByText('A new version is available')).toBeInTheDocument();
    expect(window.location.reload).not.toHaveBeenCalled();
  });

  it('treats ChunkLoadError messages as chunk errors', async () => {
    renderWithRouter(new Error('ChunkLoadError: Loading chunk 42 failed'));
    await waitFor(() => expect(window.location.reload).toHaveBeenCalledTimes(1));
  });
});
