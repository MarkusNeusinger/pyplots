# tree-phylogenetic: Phylogenetic Tree Diagram

## Description

A phylogenetic tree (evolutionary tree) visualization showing hierarchical relationships between species or sequences, with branch lengths proportional to evolutionary distance. This diagram reveals how organisms or genes evolved from common ancestors, with longer branches indicating greater divergence. Phylogenetic trees are essential for understanding evolutionary history, taxonomy, and molecular biology relationships.

## Applications

- Visualizing evolutionary relationships between species based on genetic sequence analysis
- Displaying taxonomic classification hierarchies in biology and ecology studies
- Showing protein or gene family evolution and divergence patterns
- Comparing pathogen strains to understand disease transmission and mutation patterns

## Data

- `newick_string` (string) - tree structure in Newick format with branch lengths
- `species_names` (string) - labels for leaf nodes representing species or sequences
- `branch_lengths` (numeric) - evolutionary distances between nodes
- Size: 5-50 leaf nodes recommended for readable trees
- Example: phylogenetic tree of primate species based on mitochondrial DNA

## Notes

- Use libraries like Biopython (Phylo module) or ete3 for parsing Newick format
- Branch lengths should be drawn proportionally to show evolutionary distance accurately
- Consider both rectangular (cladogram) and circular (radial) tree layouts
- Add scale bar to indicate branch length units (e.g., substitutions per site)
- Color-code clades or highlight specific lineages for emphasis
