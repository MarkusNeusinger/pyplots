# PyPlots.ai Default Style Guide

Style requirements for consistent visualizations at large canvas sizes.

## Important: Large Canvas Size

pyplots renders at high resolution (~13 million pixels). All element sizes must be scaled for visibility!

**Common Mistake:** Using default/standard sizes results in tiny, hard-to-see elements.

---

## Dimensions

Two formats are allowed (similar pixel count for consistent font sizing):

| Format | Size | Aspect Ratio | Use Case |
|--------|------|--------------|----------|
| **Landscape** | 4800 × 2700 px | 16:9 | Default, most plots |
| **Square** | 3600 × 3600 px | 1:1 | Symmetric plots (pie, radar, heatmaps, grid-based) |

**AI decides freely** which format is best for each specific plot.

**Why these sizes?**
- Landscape: 4800 × 2700 = 12.96 million pixels
- Square: 3600 × 3600 = 12.96 million pixels
- Same pixel area → same font sizes work for both

---

## Color Palette

Primary colors (always use these first):

| #  | Name          | Hex       |
|----|---------------|-----------|
| 1  | Python Blue   | #306998   |
| 2  | Python Yellow | #FFD43B   |

For additional colors: AI chooses appropriate, colorblind-safe colors.

---

## Visual Sizing Principles

Since we render at ~13 million pixels, elements must be **visually prominent**:

### Text
- **Title**: Large and clearly readable
- **Axis labels**: Prominent, not tiny
- **Tick labels**: Readable at full image size
- **Legend**: Easy to read

### Data Elements
- **Points/Markers**: Clearly visible, not tiny dots
- **Lines**: Thick enough to see clearly
- **Bars**: With subtle edges for definition

### General Rules
- Elements should be **~3-4x larger** than standard defaults
- When in doubt, make it bigger
- Test: Would this be readable on a 4K monitor?

---

## Grid

- Subtle, not dominant
- Low opacity (around 30%)
- Should enhance readability, not distract

---

## AI Discretion

The AI decides based on the specific library and visualization:

- Exact sizes and parameters (library-specific)
- Font family
- Grid style (on/off, dashed/solid)
- Legend placement
- Additional colors beyond the primary two

**Priority:** Clarity and readability at full resolution (~13 million pixels).
