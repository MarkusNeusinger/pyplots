import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { HelmetProvider } from 'react-helmet-async';
import { Layout } from './components/Layout';
import { HomePage } from './pages/HomePage';
import { SpecPage } from './pages/SpecPage';
import { CatalogPage } from './pages/CatalogPage';

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
]);

export function AppRouter() {
  return (
    <HelmetProvider>
      <RouterProvider router={router} />
    </HelmetProvider>
  );
}
