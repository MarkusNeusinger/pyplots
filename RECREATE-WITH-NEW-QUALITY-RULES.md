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
- [ ] candlestick-basic
- [ ] chord-basic
- [ ] contour-basic (7/9: missing seaborn, pygal)
- [ ] dendrogram-basic
- [ ] density-basic (8/9: missing bokeh)
- [x] donut-basic ✓ (91-92)
- [ ] dumbbell-basic
- [ ] ecdf-basic
- [ ] errorbar-basic
- [ ] funnel-basic
- [ ] gauge-basic
- [x] heatmap-basic ✓ (91-94)
- [ ] heatmap-calendar
- [x] hexbin-basic ✓ (52-93, altair 52 after 3 attempts)
- [x] histogram-basic ✓ (91-94)
- [x] line-basic ✓ (91-94, plotnine kept old)
- [ ] lollipop-basic
- [ ] marimekko-basic
- [ ] network-basic
- [ ] network-force-directed
- [ ] parallel-basic
- [x] pie-basic ✓ (91-92)
- [ ] polar-basic (7/9: missing seaborn, plotnine)
- [ ] pyramid-basic
- [ ] qq-basic
- [ ] quiver-basic
- [ ] radar-basic (7/9: missing seaborn, plotnine)
- [ ] ridgeline-basic
- [ ] rose-basic
- [ ] rug-basic
- [ ] sankey-basic
- [x] scatter-basic ✓ (85-93)
- [ ] slope-basic
- [ ] span-basic
- [ ] sparkline-basic
- [ ] stem-basic
- [ ] step-basic
- [ ] streamgraph-basic
- [ ] strip-basic
- [ ] sudoku-basic
- [ ] sunburst-basic
- [ ] surface-basic
- [ ] swarm-basic
- [ ] ternary-basic
- [ ] treemap-basic
- [x] violin-basic ✓ (91-92)
- [ ] waffle-basic
- [ ] waterfall-basic
- [ ] wireframe-3d-basic
- [ ] wordcloud-basic

## Notes
- Started: 2025-12-23
- New criteria in: `prompts/quality-criteria.md`
- Evaluator prompt: `prompts/quality-evaluator.md`
- Auto-reject rules: AR-01 to AR-07 (checked before AI review)
