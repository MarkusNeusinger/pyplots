import { useState, useCallback, useRef, useEffect } from 'react';
import Box from '@mui/material/Box';
import Chip from '@mui/material/Chip';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import ListItemText from '@mui/material/ListItemText';
import Typography from '@mui/material/Typography';
import InputBase from '@mui/material/InputBase';
import Divider from '@mui/material/Divider';
import CloseIcon from '@mui/icons-material/Close';
import SearchIcon from '@mui/icons-material/Search';
import AddIcon from '@mui/icons-material/Add';

import type { FilterCategory, ActiveFilters, FilterCounts } from '../types';
import { FILTER_LABELS, FILTER_CATEGORIES } from '../types';

interface FilterBarProps {
  activeFilters: ActiveFilters;
  filterCounts: FilterCounts | null;  // Contextual counts (for AND additions)
  orCounts: Record<string, number>[];  // Per-group counts for OR additions
  currentTotal: number;  // Current number of displayed images
  randomAnimation: { index: number; phase: 'out' | 'in'; oldLabel?: string } | null;
  searchInputRef?: React.RefObject<HTMLInputElement | null>;
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
  randomAnimation,
  searchInputRef,
  onAddFilter,
  onAddValueToGroup,
  onRemoveFilter,
  onRemoveGroup,
  onTrackEvent,
}: FilterBarProps) {
  // Search/dropdown state
  const [searchQuery, setSearchQuery] = useState('');
  const [dropdownAnchor, setDropdownAnchor] = useState<HTMLElement | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<FilterCategory | null>(null);
  const searchContainerRef = useRef<HTMLDivElement>(null);
  const localInputRef = useRef<HTMLInputElement>(null);
  const inputRef = searchInputRef || localInputRef;

  // Chip menu state
  const [chipMenuAnchor, setChipMenuAnchor] = useState<HTMLElement | null>(null);
  const [activeGroupIndex, setActiveGroupIndex] = useState<number | null>(null);

  // Dropdown keyboard navigation
  const [highlightedIndex, setHighlightedIndex] = useState<number>(-1);

  // Open dropdown
  const handleSearchFocus = useCallback(() => {
    setDropdownAnchor(searchContainerRef.current);
  }, []);

  const handleSearchClick = useCallback(() => {
    setDropdownAnchor(searchContainerRef.current);
    setTimeout(() => inputRef.current?.focus(), 0);
  }, []);

  // Close dropdown
  const handleDropdownClose = useCallback(() => {
    setDropdownAnchor(null);
    setSelectedCategory(null);
    setSearchQuery('');
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
      onTrackEvent('filter_add', { category, value });
      setDropdownAnchor(null);
      setSelectedCategory(null);
      setSearchQuery('');
      // Focus search input for next filter
      setTimeout(() => inputRef.current?.focus(), 100);
    },
    [onAddFilter, onTrackEvent]
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
        const group = activeFilters[activeGroupIndex];
        onRemoveFilter(activeGroupIndex, value);
        onTrackEvent('filter_remove', { category: group?.category || '', value });
      }
      setChipMenuAnchor(null);
      setActiveGroupIndex(null);
    },
    [activeGroupIndex, activeFilters, onRemoveFilter, onTrackEvent]
  );

  // Remove entire group
  const handleRemoveGroup = useCallback(() => {
    if (activeGroupIndex !== null) {
      const group = activeFilters[activeGroupIndex];
      onRemoveGroup(activeGroupIndex);
      onTrackEvent('filter_remove_group', { category: group?.category || '' });
    }
    setChipMenuAnchor(null);
    setActiveGroupIndex(null);
  }, [activeGroupIndex, activeFilters, onRemoveGroup, onTrackEvent]);

  // Add value to existing group (OR)
  const handleAddValueToExistingGroup = useCallback(
    (value: string) => {
      if (activeGroupIndex !== null) {
        const group = activeFilters[activeGroupIndex];
        onAddValueToGroup(activeGroupIndex, value);
        onTrackEvent('filter_add_or', { category: group?.category || '', value });
      }
      setChipMenuAnchor(null);
      setActiveGroupIndex(null);
    },
    [activeGroupIndex, activeFilters, onAddValueToGroup, onTrackEvent]
  );

  // Get counts for a category
  const getCounts = (category: FilterCategory): Record<string, number> => {
    return filterCounts?.[category] || {};
  };

  // Get all selected values across all groups for a category
  const getSelectedValuesForCategory = (category: FilterCategory): string[] => {
    return activeFilters
      .filter((f) => f.category === category)
      .flatMap((f) => f.values);
  };

  // Get available values for a category (not already selected in any group)
  const getAvailableValues = (category: FilterCategory): [string, number][] => {
    const counts = getCounts(category);
    const selected = getSelectedValuesForCategory(category);
    return Object.entries(counts)
      .filter(([value]) => !selected.includes(value))
      .sort((a, b) => b[1] - a[1]);
  };

  // Get available values for adding to a specific group (OR - not in that group)
  // Uses orCounts which has counts with all OTHER filters applied
  // Preview = currentTotal + orCounts[groupIndex][value]
  const getAvailableValuesForGroup = (groupIndex: number): [string, number][] => {
    const group = activeFilters[groupIndex];
    if (!group) return [];

    // orCounts[groupIndex] contains counts for each value with other filters applied
    const groupOrCounts = orCounts[groupIndex] || {};

    return Object.entries(groupOrCounts)
      .filter(([value]) => !group.values.includes(value))
      .map(([value, count]) => [value, currentTotal + count] as [string, number])
      .sort((a, b) => b[1] - a[1]);
  };

  // Search across all categories
  const getSearchResults = (): { category: FilterCategory; value: string; count: number }[] => {
    if (!filterCounts) return [];

    const query = searchQuery.toLowerCase().trim();
    const results: { category: FilterCategory; value: string; count: number }[] = [];

    const categoriesToSearch = selectedCategory ? [selectedCategory] : FILTER_CATEGORIES;

    for (const category of categoriesToSearch) {
      const counts = getCounts(category);
      const selected = getSelectedValuesForCategory(category);

      for (const [value, count] of Object.entries(counts)) {
        if (selected.includes(value)) continue;
        if (query && !value.toLowerCase().includes(query)) continue;
        results.push({ category, value, count });
      }
    }

    return results.sort((a, b) => b.count - a.count).slice(0, 15);
  };

  const searchResults = getSearchResults();
  const isDropdownOpen = Boolean(dropdownAnchor);
  const hasQuery = searchQuery.trim().length > 0;
  const maxFiltersReached = activeFilters.length >= 5;

  // Get dropdown items for keyboard navigation
  const getDropdownItems = useCallback(() => {
    if (!selectedCategory && !hasQuery) {
      // Categories list
      return FILTER_CATEGORIES
        .filter((cat) => {
          const availableValues = filterCounts?.[cat] ? Object.keys(filterCounts[cat]).filter((v) => !activeFilters.some((f) => f.category === cat && f.values.includes(v))) : [];
          return availableValues.length > 0;
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
  const availableValuesForActiveGroup = activeGroupIndex !== null ? getAvailableValuesForGroup(activeGroupIndex) : [];

  return (
    <Box sx={{ mb: 4, px: 2 }}>
      {/* Filter chips row */}
      <Box
        sx={{
          display: 'flex',
          flexWrap: 'wrap',
          gap: 1,
          justifyContent: 'center',
          alignItems: 'center',
        }}
      >
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
            sx={{
              fontFamily: '"JetBrains Mono", monospace',
              fontSize: '0.85rem',
              height: 32,
              bgcolor: '#f3f4f6',
              border: '1px solid #3776AB',
              color: '#374151',
              cursor: 'pointer',
              '&:hover': { bgcolor: '#e5e7eb' },
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

      {/* Search input - hidden when max 5 filters reached */}
      {!maxFiltersReached && (
        <Box
          ref={searchContainerRef}
          onClick={handleSearchClick}
          sx={{
            display: 'flex',
            alignItems: 'center',
            gap: 0.5,
            px: 1.5,
            height: 32,
            border: '1px dashed #9ca3af',
            borderRadius: '16px',
            bgcolor: isDropdownOpen ? '#f9fafb' : 'transparent',
            cursor: 'text',
            minWidth: 100,
            '&:hover': {
              borderColor: '#3776AB',
              bgcolor: '#f9fafb',
            },
          }}
        >
          <SearchIcon sx={{ color: '#9ca3af', fontSize: '1rem' }} />
          <InputBase
            inputRef={inputRef}
            placeholder={selectedCategory ? FILTER_LABELS[selectedCategory] : ''}
            value={searchQuery}
            onChange={(e) => {
              setSearchQuery(e.target.value);
              if (!dropdownAnchor) {
                setDropdownAnchor(searchContainerRef.current);
              }
            }}
            onFocus={handleSearchFocus}
            onKeyDown={handleKeyDown}
            sx={{
              flex: 1,
              fontFamily: '"JetBrains Mono", monospace',
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
          {(searchQuery || selectedCategory) && (
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
              const availableValues = getAvailableValues(category);
              if (availableValues.length === 0) return null;
              // Calculate actual index among visible items
              const visibleIdx = dropdownItems.findIndex((item) => item.type === 'category' && item.category === category);
              return (
                <MenuItem
                  key={category}
                  onClick={() => handleCategorySelect(category)}
                  selected={visibleIdx === highlightedIndex}
                  sx={{ fontFamily: '"JetBrains Mono", monospace' }}
                >
                  <ListItemText
                    primary={FILTER_LABELS[category]}
                    secondary={`${availableValues.length} options`}
                    primaryTypographyProps={{
                      fontFamily: '"JetBrains Mono", monospace',
                      fontSize: '0.9rem',
                    }}
                    secondaryTypographyProps={{
                      fontFamily: '"JetBrains Mono", monospace',
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
                      sx={{ fontFamily: '"JetBrains Mono", monospace', color: '#6b7280' }}
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
                      sx={{ fontFamily: '"JetBrains Mono", monospace' }}
                    >
                      <ListItemText
                        primary={value}
                        secondary={!selectedCategory ? FILTER_LABELS[category] : undefined}
                        primaryTypographyProps={{
                          fontFamily: '"JetBrains Mono", monospace',
                          fontSize: '0.85rem',
                        }}
                        secondaryTypographyProps={{
                          fontFamily: '"JetBrains Mono", monospace',
                          fontSize: '0.7rem',
                          color: '#9ca3af',
                        }}
                      />
                      <Typography
                        sx={{
                          fontFamily: '"JetBrains Mono", monospace',
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
                          fontFamily: '"JetBrains Mono", monospace',
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
                    fontFamily: '"JetBrains Mono", monospace',
                    textTransform: 'uppercase',
                  }}
                >
                  add (or)
                </Typography>,
                ...availableValuesForActiveGroup.slice(0, 5).map(([value, count]) => (
                  <MenuItem
                    key={`add-${value}`}
                    onClick={() => handleAddValueToExistingGroup(value)}
                    sx={{ fontFamily: '"JetBrains Mono", monospace', py: 0.5 }}
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
              sx={{ fontFamily: '"JetBrains Mono", monospace' }}
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
                  sx={{ fontFamily: '"JetBrains Mono", monospace', color: '#ef4444' }}
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
