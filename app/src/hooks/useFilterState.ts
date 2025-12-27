/**
 * Hook for managing filter state and URL synchronization.
 *
 * Encapsulates all filter-related state and callbacks used in App.tsx.
 */

import { useState, useCallback, useEffect, useRef } from 'react';

import type { PlotImage, FilterCategory, ActiveFilters, FilterCounts } from '../types';
import { FILTER_CATEGORIES } from '../types';
import { API_URL, BATCH_SIZE } from '../constants';

/**
 * Fisher-Yates shuffle algorithm.
 */
function shuffleArray<T>(array: T[]): T[] {
  const shuffled = [...array];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
}

/**
 * Parse URL params into ActiveFilters.
 * URL format: ?lib=matplotlib&lib=seaborn (AND) or ?lib=matplotlib,seaborn (OR within group)
 */
function parseUrlFilters(): ActiveFilters {
  const params = new URLSearchParams(window.location.search);
  const filters: ActiveFilters = [];

  FILTER_CATEGORIES.forEach((category) => {
    const allValues = params.getAll(category);
    allValues.forEach((value) => {
      if (value) {
        const values = value
          .split(',')
          .map((v) => v.trim())
          .filter(Boolean);
        if (values.length > 0) {
          filters.push({ category, values });
        }
      }
    });
  });

  return filters;
}

/**
 * Build URL from ActiveFilters.
 */
function buildFilterUrl(filters: ActiveFilters): string {
  const params = new URLSearchParams();
  filters.forEach(({ category, values }) => {
    if (values.length > 0) {
      params.append(category, values.join(','));
    }
  });
  const queryString = params.toString();
  return queryString ? `?${queryString}` : '/';
}

/**
 * Check if filters are empty.
 */
export function isFiltersEmpty(filters: ActiveFilters): boolean {
  return filters.length === 0 || filters.every((f) => f.values.length === 0);
}

interface UseFilterStateOptions {
  onTrackPageview: () => void;
  onTrackEvent: (event: string, props?: Record<string, string>) => void;
}

interface UseFilterStateReturn {
  // State
  activeFilters: ActiveFilters;
  filterCounts: FilterCounts | null;
  globalCounts: FilterCounts | null;
  orCounts: Record<string, number>[];
  allImages: PlotImage[];
  displayedImages: PlotImage[];
  hasMore: boolean;
  loading: boolean;
  error: string;

  // Setters for external state
  setDisplayedImages: React.Dispatch<React.SetStateAction<PlotImage[]>>;
  setHasMore: React.Dispatch<React.SetStateAction<boolean>>;
  setError: React.Dispatch<React.SetStateAction<string>>;

  // Callbacks
  handleAddFilter: (category: FilterCategory, value: string) => void;
  handleAddValueToGroup: (groupIndex: number, value: string) => void;
  handleRemoveFilter: (groupIndex: number, value: string) => void;
  handleRemoveGroup: (groupIndex: number) => void;
  handleRandom: (method?: 'click' | 'space' | 'doubletap') => void;

  // Animation state for random
  randomAnimation: { index: number; phase: 'out' | 'in'; oldLabel?: string } | null;
}

