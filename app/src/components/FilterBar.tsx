import { useState, useCallback, useRef, useEffect, useMemo } from 'react';
import { Link } from 'react-router-dom';
import Box from '@mui/material/Box';
import Chip from '@mui/material/Chip';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import ListItemText from '@mui/material/ListItemText';
import Typography from '@mui/material/Typography';
import InputBase from '@mui/material/InputBase';
import Divider from '@mui/material/Divider';
import Tooltip from '@mui/material/Tooltip';
import CloseIcon from '@mui/icons-material/Close';
import SearchIcon from '@mui/icons-material/Search';
import AddIcon from '@mui/icons-material/Add';
import ViewAgendaIcon from '@mui/icons-material/ViewAgenda';
import ViewModuleIcon from '@mui/icons-material/ViewModule';
import ListIcon from '@mui/icons-material/List';
import useMediaQuery from '@mui/material/useMediaQuery';
import { useTheme } from '@mui/material/styles';

import type { FilterCategory, ActiveFilters, FilterCounts } from '../types';
import { FILTER_LABELS, FILTER_CATEGORIES } from '../types';
import type { ImageSize } from '../constants';
import { getAvailableValues, getAvailableValuesForGroup, getSearchResults } from '../utils';

interface FilterBarProps {
  activeFilters: ActiveFilters;
  filterCounts: FilterCounts | null;  // Contextual counts (for AND additions)
  orCounts: Record<string, number>[];  // Per-group counts for OR additions
  currentTotal: number;  // Total number of filtered images
  displayedCount: number;  // Currently displayed images
  randomAnimation: { index: number; phase: 'out' | 'in'; oldLabel?: string } | null;
  searchInputRef?: React.RefObject<HTMLInputElement | null>;
  imageSize: ImageSize;
  onImageSizeChange: (size: ImageSize) => void;
  onAddFilter: (category: FilterCategory, value: string) => void;
  onAddValueToGroup: (groupIndex: number, value: string) => void;
  onRemoveFilter: (groupIndex: number, value: string) => void;
  onRemoveGroup: (groupIndex: number) => void;
  onTrackEvent: (event: string, props?: Record<string, string>) => void;
}

