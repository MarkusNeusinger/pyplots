# Quality Criteria

Two-stage evaluation: Auto-Reject + Quality Scoring.

## Overview

```text
Implementation
     │
     ▼
┌─────────────────────┐
│  Stage 1: Auto-Reject  │  ──► FAIL → Score = 0, regenerate
│  (7 quick checks)      │
└─────────────────────┘
     │ PASS
     ▼
┌─────────────────────┐
│  Stage 2: Quality      │  ──► ≥ 90 → ai-approved, merge
│  (0-100 points)        │  ──► < 90 → ai-rejected, repair (max 3x)
└─────────────────────┘
     │ After 3 attempts
     ▼
┌─────────────────────┐
│  Final Decision        │  ──► ≥ 50 → merge to repo
│                        │  ──► < 50 → not in repo, regenerate
└─────────────────────┘
```

---

## Stage 1: Auto-Reject

Quick checks **before** AI evaluation. On fail: Score=0, no retry.

| ID | Check | Description | Verification |
|----|-------|-------------|--------------|
| AR-01 | SYNTAX_ERROR | Code cannot be parsed | `python -m py_compile` |
| AR-02 | RUNTIME_ERROR | Code throws exception | Execution with timeout |
| AR-03 | NO_OUTPUT | No `plot.png` created | File exists? |
| AR-04 | EMPTY_PLOT | Image empty | < 10KB or > 95% white |
| AR-05 | NO_LIBRARY | Library not used | 0 plot functions from library |
| AR-06 | NOT_FEASIBLE | Library cannot implement spec | AI decision |
| AR-07 | WRONG_FORMAT | Wrong output type | Not .png for static libraries |

**Check order:** AR-01 → AR-02 → AR-03 → AR-04 → AR-05 → AR-06 → AR-07

### AR-05: Library Usage

Implementation must use **plot functions** from the library, not just styling.

| Library | Must use | NOT sufficient |
|---------|----------|----------------|
| seaborn | `sns.scatterplot`, `sns.barplot`, `sns.heatmap`, etc. | Only `sns.set_style()` |
| plotly | `px.*` or `go.*` plot functions | Only `update_layout()` |
| bokeh | `figure.scatter()`, `figure.line()`, etc. | Only styling |
| altair | `alt.Chart().mark_*()` | Only `configure_*()` |
| plotnine | `ggplot() + geom_*()` | Only `theme()` |
| pygal | Chart classes with data | Only config |
| highcharts | Chart with series | Only options |
| letsplot | `ggplot() + geom_*()` | Only `ggsize()` |

### AR-06: Not Feasible

When a library cannot technically implement a spec (e.g., pygal cannot do 3D), this is an Auto-Reject. No retry, no file in repo.

---

## Allowed Image Formats

| Format | Size | Aspect Ratio |
|--------|------|--------------|
| **Landscape** | 4800 × 2700 px | 16:9 |
| **Square** | 3600 × 3600 px | 1:1 |

**Both have ~13M pixels** → same font sizes work for both.

**AI decides freely** which format is best for the specific plot.

---

## Stage 2: Quality Scoring (100 Points)

**Only if Stage 1 passed.** Focus purely on quality.

### Scoring Philosophy: STRICT

| Score | Tier | Outcome |
|-------|------|---------|
| 90-100 | Excellent | **Approved immediately** - Publication quality |
| 70-89 | Good | Repair loop → merge after 3 attempts |
| 50-69 | Acceptable | Repair loop → merge after 3 attempts |
| < 50 | Poor | Repair loop → **NOT in repo** after 3 attempts |

**Workflow:**
- **≥ 90**: ai-approved, merged immediately
- **< 90**: ai-rejected, repair loop (up to 3 attempts)
- **After 3 attempts**: ≥ 50 → merge, < 50 → close PR and regenerate

**Principles:**
- Full points only for **perfect** implementation
- Small flaws = immediate deduction
- "Good enough" = maximum 70%
- 90%+ = could appear in Nature/Science

### Point Distribution

| Category | Points | Focus |
|----------|--------|-------|
| Visual Quality | 40 | Readability, clarity, design |
| Spec Compliance | 25 | Matches the spec? |
| Data Quality | 20 | Good example data? |
| Code Quality | 10 | Clean code? |
| Library Features | 5 | Uses library strengths? |
| **Total** | **100** | |

---

## Visual Quality (40 Points)

| ID | Criterion | Max | Scoring |
|----|-----------|-----|---------|
| VQ-01 | Text Legibility | 10 | 10=perfect, 7=good, 4=ok, 0=poor |
| VQ-02 | No Overlap | 8 | 8=no overlap, 4=minimal, 0=overlap |
| VQ-03 | Element Visibility | 8 | 8=optimal sizing, 4=visible, 0=barely visible |
| VQ-04 | Color Accessibility | 5 | 5=perfect colorblind-safe, 2=ok, 0=red-green |
| VQ-05 | Layout Balance | 5 | 5=perfect, 3=ok, 0=cut-off |
| VQ-06 | Axis Labels | 2 | 2=with units, 1=descriptive, 0=x/y |
| VQ-07 | Grid & Legend | 2 | 2=perfect, 1=ok, 0=distracting |

