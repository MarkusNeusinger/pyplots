# funnel-basic: Basic Funnel Chart

## Description

A funnel chart visualizes sequential stages of a process where values progressively decrease from one stage to the next. Each stage is represented as a trapezoidal segment that narrows from top to bottom, making it easy to identify drop-offs between stages. This chart is ideal for tracking conversion rates, sales pipelines, and multi-step processes where understanding stage-to-stage transitions is critical.

## Applications

- Marketing teams tracking website visitor conversion from awareness through purchase
- Sales organizations visualizing pipeline stages from leads to closed deals
- HR departments analyzing recruitment funnel from applications to hires
- E-commerce platforms monitoring checkout abandonment at each step

## Data

- `stage` (string) - Name of each sequential stage in the process
- `value` (numeric) - Count or amount at each stage, typically decreasing
- Size: 3-8 stages (too many stages reduce readability)
- Example: Sales funnel with stages ["Awareness", "Interest", "Consideration", "Intent", "Purchase"] and values [1000, 600, 400, 200, 100]

## Notes

- Stages should be ordered from largest (top) to smallest (bottom)
- Use distinct colors for each stage to improve visual differentiation
- Include value or percentage labels on each segment for clarity
- The width of each segment should be proportional to its value relative to the first stage
