import Box from '@mui/material/Box';
import Alert from '@mui/material/Alert';
import { ImageCard } from './ImageCard';
import { LoaderSpinner } from './LoaderSpinner';
import type { PlotImage, LibraryInfo, SpecInfo } from '../types';
import { IMAGE_SIZES, type ImageSize } from '../constants';

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
  imageSize: ImageSize;
  onTooltipToggle: (id: string | null) => void;
  onCardClick: (image: PlotImage) => void;
  onTrackEvent?: (name: string, props?: Record<string, string | undefined>) => void;
}

export function ImagesGrid({
  images,
  viewMode,
  selectedSpec,
  selectedLibrary: _selectedLibrary,
  loading,
  hasMore,
  isTransitioning,
  librariesData,
  specsData,
  openTooltip,
  loadMoreRef,
  imageSize,
  onTooltipToggle,
  onCardClick,
  onTrackEvent,
}: ImagesGridProps) {
  void _selectedLibrary; // Preserved for API compatibility
  const { minWidth, maxWidth, containerMax } = IMAGE_SIZES[imageSize];
  // Always show content - the old condition was breaking the "show all" default view
  // viewMode is now just for display purposes (spec name vs library name on cards)

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
          <Box
            sx={{
              display: 'grid',
              gridTemplateColumns: `repeat(auto-fit, minmax(${minWidth}px, ${maxWidth}px))`,
              justifyContent: 'center',
              gap: 3,
              mx: 'auto',
              opacity: isTransitioning ? 0 : 1,
              transition: 'opacity 0.15s ease-in-out',
            }}
          >
            {images.map((image, index) => (
              <Box
                key={image.spec_id ? `${image.spec_id}-${image.library}` : image.library}
                sx={{ width: '100%', maxWidth, mx: 'auto' }}
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
              </Box>
            ))}
          </Box>
        )}
        {/* Load more indicator */}
        {hasMore && (
          <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
            <div ref={loadMoreRef}>
              <LoaderSpinner size="small" />
            </div>
          </Box>
        )}
      </Box>
    );
  }

  return null;
}
