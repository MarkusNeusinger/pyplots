# hive-basic: Basic Hive Plot

## Description

A hive plot arranges network nodes on radial axes based on node properties (such as degree, category, or other attributes), enabling reproducible and directly comparable network visualizations. Unlike force-directed layouts which can produce different arrangements for identical networks, hive plots always render the same network identically, solving the "hairball" problem of traditional network graphs and making structural comparisons reliable.

## Applications

- Comparing software dependency networks across versions to identify structural changes
- Analyzing social network patterns where reproducibility is required for publication or reporting
- Visualizing biological interaction networks (protein-protein, gene regulatory) for systematic analysis

## Data

- `nodes` (list of dicts) - entities with unique IDs and axis assignment attribute (e.g., role, category, or degree-based grouping)
- `edges` (list of tuples/dicts) - connections as (source_id, target_id) pairs with optional weight
- `axis_attribute` (string) - the node property used to assign nodes to axes (typically 2-3 axes)
- Size: 20-100 nodes for clear visualization; axes should have balanced node counts
- Example: A software module dependency network with nodes assigned to axes by module type (core, utility, interface)

## Notes

- Use 2-3 radial axes for clarity; more axes reduce readability
- Node position along each axis should encode a meaningful property (e.g., degree, centrality, or alphabetical order)
- Edge bundling or transparency helps with dense connections between axes
- Consider using hiveplotlib library which provides matplotlib, bokeh, and plotly backends
