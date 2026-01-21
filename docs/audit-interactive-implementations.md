# Audit: Interactive Implementations Removed

**Date:** 2026-01-21
**Auditor:** Claude Code (automated analysis)

## Summary

This document records the removal of 13 implementations that claimed to provide interactive functionality but could not deliver it due to the fundamental limitations of static plotting libraries.

## Problem Statement

Several specifications require **runtime interactivity** - features like click-to-drill-down, brush selection, sliders, and real-time updates. These features require JavaScript or GUI event loops that cannot exist in static PNG output.

The following static libraries were incorrectly used to implement interactive specs:
- **matplotlib** - Produces static PNG/SVG
- **seaborn** - Built on matplotlib, static output
- **plotnine** - ggplot2 implementation, static output

While these implementations received high quality scores (82-92), they **fundamentally fail to meet the specification requirements** because:

1. PNG files cannot respond to user clicks
2. Static images cannot update in real-time
3. Widgets and sliders cannot function in saved images
4. Animations require separate GIF files, not the main PNG output

## Removed Implementations

### 1. bar-drilldown (3 implementations)

**Specification requirement:** Click on a bar to drill down into subcategories

| Library | Score | What it actually shows |
|---------|-------|------------------------|
| matplotlib | 91 | 2x2 grid showing all levels simultaneously |
| seaborn | 82 | 3 panels with fake "breadcrumb" navigation |
| plotnine | 87 | Static arrows suggesting hierarchy, no interaction |

**Why removed:** Click-to-drill requires JavaScript event handlers. Static PNG cannot respond to mouse clicks.

### 2. scatter-brush-zoom (1 implementation)

**Specification requirement:** Draw rectangle to select and zoom into data points

| Library | Score | What it actually shows |
|---------|-------|------------------------|
| matplotlib | 91 | Code includes RectangleSelector but PNG shows nothing |

**Why removed:** RectangleSelector requires matplotlib's interactive backend (Qt, Tk). PNG export captures only the static plot without widgets.

### 3. linked-views-selection (3 implementations)

**Specification requirement:** Select points in one view, see them highlighted in other views

| Library | Score | What it actually shows |
|---------|-------|------------------------|
| matplotlib | 91 | Pre-baked selection of "Cluster B" hardcoded |
| seaborn | 91 | Fixed threshold x>6.0 shown, cannot change |
| plotnine | 91 | PIL composite image stitching multiple plots |

**Why removed:** Linked selection requires bidirectional event propagation. Static images show one frozen state only.

### 4. slider-control-basic (1 implementation)

**Specification requirement:** Slider widget to adjust parameter and update plot

| Library | Score | What it actually shows |
|---------|-------|------------------------|
| matplotlib | 91 | Code creates Slider widget but it's invisible in PNG |

**Why removed:** matplotlib widgets require interactive session. `plt.savefig()` captures only the figure, not the widget axes.

### 5. bar-race-animated (2 implementations)

**Specification requirement:** Animated bar chart showing ranking changes over time

| Library | Score | What it actually shows |
|---------|-------|------------------------|
| matplotlib | 91 | Separate GIF file; PNG shows only final frame |
| seaborn | 91 | 6 small multiples showing different time points |

**Why removed:** Animation requires either HTML5 video or GIF format. The specification expects the main plot output to be animated, not a separate file.

### 6. gauge-realtime (2 implementations)

**Specification requirement:** Gauge that updates with real-time data

| Library | Score | What it actually shows |
|---------|-------|------------------------|
| matplotlib | 92 | Motion blur effect to simulate movement |
| seaborn | 91 | Motion blur effect to simulate movement |

**Why removed:** "Real-time" requires live data connection and continuous updates. Static images can only show one moment in time; motion blur is a visual trick, not actual real-time behavior.

## Files Removed

