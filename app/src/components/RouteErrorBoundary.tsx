import { useEffect, useState } from 'react';
import { Link as RouterLink, isRouteErrorResponse, useRouteError } from 'react-router-dom';
import { Alert, Box, Button, CircularProgress, Typography } from '@mui/material';
import RefreshIcon from '@mui/icons-material/Refresh';
import HomeIcon from '@mui/icons-material/Home';
import { NotFoundPage } from '../pages/NotFoundPage';

const RELOAD_ATTEMPT_KEY = 'anyplot:chunk-reload-attempt';

function isChunkLoadError(error: unknown): boolean {
  if (!error) return false;
  const message =
    error instanceof Error
      ? error.message
      : typeof error === 'string'
        ? error
        : typeof (error as { message?: unknown }).message === 'string'
          ? (error as { message: string }).message
          : '';
  return (
    /Failed to fetch dynamically imported module/i.test(message) ||
    /Importing a module script failed/i.test(message) ||
    /error loading dynamically imported module/i.test(message) ||
    /ChunkLoadError/i.test(message)
  );
}

function errorMessage(error: unknown): string {
  if (error instanceof Error) return error.message;
  if (typeof error === 'string') return error;
  try {
    return JSON.stringify(error);
  } catch {
    return 'Unknown error';
  }
}

/**
 * Route-level error boundary for the React Router data router. Catches errors
 * thrown from route loaders, actions, lazy imports, and child components.
 *
 * Chunk load failures after a deploy are transient — the user's HTML references
 * old hashed bundles that no longer exist. We reload once automatically to pick
 * up the fresh bundle, and guard against reload loops with sessionStorage.
 */
export function RouteErrorBoundary() {
  const error = useRouteError();
  const chunkError = isChunkLoadError(error);

  // Decide once at mount whether to auto-reload. Using a lazy initializer
  // avoids setState-in-effect and guarantees the reload decision and the
  // sessionStorage write happen together.
  const [isReloading] = useState(() => {
    if (!chunkError) return false;
    try {
      if (sessionStorage.getItem(RELOAD_ATTEMPT_KEY)) return false;
      sessionStorage.setItem(RELOAD_ATTEMPT_KEY, String(Date.now()));
    } catch {
      // sessionStorage can throw in private mode; skip the loop guard.
    }
    return true;
  });

  useEffect(() => {
    if (isReloading) window.location.reload();
  }, [isReloading]);

  if (isRouteErrorResponse(error) && error.status === 404) {
    return <NotFoundPage />;
  }

  if (chunkError && isReloading) {
    return (
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: '50vh',
          gap: 2,
        }}
      >
        <CircularProgress size={32} />
        <Typography variant="body2" color="text.secondary">
          Loading the latest version…
        </Typography>
      </Box>
    );
  }

  const title = chunkError ? 'A new version is available' : 'Something went wrong';
  const body = chunkError
    ? 'The page could not be loaded because the app has been updated. Reload to get the latest version.'
    : 'An unexpected error occurred while loading this page.';

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '50vh',
        padding: 4,
        textAlign: 'center',
      }}
    >
      <Alert severity={chunkError ? 'info' : 'error'} sx={{ maxWidth: 500, width: '100%', mb: 3 }}>
        <Typography variant="h6" component="div" sx={{ fontWeight: 600, mb: 1 }}>
          {title}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          {body}
        </Typography>
        {import.meta.env.DEV && (
          <Typography
            variant="caption"
            component="pre"
            sx={{
              mt: 2,
              p: 1,
              bgcolor: 'grey.100',
              borderRadius: 1,
              overflow: 'auto',
              maxHeight: 120,
              textAlign: 'left',
              fontFamily: 'monospace',
            }}
          >
            {errorMessage(error)}
          </Typography>
        )}
      </Alert>

      <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', justifyContent: 'center' }}>
        <Button
          variant="contained"
          startIcon={<RefreshIcon />}
          onClick={() => window.location.reload()}
          sx={{ textTransform: 'none' }}
        >
          Reload Page
        </Button>
        <Button
          component={RouterLink}
          to="/"
          variant="outlined"
          startIcon={<HomeIcon />}
          sx={{ textTransform: 'none' }}
        >
          Go Home
        </Button>
      </Box>
    </Box>
  );
}
