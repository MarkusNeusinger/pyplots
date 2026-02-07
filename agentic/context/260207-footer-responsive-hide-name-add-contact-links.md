# Responsive Footer Name & Legal Contact Links

**Run ID:** d7e7bdf6
**Date:** 2026-02-07
**Specification:** agentic/specs/260207-footer-responsive-hide-name-add-contact-links.md

## Overview

The footer's "markus neusinger" link is hidden on mobile viewports (below 960px / `md` breakpoint) to prevent a cramped layout, and social contact links (LinkedIn, X, GitHub) were added to the Legal Notice page's Contact section to keep contact information discoverable.

## What Was Built

- Responsive hiding of the "markus neusinger" link and its dot separators in the footer on screens below the `md` breakpoint (960px)
- LinkedIn, X (Twitter), and GitHub contact links added to the Legal Notice page Contact section with analytics tracking

## Technical Implementation

### Files Modified

- `app/src/components/Footer.tsx`: Wrapped the "markus neusinger" link and its surrounding dot separators in a `<Box>` with responsive `display` (`{ xs: 'none', md: 'contents' }`) to hide them on mobile
- `app/src/pages/LegalPage.tsx`: Added three social links (LinkedIn, X, GitHub) to the Contact section below the existing email link, each with `target="_blank"`, `rel="noopener noreferrer"`, matching `#3776AB` color styling, and `trackEvent` analytics calls

### Key Changes

- Used MUI's responsive `sx` display prop for pure CSS-based hiding — no JavaScript media query hooks needed
- The `<Box component="span" sx={{ display: { xs: 'none', md: 'contents' } }}>` wrapper ensures the name link and both adjacent dot separators are hidden/shown together, and `contents` on desktop means the Box has no visual impact
- Social links in the Legal page follow the existing pattern: `<br />` line breaks within the `<Typography>` block, consistent `#3776AB` link color
- Analytics tracking uses `trackEvent('external_link', { destination: 'linkedin' | 'x' | 'github_personal' })` matching the existing event pattern

## How to Use

1. On mobile devices or viewports narrower than 960px, the footer displays: `github · stats · mcp · legal`
2. On desktop viewports (960px and wider), the footer displays the full set: `github · stats · markus neusinger · mcp · legal`
3. Social contact links are always visible on the Legal Notice page (`/legal`) in the Contact section

## Configuration

No configuration needed. The `md` breakpoint (960px) is defined by the MUI theme and matches the FilterBar's mobile breakpoint.

## Testing

- `cd app && npx tsc --noEmit` — Verify TypeScript types
- `cd app && yarn build` — Verify no compilation errors
- Resize browser below/above 960px to confirm the footer name link hides/shows
- Visit `/legal` and verify LinkedIn, X, and GitHub links appear in the Contact section

## Notes

- The 960px breakpoint was chosen to match where the FilterBar catalog/filter row wraps to 2 lines on the homepage
- The LinkedIn URL in the footer and Legal page are intentionally the same — redundancy ensures discoverability
- The `github_personal` destination in analytics distinguishes the personal GitHub profile link from the project repository link
