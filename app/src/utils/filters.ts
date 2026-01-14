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
 * Check if a value matches the search query.
 * Supports multi-word queries where all words must appear in the value.
 *
 * @param value - The filter value to check
 * @param query - The search query (already lowercased and trimmed)
 * @returns True if the value matches the query
 *
 * @example
 * matchesSearchQuery("scatter-basic", "scatter basic") // true
 * matchesSearchQuery("bar-grouped-horizontal", "bar horiz") // true
 * matchesSearchQuery("heatmap", "heat map") // true
 * matchesSearchQuery("scatter", "bar line") // false (not all words match)
 */
function matchesSearchQuery(value: string, query: string): boolean {
  if (!query) return true;

  const valueLower = value.toLowerCase();

  // Split query into individual words (by whitespace)
  const words = query.split(/\s+/).filter((w) => w.length > 0);

  // All words must appear somewhere in the value
  return words.every((word) => valueLower.includes(word));
}

/**
 * Calculate a relevance score for a search result.
 * Higher score = more relevant.
 *
 * @param value - The filter value
 * @param query - The search query (lowercased)
 * @returns Relevance score (higher is better)
 */
function calculateRelevance(value: string, query: string): number {
  const valueLower = value.toLowerCase();

  // Exact match: highest score
  if (valueLower === query) return 1000;

  // Starts with query: high score
  if (valueLower.startsWith(query)) return 500;

  // Contains query as substring: medium score
  if (valueLower.includes(query)) return 250;

  // Multi-word match: score based on how many words match at start
  const words = query.split(/\s+/);
  const matchingWordsAtStart = words.filter((word) => valueLower.startsWith(word)).length;
  if (matchingWordsAtStart > 0) return 100 + matchingWordsAtStart * 50;

  // All words match somewhere: base score
  return 10;
}

/**
 * Search across all filter categories.
 *
 * Supports multi-word queries where all words must match.
 * Words can appear anywhere in the value (not necessarily consecutive).
 * Results are sorted by relevance and then by count.
 *
 * @param filterCounts - Available filter counts
 * @param activeFilters - Current active filters
 * @param searchQuery - Search query string
 * @param selectedCategory - Optional category to limit search to
 * @returns Matching results sorted by relevance and count
 *
 * @example
 * // Query: "scatter basic" will match: scatter-basic, basic-scatter, scatter-basic-3d
 * // Query: "bar horiz" will match: bar-horizontal, bar-grouped-horizontal
 * // Results are ranked by relevance (exact match > starts with > contains > multi-word)
 */
export function getSearchResults(
  filterCounts: FilterCounts | null,
  activeFilters: ActiveFilters,
  searchQuery: string,
  selectedCategory: FilterCategory | null
): { category: FilterCategory; value: string; count: number }[] {
  if (!filterCounts) return [];

  const query = searchQuery.toLowerCase().trim();
  const results: Array<{ category: FilterCategory; value: string; count: number; relevance: number }> = [];

  const categoriesToSearch = selectedCategory ? [selectedCategory] : FILTER_CATEGORIES;

  for (const category of categoriesToSearch) {
    const counts = getCounts(filterCounts, category);
    const selected = getSelectedValuesForCategory(activeFilters, category);

    for (const [value, count] of Object.entries(counts)) {
      if (selected.includes(value)) continue;
      if (!matchesSearchQuery(value, query)) continue;

      const relevance = calculateRelevance(value, query);
      results.push({ category, value, count, relevance });
    }
  }

  // Sort by relevance (descending) then by count (descending)
  return results.sort((a, b) => {
    if (b.relevance !== a.relevance) {
      return b.relevance - a.relevance;
    }
    return b.count - a.count;
  });
}
