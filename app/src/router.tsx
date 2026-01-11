import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { HelmetProvider } from 'react-helmet-async';
import { Layout, AppDataProvider } from './components/Layout';
import { ErrorBoundary } from './components/ErrorBoundary';
import { HomePage } from './pages/HomePage';
import { SpecPage } from './pages/SpecPage';
import { CatalogPage } from './pages/CatalogPage';
import { InteractivePage } from './pages/InteractivePage';
import { DebugPage } from './pages/DebugPage';

const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      { index: true, element: <HomePage /> },
      { path: 'catalog', element: <CatalogPage /> },
      { path: ':specId', element: <SpecPage /> },
      { path: ':specId/:library', element: <SpecPage /> },
    ],
  },
  // Fullscreen interactive view (outside Layout but inside AppDataProvider)
  { path: 'interactive/:specId/:library', element: <InteractivePage /> },
  // Hidden debug dashboard (outside Layout - no header/footer)
  { path: 'debug', element: <DebugPage /> },
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
