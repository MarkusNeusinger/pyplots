import { createBrowserRouter, RouterProvider, Navigate, useParams } from 'react-router-dom';
import { HelmetProvider } from 'react-helmet-async';
import Box from '@mui/material/Box';
import CircularProgress from '@mui/material/CircularProgress';
import { Layout, AppDataProvider } from './components/Layout';
import { ErrorBoundary } from './components/ErrorBoundary';
import { HomePage } from './pages/HomePage';
import { NotFoundPage } from './pages/NotFoundPage';
import { specPath, interactivePath } from './utils/paths';

const LazyFallback = () => (
  <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '50vh' }}>
    <CircularProgress size={32} />
  </Box>
);

// Catches old URLs without /python/ prefix and redirects to /python/ equivalents.
// Uses splat (*) to avoid route ranking conflicts with the python route group.
function LegacyCatchAll() {
  const params = useParams();
  const splatPath = params['*'] || '';
  const parts = splatPath.split('/').filter(Boolean);

  if (parts.length === 1) {
    return <Navigate to={specPath(parts[0])} replace />;
  }
  if (parts.length === 2) {
    return <Navigate to={specPath(parts[0], parts[1])} replace />;
  }
  return <NotFoundPage />;
}

function LegacyInteractiveRedirect() {
  const { specId, library } = useParams();
  return <Navigate to={interactivePath(specId!, library!)} replace />;
}

const lazySpec = () => import('./pages/SpecPage').then(m => ({ Component: m.SpecPage, HydrateFallback: LazyFallback }));

const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    HydrateFallback: LazyFallback,
    children: [
      { index: true, element: <HomePage /> },
      { path: 'catalog', lazy: () => import('./pages/CatalogPage').then(m => ({ Component: m.CatalogPage, HydrateFallback: LazyFallback })) },
      { path: 'legal', lazy: () => import('./pages/LegalPage').then(m => ({ Component: m.LegalPage, HydrateFallback: LazyFallback })) },
      { path: 'mcp', lazy: () => import('./pages/McpPage').then(m => ({ Component: m.McpPage, HydrateFallback: LazyFallback })) },
      { path: 'stats', lazy: () => import('./pages/StatsPage').then(m => ({ Component: m.StatsPage, HydrateFallback: LazyFallback })) },
      // Python language routes
      { path: 'python', children: [
        { index: true, element: <HomePage /> },
        { path: ':specId', lazy: lazySpec },
        { path: ':specId/:library', lazy: lazySpec },
      ]},
      // Legacy catch-all: redirects old /:specId and /:specId/:library to /python/ equivalents.
      // Uses * (lowest priority) so the python route group always wins.
      { path: '*', element: <LegacyCatchAll /> },
    ],
  },
  // Fullscreen interactive view (outside Layout)
  { path: 'python/interactive/:specId/:library', lazy: () => import('./pages/InteractivePage').then(m => ({ Component: m.InteractivePage, HydrateFallback: LazyFallback })) },
  // Legacy interactive redirect
  { path: 'interactive/:specId/:library', element: <LegacyInteractiveRedirect /> },
  // Hidden debug dashboard (outside Layout - no header/footer)
  { path: 'debug', lazy: () => import('./pages/DebugPage').then(m => ({ Component: m.DebugPage, HydrateFallback: LazyFallback })) },
  { path: '*', element: <NotFoundPage /> },
]);

export function AppRouter() {
  return (
    <HelmetProvider>
      <ErrorBoundary>
        <AppDataProvider>
          <RouterProvider router={router} />
        </AppDataProvider>
      </ErrorBoundary>
    </HelmetProvider>
  );
}
