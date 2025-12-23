import { memo, useState } from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Link from '@mui/material/Link';
import Tooltip from '@mui/material/Tooltip';
import ClickAwayListener from '@mui/material/ClickAwayListener';
import ShuffleIcon from '@mui/icons-material/Shuffle';

interface HeaderProps {
  stats?: { specs: number; plots: number; libraries: number } | null;
  onRandom?: () => void;
}

export const Header = memo(function Header({ stats, onRandom }: HeaderProps) {
  const [tooltipOpen, setTooltipOpen] = useState(false);
  const [pinned, setPinned] = useState(false);  // true = opened via click, stays open
  const tooltipText = stats
    ? `${stats.plots} plots across ${stats.libraries} libraries`
    : '';

  return (
    <Box sx={{ textAlign: 'center', mb: 4 }}>
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
        <Link
          href="https://pyplots.ai"
          target="_blank"
          rel="noopener noreferrer"
          underline="none"
        >
          <Box component="span" sx={{ color: '#3776AB' }}>py</Box>
          <Box component="span" sx={{ color: '#FFD43B' }}>plots</Box>
          <Box component="span" sx={{ color: '#1f2937' }}>.ai</Box>
        </Link>
        {onRandom && (
          <ShuffleIcon
            tabIndex={0}
            role="button"
            aria-hidden={false}
            aria-label="Random filter"
            onClick={(e) => {
              const el = e.currentTarget as unknown as HTMLElement;
              el.style.animation = 'none';
              void el.getBoundingClientRect();
              el.style.animation = 'shuffle-wiggle 0.8s ease';
              onRandom();
            }}
            onKeyDown={(e) => {
              if (e.key === ' ') {
                e.preventDefault();
                const el = e.currentTarget as unknown as HTMLElement;
                el.style.animation = 'none';
                void el.getBoundingClientRect();
                el.style.animation = 'shuffle-wiggle 0.8s ease';
                onRandom();
              }
            }}
            onTouchEnd={(e) => {
              const now = Date.now();
              const lastTap = (e.currentTarget as unknown as HTMLElement & { lastTap?: number }).lastTap || 0;
              if (now - lastTap < 300) {
                e.preventDefault();
                const el = e.currentTarget as unknown as HTMLElement;
                el.style.animation = 'none';
                void el.getBoundingClientRect();
                el.style.animation = 'shuffle-wiggle 0.8s ease';
                onRandom();
              }
              (e.currentTarget as unknown as HTMLElement & { lastTap?: number }).lastTap = now;
            }}
            sx={{
              color: '#9ca3af',
              cursor: 'pointer',
              fontSize: '0.5em',
              ml: 0.5,
              verticalAlign: 'super',
              '&:hover': { color: '#3776AB' },
              '&:focus': { outline: 'none', color: '#3776AB' },
              '@keyframes shuffle-wiggle': {
                '0%': { transform: 'rotate(0deg)' },
                '20%': { transform: 'rotate(-25deg)' },
                '40%': { transform: 'rotate(25deg)' },
                '60%': { transform: 'rotate(-15deg)' },
                '80%': { transform: 'rotate(15deg)' },
                '100%': { transform: 'rotate(0deg)' },
              },
            }}
          />
        )}
      </Typography>
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
        {stats ? (
          <ClickAwayListener onClickAway={() => { setTooltipOpen(false); setPinned(false); }}>
            <span>
              <Tooltip
                title={tooltipText}
                arrow
                placement="top"
                open={tooltipOpen}
                disableFocusListener
                disableTouchListener
              >
                <Box
                  component="sup"
                  onClick={() => {
                    if (pinned) {
                      setPinned(false);
                      setTooltipOpen(false);
                    } else {
                      setPinned(true);
                      setTooltipOpen(true);
                    }
                  }}
                  onMouseEnter={() => setTooltipOpen(true)}
                  onMouseLeave={() => { if (!pinned) setTooltipOpen(false); }}
                  sx={{
                    color: tooltipOpen ? '#FFD43B' : '#3776AB',
                    cursor: 'pointer',
                    fontSize: '0.65rem',
                    ml: 0.25,
                    '&:hover': { color: '#FFD43B' },
                  }}
                >
                  ✦
                </Box>
              </Tooltip>
            </span>
          </ClickAwayListener>
        ) : (
          <Box
            component="sup"
            sx={{
              color: '#3776AB',
              fontSize: '0.65rem',
              ml: 0.25,
            }}
          >
            ✦
          </Box>
        )}
        . grab the code. make it yours.
      </Typography>
    </Box>
  );
});
