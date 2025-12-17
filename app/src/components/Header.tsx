import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Link from '@mui/material/Link';

export function Header() {
  return (
    <Box sx={{ textAlign: 'center', mb: 6 }}>
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
        library-agnostic, ai-powered python plotting examples. automatically generated, tested, and maintained.
      </Typography>
    </Box>
  );
}
