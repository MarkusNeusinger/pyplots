# chord-basic: Basic Chord Diagram

## Description

A chord diagram displays relationships or flows between entities arranged around a circle's perimeter. Arcs (chords) connect related entities, with chord width proportional to the flow magnitude. This visualization excels at revealing the overall structure of connections and identifying the strongest relationships within a system.

## Applications

- Visualizing migration flows between countries or regions
- Showing trade relationships and import/export volumes between nations
- Displaying gene interactions or protein-protein interactions in bioinformatics
- Analyzing communication patterns between departments in an organization

## Data

- `source` (categorical) - Origin entity/group name
- `target` (categorical) - Destination entity/group name
- `value` (numeric) - Flow magnitude or connection strength
- Size: 4-20 entities with 10-100 connections
- Example: Migration flows between 6 continents with bidirectional flow values

## Notes

- Each entity should have a distinct color for easy identification
- Chord width should be proportional to flow value
- Consider adding hover tooltips showing exact flow values for interactive libraries
- For bidirectional flows, both directions should be visible as separate chords
