# Plausible Analytics Tracking

This document provides a comprehensive overview of Plausible Analytics implementation for pyplots.ai, including all tracked events, user interactions, and recommendations for improvement.

## Setup

**Location**: `app/index.html`

- Self-hosted Plausible script loaded via `/js/script.js`
- Custom endpoint: `/api/event` (proxied through nginx to avoid adblockers)
- Manual pageview tracking: `autoCapturePageviews: false`
- Production-only: Only tracks on `pyplots.ai` domain
- Privacy-focused: No cookies, GDPR-compliant

## Page Views

**Implementation**: Query parameters converted to URL path segments for better analytics segmentation.

### Filter-Based Pageviews

Filters create dynamic URLs with the following format:
```
https://pyplots.ai/{category}/{value}/{category}/{value}/...
```

**Ordered categories**: `lib`, `spec`, `plot`, `data`, `dom`, `feat`

**Examples**:
- `/?lib=matplotlib` → `https://pyplots.ai/lib/matplotlib`
- `/?lib=matplotlib&plot=scatter` → `https://pyplots.ai/lib/matplotlib/plot/scatter`
- `/?lib=matplotlib,seaborn` → `https://pyplots.ai/lib/matplotlib,seaborn` (OR logic)
- `/?lib=matplotlib&lib=seaborn` → `https://pyplots.ai/lib/matplotlib/lib/seaborn` (AND logic)

**Benefits**:
- Plausible shows popular filter combinations
- No manual event tracking needed for filter changes
- URL structure clearly shows user's browsing context

### Static Pages

| URL | Description |
|-----|-------------|
| `/` | Home page (no filters) |
| `/catalog` | Catalog page (alphabetical spec list) |
| `/{spec_id}` | Spec overview page (grid of all implementations) |
| `/{spec_id}/{library}` | Spec detail page (single library implementation) |
| `/interactive/{spec_id}/{library}` | Interactive fullscreen view (HTML plots) |

**Total pageview tracking**: Automated via `trackPageview()` in all pages

## Custom Events

### Navigation Events

| Event Name | Properties | Where | Description |
|------------|-----------|-------|-------------|
| `navigate_to_spec` | `spec`, `library` | HomePage | User clicks image card to view spec detail |
| `switch_library` | `spec`, `library` | SpecPage | User switches library via pills in detail view |
| `select_implementation` | `spec`, `library` | SpecPage | User clicks implementation card in overview mode |
| `back_to_overview` | `spec`, `library` | SpecPage | User clicks main image to return to overview |
| `catalog_rotate` | `spec` | CatalogPage | User clicks image in catalog to rotate library |

### Code Interaction Events

| Event Name | Properties | Where | Description |
|------------|-----------|-------|-------------|
| `copy_code` | `spec`, `library`, `method` | Multiple | User copies code to clipboard |

**Copy methods**:
- `card`: Quick copy button on image card (home/grid)
- `image`: Copy button on main image (spec detail page)
- `tab`: Copy button in Code tab

### Filter & Search Events

| Event Name | Properties | Where | Description |
|------------|-----------|-------|-------------|
| `search` | `query`, `category` | FilterBar | User searches and selects value |
| `search_no_results` | `query` | FilterBar | Search query returns no results (debounced 500ms) |
| `random` | `category`, `value`, `method` | HomePage | User triggers random filter |

**Random methods**:
- `click`: Shuffle icon clicked
- `space`: Spacebar pressed
- `doubletap`: Mobile double-tap gesture

### Tab Interaction Events

| Event Name | Properties | Where | Description |
|------------|-----------|-------|-------------|
| `tab_click` | `tab`, `library` | SpecTabs | User opens a tab |
| `tab_collapse` | `library` | SpecTabs | User closes currently open tab |

**Tab names**: `code`, `specification`, `implementation`, `quality`

### External Link Events

| Event Name | Properties | Where | Description |
|------------|-----------|-------|-------------|
| `external_link` | `destination`, `spec`, `library` | Footer | User clicks external link in footer |
| `open_interactive` | `spec`, `library` | SpecPage | User opens interactive HTML view |

**Destinations**: `linkedin`, `github`, `stats`

## User Interactions Overview

### On Home Page

**What users can do:**
1. ✅ **Browse plots** - Infinite scroll through grid
2. ✅ **Filter by category** - Search and select filters (tracked via pageview)
3. ✅ **Search** - Type to find specific plots/libraries (tracked if selected or no results)
4. ✅ **Random filter** - Shuffle icon, spacebar, or double-tap
5. ✅ **Copy code** - Quick copy from card
6. ✅ **View spec** - Click card to navigate
7. ✅ **Toggle grid size** - Normal vs compact view (NOT TRACKED)
8. ✅ **View catalog** - Click catalog icon (tracked via pageview)
9. ✅ **Click external links** - Footer links

