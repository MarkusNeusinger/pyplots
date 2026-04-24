# venn-labeled-items: Chartgeist-Style Venn Diagram with Labeled Items

## Description

An editorial, WIRED "Chartgeist"-style three-circle Venn diagram where pop-culture items — products, people, trends, apps — are plotted as labeled points inside each zone rather than represented as numeric counts. Three overlapping circles define witty, opinionated categories (e.g., "Overhyped", "Actually Useful", "Secretly Loved"), and each item lives in exactly one of the seven interior regions (or outside all circles). Unlike a classic proportional Venn, the "data" here is categorical set-membership plus a human label, making the plot ideal for commentary, taxonomy, and discussion rather than quantitative analysis.

## Applications

- Editorial and magazine-style cultural commentary on tech, media, food, or sports trends
- Team workshops classifying products, features, or ideas along three subjective traits
- Competitive positioning and taxonomy exercises in marketing decks
- Teaching set theory and Venn intersections with relatable, concrete examples
- Year-in-review or retrospective roundups summarizing a domain's "vibes"

## Data

- `circles` (list of 3 objects) - One per category, each with:
  - `name` (string) - Category label shown outside the circle (e.g., "Overhyped")
  - `color` (string, optional) - Fill/outline color for that circle
- `items` (list of objects) - Labeled items placed inside the diagram, each with:
  - `label` (string) - Item name rendered at the placement point (e.g., "NFTs", "Sourdough", "TikTok")
  - `zone` (string) - One of `A`, `B`, `C`, `AB`, `AC`, `BC`, `ABC`, or `outside`
- Size: Exactly 3 circles; 10-25 items distributed across the 7 interior zones (plus optional `outside`)
- Example: Circles "Overhyped", "Actually Useful", "Secretly Loved"; items include "NFTs" in `A`, "Google Maps" in `B`, "Dolly Parton" in `BC`, "Sourdough" in `ABC`

## Notes

- Use the standard symmetric three-circle Venn layout with equally sized circles and clear pairwise and triple overlaps
- Apply semi-transparent fills so overlapping regions remain visible through each other
- Place item labels inside their assigned zone without overlapping neighbors; use small point markers or text-only placement
- Render category names outside each circle on its outer side, aligned away from the diagram's center
- Optional witty title/subtitle in a serif editorial font to echo the magazine aesthetic
- Adopt a magazine-print look: generous whitespace, restrained palette, understated gridless background
- When the `outside` zone is used, place those items in the surrounding whitespace clearly separated from the circles
- Layout algorithm should attempt to distribute labels within each zone to minimize collisions; manual offsets may be supplied where the library allows
