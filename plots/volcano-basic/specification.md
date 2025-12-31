# volcano-basic: Volcano Plot for Statistical Significance

## Description

A volcano plot displays statistical significance (-log10 p-value) on the y-axis versus effect size (log2 fold change) on the x-axis. Points are typically color-coded to highlight features that are both statistically significant and have large effect sizes. This visualization is essential for quickly identifying the most important changes in differential expression, proteomics, and genomics studies.

## Applications

- Identifying differentially expressed genes between treatment and control conditions in RNA-seq experiments
- Detecting significantly altered proteins in mass spectrometry-based proteomics studies
- Visualizing metabolite changes in metabolomics comparisons between disease and healthy states

## Data

- `log2_fold_change` (numeric) - Effect size representing the magnitude of change (x-axis)
- `neg_log10_pvalue` (numeric) - Statistical significance as -log10(p-value) (y-axis)
- `label` (string, optional) - Gene/protein/feature identifier for annotations
- `significant` (boolean, optional) - Flag indicating if feature meets significance thresholds
- Size: 100-10000 features typical for omics data
- Example: Differential gene expression results with fold changes and adjusted p-values

## Notes

- Include horizontal threshold line at -log10(0.05) ≈ 1.3 for significance cutoff
- Include vertical threshold lines at log2 fold change of ±1 (2-fold change) for effect size cutoffs
- Color points by significance status: non-significant (gray), significant up-regulated (red), significant down-regulated (blue)
- Consider labeling top significant features by name
- Use alpha transparency to handle overlapping points in dense datasets
