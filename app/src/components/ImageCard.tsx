import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import Tooltip from '@mui/material/Tooltip';
import Link from '@mui/material/Link';
import SubjectIcon from '@mui/icons-material/Subject';
import OpenInNewIcon from '@mui/icons-material/OpenInNew';
import type { PlotImage, LibraryInfo, SpecInfo } from '../types';

interface ImageCardProps {
  image: PlotImage;
  index: number;
  viewMode: 'spec' | 'library';
  selectedSpec: string;
  librariesData: LibraryInfo[];
  specsData: SpecInfo[];
  openTooltip: string | null;
  onTooltipToggle: (id: string | null) => void;
  onClick: () => void;
}

export function ImageCard({
  image,
  index,
  viewMode,
  selectedSpec,
  librariesData,
  specsData,
  openTooltip,
  onTooltipToggle,
  onClick,
}: ImageCardProps) {
  const label = viewMode === 'library' ? image.spec_id : image.library;
  const tooltipId = viewMode === 'spec' ? image.library : (image.spec_id || '');
  const isTooltipOpen = openTooltip === tooltipId;

  const libraryInfo = librariesData.find(l => l.id === image.library);
  const specInfo = specsData.find(s => s.id === image.spec_id);

  return (
    <Box
      sx={{
        animation: 'fadeIn 0.6s ease-out',
        animationDelay: `${index * 0.1}s`,
        animationFillMode: 'backwards',
        '@keyframes fadeIn': {
          from: { opacity: 0, transform: 'translateY(20px)' },
          to: { opacity: 1, transform: 'translateY(0)' },
        },
      }}
    >
      <Card
        elevation={0}
        onClick={onClick}
        onKeyDown={(e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            onClick();
          }
        }}
        tabIndex={0}
        role="button"
        aria-label={`View ${viewMode === 'library' ? image.spec_id : image.library} plot in fullscreen`}
        sx={{
          borderRadius: 3,
          overflow: 'hidden',
          border: '2px solid rgba(55, 118, 171, 0.2)',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
          transition: 'all 0.3s ease',
          cursor: 'pointer',
          '&:hover': {
            border: '2px solid rgba(55, 118, 171, 0.4)',
            boxShadow: '0 8px 30px rgba(0,0,0,0.15)',
            transform: 'scale(1.03)',
          },
        }}
      >
        <CardMedia
          component="img"
          image={image.thumb || image.url}
          alt={viewMode === 'library' ? `${image.spec_id} - ${image.library}` : `${selectedSpec} - ${image.library}`}
          sx={{
            width: '100%',
            aspectRatio: '16 / 10',
            objectFit: 'contain',
            bgcolor: '#fff',
          }}
          onError={(e) => {
            const target = e.target as HTMLImageElement;
            target.style.display = 'none';
          }}
        />
      </Card>
      {/* Label below card: library name in spec mode, spec_id in library mode + info button */}
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', mt: 1.5 }}>
        <Typography
          sx={{
            textAlign: 'center',
            fontSize: '0.8rem',
            fontWeight: 600,
            fontFamily: '"JetBrains Mono", monospace',
            color: '#9ca3af',
            textTransform: 'lowercase',
          }}
        >
          {label}
        </Typography>
        {/* Info button: shows library desc in spec mode, spec desc in library mode */}
        {viewMode === 'spec' ? (
          <Tooltip
            title={
              <Box>
                <Typography sx={{ fontSize: '0.8rem', mb: 1 }}>
                  {libraryInfo?.description || ''}
                </Typography>
                {libraryInfo?.documentation_url && (
                  <Link
                    href={libraryInfo.documentation_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    sx={{
                      display: 'inline-flex',
                      alignItems: 'center',
                      gap: 0.5,
                      fontSize: '0.75rem',
                      color: '#90caf9',
                      textDecoration: 'underline',
                      '&:hover': { color: '#fff' },
                    }}
                  >
                    {libraryInfo.documentation_url.replace(/^https?:\/\//, '')} <OpenInNewIcon sx={{ fontSize: 12 }} />
                  </Link>
                )}
              </Box>
            }
            arrow
            placement="bottom"
            open={isTooltipOpen}
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
              onClick={(e) => {
                e.stopPropagation();
                onTooltipToggle(isTooltipOpen ? null : tooltipId);
              }}
              sx={{
                ml: 0.25,
                p: 0.25,
                color: isTooltipOpen ? '#3776AB' : '#d1d5db',
                '&:hover': {
                  color: '#3776AB',
                  bgcolor: 'transparent',
                },
              }}
            >
              <SubjectIcon sx={{ fontSize: 14 }} />
            </IconButton>
          </Tooltip>
        ) : (
          <Tooltip
            title={specInfo?.description || ''}
            arrow
            placement="bottom"
            open={isTooltipOpen}
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
              onClick={(e) => {
                e.stopPropagation();
                onTooltipToggle(isTooltipOpen ? null : tooltipId);
              }}
              sx={{
                ml: 0.25,
                p: 0.25,
                color: isTooltipOpen ? '#3776AB' : '#d1d5db',
                '&:hover': {
                  color: '#3776AB',
                  bgcolor: 'transparent',
                },
              }}
            >
              <SubjectIcon sx={{ fontSize: 14 }} />
            </IconButton>
          </Tooltip>
        )}
      </Box>
    </Box>
  );
}
