import { useRef } from 'react';
import Box from '@mui/material/Box';
import Chip from '@mui/material/Chip';
import IconButton from '@mui/material/IconButton';
import Tooltip from '@mui/material/Tooltip';
import Typography from '@mui/material/Typography';
import Link from '@mui/material/Link';
import SyncIcon from '@mui/icons-material/Sync';
import ShuffleIcon from '@mui/icons-material/Shuffle';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import SubjectIcon from '@mui/icons-material/Subject';
import OpenInNewIcon from '@mui/icons-material/OpenInNew';

interface NavigationBarProps {
  viewMode: 'spec' | 'library';
  selectedSpec: string;
  selectedLibrary: string;
  specDescription: string;
  libraryDescription: string;
  libraryDocsUrl: string;
  descriptionOpen: boolean;
  isRolling: boolean;
  isShuffling: boolean;
  onToggleViewMode: () => void;
  onMenuOpen: (element: HTMLElement) => void;
  onDescriptionToggle: () => void;
  shuffleSpec: () => void;
  goToPrevSpec: () => void;
  goToNextSpec: () => void;
  shuffleLibrary: () => void;
  goToPrevLibrary: () => void;
  goToNextLibrary: () => void;
  onTrackEvent?: (name: string, props?: Record<string, string | undefined>) => void;
}

