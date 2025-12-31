# manhattan-gwas: Manhattan Plot for GWAS

## Description

A Manhattan plot visualizes genome-wide association study (GWAS) results by displaying -log10 transformed p-values across chromosomal positions. Points are arranged by genomic position along the x-axis with alternating colors for each chromosome, making it easy to identify significant associations. A horizontal threshold line indicates genome-wide significance (typically p < 5×10⁻⁸). This plot is essential for identifying genetic variants associated with traits or diseases.

## Applications

- Identifying significant SNPs in genome-wide association studies for complex diseases
- Visualizing genetic association results across the entire genome in pharmacogenomics research
- Presenting GWAS findings in scientific publications and research presentations
- Screening for candidate loci in agricultural genomics and breeding programs

## Data

- `chromosome` (categorical) - Chromosome identifier (1-22, X, Y, or MT)
- `position` (integer) - Base pair position along the chromosome
- `p_value` (float) - P-value from association test (will be -log10 transformed)
- `snp_id` (string, optional) - SNP identifier for labeling significant hits
- Size: 100,000 - 1,000,000+ variants typical for GWAS
- Example: Simulated GWAS data with random p-values and some significant peaks

## Notes

- X-axis should show cumulative genomic position with chromosome labels centered below their region
- Use alternating colors (e.g., blue/gray) for adjacent chromosomes for visual distinction
- Include horizontal dashed line at -log10(5×10⁻⁸) ≈ 7.3 for genome-wide significance threshold
- Optionally include suggestive threshold line at -log10(1×10⁻⁵) = 5
- Consider point size reduction for dense datasets to prevent overplotting
- Significant SNPs above threshold may be labeled or highlighted with different color
