import { useState, useEffect, useCallback } from 'react';
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

  // Shuffle a group (random value from that category)
  const handleShuffle = useCallback(
    (groupIndex: number) => {
      if (!filterCounts) return;

      setActiveFilters((prev) => {
        const group = prev[groupIndex];
        if (!group) return prev;

        const counts = filterCounts[group.category];
        const availableValues = Object.keys(counts);
        if (availableValues.length === 0) return prev;

        // Pick a random value that's not in this group
        const otherValues = availableValues.filter((v) => !group.values.includes(v));
        const pool = otherValues.length > 0 ? otherValues : availableValues;
        const randomValue = pool[Math.floor(Math.random() * pool.length)];

        const newFilters = [...prev];
        newFilters[groupIndex] = { ...group, values: [randomValue] };
        return newFilters;
      });
    },
    [filterCounts]
  );

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
        <Header stats={stats} />

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
          onAddFilter={handleAddFilter}
          onAddValueToGroup={handleAddValueToGroup}
          onRemoveFilter={handleRemoveFilter}
          onRemoveGroup={handleRemoveGroup}
          onShuffle={handleShuffle}
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
