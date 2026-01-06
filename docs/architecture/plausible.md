# Plausible Analytics Tracking

This document provides a comprehensive overview of Plausible Analytics implementation for pyplots.ai, including all tracked events, user interactions, and the required Plausible dashboard configuration.

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
| `copy_code` | `spec`, `library`, `method`, `page` | Multiple | User copies code to clipboard |
| `download_image` | `spec`, `library`, `page` | SpecPage | User downloads PNG image |

**Copy methods**:
- `card`: Quick copy button on image card (home grid)
- `image`: Copy button on main image (spec page)
- `tab`: Copy button in Code tab

**Page values** (for user journey tracking):
- `home`: HomePage grid view
- `spec_overview`: SpecPage showing all library implementations
- `spec_detail`: SpecPage showing single library implementation

### Filter & Search Events

| Event Name | Properties | Where | Description |
|------------|-----------|-------|-------------|
| `search` | `query`, `category` | FilterBar | User searches and selects value |
| `search_no_results` | `query` | FilterBar | Search query returns no results (debounced 200ms) |
| `random` | `category`, `value`, `method` | HomePage | User triggers random filter |
| `filter_remove` | `category`, `value` | HomePage | User removes a filter |
| `toggle_grid_size` | `size` | FilterBar | User toggles between normal/compact view |

**Random methods**:
- `click`: Shuffle icon clicked
- `space`: Spacebar pressed
- `doubletap`: Mobile double-tap gesture

**Grid sizes**:
- `normal`: Larger cards (1-3 columns)
- `compact`: Smaller cards (2-6 columns)

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

---

## Server-Side og:image Tracking

Social media bots (Twitter, WhatsApp, Teams, etc.) don't execute JavaScript, so og:image requests can only be tracked server-side.

### Architecture

All og:images are routed through the API for tracking:

```
Bot requests page → nginx detects bot → SEO proxy serves HTML with og:image URL
                                                            ↓
                                          https://api.pyplots.ai/og/{endpoint}.png
                                                            ↓
                                          track_og_image() → Plausible Events API
                                                            ↓
                                          Return image (fire-and-forget tracking)
```

**Implementation**: `api/analytics.py` (server-side Plausible tracking)

### og:image Event

| Event Name | Properties | Description |
|------------|------------|-------------|
| `og_image_view` | `page`, `platform`, `spec`?, `library`?, `filter_*`? | Bot requested og:image |

### Properties

| Property | Values | Description |
|----------|--------|-------------|
| `page` | `home`, `catalog`, `spec_overview`, `spec_detail` | Page type |
| `platform` | See list below | Detected platform from User-Agent |
| `spec` | Specification ID | Only for spec pages |
| `library` | Library ID | Only for detail pages |
| `filter_*` | Filter value | Dynamic props for filtered URLs (e.g., `filter_lib`, `filter_dom`) |

### Platform Detection (27 platforms)

**Social Media**: twitter, facebook, linkedin, pinterest, reddit, tumblr, mastodon

**Messaging Apps**: slack, discord, telegram, whatsapp, signal, viber, skype, teams, snapchat

**Search Engines**: google, bing, yandex, duckduckgo, baidu, apple

**Link Preview Services**: embedly, quora, outbrain, rogerbot, showyoubot

**Fallback**: unknown

### API Endpoints

| Endpoint | Description | Tracking |
|----------|-------------|----------|
| `/og/home.png` | Static og:image for home page | `page=home`, `filter_*` from query params |
| `/og/catalog.png` | Static og:image for catalog | `page=catalog` |
| `/og/{spec_id}.png` | Collage og:image for spec overview | `page=spec_overview`, `spec` |
| `/og/{spec_id}/{library}.png` | Branded og:image for implementation | `page=spec_detail`, `spec`, `library` |

### Filter Tracking for Shared URLs

When users share filtered URLs (e.g., `https://pyplots.ai/?lib=plotly&dom=statistics`), the filters are passed to the og:image endpoint:

```
og:image URL: https://api.pyplots.ai/og/home.png?lib=plotly,matplotlib&dom=statistics
                                                  ↓
Tracked props: { page: "home", platform: "twitter", filter_lib: "plotly,matplotlib", filter_dom: "statistics" }
```

**Note**: Each filter category becomes a separate prop (`filter_lib`, `filter_dom`, etc.) to handle comma-separated values.

---

## Plausible Dashboard Configuration

### Required Custom Properties

To see event properties in Plausible dashboard, you **MUST** register them as custom properties.

