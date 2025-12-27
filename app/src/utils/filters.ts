/**
 * Filter utility functions for FilterBar component.
 *
 * Pure functions extracted for reusability and testing.
 */

import type { FilterCategory, ActiveFilters, FilterCounts } from '../types';
import { FILTER_CATEGORIES } from '../types';

/**
 * Get counts for a specific filter category.
 */
export function getCounts(
  filterCounts: FilterCounts | null,
  category: FilterCategory
): Record<string, number> {
  return filterCounts?.[category] || {};
}

/**
 * Get all selected values across all groups for a category.
 */
export function getSelectedValuesForCategory(
  activeFilters: ActiveFilters,
  category: FilterCategory
): string[] {
  return activeFilters
    .filter((f) => f.category === category)
    .flatMap((f) => f.values);
}

/**
 * Get available values for a category (not already selected in any group).
 *
 * @returns Array of [value, count] tuples sorted by count descending
 */
export function getAvailableValues(
  filterCounts: FilterCounts | null,
  activeFilters: ActiveFilters,
  category: FilterCategory
): [string, number][] {
  const counts = getCounts(filterCounts, category);
  const selected = getSelectedValuesForCategory(activeFilters, category);

  return Object.entries(counts)
    .filter(([value]) => !selected.includes(value))
    .sort((a, b) => b[1] - a[1]);
}

/**
 * Get available values for adding to a specific group (OR operation).
 * Uses orCounts which has counts with all OTHER filters applied.
 *
 * @param groupIndex - Index of the filter group
 * @param activeFilters - Current active filters
 * @param orCounts - Per-group OR counts from API
 * @param currentTotal - Current total number of images
 * @returns Array of [value, previewCount] tuples
 */
export function getAvailableValuesForGroup(
  groupIndex: number,
  activeFilters: ActiveFilters,
  orCounts: Record<string, number>[],
  currentTotal: number
): [string, number][] {
  const group = activeFilters[groupIndex];
  if (!group) return [];

  const groupOrCounts = orCounts[groupIndex] || {};

  return Object.entries(groupOrCounts)
    .filter(([value]) => !group.values.includes(value))
    .map(([value, count]) => [value, currentTotal + count] as [string, number])
    .sort((a, b) => b[1] - a[1]);
}

/**
 * Search across all filter categories.
 *
 * @param filterCounts - Available filter counts
 * @param activeFilters - Current active filters
 * @param searchQuery - Search query string
 * @param selectedCategory - Optional category to limit search to
 * @returns Matching results sorted by count
 */
export function getSearchResults(
  filterCounts: FilterCounts | null,
  activeFilters: ActiveFilters,
  searchQuery: string,
  selectedCategory: FilterCategory | null
): { category: FilterCategory; value: string; count: number }[] {
  if (!filterCounts) return [];

  const query = searchQuery.toLowerCase().trim();
  const results: { category: FilterCategory; value: string; count: number }[] = [];

  const categoriesToSearch = selectedCategory ? [selectedCategory] : FILTER_CATEGORIES;

  for (const category of categoriesToSearch) {
    const counts = getCounts(filterCounts, category);
    const selected = getSelectedValuesForCategory(activeFilters, category);

    for (const [value, count] of Object.entries(counts)) {
      if (selected.includes(value)) continue;
      if (query && !value.toLowerCase().includes(query)) continue;
      results.push({ category, value, count });
    }
  }

  return results.sort((a, b) => b.count - a.count);
}
