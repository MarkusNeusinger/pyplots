import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Link from '@mui/material/Link';
import Tooltip from '@mui/material/Tooltip';

interface HeaderProps {
  stats?: { specs: number; plots: number; libraries: number } | null;
}

export function Header({ stats }: HeaderProps) {
  const tooltipText = stats
    ? `${stats.plots} plots across ${stats.libraries} libraries`
    : 'loading...';
  return (
    <Box sx={{ textAlign: 'center', mb: 4 }}>
      <Link
        href="https://pyplots.ai"
        target="_blank"
        rel="noopener noreferrer"
        underline="none"
      >
        <Typography
          variant="h2"
          component="h1"
          sx={{
            fontWeight: 700,
            fontFamily: '"JetBrains Mono", monospace',
            mb: 3,
            letterSpacing: '-0.02em',
          }}
        >
          <Box component="span" sx={{ color: '#3776AB' }}>py</Box>
          <Box component="span" sx={{ color: '#FFD43B' }}>plots</Box>
          <Box component="span" sx={{ color: '#1f2937' }}>.ai</Box>
        </Typography>
      </Link>
      <Typography
        variant="body1"
        sx={{
          maxWidth: 560,
          mx: 'auto',
          lineHeight: 1.8,
          fontFamily: '"JetBrains Mono", monospace',
          color: '#6b7280',
          fontSize: '1rem',
        }}
      >
        library-agnostic, ai-powered python plotting examples.
      </Typography>
      <Typography
        variant="body1"
        sx={{
          maxWidth: 560,
          mx: 'auto',
          mt: 1.5,
          lineHeight: 1.8,
          fontFamily: '"JetBrains Mono", monospace',
          color: '#374151',
          fontSize: '1.05rem',
          fontWeight: 500,
        }}
      >
        get inspired
        <Tooltip title={tooltipText} arrow placement="top">
          <Box
            component="sup"
            sx={{
              color: '#3776AB',
              cursor: 'help',
              fontSize: '0.65rem',
              ml: 0.25,
              '&:hover': { color: '#FFD43B' },
            }}
          >
            ✦
          </Box>
        </Tooltip>
        . grab the code. make it yours.
      </Typography>
    </Box>
  );
}
