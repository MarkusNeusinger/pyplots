# PyPlots.ai Default Style Guide

Style requirements for consistent visualizations at **4800 × 2700 px**.

## Important: Large Canvas Size

pyplots renders at **4800 × 2700 px** (much larger than standard plots). All element sizes must be scaled for visibility!

**Common Mistake:** Using default/standard sizes results in tiny, hard-to-see elements.

---

## Dimensions

| Property         | Value            |
|------------------|------------------|
| Image Size       | 4800 × 2700 px   |
| Aspect Ratio     | 16:9             |

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

Since we render at 4800 × 2700 px, elements must be **visually prominent**:

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

**Priority:** Clarity and readability at 4800 × 2700 px.