### VQ-01: Text Legibility (10 Points)

All text must be clearly readable at 4800×2700 / 3600×3600 px.

| Points | Criterion |
|--------|-----------|
| 10 | Title ≥24pt, Labels ≥20pt, Ticks ≥16pt, all perfectly readable |
| 7 | All readable, but not optimal |
| 4 | Partially too small |
| 0 | Text hard to read |

### VQ-02: No Overlap (8 Points)

No overlapping text elements.

| Points | Criterion |
|--------|-----------|
| 8 | No overlap - all text fully readable |
| 4 | Minimal overlap, main content readable |
| 0 | Significant overlap, text unreadable |

**Common problems:**
- X-axis labels overlap with many categories
- Tick labels overlap each other
- Legend overlaps data

### VQ-03: Element Visibility (8 Points)

Data elements must be visible and adapted to data density.

| Points | Criterion |
|--------|-----------|
| 8 | Markers/lines perfectly adapted to data density |
| 4 | Visible, but not optimal (too big/small) |
| 0 | Elements barely visible or completely overlapping |

**Guidelines for Scatter:**

| Data points | Marker Size (s=) | Alpha |
|-------------|------------------|-------|
| < 30 | 200-400 | 0.9-1.0 |
| 30-100 | 100-200 | 0.7-0.9 |
| 100-300 | 50-100 | 0.5-0.7 |
| 300+ | 20-50 | 0.3-0.5 |

### VQ-04: Color Accessibility (5 Points)

| Points | Criterion |
|--------|-----------|
| 5 | Perfect colorblind-safe, good contrast |
| 2 | Acceptable, but not optimal |
| 0 | Red-green as only difference |

**Recommended palettes:** `viridis`, `colorblind`, `tab10`

### VQ-05: Layout Balance & Canvas Utilization (5 Points)

| Points | Criterion |
|--------|-----------|
| 5 | Perfect layout: plot fills 50-80% of canvas, balanced margins |
| 3 | Minor issues: plot fills 30-50% of canvas, some wasted space |
| 0 | **Severe**: plot fills <30% of canvas, OR content cut-off, OR legend isolated |

**Canvas Utilization Rules:**
- Plot elements (chart, axes, labels) should use **at least 40%** of the canvas area
- Whitespace should be **balanced** around the plot (not all on one side)
- Legend should be **near** the plot, not floating isolated in empty space
- Tiny plot in center of huge canvas = **automatic 0 points**

**Common failures:**
- Pie/donut charts that are tiny dots in the center
- Legends placed far from the chart with massive gaps
- Default library sizing that ignores the 4800×2700 canvas

### VQ-06: Axis Labels (2 Points)

| Points | Criterion |
|--------|-----------|
| 2 | Descriptive with units: "Temperature (°C)" |
| 1 | Descriptive without units: "Temperature" |
| 0 | Generic: "x", "y", or empty |

### VQ-07: Grid & Legend (2 Points)

| Points | Criterion |
|--------|-----------|
| 2 | Grid subtle (alpha 0.2-0.4), legend well placed |
| 1 | Acceptable |
| 0 | Grid dominant or legend covers data |

---

## Spec Compliance (25 Points)

| ID | Criterion | Points | Description |
|----|-----------|--------|-------------|
| SC-01 | Plot Type | 8 | Correct chart type |
| SC-02 | Data Mapping | 5 | X/Y correctly assigned |
| SC-03 | Required Features | 5 | All spec features present |
| SC-04 | Data Range | 3 | Axes show all data |
| SC-05 | Legend Accuracy | 2 | Legend labels correct |
| SC-06 | Title Format | 2 | `{spec-id} · {library} · pyplots.ai` |

---

## Data Quality (20 Points)

| ID | Criterion | Max | Scoring |
|----|-----------|-----|---------|
| DQ-01 | Feature Coverage | 8 | 8=shows ALL aspects, 4=most, 0=one-sided |
| DQ-02 | Realistic Context | 7 | 7=real scenario, 3=plausible, 0=nonsense |
| DQ-03 | Appropriate Scale | 5 | 5=perfect values, 2=ok, 0=impossible |

### DQ-01: Feature Coverage (8 Points)

Example data must show ALL features of the plot type.

| Points | Criterion |
|--------|-----------|
| 8 | Shows all aspects (e.g., boxplot with outliers AND different distributions) |
| 4 | Shows main features, but not all edge cases |
| 0 | All groups look the same, no variation |

**Examples:**
- Candlestick: Bullish AND bearish candles
- Boxplot: Outliers AND different spreads
- Histogram: Multimodal distribution when appropriate

### DQ-02: Realistic Context (7 Points)