### On Catalog Page

**What users can do:**
1. ✅ **Browse specs** - Alphabetical list
2. ✅ **Rotate libraries** - Click image to cycle implementations
3. ✅ **Navigate to spec** - Click title/description
4. ✅ **Expand descriptions** - Click to read full text (NOT TRACKED)
5. ✅ **Scroll** - Scroll-to-top button (NOT TRACKED)

### On Spec Overview Page (`/{spec_id}`)

**What users can do:**
1. ✅ **View all implementations** - Grid of library implementations
2. ✅ **Navigate to detail** - Click card to view single library
3. ✅ **Copy code** - Quick copy from card
4. ✅ **Download image** - Download PNG (NOT TRACKED)
5. ✅ **Open interactive** - View HTML plot fullscreen
6. ✅ **View library info** - Tooltip with description/docs (NOT TRACKED)
7. ✅ **View quality score** - Displayed below card (NOT TRACKED)
8. ✅ **Read spec tabs** - Spec info only (overview mode)

### On Spec Detail Page (`/{spec_id}/{library}`)

**What users can do:**
1. ✅ **View implementation** - Large image display
2. ✅ **Switch library** - Pills to change library
3. ✅ **Back to overview** - Click image
4. ✅ **Copy code** - From image or Code tab
5. ✅ **Download image** - Download PNG (NOT TRACKED)
6. ✅ **Open interactive** - View HTML plot fullscreen
7. ✅ **Browse tabs** - Code, Spec, Impl, Quality
8. ✅ **Expand quality criteria** - View detailed breakdown (NOT TRACKED)

### On Interactive Page (`/interactive/{spec_id}/{library}`)

**What users can do:**
1. ✅ **Interact with plot** - Fullscreen HTML plot
2. ✅ **Navigate** - Breadcrumb navigation (tracked via pageview)
3. ✅ **View raw HTML** - Opens in new tab (NOT TRACKED)
4. ✅ **Close** - Returns to spec detail (tracked via pageview)

## Missing / Not Tracked

### Potentially Valuable Events

| Action | Where | Why Track? | Priority |
|--------|-------|-----------|----------|
| **Grid size toggle** | FilterBar | Understand user preference for compact vs normal | Medium |
| **Download image** | SpecPage | Measure plot reuse/export | High |
| **Tooltip open** | ImageCard | Measure interest in descriptions/docs | Low |
| **Description expand** | SpecPage/CatalogPage | Measure reading depth | Low |
| **Quality criteria expand** | SpecTabs | Measure interest in AI review details | Low |
| **View raw HTML** | InteractivePage | Measure advanced usage | Low |
| **Scroll-to-top** | HomePage/CatalogPage | UX metric (low value) | Very Low |

### Recommended to Add

#### High Priority

**1. Download tracking**
```typescript
// SpecPage.tsx - handleDownload
trackEvent('download_image', { spec: specId, library: impl.library_id });
```
**Value**: Understand which plots are being saved/reused. Key metric for platform utility.

**2. Grid size toggle**
```typescript
// FilterBar.tsx - Grid size toggle
trackEvent('toggle_grid_size', { size: newSize, previous: oldSize });
```
**Value**: Optimize default view based on user preference.

#### Medium Priority

**3. Library info tooltip opened**
```typescript
// ImageCard.tsx - onTooltipToggle
trackEvent('view_library_info', { library: image.library });
```
**Value**: Measure which libraries need better documentation/visibility.

**4. External link tracking improvement**
Add `source` property to distinguish where link was clicked:
```typescript
// Current: { destination: 'github', spec, library }
// Better:  { destination: 'github', spec, library, source: 'footer' }
```

## Event Naming Conventions

### Current Patterns

✅ **Good patterns**:
- Verb-object format: `navigate_to_spec`, `copy_code`, `switch_library`
- Consistent property names: `spec`, `library`, `method`
- Descriptive methods: `card`, `image`, `tab` for copy_code

✅ **Consistent usage**:
- All events use snake_case
- Properties always lowercase
- Clear action-oriented names

### Recommendations

**No changes needed!** Current naming is:
- ✅ Clear and descriptive
- ✅ Consistent snake_case
- ✅ Action-oriented verbs
- ✅ Unique and unambiguous
- ✅ Future-proof (easy to extend)

## Properties Standardization

### Current Properties

| Property | Type | Values | Usage |
|----------|------|--------|-------|
| `spec` | string | spec_id | Present in most events |
| `library` | string | library name | Present in most events |
| `method` | string | `card`, `image`, `tab`, `click`, `space`, `doubletap` | Context for copy/random |
| `category` | string | Filter category | Search/random events |
| `value` | string | Filter value | Random event |
| `query` | string | Search query text | Search events |
| `destination` | string | `linkedin`, `github`, `stats` | External links |
| `tab` | string | Tab name | Tab events |

