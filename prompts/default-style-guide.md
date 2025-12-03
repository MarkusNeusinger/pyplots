# PyPlots.ai Default Visualization Style Guide

A consistent, recognizable visual identity for all PyPlots.ai examples and generated visualizations.

## Color Palette

Use colors in this order for data series:

| #  | Name          | Hex       | RGB                 | Usage              |
|----|---------------|-----------|---------------------|--------------------|
| 1  | Python Blue   | #306998   | rgb(48, 105, 152)   | Primary / First    |
| 2  | Python Yellow | #FFD43B   | rgb(255, 212, 59)   | Secondary          |
| 3  | Signal Red    | #DC2626   | rgb(220, 38, 38)    | Alerts / Third     |
| 4  | Teal Green    | #059669   | rgb(5, 150, 105)    | Success / Fourth   |
| 5  | Violet        | #8B5CF6   | rgb(139, 92, 246)   | Accent / Fifth     |
| 6  | Orange        | #F97316   | rgb(249, 115, 22)   | Highlight / Sixth  |

## Dimensions

| Property         | Value       |
|------------------|-------------|
| Aspect Ratio     | 16:9        |
| Export DPI       | 300         |

## Typography

| Element          | Font        | Size   | Weight     |
|------------------|-------------|--------|------------|
| Title            | Inter       | 20pt   | Semi-Bold  |
| Axis Labels      | Inter       | 20pt   | Regular    |
| Tick Labels      | Inter       | 16pt   | Regular    |
| Legend           | Inter       | 16pt   | Regular    |
| Annotations      | Inter       | 14pt   | Regular    |

**Fallback Fonts:** DejaVu Sans → Arial → Helvetica → system sans-serif

## Lines & Markers

| Element          | Value       |
|------------------|-------------|
| Line Width       | 2 px        |
| Marker Size      | 4 px        |
| Axis Frame       | 2 px, black |

## Grid

| Property         | Value              |
|------------------|--------------------|
| Style            | Dashed (--)        |
| Color            | Black, 50% opacity |
| Line Width       | 1 px               |
| Position         | Behind data        |

## Ticks

| Property         | Value                      |
|------------------|----------------------------|
| Direction        | Inward                     |
| Major Size       | 10 px long, 2 px wide      |
| Minor Size       | 5 px long, 1 px wide       |
| Minor Visible    | Yes                        |
| Placement        | All four sides             |

## Legend

| Property         | Value              |
|------------------|--------------------|
| Frame            | Visible            |
| Background       | White, 100% opaque |
| Corners          | Slightly rounded   |

## Background

| Element          | Color              |
|------------------|--------------------|
| Figure           | #FFFFFF (white)    |
| Plot Area        | #FFFFFF (white)    |

## Design Principles

1. **Clarity over decoration** — Every element serves a purpose
2. **Distinct colors** — All six colors are clearly distinguishable
3. **Supportive grid** — Aids reading without dominating
4. **Consistent proportions** — Same style across all visualizations
5. **Python Blue first** — #306998 as the signature primary color
6. **Inter typography** — Matches PyPlots.ai web identity