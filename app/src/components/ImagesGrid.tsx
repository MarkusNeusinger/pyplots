import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import Alert from '@mui/material/Alert';
import { ImageCard } from './ImageCard';
import { LoaderSpinner } from './LoaderSpinner';
import type { PlotImage, LibraryInfo, SpecInfo } from '../types';
import type { ImageSize } from '../constants';

interface ImagesGridProps {
  images: PlotImage[];
  viewMode: 'spec' | 'library';
  selectedSpec: string;
  selectedLibrary: string;
  loading: boolean;
  hasMore: boolean;
  isLoadingMore: boolean;
  isTransitioning: boolean;
  librariesData: LibraryInfo[];
  specsData: SpecInfo[];
  openTooltip: string | null;
  loadMoreRef: React.RefObject<HTMLDivElement | null>;
  imageSize: ImageSize;
  onTooltipToggle: (id: string | null) => void;
  onCardClick: (image: PlotImage) => void;
  onTrackEvent?: (name: string, props?: Record<string, string | undefined>) => void;
  onImageLoad?: () => void;
}

export function ImagesGrid({
  images,
  viewMode,
  selectedSpec,
  selectedLibrary: _selectedLibrary,
  loading,
  hasMore,
  isLoadingMore,
  isTransitioning,
  librariesData,
  specsData,
  openTooltip,
  loadMoreRef,
  imageSize,
  onTooltipToggle,
  onCardClick,
  onTrackEvent,
  onImageLoad,
}: ImagesGridProps) {
  void _selectedLibrary; // Preserved for API compatibility

  // Grid columns: normal = max 3 cols, compact = max 6 cols
  const gridColumns = imageSize === 'compact'
    ? { xs: 6, sm: 6, md: 3, lg: 3, xl: 2 }  // 2→2→4→4→6 cols
    : { xs: 12, sm: 12, md: 6, lg: 6, xl: 4 }; // 1→1→2→2→3 cols

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
            sx={{
              opacity: isTransitioning ? 0 : 1,
              transition: 'opacity 0.15s ease-in-out',
            }}
          >
            {images.map((image, index) => (
              <Grid
                key={image.spec_id ? `${image.spec_id}-${image.library}` : image.library}
                size={gridColumns}
              >
                <ImageCard
                  image={image}
                  index={index}
                  viewMode={viewMode}
                  selectedSpec={selectedSpec}
                  librariesData={librariesData}
                  specsData={specsData}
                  openTooltip={openTooltip}
                  imageSize={imageSize}
                  onTooltipToggle={onTooltipToggle}
                  onClick={() => onCardClick(image)}
                  onTrackEvent={onTrackEvent}
                  onImageLoad={onImageLoad}
                />
              </Grid>
            ))}
          </Grid>
        )}
        {/* Load more trigger (invisible) */}
        {hasMore && (
          <Box ref={loadMoreRef} sx={{ height: 1 }} />
        )}
        {/* Fixed loading indicator at bottom - only when actively loading */}
        {isLoadingMore && hasMore && (
          <Box
            sx={{
              position: 'fixed',
              bottom: 24,
              left: '50%',
              transform: 'translateX(-50%)',
              zIndex: 50,
              bgcolor: 'rgba(255,255,255,0.9)',
              borderRadius: 3,
              px: 3,
              py: 1.5,
              boxShadow: '0 2px 12px rgba(0,0,0,0.15)',
              display: 'flex',
              alignItems: 'center',
              gap: 1.5,
            }}
          >
            <LoaderSpinner size="small" />
          </Box>
        )}
      </Box>
    );
  }

  return null;
}
