import { useState, useCallback } from 'react';
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import Tooltip from '@mui/material/Tooltip';
import Link from '@mui/material/Link';
import OpenInNewIcon from '@mui/icons-material/OpenInNew';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import CheckIcon from '@mui/icons-material/Check';
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
  onTrackEvent?: (name: string, props?: Record<string, string | undefined>) => void;
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
  onTrackEvent,
}: ImageCardProps) {
  const [copied, setCopied] = useState(false);

  const cardId = `${image.spec_id}-${image.library}`;
  const specTooltipId = `spec-${cardId}`;
  const libTooltipId = `lib-${cardId}`;
  const isSpecTooltipOpen = openTooltip === specTooltipId;
  const isLibTooltipOpen = openTooltip === libTooltipId;

  const libraryInfo = librariesData.find(l => l.id === image.library);
  const specInfo = specsData.find(s => s.id === image.spec_id);

  const handleCopyCode = useCallback((e: React.MouseEvent) => {
    e.stopPropagation();
    if (image.code) {
      navigator.clipboard.writeText(image.code);
      setCopied(true);
      onTrackEvent?.('copy_code', { spec: image.spec_id || selectedSpec, library: image.library, method: 'card' });
      setTimeout(() => setCopied(false), 2000);
    }
  }, [image.code, image.library, image.spec_id, selectedSpec, onTrackEvent]);

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
          position: 'relative',
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
          '&:hover .copy-button': {
            opacity: 1,
          },
        }}
      >
        {/* Copy Code Button */}
        {image.code && (
          <Tooltip
            title={copied ? "Code copied!" : "Copy code"}
            placement="left"
            arrow
          >
            <Box
              className="copy-button"
              onClick={handleCopyCode}
              aria-label="Copy code to clipboard"
              sx={{
                position: 'absolute',
                top: 12,
                right: 12,
                zIndex: 2,
                opacity: copied ? 1 : 0,
                transition: 'all 0.2s ease',
                color: copied ? '#22c55e' : '#6b7280',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                filter: 'drop-shadow(0 1px 2px rgba(0,0,0,0.3))',
                '&:hover': {
                  color: copied ? '#22c55e' : '#374151',
                  transform: 'scale(1.1)',
                },
              }}
            >
              {copied ? <CheckIcon sx={{ fontSize: 22 }} /> : <ContentCopyIcon sx={{ fontSize: 20 }} />}
            </Box>
          </Tooltip>
        )}
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
      {/* Label below card: clickable spec-id · library */}
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', mt: 1.5, gap: 0.5 }}>
        {/* Clickable Spec ID */}
        <Tooltip
          title={specInfo?.description || 'No description available'}
          arrow
          placement="bottom"
          open={isSpecTooltipOpen}
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
          <Typography
            data-description-btn
            onClick={(e) => {
              e.stopPropagation();
              onTooltipToggle(isSpecTooltipOpen ? null : specTooltipId);
              if (!isSpecTooltipOpen) {
                onTrackEvent?.('description_spec', { spec: image.spec_id });
              }
            }}
            sx={{
              fontSize: '0.8rem',
              fontWeight: 600,
              fontFamily: '"JetBrains Mono", monospace',
              color: isSpecTooltipOpen ? '#3776AB' : '#9ca3af',
              textTransform: 'lowercase',
              cursor: 'pointer',
              '&:hover': {
                color: '#3776AB',
              },
            }}
          >
            {image.spec_id}
          </Typography>
        </Tooltip>

        <Typography sx={{ color: '#d1d5db', fontSize: '0.8rem' }}>·</Typography>

        {/* Clickable Library */}
        <Tooltip
          title={
            <Box>
              <Typography sx={{ fontSize: '0.8rem', mb: 1 }}>
                {libraryInfo?.description || 'No description available'}
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
          open={isLibTooltipOpen}
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
          <Typography
            data-description-btn
            onClick={(e) => {
              e.stopPropagation();
              onTooltipToggle(isLibTooltipOpen ? null : libTooltipId);
              if (!isLibTooltipOpen) {
                onTrackEvent?.('description_lib', { library: image.library });
              }
            }}
            sx={{
              fontSize: '0.8rem',
              fontWeight: 600,
              fontFamily: '"JetBrains Mono", monospace',
              color: isLibTooltipOpen ? '#3776AB' : '#9ca3af',
              textTransform: 'lowercase',
              cursor: 'pointer',
              '&:hover': {
                color: '#3776AB',
              },
            }}
          >
            {image.library}
          </Typography>
        </Tooltip>
      </Box>
    </Box>
  );
}
