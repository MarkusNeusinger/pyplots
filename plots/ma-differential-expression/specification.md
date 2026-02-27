# ma-differential-expression: MA Plot for Differential Expression

## Description

An MA plot (M-versus-A plot) visualizes the relationship between log fold change (M) and mean average expression (A) when comparing two experimental conditions. Each point represents a gene or feature, with significantly differentially expressed genes highlighted. This plot is a standard diagnostic tool in RNA-seq and microarray analysis for assessing differential expression results and detecting systematic expression-dependent bias.

## Applications

- Identifying differentially expressed genes between treatment and control conditions in RNA-seq experiments
- Assessing normalization quality and detecting expression-dependent bias in microarray data
- Comparing treatment versus control conditions in transcriptomics studies
- Quality control in high-throughput genomics pipelines to verify fold-change distributions

## Data

- `mean_expression` (numeric) - A value: average log expression level across both conditions (x-axis)
- `log_fold_change` (numeric) - M value: log2 fold change between conditions (y-axis)
- `significant` (boolean) - Whether the gene passes the significance threshold (e.g., adjusted p < 0.05)
- `gene_name` (string, optional) - Gene identifier for labeling notable points
- Size: 10,000-20,000 genes typical for whole-transcriptome experiments
- Example: DESeq2 or edgeR differential expression results with baseMean, log2FoldChange, and padj columns

## Notes

- Highlight significant genes (adjusted p < 0.05) in a distinct color (e.g., red) against non-significant genes in gray
- Draw a horizontal reference line at M = 0 (no change) and dashed lines at M = +1 and M = -1 (2-fold change thresholds)
- Include a LOESS smoothing curve to reveal any systematic expression-dependent bias
- Use transparency (alpha ~0.3) to handle overplotting in dense regions
- Optionally label a small number of top differentially expressed genes by name
