import Box from '@mui/material/Box';
import Link from '@mui/material/Link';
import { GITHUB_URL } from '../constants';

interface FooterProps {
  onTrackEvent?: (name: string, props?: Record<string, string | undefined>) => void;
  selectedSpec?: string;
  selectedLibrary?: string;
}

export function Footer({ onTrackEvent, selectedSpec, selectedLibrary }: FooterProps) {
  return (
    <Box sx={{ textAlign: 'center', mt: 4, pt: 4, borderTop: '1px solid #f3f4f6' }}>
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          gap: 1,
          fontSize: '0.8rem',
          fontFamily: '"MonoLisa", "MonoLisa Fallback", monospace',
          color: '#9ca3af',
        }}
      >
        <Link
          href="https://www.linkedin.com/in/markus-neusinger/"
          target="_blank"
          rel="noopener noreferrer"
          onClick={() => onTrackEvent?.('external_link', { destination: 'linkedin', spec: selectedSpec, library: selectedLibrary })}
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
          onClick={() => onTrackEvent?.('external_link', { destination: 'github', spec: selectedSpec, library: selectedLibrary })}
          sx={{
            color: '#9ca3af',
            textDecoration: 'none',
            '&:hover': { color: '#6b7280' },
          }}
        >
          github
        </Link>
        <span>·</span>
        <Link
          href="https://plausible.io/pyplots.ai"
          target="_blank"
          rel="noopener noreferrer"
          onClick={() => onTrackEvent?.('external_link', { destination: 'stats', spec: selectedSpec, library: selectedLibrary })}
          sx={{
            color: '#9ca3af',
            textDecoration: 'none',
            '&:hover': { color: '#6b7280' },
          }}
        >
          stats
        </Link>
      </Box>
    </Box>
  );
}
