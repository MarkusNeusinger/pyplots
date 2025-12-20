import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import Alert from '@mui/material/Alert';
import { ImageCard } from './ImageCard';
import { LoaderSpinner } from './LoaderSpinner';
import type { PlotImage, LibraryInfo, SpecInfo } from '../types';

interface ImagesGridProps {
  images: PlotImage[];
  viewMode: 'spec' | 'library';
  selectedSpec: string;
  selectedLibrary: string;
  loading: boolean;
  hasMore: boolean;
  isTransitioning: boolean;
  librariesData: LibraryInfo[];
  specsData: SpecInfo[];
  openTooltip: string | null;
  loadMoreRef: React.RefObject<HTMLDivElement | null>;
  onTooltipToggle: (id: string | null) => void;
  onCardClick: (image: PlotImage) => void;
  onTrackEvent?: (name: string, props?: Record<string, string | undefined>) => void;
}

export function ImagesGrid({
  images,
  viewMode,
  selectedSpec,
  selectedLibrary,
  loading,
  hasMore,
  isTransitioning,
  librariesData,
  specsData,
  openTooltip,
  loadMoreRef,
  onTooltipToggle,
  onCardClick,
  onTrackEvent,
}: ImagesGridProps) {
  const showContent = (viewMode === 'spec' && selectedSpec) || (viewMode === 'library' && selectedLibrary);

  if (!showContent) return null;

  // Show loading spinner on initial load
  if (loading && !isTransitioning && images.length === 0) {
    return (
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          my: 8,
          opacity: 0,
          animation: 'fadeInDelayed 1.5s ease-out 0.3s forwards',
          '@keyframes fadeInDelayed': {
            '0%': { opacity: 0 },
            '100%': { opacity: 1 },
          },
        }}
      >
        <LoaderSpinner size="large" />
      </Box>
    );
  }

  // Show content
  if (images.length > 0 || !loading) {
    return (
      <Box>
        {images.length === 0 ? (
          <Alert
            severity="info"
            sx={{
              maxWidth: 400,
              mx: 'auto',
              bgcolor: '#f9fafb',
              border: '1px solid #e5e7eb',
              '& .MuiAlert-icon': { color: '#9ca3af' },
            }}
          >
            No images found for this spec.
          </Alert>
        ) : (
          <Grid
            container
            spacing={3}
            justifyContent="center"
            sx={{
              maxWidth: 1800,
              mx: 'auto',
              minHeight: '60vh',
              opacity: isTransitioning ? 0 : 1,
              transition: 'opacity 0.15s ease-in-out',
            }}
          >
            {images.map((image, index) => (
              <Grid
                size={{ xs: 12, sm: 6, lg: 4 }}
                key={image.spec_id ? `${image.spec_id}-${image.library}` : image.library}
                sx={{ maxWidth: 600 }}
              >
                <ImageCard
                  image={image}
                  index={index}
                  viewMode={viewMode}
                  selectedSpec={selectedSpec}
                  librariesData={librariesData}
                  specsData={specsData}
                  openTooltip={openTooltip}
                  onTooltipToggle={onTooltipToggle}
                  onClick={() => onCardClick(image)}
                  onTrackEvent={onTrackEvent}
                />
              </Grid>
            ))}
            {/* Load more indicator */}
            {hasMore && (
              <Grid size={{ xs: 12 }} sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
                <div ref={loadMoreRef}>
                  <LoaderSpinner size="small" />
                </div>
              </Grid>
            )}
          </Grid>
        )}
      </Box>
    );
  }

  return null;
}
