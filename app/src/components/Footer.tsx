import Box from '@mui/material/Box';
import Link from '@mui/material/Link';
import { GITHUB_URL } from '../constants';

interface FooterProps {
  onTrackEvent?: (name: string, props?: Record<string, string | undefined>) => void;
}

export function Footer({ onTrackEvent }: FooterProps) {
  return (
    <Box sx={{ textAlign: 'center', mt: 8, pt: 5, borderTop: '1px solid #f3f4f6' }}>
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          gap: 1,
          fontSize: '0.8rem',
          fontFamily: '"JetBrains Mono", monospace',
          color: '#9ca3af',
        }}
      >
        <Link
          href="https://www.linkedin.com/in/markus-neusinger/"
          target="_blank"
          rel="noopener noreferrer"
          onClick={() => onTrackEvent?.('external_link', { destination: 'linkedin' })}
          sx={{
            color: '#9ca3af',
            textDecoration: 'none',
            '&:hover': { color: '#6b7280' },
          }}
        >
          markus neusinger
        </Link>
        <span>·</span>
        <Link
          href={GITHUB_URL}
          target="_blank"
          rel="noopener noreferrer"
          onClick={() => onTrackEvent?.('external_link', { destination: 'github' })}
          sx={{
            color: '#9ca3af',
            textDecoration: 'none',
            '&:hover': { color: '#6b7280' },
          }}
        >
          github
        </Link>
      </Box>
    </Box>
  );
}
