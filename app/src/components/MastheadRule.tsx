import { Link as RouterLink, useLocation } from 'react-router-dom';
import Box from '@mui/material/Box';
import { typography, colors } from '../theme';
import { ThemeToggle } from './ThemeToggle';
import { useTheme, useLatestRelease } from '../hooks';
import { RESERVED_TOP_LEVEL } from '../utils/paths';

const REPO_URL = 'https://github.com/MarkusNeusinger/anyplot';

const linkSx = {
  color: 'inherit',
  textDecoration: 'none',
  borderBottom: '1px dotted transparent',
  transition: 'color 0.2s, border-color 0.2s',
  '&:hover': { color: colors.primary, borderBottomColor: 'currentColor' },
} as const;

const staticSx = {
  color: 'inherit',
} as const;

interface Segment {
  label: string;
  to?: string;
}

/**
 * Build path segments from the current pathname. Returned segments are rendered
 * after the `~/anyplot.ai` root marker. Each segment may carry an internal
 * route — the last segment never does (it's the current page).
 *
 * Routes covered:
 *   /<page>                                 → [<page>]
 *   /:specId                                → [specId]
 *   /:specId/:language                      → [specId(→/specId), language]
 *   /:specId/:language/:library             → [specId(→/specId), language(→/specId/language), library]
 */
function pathSegments(pathname: string): Segment[] {
  const parts = pathname.split('/').filter(Boolean);
  if (parts.length === 0) return [];

  // Reserved top-level routes (single segment)
  if (RESERVED_TOP_LEVEL.has(parts[0])) {
    return [{ label: parts[0] }];
  }

  // Spec routes: /:specId[/:language[/:library]]
  const [specId, language, library] = parts;
  const segs: Segment[] = [];
  if (language) {
    segs.push({ label: specId, to: `/${specId}` });
  } else {
    segs.push({ label: specId });
  }
  if (language) {
    if (library) {
      segs.push({ label: language, to: `/${specId}/${language}` });
      segs.push({ label: library });
    } else {
      segs.push({ label: language });
    }
  }
  return segs;
}

/**
 * Top masthead bar (style-guide §6.4) — also serves as the global breadcrumb.
 *
 * On `/`, the linkable left slot shows `~/anyplot.ai · main · v1.1.0` and the
 * center carries the catchphrase. On every other route, the left slot becomes
 * the breadcrumb path (`~/anyplot.ai · python · scatter-basic · matplotlib`)
 * and the catchphrase is suppressed so the line stays uncluttered.
 */
export function MastheadRule() {
  const { isDark, toggle } = useTheme();
  const releaseTag = useLatestRelease();
  const location = useLocation();
  const segments = pathSegments(location.pathname);
  const isLanding = segments.length === 0;
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
      <Box sx={{
        display: { xs: isLanding ? 'none' : 'block', sm: 'block' },
        whiteSpace: 'nowrap',
        overflow: 'hidden',
        textOverflow: 'ellipsis',
      }}>
        {/* Always-visible root marker */}
        <Box component={RouterLink} to="/" sx={linkSx}>
          ~/anyplot.ai
        </Box>

        {isLanding ? (
          <>
            {' · '}
            <Box component="a" href={`${REPO_URL}/tree/main`} target="_blank" rel="noopener noreferrer" sx={linkSx}>
              main
            </Box>
            {' · '}
            <Box
              component="a"
              href={releaseTag ? `${REPO_URL}/releases/tag/${releaseTag}` : `${REPO_URL}/releases`}
              target="_blank"
              rel="noopener noreferrer"
              sx={linkSx}
            >
              {version}
            </Box>
          </>
        ) : (
          segments.map((seg, i) => (
            <Box key={`${seg.label}-${i}`} component="span">
              {' · '}
              {seg.to ? (
                <Box component={RouterLink} to={seg.to} sx={linkSx}>
                  {seg.label}
                </Box>
              ) : (
                <Box component="span" sx={{ ...staticSx, color: 'var(--ink-soft)' }}>
                  {seg.label}
                </Box>
              )}
            </Box>
          ))
        )}
      </Box>

      <Box sx={{
        px: 2,
        fontFeatureSettings: '"tnum"',
        textAlign: 'center',
        display: { xs: 'none', md: isLanding ? 'block' : 'none' },
      }}>
        // the open plot catalogue.
      </Box>

      <Box sx={{
        textAlign: 'right',
        // Explicit column pin so display:none on the center cell (non-landing)
        // doesn't cause the toggle to auto-place into track 2.
        gridColumn: { xs: '1 / -1', sm: '3' },
        display: 'flex',
        justifyContent: { xs: 'center', sm: 'flex-end' },
      }}>
        <ThemeToggle isDark={isDark} onToggle={toggle} />
      </Box>
    </Box>
  );
}
