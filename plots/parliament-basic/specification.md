# parliament-basic: Parliament Seat Chart

## Description

A semicircular parliament seat chart visualizes political party representation by arranging seats in concentric arcs. Each seat is displayed as an individual dot or segment, colored by party affiliation. This visualization is ideal for showing the composition of legislative bodies, election results, and voting bloc distributions at a glance.

## Applications

- Visualizing election results showing party seat distributions in parliament
- Displaying committee or board composition by faction or affiliation
- Analyzing voting bloc strength and coalition possibilities
- Comparing party representation across different legislative periods

## Data

- `party` (str) - Name of the political party or group
- `seats` (int) - Number of seats held by each party
- `color` (str) - Hex color code representing the party
- Size: 3-15 parties, total seats typically 50-700
- Example: Election results with party names, seat counts, and official party colors

## Notes

- Seats arranged in semicircular arcs from left to right
- Individual seats rendered as dots or small segments
- Legend should display party names with seat counts
- Optional: highlight majority threshold line (e.g., 50%+1 seats)
- Color ordering typically follows political spectrum (left to right)