export function FilterBar({
  activeFilters,
  filterCounts,
  orCounts,
  currentTotal,
  displayedCount,
  randomAnimation,
  searchInputRef,
  imageSize,
  onImageSizeChange,
  onAddFilter,
  onAddValueToGroup,
  onRemoveFilter,
  onRemoveGroup,
  onTrackEvent,
}: FilterBarProps) {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));

  // Scroll percentage and sticky detection
  const [scrollPercent, setScrollPercent] = useState(0);
  const [isSticky, setIsSticky] = useState(false);
  const filterBarRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const calculatePercent = () => {
      const scrollY = window.scrollY;
      const docHeight = document.documentElement.scrollHeight;
      const windowHeight = window.innerHeight;

      // Estimate total height based on ratio of loaded vs total plots
      const loadRatio = displayedCount > 0 && currentTotal > 0
        ? currentTotal / displayedCount
        : 1;
      const estimatedTotalHeight = (docHeight - windowHeight) * loadRatio;

      const percent = Math.round((scrollY / estimatedTotalHeight) * 100);
      setScrollPercent(Math.min(100, Math.max(0, percent || 0)));

      // Detect if bar is in sticky mode (scrolled past threshold)
      // The bar becomes sticky when scrollY > ~200px (header height)
      setIsSticky(scrollY > 200);
    };
    calculatePercent();
    window.addEventListener('scroll', calculatePercent);
    const resizeObserver = new ResizeObserver(calculatePercent);
    resizeObserver.observe(document.body);
    return () => {
      window.removeEventListener('scroll', calculatePercent);
      resizeObserver.disconnect();
    };
  }, [displayedCount, currentTotal]);

  // Search/dropdown state
  const [searchQuery, setSearchQuery] = useState('');
  const [dropdownAnchor, setDropdownAnchor] = useState<HTMLElement | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<FilterCategory | null>(null);
  const [isSearchManuallyExpanded, setIsSearchManuallyExpanded] = useState(false);
  const searchContainerRef = useRef<HTMLDivElement>(null);
  const localInputRef = useRef<HTMLInputElement>(null);
  const inputRef = searchInputRef || localInputRef;

  // Search is expanded when: no filters OR manually expanded
  const isSearchExpanded = activeFilters.length === 0 || isSearchManuallyExpanded;

  // Chip menu state
  const [chipMenuAnchor, setChipMenuAnchor] = useState<HTMLElement | null>(null);
  const [activeGroupIndex, setActiveGroupIndex] = useState<number | null>(null);

  // Dropdown keyboard navigation
  const [highlightedIndex, setHighlightedIndex] = useState<number>(-1);

  // Expand and open dropdown
  const handleSearchExpand = useCallback(() => {
    setIsSearchManuallyExpanded(true);
    setDropdownAnchor(searchContainerRef.current);
    setTimeout(() => inputRef.current?.focus(), 0);
  }, []);

  // Collapse when empty and loses focus (only if there are filters)
  const handleSearchBlur = useCallback(() => {
    // Delay to allow click events on dropdown to fire first
    setTimeout(() => {
      if (!searchQuery && !selectedCategory && !dropdownAnchor && activeFilters.length > 0) {
        setIsSearchManuallyExpanded(false);
      }
    }, 200);
  }, [searchQuery, selectedCategory, dropdownAnchor, activeFilters.length]);

  // Close dropdown and collapse if empty
  const handleDropdownClose = useCallback(() => {
    setDropdownAnchor(null);
    setSelectedCategory(null);
    setSearchQuery('');
    setIsSearchManuallyExpanded(false);
  }, []);

  // Select category from dropdown
  const handleCategorySelect = useCallback((category: FilterCategory) => {
    setSelectedCategory(category);
    setSearchQuery('');
    setTimeout(() => inputRef.current?.focus(), 50);
  }, []);

  // Select value (add new filter group)
  const handleValueSelect = useCallback(
    (category: FilterCategory, value: string) => {
      onAddFilter(category, value);
      // Track search if query was used (filter changes tracked via pageview)
      if (searchQuery.trim()) {
        onTrackEvent('search', { query: searchQuery.trim(), category });
      }
      setSelectedCategory(null);
      setSearchQuery('');
      // Keep expanded and focused for next filter
      setIsSearchManuallyExpanded(true);
      setTimeout(() => {
        setDropdownAnchor(searchContainerRef.current);
        inputRef.current?.focus();
      }, 50);
    },
    [onAddFilter, onTrackEvent, searchQuery]
  );

  // Chip click - open chip menu
  const handleChipClick = useCallback(
    (event: React.MouseEvent<HTMLElement>, groupIndex: number) => {
      setChipMenuAnchor(event.currentTarget);
      setActiveGroupIndex(groupIndex);
    },
    []
  );

  // Remove single value from group
  const handleRemoveValue = useCallback(
    (value: string) => {
      if (activeGroupIndex !== null) {
        onRemoveFilter(activeGroupIndex, value);
      }
      setChipMenuAnchor(null);
      setActiveGroupIndex(null);
    },
    [activeGroupIndex, onRemoveFilter]
  );

  // Remove entire group
  const handleRemoveGroup = useCallback(() => {
    if (activeGroupIndex !== null) {
      onRemoveGroup(activeGroupIndex);
    }
    setChipMenuAnchor(null);
    setActiveGroupIndex(null);
  }, [activeGroupIndex, onRemoveGroup]);

  // Add value to existing group (OR)
  const handleAddValueToExistingGroup = useCallback(
    (value: string) => {
      if (activeGroupIndex !== null) {
        onAddValueToGroup(activeGroupIndex, value);
      }
      setChipMenuAnchor(null);
      setActiveGroupIndex(null);
    },
    [activeGroupIndex, onAddValueToGroup]
  );

  // Memoize search results to avoid recalculating on every render
  const searchResults = useMemo(
    () => getSearchResults(filterCounts, activeFilters, searchQuery, selectedCategory),
    [filterCounts, activeFilters, searchQuery, selectedCategory]
  );

  // Track searches with no results (debounced, to discover missing specs)
  const lastTrackedQueryRef = useRef<string>('');
  useEffect(() => {
    const query = searchQuery.trim();
    // Only track if: query >= 2 chars, no results, not already tracked this query
    if (query.length >= 2 && searchResults.length === 0 && query !== lastTrackedQueryRef.current) {
      const timer = setTimeout(() => {
        onTrackEvent('search_no_results', { query });
        lastTrackedQueryRef.current = query;
      }, 500);
      return () => clearTimeout(timer);
    }
  }, [searchQuery, searchResults.length, onTrackEvent]);

  // Reset tracked query when dropdown closes
  useEffect(() => {
    if (!dropdownAnchor) {
      lastTrackedQueryRef.current = '';
    }
  }, [dropdownAnchor]);

  // Only open if anchor is valid and in document
  const isDropdownOpen = Boolean(dropdownAnchor) && document.body.contains(dropdownAnchor);
  const hasQuery = searchQuery.trim().length > 0;
  const maxFiltersReached = activeFilters.length >= 5;

  // Get dropdown items for keyboard navigation
  const getDropdownItems = useCallback(() => {
    if (!selectedCategory && !hasQuery) {
      // Categories list
      return FILTER_CATEGORIES
        .filter((cat) => {
          const available = getAvailableValues(filterCounts, activeFilters, cat);
          return available.length > 0;
        })
        .map((cat) => ({ type: 'category' as const, category: cat }));
    } else {
      // Search results or category values
      return searchResults.map((r) => ({ type: 'value' as const, ...r }));
    }
  }, [selectedCategory, hasQuery, filterCounts, activeFilters, searchResults]);

  const dropdownItems = getDropdownItems();

  // Reset highlight when dropdown content changes
  useEffect(() => {
    setHighlightedIndex(-1);
  }, [searchQuery, selectedCategory, dropdownAnchor]);

  // Handle keyboard navigation
  const handleKeyDown = useCallback(
    (event: React.KeyboardEvent) => {
      if (event.key === 'ArrowDown') {
        event.preventDefault();
        setHighlightedIndex((prev) => Math.min(prev + 1, dropdownItems.length - 1));
      } else if (event.key === 'ArrowUp') {
        event.preventDefault();
        setHighlightedIndex((prev) => Math.max(prev - 1, -1));
      } else if (event.key === 'Enter') {
        event.preventDefault();
        const item = dropdownItems[highlightedIndex] || dropdownItems[0];
        if (item) {
          if (item.type === 'category') {
            handleCategorySelect(item.category);
            setHighlightedIndex(-1);
          } else {
            handleValueSelect(item.category, item.value);
          }
        }
      } else if (event.key === 'Escape') {
        handleDropdownClose();
        inputRef.current?.blur();
      }
    },
    [dropdownItems, highlightedIndex, handleCategorySelect, handleValueSelect, handleDropdownClose]
  );

  // Get active group for chip menu
  const activeGroup = activeGroupIndex !== null ? activeFilters[activeGroupIndex] : null;
  const availableValuesForActiveGroup = activeGroupIndex !== null
    ? getAvailableValuesForGroup(activeGroupIndex, activeFilters, orCounts, currentTotal)
    : [];

  return (
    <Box
      ref={filterBarRef}
      sx={{
        mb: 4,
        position: 'sticky',
        top: 0,
        zIndex: 100,
        py: 1,
        transition: 'background-color 0.2s, border-color 0.2s, margin 0.2s, padding 0.2s',
        // Only apply full-width styling when sticky
        ...(isSticky
          ? {
              mx: { xs: -2, sm: -4, md: -8, lg: -12 },
              px: { xs: 2, sm: 4, md: 8, lg: 12 },
              bgcolor: '#f3f4f6',
              borderBottom: '1px solid #e5e7eb',
            }
          : {
              px: 2,
              bgcolor: 'transparent',
              borderBottom: '1px solid transparent',
            }),
      }}
    >
      {/* Filter chips row */}
      <Box
        sx={{
          display: 'flex',
          flexWrap: 'wrap',
          gap: 1,
          justifyContent: 'center',
          alignItems: 'center',
          position: { xs: 'static', md: 'relative' },
        }}
      >
        {/* Progress counter - absolute left (desktop only) */}
        {!isMobile && currentTotal > 0 && (
          <Typography
            sx={{
              position: 'absolute',
              left: 0,
              fontFamily: '"MonoLisa", "MonoLisa Fallback", monospace',
              fontSize: '0.75rem',
              color: '#9ca3af',
              whiteSpace: 'nowrap',
            }}
          >
            {scrollPercent}% · {currentTotal}
          </Typography>
        )}
        {/* Catalog icon + Grid size toggle - absolute right (desktop only) */}
        {!isMobile && (
          <Box
            sx={{
              position: 'absolute',
              right: 0,
              display: 'flex',
              alignItems: 'center',
              gap: 0.5,
            }}
          >
            {/* Catalog icon */}
            <Tooltip title="catalog">
              <Box
                component={Link}
                to="/catalog"
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  width: 32,
                  height: 32,
                  color: '#9ca3af',
                  '&:hover': { color: '#3776AB' },
                }}
              >
                <ListIcon sx={{ fontSize: '1.25rem' }} />
              </Box>
            </Tooltip>
            {/* Grid size toggle */}
            <Tooltip title={imageSize === 'normal' ? 'compact view' : 'normal view'}>
              <Box
                onClick={() => onImageSizeChange(imageSize === 'normal' ? 'compact' : 'normal')}
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  width: 32,
                  height: 32,
                  cursor: 'pointer',
                  color: '#9ca3af',
                  '&:hover': { color: '#3776AB' },
                }}
              >
                {imageSize === 'normal' ? (
                  <ViewAgendaIcon sx={{ fontSize: '1.25rem' }} />
                ) : (
                  <ViewModuleIcon sx={{ fontSize: '1.25rem' }} />
                )}
              </Box>
            </Tooltip>
          </Box>
        )}
        {/* Active filter chips */}
      {activeFilters.map((group, index) => {
        const isAnimating = randomAnimation?.index === index;
        const animationClass = isAnimating ? `chip-blur-${randomAnimation.phase}` : undefined;
        // Show old label during 'out' phase, new label during 'in' phase
        const displayLabel = isAnimating && randomAnimation.phase === 'out' && randomAnimation.oldLabel
          ? randomAnimation.oldLabel
          : `${group.category}:${group.values.join(',')}`;

        return (
          <Chip
            key={`${group.category}-${index}`}
            label={displayLabel}
            onClick={(e) => handleChipClick(e, index)}
            onDelete={() => onRemoveGroup(index)}
            deleteIcon={<CloseIcon sx={{ fontSize: '1rem !important' }} />}
            sx={{
              fontFamily: '"MonoLisa", "MonoLisa Fallback", monospace',
              fontSize: '0.85rem',
              height: 32,
              bgcolor: '#f3f4f6',
              border: '1px solid #3776AB',
              color: '#374151',
              cursor: 'pointer',
              '&:hover': { bgcolor: '#e5e7eb' },
              '& .MuiChip-deleteIcon': {
                color: '#9ca3af',
                '&:hover': { color: '#3776AB' },
              },
              ...(animationClass === 'chip-blur-out' && {
                animation: 'chip-roll-out 0.5s ease-in forwards',
              }),
              ...(animationClass === 'chip-blur-in' && {
                animation: 'chip-roll-in 0.5s ease-out forwards',
              }),
              '@keyframes chip-roll-out': {
                '0%': { transform: 'perspective(200px) rotateX(0deg)' },
                '100%': { transform: 'perspective(200px) rotateX(180deg)' },
              },
              '@keyframes chip-roll-in': {
                '0%': { transform: 'perspective(200px) rotateX(180deg)' },
                '100%': { transform: 'perspective(200px) rotateX(360deg)' },
              },
            }}
          />
        );
      })}

      {/* Search input - collapsed icon or expanded input */}
      {!maxFiltersReached && (
        <Box
          ref={searchContainerRef}
          onClick={handleSearchExpand}
          sx={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: 0.5,
            px: isSearchExpanded ? 1.5 : 0,
            height: 32,
            width: isSearchExpanded ? { xs: 80, sm: 160, md: 'auto' } : 32,
            minWidth: isSearchExpanded ? { xs: 80, sm: 160, md: 120 } : 32,
            border: isSearchExpanded ? '1px dashed #9ca3af' : 'none',
            borderRadius: '16px',
            bgcolor: isDropdownOpen ? '#f9fafb' : 'transparent',
            cursor: 'pointer',
            transition: 'all 0.2s ease',
            '&:hover': {
              borderColor: isSearchExpanded ? '#3776AB' : undefined,
              bgcolor: isSearchExpanded ? '#f9fafb' : undefined,
            },
            '&:hover .search-icon': {
              color: '#3776AB',
            },
          }}
        >
          <Tooltip title={isSearchExpanded ? '' : 'search'}>
            <SearchIcon
              className="search-icon"
              sx={{
                color: '#9ca3af',
                fontSize: isSearchExpanded ? '1rem' : '1.25rem',
                transition: 'all 0.2s ease',
                flexShrink: 0,
              }}
            />
          </Tooltip>
          <InputBase
            inputRef={inputRef}
            id="filter-search"
            name="filter-search"
            placeholder={selectedCategory ? FILTER_LABELS[selectedCategory] : ''}
            value={searchQuery}
            onChange={(e) => {
              setSearchQuery(e.target.value);
              if (!dropdownAnchor) {
                setDropdownAnchor(searchContainerRef.current);
              }
            }}
            onFocus={() => {
              if (!isSearchManuallyExpanded && activeFilters.length > 0) {
                setIsSearchManuallyExpanded(true);
              }
              setDropdownAnchor(searchContainerRef.current);
            }}
            onBlur={handleSearchBlur}
            onKeyDown={handleKeyDown}
            sx={{
              flex: isSearchExpanded ? 1 : 0,
              width: isSearchExpanded ? 'auto' : 0,
              opacity: isSearchExpanded ? 1 : 0,
              transition: 'all 0.2s ease',
              fontFamily: '"MonoLisa", "MonoLisa Fallback", monospace',
              fontSize: '0.85rem',
              '& input': {
                padding: 0,
                '&::placeholder': {
                  color: '#9ca3af',
                  opacity: 1,
                },
              },
            }}
          />
          {isSearchExpanded && (searchQuery || selectedCategory) && (
            <CloseIcon
              onClick={(e) => {
                e.stopPropagation();
                setSearchQuery('');
                setSelectedCategory(null);
              }}
              sx={{
                color: '#9ca3af',
                fontSize: '0.9rem',
                cursor: 'pointer',
                '&:hover': { color: '#6b7280' },
              }}
            />
          )}
        </Box>
      )}
      </Box>

      {/* Counter and toggle row (mobile only) */}
      {isMobile && (
        <Box
          sx={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            mt: 1,
          }}
        >
          {currentTotal > 0 ? (
            <Typography
              sx={{
                fontFamily: '"MonoLisa", "MonoLisa Fallback", monospace',
                fontSize: '0.75rem',
                color: '#9ca3af',
                whiteSpace: 'nowrap',
              }}
            >
              {scrollPercent}% · {currentTotal}
            </Typography>
          ) : (
            <Box />
          )}
          <Tooltip title={imageSize === 'normal' ? 'compact view' : 'normal view'}>
            <Box
              onClick={() => onImageSizeChange(imageSize === 'normal' ? 'compact' : 'normal')}
              sx={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                width: 32,
                height: 32,
                cursor: 'pointer',
                color: '#9ca3af',
                '&:hover': { color: '#3776AB' },
              }}
            >
              {imageSize === 'normal' ? (
                <ViewAgendaIcon sx={{ fontSize: '1.25rem' }} />
              ) : (
                <ViewModuleIcon sx={{ fontSize: '1.25rem' }} />
              )}
            </Box>
          </Tooltip>
        </Box>
      )}

      {/* Dropdown menu */}
      <Menu
        anchorEl={dropdownAnchor}
        open={isDropdownOpen}
        onClose={handleDropdownClose}
        autoFocus={false}
        disableAutoFocus
        disableRestoreFocus
        disableEnforceFocus
        PaperProps={{
          sx: {
            maxHeight: 350,
            minWidth: 240,
            mt: 0.5,
          },
        }}
        slotProps={{
          root: {
            slotProps: {
              backdrop: {
                invisible: true,
              },
            },
          },
        }}
      >
        {!selectedCategory && !hasQuery
          ? // Show categories
            FILTER_CATEGORIES.map((category) => {
              const availableVals = getAvailableValues(filterCounts, activeFilters, category);
              if (availableVals.length === 0) return null;
              // Calculate actual index among visible items
              const visibleIdx = dropdownItems.findIndex((item) => item.type === 'category' && item.category === category);
              return (
                <MenuItem
                  key={category}
                  onClick={() => handleCategorySelect(category)}
                  selected={visibleIdx === highlightedIndex}
                  sx={{ fontFamily: '"MonoLisa", "MonoLisa Fallback", monospace' }}
                >
                  <ListItemText
                    primary={FILTER_LABELS[category]}
                    secondary={`${availableVals.length} options`}
                    primaryTypographyProps={{
                      fontFamily: '"MonoLisa", "MonoLisa Fallback", monospace',
                      fontSize: '0.9rem',
                    }}
                    secondaryTypographyProps={{
                      fontFamily: '"MonoLisa", "MonoLisa Fallback", monospace',
                      fontSize: '0.75rem',
                      color: '#9ca3af',
                    }}
                  />
                </MenuItem>
              );
            })
          : // Show search results or category values
            [
              ...(selectedCategory
                ? [
                    <MenuItem
                      key="back"
                      onClick={() => {
                        setSelectedCategory(null);
                        setSearchQuery('');
                      }}
                      sx={{ fontFamily: '"MonoLisa", "MonoLisa Fallback", monospace', color: '#6b7280' }}
                    >
                      &larr; {FILTER_LABELS[selectedCategory]}
                    </MenuItem>,
                    <Divider key="divider" />,
                  ]
                : []),
              ...(searchResults.length > 0
                ? searchResults.map(({ category, value, count }, idx) => (
                    <MenuItem
                      key={`${category}-${value}`}
                      onClick={() => handleValueSelect(category, value)}
                      selected={idx === highlightedIndex}
                      sx={{ fontFamily: '"MonoLisa", "MonoLisa Fallback", monospace' }}
                    >
                      <ListItemText
                        primary={value}
                        secondary={!selectedCategory ? FILTER_LABELS[category] : undefined}
                        primaryTypographyProps={{
                          fontFamily: '"MonoLisa", "MonoLisa Fallback", monospace',
                          fontSize: '0.85rem',
                        }}
                        secondaryTypographyProps={{
                          fontFamily: '"MonoLisa", "MonoLisa Fallback", monospace',
                          fontSize: '0.7rem',
                          color: '#9ca3af',
                        }}
                      />
                      <Typography
                        sx={{
                          fontFamily: '"MonoLisa", "MonoLisa Fallback", monospace',
                          fontSize: '0.75rem',
                          color: '#9ca3af',
                          ml: 2,
                        }}
                      >
                        ({count})
                      </Typography>
                    </MenuItem>
                  ))
                : [
                    <MenuItem key="no-results" disabled>
                      <Typography
                        sx={{
                          fontFamily: '"MonoLisa", "MonoLisa Fallback", monospace',
                          fontSize: '0.85rem',
                          color: '#9ca3af',
                        }}
                      >
                        no matches
                      </Typography>
                    </MenuItem>,
                  ]),
            ]}
      </Menu>

      {/* Chip action menu */}
      <Menu
        anchorEl={chipMenuAnchor}
        open={Boolean(chipMenuAnchor)}
        onClose={() => {
          setChipMenuAnchor(null);
          setActiveGroupIndex(null);
        }}
        PaperProps={{
          sx: {
            minWidth: 180,
            maxHeight: 350,
          },
        }}
      >
        {activeGroup && [
          // Add value (OR) - submenu with available values
          ...(availableValuesForActiveGroup.length > 0
            ? [
                <Typography
                  key="add-or-header"
                  sx={{
                    px: 2,
                    py: 0.5,
                    fontSize: '0.7rem',
                    color: '#9ca3af',
                    fontFamily: '"MonoLisa", "MonoLisa Fallback", monospace',
                    textTransform: 'uppercase',
                  }}
                >
                  add (or)
                </Typography>,
                ...availableValuesForActiveGroup.map(([value, count]) => (
                  <MenuItem
                    key={`add-${value}`}
                    onClick={() => handleAddValueToExistingGroup(value)}
                    sx={{ fontFamily: '"MonoLisa", "MonoLisa Fallback", monospace', py: 0.5 }}
                  >
                    <AddIcon fontSize="small" sx={{ mr: 1, color: '#22c55e', fontSize: '1rem' }} />
                    <Typography sx={{ fontSize: '0.85rem', flex: 1 }}>{value}</Typography>
                    <Typography sx={{ fontSize: '0.75rem', color: '#9ca3af' }}>({count})</Typography>
                  </MenuItem>
                )),
                <Divider key="divider-add" />,
              ]
            : []),
          // Remove individual values
          ...activeGroup.values.map((value) => (
            <MenuItem
              key={`remove-${value}`}
              onClick={() => handleRemoveValue(value)}
              sx={{ fontFamily: '"MonoLisa", "MonoLisa Fallback", monospace' }}
            >
              <CloseIcon fontSize="small" sx={{ mr: 1, color: '#ef4444' }} />
              {value}
            </MenuItem>
          )),
          // Remove all (only if more than 1 value)
          ...(activeGroup.values.length > 1
            ? [
                <Divider key="divider-remove" />,
                <MenuItem
                  key="remove-all"
                  onClick={handleRemoveGroup}
                  sx={{ fontFamily: '"MonoLisa", "MonoLisa Fallback", monospace', color: '#ef4444' }}
                >
                  <CloseIcon fontSize="small" sx={{ mr: 1 }} />
                  remove all
                </MenuItem>,
              ]
            : []),
        ]}
      </Menu>
    </Box>
  );
}