**Go to**: Plausible Dashboard → Site Settings → Custom Properties → Add Property

#### Properties to Register

| Property | Description | Used By Events |
|----------|-------------|----------------|
| `spec` | Plot specification ID | `copy_code`, `download_image`, `navigate_to_spec`, `switch_library`, `select_implementation`, `back_to_overview`, `catalog_rotate`, `external_link`, `open_interactive`, `og_image_view` |
| `library` | Library name (matplotlib, seaborn, etc.) | `copy_code`, `download_image`, `navigate_to_spec`, `switch_library`, `select_implementation`, `back_to_overview`, `external_link`, `open_interactive`, `tab_click`, `tab_collapse`, `og_image_view` |
| `method` | Action method (card, image, tab, click, space, doubletap) | `copy_code`, `random` |
| `page` | Page context (home, catalog, spec_overview, spec_detail) | `copy_code`, `download_image`, `og_image_view` |
| `platform` | Bot/platform name (twitter, whatsapp, teams, etc.) | `og_image_view` |
| `category` | Filter category (lib, plot, dom, feat, data, spec) | `search`, `random`, `filter_remove` |
| `value` | Filter value | `random`, `filter_remove` |
| `query` | Search query text | `search`, `search_no_results` |
| `destination` | External link target (linkedin, github, stats) | `external_link` |
| `tab` | Tab name (code, specification, implementation, quality) | `tab_click` |
| `size` | Grid size (normal, compact) | `toggle_grid_size` |
| `filter_lib` | Library filter value (for og:image) | `og_image_view` |
| `filter_dom` | Domain filter value (for og:image) | `og_image_view` |
| `filter_plot` | Plot type filter value (for og:image) | `og_image_view` |
| `filter_feat` | Features filter value (for og:image) | `og_image_view` |
| `filter_data` | Data type filter value (for og:image) | `og_image_view` |

### Goals Configuration

**Go to**: Plausible Dashboard → Site Settings → Goals → Add Goal

#### Recommended Goals

| Goal Name | Type | Description |
|-----------|------|-------------|
| `copy_code` | Custom Event | Track code copies (primary conversion) |
| `download_image` | Custom Event | Track image downloads |
| `navigate_to_spec` | Custom Event | Track spec navigation |
| `search` | Custom Event | Track successful searches |
| `search_no_results` | Custom Event | Track failed searches (content gaps) |
| `random` | Custom Event | Track random filter usage |
| `filter_remove` | Custom Event | Track filter removal |
| `toggle_grid_size` | Custom Event | Track view preference |
| `external_link` | Custom Event | Track outbound clicks |
| `open_interactive` | Custom Event | Track interactive mode usage |
| `tab_click` | Custom Event | Track tab interactions |
| `og_image_view` | Custom Event | Track og:image requests from social media bots |

### Funnels (Optional)

**Example funnel**: Home → Spec → Copy

1. Pageview `/` (home)
2. `navigate_to_spec` event
3. `copy_code` event

### Dashboard Widgets

Recommended custom widgets:

1. **Top Specs Copied**: `copy_code` breakdown by `spec`
2. **Popular Libraries**: `copy_code` breakdown by `library`
3. **Copy Journey**: `copy_code` breakdown by `page`
4. **Search Terms**: `search` breakdown by `query`
5. **Missing Content**: `search_no_results` breakdown by `query`
6. **View Preference**: `toggle_grid_size` breakdown by `size`

---

## User Journey Tracking

### Understanding `page` Property

The `page` property tracks **where** users perform actions to understand their journey:

```
User lands on pyplots.ai
    │
    ├─→ Home (grid view)
    │   └─→ copy_code { page: 'home' }
    │
    ├─→ Spec Overview (/{spec_id})
    │   └─→ copy_code { page: 'spec_overview' }
    │   └─→ download_image { page: 'spec_overview' }
    │
    └─→ Spec Detail (/{spec_id}/{library})
        └─→ copy_code { page: 'spec_detail' }
        └─→ download_image { page: 'spec_detail' }
```

### Journey Examples in Plausible

**Q: Do users copy from search results or spec pages?**
- Filter `copy_code` by `page` property
- `home` = direct from search/browse
- `spec_overview` = after viewing all implementations
- `spec_detail` = after deep-diving into one library

**Q: Which library implementations are most downloaded?**
- Filter `download_image` by `library` property
- Filter by `page` to see if users download from overview or detail

---

## Complete Event Reference

