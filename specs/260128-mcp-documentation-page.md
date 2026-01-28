# Feature: MCP Documentation Page

## Feature Description
Add an "MCP" link to the website footer (similar style to "Legal") that navigates to a dedicated `/mcp` page explaining the MCP (Model Context Protocol) server and how AI assistants can use it to access pyplots data.

The page will serve as a user-friendly guide for developers who want to integrate pyplots with their AI assistants (Claude Desktop, Claude Code, etc.), providing configuration examples, tool documentation, and use cases.

## User Story
As a developer using AI assistants
I want to easily find MCP configuration documentation on pyplots.ai
So that I can set up my AI assistant to access pyplots data for code generation and plot discovery

## Problem Statement
The MCP server documentation currently exists only in:
1. `README.md` (brief overview)
2. `docs/reference/mcp.md` (detailed technical reference)

Users visiting pyplots.ai have no way to discover or access MCP documentation from the website. Adding a visible "MCP" link in the footer (like the existing "Legal" link) and a dedicated page will make this feature discoverable and accessible.

## Solution Statement
1. Add "MCP" link to the footer component (same style as existing links)
2. Create a new `/mcp` route and `McpPage.tsx` page component
3. The page will contain:
   - What is MCP (brief explanation with link to official docs)
   - Available tools (list_specs, search_specs_by_tags, get_implementation, etc.)
   - Configuration examples for Claude Desktop and Claude Code (SSE + Streamable HTTP)
   - Common use cases (AI-assisted plotting, code generation)
   - Link to full technical documentation in the repo

## Relevant Files
Use these files to implement the feature:

- `app/src/components/Footer.tsx` - Add the new "MCP" link next to existing footer links
- `app/src/router.tsx` - Add the new `/mcp` route
- `app/src/pages/LegalPage.tsx` - Reference for page structure, styling, and patterns
- `app/src/constants/index.ts` - Reference for constants pattern
- `app/src/hooks/useAnalytics.ts` - Reference for analytics hook usage
- `app/src/components/index.ts` - Export components for clean imports
- `docs/reference/mcp.md` - Source of truth for MCP documentation content
- `README.md` - Reference for MCP configuration examples

### New Files
- `app/src/pages/McpPage.tsx` - New MCP documentation page component

## Implementation Plan

### Phase 1: Foundation
- Review existing page patterns (LegalPage.tsx) to ensure consistency
- Understand analytics tracking patterns for internal links
- Review the MCP documentation content to determine what to include on the page

### Phase 2: Core Implementation
- Create the McpPage.tsx component following existing patterns
- Add routing for /mcp in router.tsx
- Add MCP link to Footer component
- Implement analytics tracking for the new page and link

### Phase 3: Integration
- Export the new page component properly
- Test navigation from footer to new page
- Verify analytics events are tracked
- Ensure breadcrumb navigation works correctly

## Step by Step Tasks

### Step 1: Create McpPage Component
- Create `app/src/pages/McpPage.tsx` following the pattern from `LegalPage.tsx`
- Use the same MUI components: Box, Typography, Paper, Link, Table
- Include Helmet for SEO (title, meta description, og:title, og:description)
- Include Breadcrumb component (pyplots.ai > mcp)
- Include Footer component
- Track pageview with useAnalytics hook
- Structure content into logical sections with Paper components

### Step 2: Implement MCP Page Content
Content sections (based on `docs/reference/mcp.md` and `README.md`):

1. **What is MCP** - Brief explanation linking to modelcontextprotocol.io
2. **Configuration** - Two subsections:
   - Claude Desktop configuration (URL-based)
   - Claude Code configuration (npx mcp-remote approach for SSE and Streamable HTTP)
3. **Available Tools** - Table listing:
   - list_specs
   - search_specs_by_tags
   - get_spec_detail
   - get_implementation
   - list_libraries
   - get_tag_values
4. **Use Cases** - Common scenarios:
   - AI-assisted plot discovery
   - Code generation with AI
   - Comparing library implementations
5. **Resources** - Links to:
   - Full MCP documentation (GitHub docs/reference/mcp.md)
   - MCP official website
   - GitHub repository

### Step 3: Add Route to Router
- Import McpPage in `app/src/router.tsx`
- Add route: `{ path: 'mcp', element: <McpPage /> }` inside the Layout children

### Step 4: Add MCP Link to Footer
- In `app/src/components/Footer.tsx`, add a new link after "legal":
  - Add separator span (`·`)
  - Add RouterLink to "/mcp" with same styling as "legal" link
  - Include onClick handler for analytics tracking: `onTrackEvent?.('internal_link', { destination: 'mcp', spec: selectedSpec, library: selectedLibrary })`

### Step 5: Export Page Component
- Add export for McpPage in `app/src/pages/index.ts` (if exists) or ensure proper import in router.tsx

### Step 6: Add Plausible Tracking Event
- Update `docs/reference/plausible.md` to document the new MCP page pageview event

### Step 7: Run Tests and Validation
- Run frontend linting: `cd app && yarn lint`
- Run frontend build to check for errors: `cd app && yarn build`
- Start dev server and manually test navigation
- Verify analytics tracking works (check console in dev, or test in production)

## Testing Strategy

### Unit Tests
- No unit tests required for static page content
- The page uses existing, tested hooks (useAnalytics)

### Integration Tests
- No integration tests required (static content page)

### Edge Cases
- Deep linking to /mcp should work directly
- Footer link should work from all pages (homepage, spec pages, legal page)
- Breadcrumb should navigate back to homepage

## Acceptance Criteria
- [ ] Footer displays "MCP" link next to "legal" with same styling
- [ ] Clicking "MCP" link navigates to /mcp page
- [ ] /mcp page loads without errors
- [ ] Page has proper SEO tags (title, description, og tags)
- [ ] Page content includes: What is MCP, Configuration (Claude Desktop + Claude Code), Available Tools, Use Cases
- [ ] Page follows existing design patterns (MonoLisa font, Paper sections, consistent colors)
- [ ] Analytics tracking works for page view and footer link click
- [ ] Breadcrumb shows "pyplots.ai > mcp" and navigates correctly
- [ ] Frontend builds without errors

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `cd app && yarn lint` - Lint frontend code
- `cd app && yarn build` - Build frontend for production (catches TypeScript errors)
- `cd app && yarn dev` - Start dev server for manual testing
- `uv run ruff check . && uv run ruff format .` - Lint and format Python code (no Python changes expected)
- `uv run pytest tests/unit` - Run unit tests (no backend changes expected)

## Notes
- The page content is derived from existing documentation in `docs/reference/mcp.md` and `README.md`
- Keep the page simple and focused - link to full technical docs for advanced details
- The MCP endpoints are `/mcp/` (Streamable HTTP) and `/sse/` (SSE transport)
- Claude Desktop uses direct URL config, Claude Code uses npx mcp-remote wrapper
- Consider adding a "Last updated" timestamp at the bottom like LegalPage
- Related GitHub Issue: #4150