export function useFilterState({
  onTrackPageview,
  onTrackEvent,
}: UseFilterStateOptions): UseFilterStateReturn {
  // Filter state - initialize from URL params immediately
  const [activeFilters, setActiveFilters] = useState<ActiveFilters>(() => parseUrlFilters());
  const [filterCounts, setFilterCounts] = useState<FilterCounts | null>(null);
  const [globalCounts, setGlobalCounts] = useState<FilterCounts | null>(null);
  const [orCounts, setOrCounts] = useState<Record<string, number>[]>([]);

  // Image state
  const [allImages, setAllImages] = useState<PlotImage[]>([]);
  const [displayedImages, setDisplayedImages] = useState<PlotImage[]>([]);
  const [hasMore, setHasMore] = useState(false);

  // UI state
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');
  const [randomAnimation, setRandomAnimation] = useState<{
    index: number;
    phase: 'out' | 'in';
    oldLabel?: string;
  } | null>(null);

  // Refs for stable callbacks
  const activeFiltersRef = useRef(activeFilters);
  activeFiltersRef.current = activeFilters;

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
  const handleRandom = useCallback(
    (method: 'click' | 'space' | 'doubletap' = 'click') => {
      const currentFilters = activeFiltersRef.current;
      // Use contextual counts if filters exist, otherwise global
      const countsToUse = currentFilters.length > 0 ? filterCounts : globalCounts;
      if (!countsToUse) return;

      const availableCategories = FILTER_CATEGORIES.filter((cat) => {
        const counts = countsToUse[cat];
        return counts && Object.keys(counts).length > 0;
      });

      if (availableCategories.length === 0) return;

      const randomCategory =
        availableCategories[Math.floor(Math.random() * availableCategories.length)];
      const values = Object.keys(countsToUse[randomCategory]);

      if (values.length === 0) return;

      const randomValue = values[Math.floor(Math.random() * values.length)];
      const newFilter = { category: randomCategory, values: [randomValue] };

      // Get old label before changing
      const newIndex = currentFilters.length === 0 ? 0 : currentFilters.length - 1;
      const oldGroup = currentFilters[newIndex];
      const oldLabel = oldGroup ? `${oldGroup.category}:${oldGroup.values.join(',')}` : '';

      // Start animation with old label, change filter immediately (so images load)
      setRandomAnimation({ index: newIndex, phase: 'out', oldLabel });
      setActiveFilters((prev) => {
        if (prev.length === 0) {
          return [newFilter];
        }
        return [...prev.slice(0, -1), newFilter];
      });

      // Switch to 'in' phase at halfway point
      setTimeout(() => {
        setRandomAnimation({ index: newIndex, phase: 'in' });
      }, 500);

      // Clear animation state
      setTimeout(() => setRandomAnimation(null), 1000);

      onTrackEvent('random', { category: randomCategory, value: randomValue, method });
    },
    [filterCounts, globalCounts, onTrackEvent]
  );

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
    onTrackPageview();
  }, [activeFilters, onTrackPageview]);

  // Load filtered images when filters change
  useEffect(() => {
    const abortController = new AbortController();

    const fetchFilteredImages = async () => {
      setLoading(true);

      try {
        // Build query string from filters
        const params = new URLSearchParams();
        activeFilters.forEach(({ category, values }) => {
          if (values.length > 0) {
            params.append(category, values.join(','));
          }
        });

        const queryString = params.toString();
        const url = `${API_URL}/plots/filter${queryString ? `?${queryString}` : ''}`;

        const response = await fetch(url, { signal: abortController.signal });
        if (!response.ok) throw new Error('Failed to fetch filtered plots');

        const data = await response.json();

        if (abortController.signal.aborted) return;

        // Update filter counts
        setFilterCounts(data.counts);
        setGlobalCounts(data.globalCounts || data.counts);
        setOrCounts(data.orCounts || []);

        // Shuffle and set images
        const shuffled = shuffleArray<PlotImage>(data.images || []);
        setAllImages(shuffled);
        setDisplayedImages(shuffled.slice(0, BATCH_SIZE));
        setHasMore(shuffled.length > BATCH_SIZE);
      } catch (err) {
        if (abortController.signal.aborted) return;
        setError(`Error loading images: ${err}`);
      } finally {
        if (!abortController.signal.aborted) {
          setLoading(false);
        }
      }
    };

    fetchFilteredImages();

    return () => abortController.abort();
  }, [activeFilters]);

  return {
    // State
    activeFilters,
    filterCounts,
    globalCounts,
    orCounts,
    allImages,
    displayedImages,
    hasMore,
    loading,
    error,

    // Setters
    setDisplayedImages,
    setHasMore,
    setError,

    // Callbacks
    handleAddFilter,
    handleAddValueToGroup,
    handleRemoveFilter,
    handleRemoveGroup,
    handleRandom,

    // Animation
    randomAnimation,
  };
}