export function NavigationBar({
  viewMode,
  selectedSpec,
  selectedLibrary,
  specDescription,
  libraryDescription,
  libraryDocsUrl,
  descriptionOpen,
  isRolling,
  isShuffling,
  onToggleViewMode,
  onMenuOpen,
  onDescriptionToggle,
  shuffleSpec,
  goToPrevSpec,
  goToNextSpec,
  shuffleLibrary,
  goToPrevLibrary,
  goToNextLibrary,
  onTrackEvent,
}: NavigationBarProps) {
  const shuffleButtonRef = useRef<HTMLButtonElement>(null);

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: 1.5,
        mb: 5,
      }}
    >
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        {/* Toggle view mode button */}
        <Tooltip title={viewMode === 'spec' ? 'Switch to Library view' : 'Switch to Spec view'} arrow placement="bottom">
          <IconButton
            size="small"
            onClick={onToggleViewMode}
            sx={{
              color: '#9ca3af',
              transition: 'transform 0.3s ease',
              transform: isRolling ? 'rotate(180deg)' : 'rotate(0deg)',
              '&:hover': {
                color: '#3776AB',
                bgcolor: 'transparent',
              },
            }}
          >
            <SyncIcon sx={{ fontSize: 20 }} />
          </IconButton>
        </Tooltip>
        <Box
          sx={{
            perspective: '200px',
            overflow: 'hidden',
          }}
        >
          <Chip
            data-spec-chip
            label={viewMode === 'spec' ? selectedSpec : selectedLibrary}
            variant="outlined"
            onClick={(e) => onMenuOpen(e.currentTarget)}
            onKeyDown={(e) => {
              // Prevent space from triggering click (space is for shuffle)
              if (e.code === 'Space') {
                e.preventDefault();
              }
            }}
            sx={{
              fontSize: '0.95rem',
              fontWeight: 600,
              fontFamily: '"JetBrains Mono", monospace',
              color: '#3776AB',
              borderColor: '#3776AB',
              bgcolor: '#f9fafb',
              py: 2,
              px: 0.5,
              cursor: 'pointer',
              transition: 'transform 0.3s ease, opacity 0.3s ease',
              transform: isRolling ? 'rotateX(90deg)' : 'rotateX(0deg)',
              opacity: isRolling ? 0 : 1,
              '&:hover': {
                bgcolor: '#e8f4fc',
              },
            }}
          />
        </Box>
        {viewMode === 'spec' && (
          <Tooltip
            title={specDescription}
            arrow
            placement="bottom"
            open={descriptionOpen}
            disableFocusListener
            disableHoverListener
            disableTouchListener
            slotProps={{
              tooltip: {
                sx: {
                  maxWidth: { xs: '80vw', sm: 400 },
                  fontFamily: '"JetBrains Mono", monospace',
                  fontSize: '0.8rem',
                },
              },
            }}
          >
            <IconButton
              data-description-btn
              size="small"
              onClick={() => {
                onDescriptionToggle();
                onTrackEvent?.('description_toggle', { mode: 'spec', open: String(!descriptionOpen) });
              }}
              aria-label="Show specification description"
              sx={{
                ml: 0.5,
                color: descriptionOpen ? '#3776AB' : '#9ca3af',
                '&:hover': {
                  color: '#3776AB',
                  bgcolor: 'transparent',
                },
              }}
            >
              <SubjectIcon sx={{ fontSize: 18 }} />
            </IconButton>
          </Tooltip>
        )}
        {viewMode === 'library' && (
          <Tooltip
            title={
              <Box>
                <Typography sx={{ fontSize: '0.8rem', mb: 1 }}>{libraryDescription}</Typography>
                {libraryDocsUrl && (
                  <Link
                    href={libraryDocsUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    sx={{
                      display: 'inline-flex',
                      alignItems: 'center',
                      gap: 0.5,
                      fontSize: '0.75rem',
                      color: '#90caf9',
                      textDecoration: 'underline',
                      '&:hover': {
                        color: '#fff',
                      },
                    }}
                  >
                    {libraryDocsUrl.replace(/^https?:\/\//, '')} <OpenInNewIcon sx={{ fontSize: 12 }} />
                  </Link>
                )}
              </Box>
            }
            arrow
            placement="bottom"
            open={descriptionOpen}
            disableFocusListener
            disableHoverListener
            disableTouchListener
            slotProps={{
              tooltip: {
                sx: {
                  maxWidth: { xs: '80vw', sm: 400 },
                  fontFamily: '"JetBrains Mono", monospace',
                  fontSize: '0.8rem',
                },
              },
            }}
          >
            <IconButton
              data-description-btn
              size="small"
              onClick={() => {
                onDescriptionToggle();
                onTrackEvent?.('description_toggle', { mode: 'library', open: String(!descriptionOpen) });
              }}
              aria-label="Show library description"
              sx={{
                ml: 0.5,
                color: descriptionOpen ? '#3776AB' : '#9ca3af',
                '&:hover': {
                  color: '#3776AB',
                  bgcolor: 'transparent',
                },
              }}
            >
              <SubjectIcon sx={{ fontSize: 18 }} />
            </IconButton>
          </Tooltip>
        )}
      </Box>

      {/* Navigation buttons */}
      {viewMode === 'spec' && (
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
          <Tooltip title="Previous (← / Swipe right)" arrow placement="bottom">
            <IconButton
              onClick={() => {
                goToPrevSpec();
                onTrackEvent?.('navigate_prev', { mode: 'spec' });
              }}
              size="small"
              aria-label="Previous spec"
              sx={{
                color: '#9ca3af',
                '&:hover': {
                  color: '#3776AB',
                  bgcolor: '#e8f4fc',
                },
              }}
            >
              <ChevronLeftIcon />
            </IconButton>
          </Tooltip>
          <Tooltip title="Random (Space / Double-tap)" arrow placement="bottom">
            <IconButton
              ref={shuffleButtonRef}
              onClick={() => {
                shuffleSpec();
                onTrackEvent?.('navigate_shuffle', { mode: 'spec' });
              }}
              size="small"
              aria-label="Shuffle to a different random spec"
              sx={{
                color: '#3776AB',
                transition: 'transform 0.5s ease',
                transform: isShuffling ? 'rotate(180deg)' : 'rotate(0deg)',
                '&:hover': {
                  color: '#2c5d8a',
                  bgcolor: '#e8f4fc',
                },
              }}
            >
              <ShuffleIcon />
            </IconButton>
          </Tooltip>
          <Tooltip title="Next (→ / Swipe left)" arrow placement="bottom">
            <IconButton
              onClick={() => {
                goToNextSpec();
                onTrackEvent?.('navigate_next', { mode: 'spec' });
              }}
              size="small"
              aria-label="Next spec"
              sx={{
                color: '#9ca3af',
                '&:hover': {
                  color: '#3776AB',
                  bgcolor: '#e8f4fc',
                },
              }}
            >
              <ChevronRightIcon />
            </IconButton>
          </Tooltip>
        </Box>
      )}
      {viewMode === 'library' && (
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
          <Tooltip title="Previous (← / Swipe right)" arrow placement="bottom">
            <IconButton
              onClick={() => {
                goToPrevLibrary();
                onTrackEvent?.('navigate_prev', { mode: 'library' });
              }}
              size="small"
              aria-label="Previous library"
              sx={{
                color: '#9ca3af',
                '&:hover': {
                  color: '#3776AB',
                  bgcolor: '#e8f4fc',
                },
              }}
            >
              <ChevronLeftIcon />
            </IconButton>
          </Tooltip>
          <Tooltip title="Random (Space / Double-tap)" arrow placement="bottom">
            <IconButton
              ref={shuffleButtonRef}
              onClick={() => {
                shuffleLibrary();
                onTrackEvent?.('navigate_shuffle', { mode: 'library' });
              }}
              size="small"
              aria-label="Shuffle to a different random library"
              sx={{
                color: '#3776AB',
                transition: 'transform 0.5s ease',
                transform: isShuffling ? 'rotate(180deg)' : 'rotate(0deg)',
                '&:hover': {
                  color: '#2c5d8a',
                  bgcolor: '#e8f4fc',
                },
              }}
            >
              <ShuffleIcon />
            </IconButton>
          </Tooltip>
          <Tooltip title="Next (→ / Swipe left)" arrow placement="bottom">
            <IconButton
              onClick={() => {
                goToNextLibrary();
                onTrackEvent?.('navigate_next', { mode: 'library' });
              }}
              size="small"
              aria-label="Next library"
              sx={{
                color: '#9ca3af',
                '&:hover': {
                  color: '#3776AB',
                  bgcolor: '#e8f4fc',
                },
              }}
            >
              <ChevronRightIcon />
            </IconButton>
          </Tooltip>
        </Box>
      )}
    </Box>
  );
}
