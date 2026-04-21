import { Link as RouterLink, useLocation, useNavigate } from 'react-router-dom';
import Box from '@mui/material/Box';
import { colors, typography } from '../theme';

const NAV_LINKS: { label: string; to: string; short?: string }[] = [
  { label: 'specs', to: '/specs' },
  { label: 'plots', to: '/plots' },
  { label: 'libraries', to: '/libraries', short: 'libs' },
  { label: 'stats', to: '/stats' },
  { label: 'palette', to: '/palette', short: 'pal' },
  { label: 'mcp', to: '/mcp' },
];

const linkSx = {
  color: 'var(--ink-soft)',
  textDecoration: 'none',
  position: 'relative' as const,
  padding: '4px 0',
  transition: 'color 0.2s',
  '&::after': {
    content: '""',
    position: 'absolute' as const,
    bottom: 0,
    left: 0,
    right: 0,
    height: '1px',
    background: colors.primary,
    transform: 'scaleX(0)',
    transformOrigin: 'left',
    transition: 'transform 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
  },
  '&:hover': {
    color: 'var(--ink)',
    '&::after': { transform: 'scaleX(1)' },
  },
} as const;

const activeLinkSx = {
  ...linkSx,
  color: 'var(--ink)',
  '&::before': {
    content: '"•"',
    color: colors.primary,
    position: 'absolute' as const,
    left: -12,
    fontSize: '18px',
    lineHeight: 1,
    top: '3px',
  },
} as const;

export function NavBar() {
  const navigate = useNavigate();
  const location = useLocation();

  const handleSearch = () => {
    navigate('/plots?focus=search');
  };

  return (
    <Box component="nav" sx={{
      display: 'grid',
      // On xs: two rows (logo+search top, nav-links spanning wide below).
      // On sm+: single row: logo | nav-links | search.
      gridTemplateColumns: { xs: '1fr auto', sm: 'auto 1fr auto' },
      gridTemplateAreas: {
        xs: `"logo search" "nav nav"`,
        sm: `"logo nav search"`,
      },
      alignItems: 'center',
      rowGap: { xs: 1.25, sm: 0 },
      columnGap: { xs: 1.5, sm: 4 },
      py: { xs: 1.25, sm: 2 },
      borderBottom: '1px solid var(--rule)',
    }}>
      {/* Logo */}
      <Box
        component={RouterLink}
        to="/"
        sx={{
          gridArea: 'logo',
          fontFamily: typography.mono,
          fontWeight: 700,
          fontSize: { xs: '18px', sm: '22px' },
          letterSpacing: '-0.02em',
          textDecoration: 'none',
          color: 'var(--ink)',
        }}
      >
        any<Box component="span" sx={{ color: colors.primary, display: 'inline-block', transform: 'scale(1.45)', mx: '2px' }}>.</Box>plot<Box component="span" sx={{ fontWeight: 400, opacity: 0.45 }}>()</Box>
      </Box>

      {/* Nav links — full row on xs (shorthand labels), inline on sm+ */}
      <Box component="ul" sx={{
        gridArea: 'nav',
        display: 'flex',
        gap: { xs: 2, sm: 2.25, md: 3.5 },
        listStyle: 'none',
        m: 0,
        p: 0,
        fontFamily: typography.mono,
        fontSize: { xs: '12px', sm: '12px', md: '13px' },
        justifyContent: { xs: 'space-between', sm: 'flex-start' },
        flexWrap: 'nowrap',
      }}>
        {NAV_LINKS.map(link => (
          <li key={link.to}>
            <Box
              component={RouterLink}
              to={link.to}
              sx={location.pathname === link.to ? activeLinkSx : linkSx}
            >
              {/* Full label on ≥md, short label on smaller screens where it saves room */}
              <Box component="span" sx={{ display: { xs: 'none', md: 'inline' } }}>
                {link.label}
              </Box>
              <Box component="span" sx={{ display: { xs: 'inline', md: 'none' } }}>
                {link.short || link.label}
              </Box>
            </Box>
          </li>
        ))}
      </Box>

      {/* Search — method-call link, opens the filter-bar search on /plots */}
      <Box
        component="button"
        onClick={handleSearch}
        aria-label="Search plots"
        sx={{
          gridArea: 'search',
          all: 'unset',
          fontFamily: typography.mono,
          fontSize: { xs: '11px', sm: '12px', md: '13px' },
          color: 'var(--ink-soft)',
          cursor: 'pointer',
          transition: 'color 0.2s',
          textAlign: 'right',
          '& .subj': { opacity: 0.55, transition: 'opacity 0.2s' },
          '&:hover': { color: colors.primary },
          '&:hover .subj': { opacity: 0.8 },
        }}
      >
        <span className="subj">plots</span>.search()
      </Box>
    </Box>
  );
}
