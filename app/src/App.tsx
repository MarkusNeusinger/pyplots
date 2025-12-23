import { useState, useEffect, useCallback, useRef } from 'react';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Alert from '@mui/material/Alert';

import type { PlotImage, LibraryInfo, SpecInfo, FilterCategory, ActiveFilters, FilterCounts } from './types';
import { FILTER_CATEGORIES } from './types';
import { API_URL, BATCH_SIZE } from './constants';
import { useInfiniteScroll, useAnalytics } from './hooks';
import { Header, Footer, FilterBar, ImagesGrid, FullscreenModal } from './components';

// Fisher-Yates shuffle algorithm
const shuffleArray = <T,>(array: T[]): T[] => {
  const shuffled = [...array];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
};

// Parse URL params into ActiveFilters (array-based)
// URL format: ?lib=matplotlib&lib=seaborn (AND) or ?lib=matplotlib,seaborn (OR within group)
const parseUrlFilters = (): ActiveFilters => {
  const params = new URLSearchParams(window.location.search);
  const filters: ActiveFilters = [];

  FILTER_CATEGORIES.forEach((category) => {
    // getAll returns all values for params with same name (for AND)
    const allValues = params.getAll(category);
    allValues.forEach((value) => {
      if (value) {
        const values = value.split(',').map((v) => v.trim()).filter(Boolean);
        if (values.length > 0) {
          filters.push({ category, values });
        }
      }
    });
  });

  return filters;
};

// Build URL from ActiveFilters (array-based)
const buildFilterUrl = (filters: ActiveFilters): string => {
  const params = new URLSearchParams();
  filters.forEach(({ category, values }) => {
    if (values.length > 0) {
      // append allows multiple params with same name (for AND)
      params.append(category, values.join(','));
    }
  });
  const queryString = params.toString();
  return queryString ? `?${queryString}` : '/';
};

// Check if filters are empty
const isFiltersEmpty = (filters: ActiveFilters): boolean => {
  return filters.length === 0 || filters.every((f) => f.values.length === 0);
};

