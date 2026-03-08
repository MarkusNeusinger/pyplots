import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { HelmetProvider } from 'react-helmet-async';
import { Layout, AppDataProvider } from './components/Layout';
import { ErrorBoundary } from './components/ErrorBoundary';
import { HomePage } from './pages/HomePage';
import { SpecPage } from './pages/SpecPage';
import { NotFoundPage } from './pages/NotFoundPage';

const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      { index: true, element: <HomePage /> },
      { path: 'catalog', lazy: () => import('./pages/CatalogPage').then(m => ({ Component: m.CatalogPage })) },
      { path: 'legal', lazy: () => import('./pages/LegalPage').then(m => ({ Component: m.LegalPage })) },
      { path: 'mcp', lazy: () => import('./pages/McpPage').then(m => ({ Component: m.McpPage })) },
      { path: ':specId', element: <SpecPage /> },
      { path: ':specId/:library', element: <SpecPage /> },
      { path: '*', element: <NotFoundPage /> },
    ],
  },
  // Fullscreen interactive view (outside Layout but inside AppDataProvider)
  { path: 'interactive/:specId/:library', lazy: () => import('./pages/InteractivePage').then(m => ({ Component: m.InteractivePage })) },
  // Hidden debug dashboard (outside Layout - no header/footer)
  { path: 'debug', lazy: () => import('./pages/DebugPage').then(m => ({ Component: m.DebugPage })) },
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
