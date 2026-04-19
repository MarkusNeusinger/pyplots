import { Outlet } from 'react-router-dom';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';

import { useAnalytics } from '../hooks';
import { MastheadRule } from './MastheadRule';
import { NavBar } from './NavBar';
import { Footer } from './Footer';

const containerSx = {
  px: { xs: 2, sm: 4, md: 8, lg: 12 },
  maxWidth: 'var(--max-catalog)',
  mx: 'auto',
} as const;

/**
 * Global layout shell — sticky masthead + navbar above, footer below, page
 * content via <Outlet />. The header sticks to the top so the breadcrumb path
 * (in the masthead) stays visible while scrolling. The outer flex column with
 * min-height keeps the footer pinned below short pages while flowing
 * naturally below long ones, so footer spacing is consistent across routes.
 */
export function RootLayout() {
  const { trackEvent } = useAnalytics();

  return (
    <Box sx={{
      display: 'flex',
      flexDirection: 'column',
      minHeight: '100svh',
      bgcolor: 'var(--bg-page)',
    }}>
      {/* Masthead sticks — carries the breadcrumb path that should stay visible while scrolling. */}
      <Box
        sx={{
          position: 'sticky',
          top: 0,
          zIndex: 100,
          bgcolor: 'var(--bg-page)',
          backdropFilter: 'saturate(180%) blur(8px)',
          boxShadow: '0 1px 0 rgba(0,0,0,0.02)',
        }}
      >
        <Container maxWidth={false} sx={containerSx}>
          <MastheadRule />
        </Container>
      </Box>

      {/* NavBar flows with the page — scrolls out of view with the hero. */}
      <Container component="header" maxWidth={false} sx={containerSx}>
        <NavBar />
      </Container>

      <Box component="main" sx={{ flex: 1 }}>
        <Container maxWidth={false} sx={containerSx}>
          <Outlet />
        </Container>
      </Box>

      <Container maxWidth={false} sx={{ ...containerSx, pb: { xs: 4, md: 6 } }}>
        <Footer onTrackEvent={trackEvent} />
      </Container>
    </Box>
  );
}
