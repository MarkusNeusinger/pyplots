# line-impurity-comparison: Gini Impurity vs Entropy Comparison

## Description

A theoretical comparison plot showing Gini impurity and entropy (information gain) as splitting criteria for decision trees across the probability range [0, 1]. Both curves are displayed on the same axes to illustrate their similar behavior and slight differences. This educational visualization helps understand the mathematical foundation of tree-based algorithms and why both criteria lead to similar tree structures in practice.

## Applications

- Machine learning education: explaining decision tree splitting criteria
- Algorithm comparison: understanding why Gini and entropy perform similarly
- Feature importance interpretation: theoretical foundation for tree-based models
- Textbook illustration: fundamental ML concept visualization

## Data

- `p` (numeric array) - probability values from 0 to 1 (100 points recommended)
- Gini impurity calculated as: 2 * p * (1 - p)
- Entropy calculated as: -p * log2(p) - (1-p) * log2(1-p), normalized to [0, 1]
- Size: 100 points for smooth curves

## Notes

- X-axis: probability p in range [0, 1]
- Y-axis: impurity measure (normalized to [0, 1] for comparison)
- Both curves should be clearly distinguishable with different colors/line styles
- Include legend explaining both metrics with their formulas
- Annotate maximum impurity point at p=0.5 (both maxima occur here)
- Handle edge cases at p=0 and p=1 where entropy is defined as 0
- Consider adding a light grid for readability