### Events Summary Table

| Event | Properties | Code Location |
|-------|------------|---------------|
| `copy_code` | `spec`, `library`, `method`, `page` | ImageCard.tsx, SpecPage.tsx, SpecTabs.tsx |
| `download_image` | `spec`, `library`, `page` | SpecPage.tsx |
| `navigate_to_spec` | `spec`, `library` | HomePage.tsx |
| `switch_library` | `spec`, `library` | SpecPage.tsx |
| `select_implementation` | `spec`, `library` | SpecPage.tsx |
| `back_to_overview` | `spec`, `library` | SpecPage.tsx |
| `catalog_rotate` | `spec` | CatalogPage.tsx |
| `search` | `query`, `category` | FilterBar.tsx |
| `search_no_results` | `query` | FilterBar.tsx |
| `random` | `category`, `value`, `method` | useFilterState.ts |
| `filter_remove` | `category`, `value` | useFilterState.ts |
| `toggle_grid_size` | `size` | FilterBar.tsx |
| `tab_click` | `tab`, `library` | SpecTabs.tsx |
| `tab_collapse` | `library` | SpecTabs.tsx |
| `external_link` | `destination`, `spec`, `library` | Footer.tsx |
| `open_interactive` | `spec`, `library` | SpecPage.tsx |
| `view_spec_overview` | `spec` | SpecPage.tsx |
| `view_spec` | `spec`, `library` | SpecPage.tsx |
| `og_image_view` | `page`, `platform`, `spec`?, `library`?, `filter_*`? | api/analytics.py (server-side) |

---

## Property Values Reference

### `spec` Values
Any valid specification ID (e.g., `scatter-basic`, `heatmap-correlation`, `bar-grouped`)

### `library` Values
```
matplotlib | seaborn | plotly | bokeh | altair | plotnine | pygal | highcharts | letsplot
```

### `method` Values
```
card      # ImageCard copy button (home grid)
image     # SpecPage image copy button
tab       # SpecTabs code tab copy button
click     # Random icon clicked
space     # Spacebar pressed
doubletap # Mobile double-tap
```

### `page` Values
```
home          # HomePage grid view (client) or og:image home endpoint (server)
catalog       # CatalogPage (server og:image only)
spec_overview # SpecPage showing all libraries
spec_detail   # SpecPage showing single library
```

### `platform` Values (server-side og:image tracking only)
```
# Social Media
twitter | facebook | linkedin | pinterest | reddit | tumblr | mastodon

# Messaging Apps
slack | discord | telegram | whatsapp | signal | viber | skype | teams | snapchat

# Search Engines
google | bing | yandex | duckduckgo | baidu | apple

# Link Preview Services
embedly | quora | outbrain | rogerbot | showyoubot

# Fallback
unknown
```

### `category` Values
```
lib   # library filter
plot  # plot_type filter
dom   # domain filter
feat  # features filter
data  # data_type filter
spec  # specification filter
```

### `tab` Values
```
code           # Python code tab
specification  # Spec details tab
implementation # AI implementation review tab
quality        # Quality score breakdown tab
```

### `destination` Values
```
linkedin  # LinkedIn profile link
github    # GitHub repository link
stats     # Plausible stats dashboard link
```

### `size` Values
```
normal   # Larger cards (1-3 columns)
compact  # Smaller cards (2-6 columns)
```

---

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

## Implementation Checklist

- [x] Plausible script loaded
- [x] Manual pageview tracking
- [x] Filter-based URL generation
- [x] Navigation events (`navigate_to_spec`, `switch_library`, etc.)
- [x] Code copy events with journey tracking (`copy_code` + `page`)
- [x] Download tracking (`download_image` + `page`)
- [x] Search events (`search`, `search_no_results`)
- [x] Random filter events (`random`)
- [x] Filter removal tracking (`filter_remove`)
- [x] Grid size toggle tracking (`toggle_grid_size`)
- [x] Tab interaction events (`tab_click`, `tab_collapse`)
- [x] External link events (`external_link`, `open_interactive`)
- [x] Server-side og:image tracking (`og_image_view`) with platform detection

### Plausible Dashboard Checklist

- [ ] Register all custom properties (see table above, including `platform` and `filter_*`)
- [ ] Create goals for key events (including `og_image_view`)
- [ ] Set up funnels (optional)
- [ ] Create custom dashboard widgets (optional)

---

**Last Updated**: 2026-01-06
**Status**: Production-ready with full journey tracking and server-side og:image analytics