### Implementations (13 files)
```
plots/bar-drilldown/implementations/matplotlib.py
plots/bar-drilldown/implementations/seaborn.py
plots/bar-drilldown/implementations/plotnine.py
plots/scatter-brush-zoom/implementations/matplotlib.py
plots/linked-views-selection/implementations/matplotlib.py
plots/linked-views-selection/implementations/seaborn.py
plots/linked-views-selection/implementations/plotnine.py
plots/slider-control-basic/implementations/matplotlib.py
plots/bar-race-animated/implementations/matplotlib.py
plots/bar-race-animated/implementations/seaborn.py
plots/gauge-realtime/implementations/matplotlib.py
plots/gauge-realtime/implementations/seaborn.py
```

### Metadata (13 files)
```
plots/bar-drilldown/metadata/matplotlib.yaml
plots/bar-drilldown/metadata/seaborn.yaml
plots/bar-drilldown/metadata/plotnine.yaml
plots/scatter-brush-zoom/metadata/matplotlib.yaml
plots/linked-views-selection/metadata/matplotlib.yaml
plots/linked-views-selection/metadata/seaborn.yaml
plots/linked-views-selection/metadata/plotnine.yaml
plots/slider-control-basic/metadata/matplotlib.yaml
plots/bar-race-animated/metadata/matplotlib.yaml
plots/bar-race-animated/metadata/seaborn.yaml
plots/gauge-realtime/metadata/matplotlib.yaml
plots/gauge-realtime/metadata/seaborn.yaml
```

## Remaining Valid Implementations

These specifications still have valid implementations from interactive libraries:

| Spec | Valid Libraries |
|------|-----------------|
| bar-drilldown | plotly, bokeh, altair, highcharts |
| scatter-brush-zoom | plotly, bokeh, altair, highcharts, letsplot |
| linked-views-selection | plotly, bokeh, altair, highcharts |
| slider-control-basic | plotly, bokeh, altair, highcharts |
| bar-race-animated | plotly, bokeh, altair, highcharts, pygal |
| gauge-realtime | plotly, bokeh, altair, highcharts |

## Lessons Learned

1. **Quality review should check spec compliance first** - A visually appealing plot that doesn't meet the spec requirements should not pass review.

2. **Interactive specs should exclude static libraries** - The specification system should mark certain specs as requiring interactive output formats (HTML).

3. **Static library workarounds are not acceptable** - Showing "what it would look like if clicked" is not the same as actual click functionality.

## Recommendations

1. **Add `output_format: html` requirement** to interactive specs
2. **Update quality-evaluator.md** to fail implementations that cannot deliver required interactivity
3. **Consider adding library capability matrix** to prevent incompatible library/spec combinations

---

## GCS Cleanup Completed

The following GCS images were deleted on 2026-01-21:

**Production images removed (24 files):**
- `gs://pyplots-images/plots/bar-drilldown/{matplotlib,seaborn,plotnine}/plot.png`
- `gs://pyplots-images/plots/bar-drilldown/{matplotlib,seaborn,plotnine}/plot_thumb.png`
- `gs://pyplots-images/plots/scatter-brush-zoom/matplotlib/plot.png`
- `gs://pyplots-images/plots/scatter-brush-zoom/matplotlib/plot_thumb.png`
- `gs://pyplots-images/plots/linked-views-selection/{matplotlib,seaborn,plotnine}/plot.png`
- `gs://pyplots-images/plots/linked-views-selection/{matplotlib,seaborn,plotnine}/plot_thumb.png`
- `gs://pyplots-images/plots/slider-control-basic/matplotlib/plot.png`
- `gs://pyplots-images/plots/slider-control-basic/matplotlib/plot_thumb.png`
- `gs://pyplots-images/plots/bar-race-animated/{matplotlib,seaborn}/plot.png`
- `gs://pyplots-images/plots/bar-race-animated/{matplotlib,seaborn}/plot_thumb.png`
- `gs://pyplots-images/plots/gauge-realtime/{matplotlib,seaborn}/plot.png`
- `gs://pyplots-images/plots/gauge-realtime/{matplotlib,seaborn}/plot_thumb.png`

**Staging:** No staging images existed for these implementations.

---

*This audit was performed as part of routine quality maintenance to ensure pyplots.ai only serves implementations that actually deliver what they promise.*
