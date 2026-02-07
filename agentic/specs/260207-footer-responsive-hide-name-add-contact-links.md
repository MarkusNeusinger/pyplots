# Feature: Responsive Footer Name & Legal Contact Links

## Metadata

run_id: `d7e7bdf6`
prompt: `In the footer, my full name "markus neusinger" is quite long and on small mobile screens it no longer looks clean or minimal. Starting at the same breakpoint where the filter row on the homepage ("catalog" / filters) wraps to two lines, I want my name to no longer be shown in the footer. Instead, in the Legal page Contact section there should be links to my LinkedIn, X, and GitHub accounts in addition to the existing email: https://x.com/MarkusNeusinger https://github.com/MarkusNeusinger https://www.linkedin.com/in/markus-neusinger/`

## Feature Description

Two related changes to improve the mobile experience:

1. **Footer**: Hide the "markus neusinger" link on small screens (below `md` / 900px breakpoint) — the same breakpoint where the FilterBar catalog/filter row wraps to 2 lines on the homepage. The name is too long and makes the footer look cramped on mobile. The dot separator before/after the name link should also be hidden.

2. **Legal Page**: Add social/contact links (LinkedIn, X/Twitter, GitHub) to the Contact section in the Legal Notice, alongside the existing email. This ensures the contact information remains discoverable even when the footer name link is hidden on mobile.

## Requirements

- Hide the "markus neusinger" link (and its surrounding dot separators) in the footer when viewport width is below `md` (900px) — matching the FilterBar's `isMobile` breakpoint
- On viewports `md` and above (900px+), the footer remains unchanged
- Add LinkedIn, X (Twitter), and GitHub links to the Contact section of the Legal Notice on LegalPage
- Social links: LinkedIn (`https://www.linkedin.com/in/markus-neusinger/`), X (`https://x.com/MarkusNeusinger`), GitHub (`https://github.com/MarkusNeusinger`)
- Maintain consistent styling with existing Legal Page link patterns (color `#3776AB`, monospace font)
- Track social link clicks via existing analytics (`onTrackEvent` / `trackEvent`)

## Relevant Files

### Existing Files to Modify

- **`app/src/components/Footer.tsx`** — Hide the "markus neusinger" `<Link>` and its adjacent dot `<span>` separators on screens below `md` breakpoint using MUI's `sx` display responsive prop
- **`app/src/pages/LegalPage.tsx`** — Add LinkedIn, X, and GitHub links to the Contact section (lines 102-109) in the Legal Notice Paper, below the existing email link

### New Files to Create

None.

## Implementation Plan

IMPORTANT: Execute every step in order, top to bottom.

### 1. Update Footer to hide name on mobile

In `app/src/components/Footer.tsx`:

- Add `useMediaQuery` and `useTheme` imports from MUI
- Add `const theme = useTheme()` and `const isMobile = useMediaQuery(theme.breakpoints.down('md'))` inside the component
- Wrap the "markus neusinger" `<Link>` (lines 54-66) and the `<span>·</span>` separator immediately **before** it (line 53) in a `<Box>` (or use `sx={{ display: { xs: 'none', md: 'contents' } }}`) to hide them on small screens
- The simplest approach: use MUI's responsive `display` prop on the separator span and the link:
  - On the `<span>·</span>` at line 53: add `sx={{ display: { xs: 'none', md: 'inline' } }}`
  - On the `<Link>` for "markus neusinger": add `display: { xs: 'none', md: 'inline' }` to its `sx` prop
- This leaves the remaining 4 links (github · stats · mcp · legal) visible on mobile, with proper dot separation

### 2. Add social/contact links to Legal Page

In `app/src/pages/LegalPage.tsx`:

- Locate the Contact section inside the Legal Notice Paper (around lines 102-109)
- After the existing email link `<Link>`, add three more links on separate lines:
  - LinkedIn: `https://www.linkedin.com/in/markus-neusinger/`
  - X: `https://x.com/MarkusNeusinger`
  - GitHub: `https://github.com/MarkusNeusinger`
- Use the same styling pattern as the email link (`sx={{ color: '#3776AB' }}`)
- Add `target="_blank"` and `rel="noopener noreferrer"` for external links
- Add `onClick` analytics tracking with `trackEvent('external_link', { destination: 'linkedin' })` etc.
- Structure: keep it as a simple list within the existing `<Typography sx={textStyle}>` block using `<br />` for line breaks (matching the existing pattern in the Contact section)

### 3. Verify responsive behavior

- Build the frontend to ensure no TypeScript/compilation errors
- Verify the footer shows 4 links on mobile (<900px) and 5 links on desktop (>=900px)
- Verify the Legal page Contact section shows email + 3 social links

### 4. Add Tests

- No frontend test files exist in the project currently — skip test creation as there is no test infrastructure for React components

## Validation Commands

Execute these commands to validate the feature:

- `cd app && npx tsc --noEmit` - Check TypeScript types
- `cd app && yarn build` - Build frontend to verify no compilation errors

## Notes

- The `md` breakpoint (900px) was chosen because the user specifically asked for the same breakpoint where the FilterBar wraps to 2 lines, and `FilterBar.tsx` uses `theme.breakpoints.down('md')` for its `isMobile` check
- Using MUI responsive `display` (`{ xs: 'none', md: 'inline' }`) is the lightest-weight approach — no JS needed, pure CSS media queries via MUI's system
- The existing LinkedIn link in the footer (`markus neusinger`) already points to the same URL that will be added to the Legal page — this is intentional redundancy for discoverability
- The GitHub link uses `GITHUB_URL` constant already imported in LegalPage for the Source Code section; the personal GitHub URL (`https://github.com/MarkusNeusinger`) is different from the project repo URL
