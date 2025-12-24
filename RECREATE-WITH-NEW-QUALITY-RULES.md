# Recreate Implementations with New Quality Rules (v2)

Track progress of regenerating all implementations using the stricter evaluation criteria.

## New Scoring System
- **90-100**: Excellent - Approved immediately
- **70-89**: Good - Repair loop, merge after 3 attempts
- **50-69**: Acceptable - Repair loop, merge after 3 attempts
- **< 50**: Poor - Repair loop, NOT merged after 3 attempts

## Progress

### All Specs (59 total)
- [x] arc-basic ✓ (88-94)
- [x] area-basic ✓ (91-92)
- [x] band-basic ✓ (91-98)
- [x] bar-basic ✓ (91-100)
- [x] box-basic ✓ (91-98)
- [x] bubble-basic ✓ (90-93)
- [x] bubble-packed ✓ (90-93)
- [x] bullet-basic ✓ (91-97)
- [x] bump-basic ✓ (94-96)
- [x] candlestick-basic ✓ (90-93)
- [x] chord-basic ✓ (7/9: 78-98, seaborn+plotnine not-feasible)
- [x] contour-basic ✓ (8/9: 72-98, pygal not-feasible)
- [x] dendrogram-basic ✓ (90-93)
- [x] density-basic ✓ (91-93)
- [x] donut-basic ✓ (91-92)
- [x] dumbbell-basic ✓ (91-93)
- [x] ecdf-basic ✓ (91-96)
- [x] errorbar-basic ✓ (91-92)
- [x] funnel-basic ✓ (90-96)
- [x] gauge-basic ✓ (91-95)
- [x] heatmap-basic ✓ (91-94)
- [x] heatmap-calendar ✓ (88-93)
- [x] hexbin-basic ✓ (52-93, altair 52 after 3 attempts)
- [x] histogram-basic ✓ (91-94)
- [x] line-basic ✓ (91-94)
- [x] lollipop-basic ✓ (91-92)
- [x] marimekko-basic ✓ (88-93)
- [x] network-basic ✓ (8/9: 88-92, plotnine not-feasible)
- [x] network-force-directed ✓ (8/9: 88-92, plotnine not-feasible)
- [x] parallel-basic ✓ (78-97)
- [x] pie-basic ✓ (91-92)
- [x] polar-basic ✓ (91-92)
- [x] pyramid-basic ✓ (90-98)
- [x] qq-basic ✓ (90-92)
- [x] quiver-basic ✓ (8/9: 82-99, seaborn not-feasible)
- [x] radar-basic ✓ (88-99)
- [x] ridgeline-basic ✓ (91-93)
- [x] rose-basic ✓ (73-92, pygal 73 after 3 attempts)
- [x] rug-basic ✓ (78-94, bokeh 78 after 3 attempts)
- [x] sankey-basic ✓ (78-93, seaborn 78 after 3 attempts)
- [x] scatter-basic ✓ (85-93)
- [x] slope-basic ✓ (86-92, pygal 86 after 3 attempts)
- [x] span-basic ✓ (91-93)
- [x] sparkline-basic ✓ (78-93, pygal 78 after 3 attempts)
- [x] stem-basic ✓ (86-94, pygal 86 after 3 attempts)
- [x] step-basic ✓ (90-94)
- [x] streamgraph-basic ✓ (75-93, pygal 75 after 3 attempts)
- [x] strip-basic ✓ (91-96)
- [x] sudoku-basic ✓ (91-94)
- [x] sunburst-basic ✓ (7/9: 88-92, plotnine+pygal not-feasible)
- [x] surface-basic ✓ (6/9: 87-91, seaborn+plotnine+pygal not-feasible)
- [x] swarm-basic ✓ (91-94)
- [x] ternary-basic ✓ (8/9: 62-92, pygal 62 after 3 attempts)
- [x] treemap-basic ✓ (91-92)
- [x] violin-basic ✓ (91-92)
- [x] waffle-basic ✓ (91-92)
- [x] waterfall-basic ✓ (90-97)
- [x] wireframe-3d-basic ✓ (6/9: 82-92, seaborn+plotnine+pygal not-feasible)
- [x] wordcloud-basic ✓ (68-92, plotnine 68 after 3 attempts, bokeh 78 after 3 attempts, seaborn 78 after 3 attempts)

## Notes
- Started: 2025-12-23
- New criteria in: `prompts/quality-criteria.md`
- Evaluator prompt: `prompts/quality-evaluator.md`
- Auto-reject rules: AR-01 to AR-07 (checked before AI review)