function App() {
  // Filter state - initialize from URL params immediately
  const [activeFilters, setActiveFilters] = useState<ActiveFilters>(() => parseUrlFilters());
  const [filterCounts, setFilterCounts] = useState<FilterCounts | null>(null);
  const [globalCounts, setGlobalCounts] = useState<FilterCounts | null>(null);
  const [orCounts, setOrCounts] = useState<Record<string, number>[]>([]);

  // Data state
  const [specsData, setSpecsData] = useState<SpecInfo[]>([]);
  const [librariesData, setLibrariesData] = useState<LibraryInfo[]>([]);
  const [stats, setStats] = useState<{ specs: number; plots: number; libraries: number } | null>(null);
  const [allImages, setAllImages] = useState<PlotImage[]>([]);
  const [displayedImages, setDisplayedImages] = useState<PlotImage[]>([]);
  const [hasMore, setHasMore] = useState(false);

  // UI state
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');
  const [modalImage, setModalImage] = useState<PlotImage | null>(null);
  const [openImageTooltip, setOpenImageTooltip] = useState<string | null>(null);
  const [randomAnimation, setRandomAnimation] = useState<{ index: number; phase: 'out' | 'in'; oldLabel?: string } | null>(null);

  // Refs
  const searchInputRef = useRef<HTMLInputElement>(null);

  // Custom hooks
  const { trackPageview, trackEvent } = useAnalytics();

  const { loadMoreRef } = useInfiniteScroll({
    allImages,
    displayedImages,
    hasMore,
    setDisplayedImages,
    setHasMore,
  });

  // Handle card click - open modal
  const handleCardClick = useCallback(
    (img: PlotImage) => {
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

  // Add a new filter group (creates new chip - AND with other groups)
  const handleAddFilter = useCallback((category: FilterCategory, value: string) => {
    setActiveFilters((prev) => [...prev, { category, values: [value] }]);
  }, []);

  // Add value to existing group by index (OR within that group)
  const handleAddValueToGroup = useCallback((groupIndex: number, value: string) => {
    setActiveFilters((prev) => {
      const newFilters = [...prev];
      const group = newFilters[groupIndex];
      if (group && !group.values.includes(value)) {
        newFilters[groupIndex] = { ...group, values: [...group.values, value] };
      }
      return newFilters;
    });
  }, []);

  // Remove a filter value from a specific group
  const handleRemoveFilter = useCallback((groupIndex: number, value: string) => {
    setActiveFilters((prev) => {
      const newFilters = [...prev];
      const group = newFilters[groupIndex];
      if (!group) return prev;

      const updatedValues = group.values.filter((v) => v !== value);
      if (updatedValues.length === 0) {
        // Remove entire group if no values left
        return newFilters.filter((_, i) => i !== groupIndex);
      }
      newFilters[groupIndex] = { ...group, values: updatedValues };
      return newFilters;
    });
  }, []);

  // Remove entire group by index
  const handleRemoveGroup = useCallback((groupIndex: number) => {
    setActiveFilters((prev) => prev.filter((_, i) => i !== groupIndex));
  }, []);

  // Random filter - replaces last filter slot (or adds first one)
  const handleRandom = useCallback((method: 'click' | 'space' | 'doubletap' = 'click') => {
    // Use contextual counts if filters exist, otherwise global
    const countsToUse = activeFilters.length > 0 ? filterCounts : globalCounts;
    if (!countsToUse) return;

    const availableCategories = FILTER_CATEGORIES.filter((cat) => {
      const counts = countsToUse[cat];
      return counts && Object.keys(counts).length > 0;
    });

    if (availableCategories.length === 0) return;

    const randomCategory = availableCategories[Math.floor(Math.random() * availableCategories.length)];
    const values = Object.keys(countsToUse[randomCategory]);

    if (values.length === 0) return;

    const randomValue = values[Math.floor(Math.random() * values.length)];
    const newFilter = { category: randomCategory, values: [randomValue] };

    // Get old label before changing
    const newIndex = activeFilters.length === 0 ? 0 : activeFilters.length - 1;
    const oldGroup = activeFilters[newIndex];
    const oldLabel = oldGroup ? `${oldGroup.category}:${oldGroup.values.join(',')}` : '';

    // Start animation with old label, change filter immediately (so images load)
    setRandomAnimation({ index: newIndex, phase: 'out', oldLabel });
    setActiveFilters((prev) => {
      if (prev.length === 0) {
        return [newFilter];
      }
      return [...prev.slice(0, -1), newFilter];
    });

    // Switch to 'in' phase at halfway point (now showing new label)
    setTimeout(() => {
      setRandomAnimation({ index: newIndex, phase: 'in' });
    }, 500);

    // Clear animation state
    setTimeout(() => setRandomAnimation(null), 1000);

    trackEvent('random', { category: randomCategory, value: randomValue, method });
  }, [activeFilters.length, filterCounts, globalCounts, trackEvent]);

  // Global keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Don't trigger if typing in input or modal is open
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
        // Fetch specs, libraries, and stats in parallel
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

  // Update URL when filters change
  useEffect(() => {
    const newUrl = buildFilterUrl(activeFilters);
    window.history.replaceState({}, '', newUrl);

    // Update document title
    const filterParts = activeFilters
      .filter((f) => f.values.length > 0)
      .map((f) => `${f.category}:${f.values.join(',')}`)
      .join(' ');

    document.title = filterParts ? `${filterParts} | pyplots.ai` : 'pyplots.ai';
    trackPageview();
  }, [activeFilters, trackPageview]);

  // Load filtered images when filters change
  useEffect(() => {
    const fetchFilteredImages = async () => {
      setLoading(true);
      setOpenImageTooltip(null);

      try {
        // Build query string from filters (multiple params with same name for AND)
        const params = new URLSearchParams();
        activeFilters.forEach(({ category, values }) => {
          if (values.length > 0) {
            params.append(category, values.join(','));
          }
        });

        const queryString = params.toString();
        const url = `${API_URL}/plots/filter${queryString ? `?${queryString}` : ''}`;

        const response = await fetch(url);
        if (!response.ok) throw new Error('Failed to fetch filtered plots');

        const data = await response.json();

        // Update filter counts
        setFilterCounts(data.counts);  // Contextual for AND additions
        setGlobalCounts(data.globalCounts || data.counts);  // Global for random
        setOrCounts(data.orCounts || []);  // Per-group for OR additions

        // Shuffle and set images
        const shuffled = shuffleArray<PlotImage>(data.images || []);
        setAllImages(shuffled);
        setDisplayedImages(shuffled.slice(0, BATCH_SIZE));
        setHasMore(shuffled.length > BATCH_SIZE);
      } catch (err) {
        setError(`Error loading images: ${err}`);
      } finally {
        setLoading(false);
      }
    };

    fetchFilteredImages();
  }, [activeFilters]);

  // Get selected spec/library for compatibility with existing components
  const specFilter = activeFilters.find((f) => f.category === 'spec');
  const libFilter = activeFilters.find((f) => f.category === 'lib');
  const selectedSpec = specFilter?.values[0] || '';
  const selectedLibrary = libFilter?.values[0] || '';

  return (
    <Box onClick={handleContainerClick} sx={{ minHeight: '100vh', bgcolor: '#fafafa', py: 5 }}>
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
          randomAnimation={randomAnimation}
          searchInputRef={searchInputRef}
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
          isTransitioning={false}
          librariesData={librariesData}
          specsData={specsData}
          openTooltip={openImageTooltip}
          loadMoreRef={loadMoreRef}
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
    </Box>
  );
}

export default App;