| Points | Criterion |
|--------|-----------|
| 7 | Real, comprehensible scenario |
| 3 | Plausible, but generic |
| 0 | Nonsensical data (bicycle with fuel consumption) |

### DQ-03: Appropriate Scale (5 Points)

| Points | Criterion |
|--------|-----------|
| 5 | Perfect, realistic values for the context |
| 2 | Acceptable |
| 0 | Impossible values (temperatures of 500°C for weather) |

---

## Code Quality (10 Points)

| ID | Criterion | Points | Description |
|----|-----------|--------|-------------|
| CQ-01 | KISS Structure | 3 | Imports → Data → Plot → Save (no functions/classes) |
| CQ-02 | Reproducibility | 3 | `np.random.seed(42)` or deterministic data |
| CQ-03 | Clean Imports | 2 | Only used imports |
| CQ-04 | No Deprecated API | 1 | No outdated functions |
| CQ-05 | Output Correct | 1 | Saves as `plot.png` |

---

## Library Features (5 Points)

| ID | Criterion | Points | Description |
|----|-----------|--------|-------------|
| LF-01 | Distinctive Features | 5 | Uses library-specific strengths |

**Note:** Basic library usage is checked by AR-05. This is for bonus points for good usage.

| Points | Criterion |
|--------|-----------|
| 5 | Uses distinctive features (e.g., seaborn's `regplot`, plotly's interactivity) |
| 3 | Uses library correctly, but no special features |
| 0 | Only minimal library usage |

---

## Score Caps

Certain errors limit the maximum score:

| Problem | Max Score |
|---------|-----------|
| VQ-02 = 0 (severe overlap) | 49 |
| VQ-03 = 0 (invisible elements) | 49 |
| SC-01 = 0 (wrong plot type) | 40 |

---

## Example Evaluation

A "good" plot (formerly 95%, now 80%):

```text
VISUAL QUALITY (30/40)
  VQ-01: 7/10  (readable, but not perfect)
  VQ-02: 8/8   (no overlap)
  VQ-03: 4/8   (visible, but markers could be better)
  VQ-04: 5/5   (good colors)
  VQ-05: 3/5   (ok layout)
  VQ-06: 1/2   (labels without units)
  VQ-07: 2/2   (grid ok)

SPEC COMPLIANCE (23/25)
  SC-01: 8/8   (correct type)
  SC-02: 5/5   (mapping ok)
  SC-03: 4/5   (one feature missing)
  SC-04: 3/3   (range ok)
  SC-05: 2/2   (legend ok)
  SC-06: 1/2   (title not perfect)

DATA QUALITY (15/20)
  DQ-01: 6/8   (shows most features)
  DQ-02: 5/7   (plausible scenario)
  DQ-03: 4/5   (good values)

CODE QUALITY (9/10)
  CQ-01: 3/3   (KISS)
  CQ-02: 3/3   (seed set)
  CQ-03: 2/2   (clean imports)
  CQ-04: 1/1   (current)
  CQ-05: 0/1   (wrong filename)

LIBRARY FEATURES (3/5)
  LF-01: 3/5   (uses library, but no special features)

TOTAL: 80/100 = "Good" Tier
```

---

## Evaluation Checklist

### Stage 1: Auto-Reject
- [ ] AR-01: Code compiles
- [ ] AR-02: Code runs without error
- [ ] AR-03: plot.png exists
- [ ] AR-04: Image not empty
- [ ] AR-05: Library is used
- [ ] AR-06: Library can implement spec
- [ ] AR-07: Correct file format

### Stage 2: Quality (only if Stage 1 passed)

**Visual Quality (40 pts)**
- [ ] VQ-01: Text Legibility (10)
- [ ] VQ-02: No Overlap (8)
- [ ] VQ-03: Element Visibility (8)
- [ ] VQ-04: Color Accessibility (5)
- [ ] VQ-05: Layout Balance (5)
- [ ] VQ-06: Axis Labels (2)
- [ ] VQ-07: Grid & Legend (2)

**Spec Compliance (25 pts)**
- [ ] SC-01: Plot Type (8)
- [ ] SC-02: Data Mapping (5)
- [ ] SC-03: Required Features (5)
- [ ] SC-04: Data Range (3)
- [ ] SC-05: Legend Accuracy (2)
- [ ] SC-06: Title Format (2)

**Data Quality (20 pts)**
- [ ] DQ-01: Feature Coverage (8)
- [ ] DQ-02: Realistic Context (7)
- [ ] DQ-03: Appropriate Scale (5)

**Code Quality (10 pts)**
- [ ] CQ-01: KISS Structure (3)
- [ ] CQ-02: Reproducibility (3)
- [ ] CQ-03: Clean Imports (2)
- [ ] CQ-04: No Deprecated API (1)
- [ ] CQ-05: Output Correct (1)

**Library Features (5 pts)**
- [ ] LF-01: Distinctive Features (5)

**Total: ___ / 100**
