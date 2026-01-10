import { Component, ReactNode } from 'react';
import { Box, Alert, Button, Typography } from '@mui/material';
import RefreshIcon from '@mui/icons-material/Refresh';
import HomeIcon from '@mui/icons-material/Home';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

/**
 * Error boundary component that catches rendering errors in child components.
 * Displays a user-friendly error message with recovery options.
 */
export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo): void {
    console.error('ErrorBoundary caught an error:', error, errorInfo);
  }

  handleReload = (): void => {
    window.location.reload();
  };

  handleGoHome = (): void => {
    window.location.href = '/';
  };

  handleRetry = (): void => {
    this.setState({ hasError: false, error: null });
  };

  render(): ReactNode {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

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
          <Alert
            severity="error"
            sx={{
              maxWidth: 500,
              width: '100%',
              mb: 3,
            }}
          >
            <Typography variant="h6" component="div" sx={{ fontWeight: 600, mb: 1 }}>
              Something went wrong
            </Typography>
            <Typography variant="body2" color="text.secondary">
              An unexpected error occurred. Please try reloading the page.
            </Typography>
            {import.meta.env.DEV && this.state.error && (
              <Typography
                variant="caption"
                component="pre"
                sx={{
                  mt: 2,
                  p: 1,
                  bgcolor: 'grey.100',
                  borderRadius: 1,
                  overflow: 'auto',
                  maxHeight: 100,
                  textAlign: 'left',
                  fontFamily: 'monospace',
                }}
              >
                {this.state.error.message}
              </Typography>
            )}
          </Alert>

          <Box sx={{ display: 'flex', gap: 2 }}>
            <Button
              variant="contained"
              startIcon={<RefreshIcon />}
              onClick={this.handleReload}
              sx={{ textTransform: 'none' }}
            >
              Reload Page
            </Button>
            <Button
              variant="outlined"
              startIcon={<HomeIcon />}
              onClick={this.handleGoHome}
              sx={{ textTransform: 'none' }}
            >
              Go Home
            </Button>
          </Box>
        </Box>
      );
    }

    return this.props.children;
  }
}