**Consistency**: ✅ Excellent - all properties are well-defined and non-overlapping

## Potential Improvements

### 1. Add Engagement Metrics

**Time on tab**: Track how long users spend on each tab
```typescript
// Track tab open time
const tabOpenTime = useRef<number>(0);
useEffect(() => {
  if (tabIndex !== null) {
    tabOpenTime.current = Date.now();
    return () => {
      const duration = Math.round((Date.now() - tabOpenTime.current) / 1000);
      if (duration > 2) { // Only track if >2 seconds
        trackEvent('tab_view_duration', {
          tab: tabNames[tabIndex],
          library: libraryId,
          seconds: duration.toString()
        });
      }
    };
  }
}, [tabIndex]);
```

### 2. Track Filter Removal

Currently only filter **additions** trigger pageview changes. Track removals separately:
```typescript
// FilterBar.tsx
const handleRemoveFilter = (groupIndex: number, value: string) => {
  onRemoveFilter(groupIndex, value);
  trackEvent('filter_remove', {
    category: activeFilters[groupIndex].category,
    value
  });
};
```

### 3. Error Tracking

Track when things go wrong:
```typescript
// ImageCard.tsx - onError
trackEvent('image_load_error', { spec: image.spec_id, library: image.library });

// SpecPage.tsx - 404s
trackEvent('spec_not_found', { spec: specId });
```

### 4. Interaction Depth Metrics

**Scroll depth**: Already tracked via scroll percentage display, but not sent to Plausible
```typescript
// Send scroll milestones
const milestones = useRef(new Set<number>());
useEffect(() => {
  if ([25, 50, 75, 100].includes(scrollPercent) && !milestones.current.has(scrollPercent)) {
    milestones.current.add(scrollPercent);
    trackEvent('scroll_depth', { percent: scrollPercent.toString() });
  }
}, [scrollPercent]);
```

## Data Privacy

✅ **GDPR Compliant**:
- No cookies or local storage for tracking
- No personal data collected
- IP addresses anonymized by Plausible
- Users can opt-out via browser extensions

✅ **Transparent**:
- Public stats dashboard linked in footer
- Open-source tracking code
- Clear documentation (this file)

## Plausible Dashboard

**URL**: https://plausible.io/pyplots.ai

**Available metrics**:
- Pageviews by URL (including filter combinations)
- Custom event breakdown
- Geographic distribution
- Device/browser stats
- Referrer sources

## Summary

### What's Working Well

1. ✅ **Comprehensive pageview tracking** - Filter combinations as URL paths is elegant
2. ✅ **Clear event naming** - Consistent, descriptive, action-oriented
3. ✅ **Good property standardization** - No conflicts, clear semantics
4. ✅ **Privacy-focused** - No cookies, GDPR-compliant
5. ✅ **Production-only** - Clean development experience

### Quick Wins

1. **Add download tracking** (5 min)
2. **Add grid size toggle tracking** (2 min)
3. **Track filter removals** (5 min)

### Nice-to-Have

1. Track library info tooltip opens
2. Add scroll depth milestones
3. Track error events
4. Add tab view duration

### Not Worth Tracking

- Scroll-to-top button clicks
- Description expand/collapse
- Hover states
- Keyboard shortcuts (too noisy)
- Mouse movements (privacy concerns)

## Implementation Checklist

- [x] Plausible script loaded
- [x] Manual pageview tracking
- [x] Filter-based URL generation
- [x] Navigation events
- [x] Code copy events
- [x] Search events
- [x] Random filter events
- [x] Tab interaction events
- [x] External link events
- [ ] Download tracking (RECOMMENDED)
- [ ] Grid size toggle tracking (RECOMMENDED)
- [ ] Filter removal tracking (RECOMMENDED)
- [ ] Library info tooltip tracking (OPTIONAL)
- [ ] Error tracking (OPTIONAL)
- [ ] Scroll depth milestones (OPTIONAL)

## Code Locations

- **Plausible setup**: `app/index.html` (lines 59-68)
- **Analytics hook**: `app/src/hooks/useAnalytics.ts`
- **Pageview building**: `buildPlausibleUrl()` in useAnalytics.ts
- **Event tracking**: Passed via `onTrackEvent` prop throughout component tree

## Testing

**Development**: Tracking disabled (not on pyplots.ai domain)

**Production testing**:
1. Open https://pyplots.ai
2. Open browser console
3. Check for Plausible script load
4. Trigger events and verify in Plausible dashboard (may take 1-2 min)

**Debug mode**:
```javascript
// In browser console
window.plausible = function(...args) { console.log('Plausible:', args); };
```

---

**Last Updated**: 2026-01-05
**Status**: Production-ready, recommended improvements identified
