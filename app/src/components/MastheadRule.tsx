import Box from '@mui/material/Box';
import { typography, colors } from '../theme';
import { ThemeToggle } from './ThemeToggle';
import { useTheme, useLatestRelease } from '../hooks';

const REPO_URL = 'https://github.com/MarkusNeusinger/anyplot';

const mastheadLinkSx = {
  color: 'inherit',
  textDecoration: 'none',
  borderBottom: '1px dotted transparent',
  transition: 'color 0.2s, border-color 0.2s',
  '&:hover': { color: colors.primary, borderBottomColor: 'currentColor' },
} as const;

/**
 * Top masthead bar (style-guide §6.4).
 *
 * Lowercase, monospace, three slots separated by │. Reads as a status line
 * from a tool — positions the site as a curated publication that lives
 * inside a terminal.
 */
export function MastheadRule() {
  const { isDark, toggle } = useTheme();
  const releaseTag = useLatestRelease();
  const version = releaseTag ?? 'v1.0';

  return (
    <Box sx={{
      display: 'grid',
      gridTemplateColumns: '1fr auto 1fr',
      alignItems: 'center',
      py: 1.25,
      mb: 0,
      borderBottom: '1px solid var(--rule)',
      fontFamily: typography.mono,
      fontSize: '11px',
      color: 'var(--ink-muted)',
      letterSpacing: '0.04em',
    }}>
      <Box sx={{ display: { xs: 'none', sm: 'block' } }}>
        ~/anyplot.ai ·{' '}
        <Box
          component="a"
          href={`${REPO_URL}/tree/main`}
          target="_blank"
          rel="noopener noreferrer"
          sx={mastheadLinkSx}
        >
          main
        </Box>{' '}
        ·{' '}
        <Box
          component="a"
          href={releaseTag ? `${REPO_URL}/releases/tag/${releaseTag}` : `${REPO_URL}/releases`}
          target="_blank"
          rel="noopener noreferrer"
          sx={mastheadLinkSx}
        >
          {version}
        </Box>
      </Box>
      <Box sx={{
        px: 2,
        fontFeatureSettings: '"tnum"',
        textAlign: 'center',
        display: { xs: 'none', md: 'block' },
      }}>
        // the open plot catalogue.
      </Box>
      <Box sx={{
        textAlign: 'right',
        gridColumn: { xs: '1 / -1', sm: 'auto' },
        display: 'flex',
        justifyContent: { xs: 'center', sm: 'flex-end' },
      }}>
        <ThemeToggle isDark={isDark} onToggle={toggle} />
      </Box>
    </Box>
  );
}
