import { useState, useEffect, useCallback, useRef } from 'react';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Alert from '@mui/material/Alert';
import Fab from '@mui/material/Fab';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';

import type { PlotImage, LibraryInfo, SpecInfo } from './types';
import { API_URL, type ImageSize } from './constants';
import { useInfiniteScroll, useAnalytics, useFilterState, isFiltersEmpty } from './hooks';
import { Header, Footer, FilterBar, ImagesGrid, FullscreenModal } from './components';

function App() {
  // Disable browser scroll restoration to prevent F5 reload from cascading infinite scroll
  useEffect(() => {
    if ('scrollRestoration' in history) {
      history.scrollRestoration = 'manual';
    }
    window.scrollTo(0, 0);
  }, []);

  // Custom hooks
  const { trackPageview, trackEvent } = useAnalytics();

  const {
    activeFilters,
    filterCounts,
    orCounts,
    allImages,
    displayedImages,
    hasMore,
    loading,
    error,
    setDisplayedImages,
    setHasMore,
    handleAddFilter,
    handleAddValueToGroup,
    handleRemoveFilter,
    handleRemoveGroup,
    handleRandom,
    randomAnimation,
  } = useFilterState({
    onTrackPageview: trackPageview,
    onTrackEvent: trackEvent,
  });

  const { loadMoreRef } = useInfiniteScroll({
    allImages,
    displayedImages,
    hasMore,
    setDisplayedImages,
    setHasMore,
  });

  // Data state
  const [specsData, setSpecsData] = useState<SpecInfo[]>([]);
  const [librariesData, setLibrariesData] = useState<LibraryInfo[]>([]);
  const [stats, setStats] = useState<{ specs: number; plots: number; libraries: number } | null>(null);

  // UI state
  const [modalImage, setModalImage] = useState<PlotImage | null>(null);
  const [openImageTooltip, setOpenImageTooltip] = useState<string | null>(null);
  const [imageSize, setImageSize] = useState<ImageSize>(() => {
    const stored = localStorage.getItem('imageSize');
    return stored === 'normal' || stored === 'compact' ? stored : 'normal';
  });
  const [showScrollTop, setShowScrollTop] = useState(false);

  // Refs
  const searchInputRef = useRef<HTMLInputElement>(null);

  // Persist imageSize to localStorage
  useEffect(() => {
    localStorage.setItem('imageSize', imageSize);
  }, [imageSize]);

  // Show/hide scroll-to-top button based on scroll position
  useEffect(() => {
    const handleScroll = () => {
      setShowScrollTop(window.scrollY > 300);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Handle card click - open modal
  const handleCardClick = useCallback(
    (img: PlotImage) => {
      if (document.activeElement instanceof HTMLElement) {
        document.activeElement.blur();
      }
      setModalImage(img);
      trackEvent('modal_open', { spec: img.spec_id || '', library: img.library });
    },
    [trackEvent]
  );

  // Close tooltip when clicking anywhere
  const handleContainerClick = useCallback(
    (e: React.MouseEvent) => {
      const target = e.target as HTMLElement;
      if (target.closest('[data-description-btn]')) return;
      if (openImageTooltip) setOpenImageTooltip(null);
    },
    [openImageTooltip]
  );

  // Global keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      const target = e.target as HTMLElement;
      if (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA' || modalImage) return;

      if (e.key === ' ') {
        e.preventDefault();
        handleRandom('space');
      } else if (e.key === 'Enter' && searchInputRef.current) {
        e.preventDefault();
        searchInputRef.current.focus();
      } else if (e.key === 'Backspace' && activeFilters.length > 0) {
        e.preventDefault();
        handleRemoveGroup(activeFilters.length - 1);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [handleRandom, handleRemoveGroup, activeFilters.length, modalImage]);

  // Load initial data on mount
  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        const [specsRes, libsRes, statsRes] = await Promise.all([
          fetch(`${API_URL}/specs`),
          fetch(`${API_URL}/libraries`),
          fetch(`${API_URL}/stats`),
        ]);

        if (specsRes.ok) {
          const data = await specsRes.json();
          setSpecsData(Array.isArray(data) ? data : data.specs || []);
        }

        if (libsRes.ok) {
          const data = await libsRes.json();
          setLibrariesData(data.libraries || []);
        }

        if (statsRes.ok) {
          const data = await statsRes.json();
          setStats(data);
        }
      } catch (err) {
        console.error('Error loading initial data:', err);
      }
    };
    fetchInitialData();
  }, []);

  // Get selected spec/library for compatibility with existing components
  const specFilter = activeFilters.find((f) => f.category === 'spec');
  const libFilter = activeFilters.find((f) => f.category === 'lib');
  const selectedSpec = specFilter?.values[0] || '';
  const selectedLibrary = libFilter?.values[0] || '';

  return (
    <Box onClick={handleContainerClick} sx={{ minHeight: '100vh', bgcolor: '#fafafa', py: 5, position: 'relative' }}>
      <Container maxWidth={false} sx={{ px: { xs: 4, sm: 8, lg: 12 } }}>
        <Header stats={stats} onRandom={handleRandom} />

        {error && (
          <Alert severity="error" sx={{ mb: 4, maxWidth: 500, mx: 'auto' }}>
            {error}
          </Alert>
        )}

        <FilterBar
          activeFilters={activeFilters}
          filterCounts={filterCounts}
          orCounts={orCounts}
          currentTotal={allImages.length}
          displayedCount={displayedImages.length}
          randomAnimation={randomAnimation}
          searchInputRef={searchInputRef}
          imageSize={imageSize}
          onImageSizeChange={setImageSize}
          onAddFilter={handleAddFilter}
          onAddValueToGroup={handleAddValueToGroup}
          onRemoveFilter={handleRemoveFilter}
          onRemoveGroup={handleRemoveGroup}
          onTrackEvent={trackEvent}
        />

        <ImagesGrid
          images={displayedImages}
          viewMode={isFiltersEmpty(activeFilters) ? 'library' : 'spec'}
          selectedSpec={selectedSpec}
          selectedLibrary={selectedLibrary}
          loading={loading}
          hasMore={hasMore}
          isLoadingMore={false}
          isTransitioning={false}
          librariesData={librariesData}
          specsData={specsData}
          openTooltip={openImageTooltip}
          loadMoreRef={loadMoreRef}
          imageSize={imageSize}
          onTooltipToggle={setOpenImageTooltip}
          onCardClick={handleCardClick}
          onTrackEvent={trackEvent}
        />

        {!loading && allImages.length === 0 && !isFiltersEmpty(activeFilters) && (
          <Alert severity="info" sx={{ maxWidth: 400, mx: 'auto' }}>
            No plots match these filters.
          </Alert>
        )}

        <Footer onTrackEvent={trackEvent} selectedSpec={selectedSpec} selectedLibrary={selectedLibrary} />
      </Container>

      <FullscreenModal
        image={modalImage}
        selectedSpec={modalImage?.spec_id || selectedSpec}
        onClose={() => setModalImage(null)}
        onTrackEvent={trackEvent}
      />

      {/* Floating scroll-to-top button */}
      <Fab
        size="small"
        onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
        sx={{
          position: 'fixed',
          bottom: 24,
          right: 24,
          bgcolor: '#f3f4f6',
          color: '#6b7280',
          opacity: showScrollTop ? 1 : 0,
          visibility: showScrollTop ? 'visible' : 'hidden',
          transition: 'opacity 0.3s, visibility 0.3s',
          '&:hover': { bgcolor: '#e5e7eb', color: '#3776AB' },
        }}
      >
        <KeyboardArrowUpIcon />
      </Fab>
    </Box>
  );
}

export default App;
