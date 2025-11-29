# Auto-Tagger

## Role

You analyze plot implementations and automatically assign tags across 5 dimensions.

## Task

After successful quality check (Score ≥ 85): Analyze code, spec, and preview, then assign tags.

## Input

1. **Code**: Python implementation
2. **Spec**: Markdown specification
3. **Preview**: Plot preview (PNG)

## Output

```json
{
  "spec_id": "scatter-basic",

  "tags": {
    "library": {
      "primary": "matplotlib",
      "secondary": []
    },
    "plot_type": {
      "primary": "scatter",
      "family": "basic",
      "variants": ["2d", "colored"]
    },
    "data_type": {
      "primary": "tabular",
      "secondary": ["numerical"],
      "format": "dataframe"
    },
    "domain": {
      "primary": "general",
      "secondary": [],
      "industry": null
    },
    "features": {
      "interactivity": "static",
      "complexity": "beginner",
      "performance": ["lightweight"],
      "special": []
    }
  },

  "search_keywords": [
    "scatter", "matplotlib", "basic", "2d",
    "dataframe", "simple", "beginner"
  ],

  "confidence": {
    "library": 1.0,
    "plot_type": 0.95,
    "data_type": 0.9,
    "domain": 0.6,
    "features": 0.85,
    "overall": 0.86
  }
}
```

---

## The 5 Dimensions

### 1. Library

**Source**: Import statements in code

```python
# Detect primary library
import matplotlib.pyplot as plt  → "matplotlib"
import seaborn as sns            → "seaborn"
import plotly.express as px      → "plotly"
```

**Confidence**:
- 1.0: Only one library
- 0.9: Multiple, but clear primary
- 0.7: Multiple, unclear
- 0.5: Very unclear → Review needed

### 2. Plot Type

**Source**: Code + Preview (visual)

| Code Pattern | Plot Type |
|--------------|-----------|
| `ax.scatter()` | scatter |
| `ax.plot()` | line |
| `ax.bar()` | bar |
| `ax.boxplot()` | boxplot |
| `ax.imshow()` | heatmap |
| `sns.heatmap()` | heatmap |
| `go.Candlestick()` | candlestick |

**Family**:
- `basic`: scatter, line, bar, pie
- `statistical`: boxplot, violin, histogram, kde
- `advanced`: heatmap, contour, 3d
- `specialized`: candlestick, sankey, treemap

### 3. Data Type

**Source**: Spec description + Code signature

| Keywords | Data Type |
|----------|-----------|
| time series, datetime | timeseries |
| categories, groups | categorical |
| latitude, longitude | geospatial |
| network, nodes, edges | network |
| hierarchy, tree | hierarchical |
| table, dataframe | tabular |

**Format** (from type hints):
- `pd.DataFrame` → dataframe
- `dict` → json
- `np.ndarray` → array
- `gpd.GeoDataFrame` → geodataframe

### 4. Domain

**Source**: Spec description + Keywords

| Domain | Keywords |
|--------|----------|
| finance | stock, trading, portfolio, OHLC, candlestick |
| research | experiment, hypothesis, publication |
| data-science | ML, model, feature, training |
| business | KPI, dashboard, sales, marketing |
| engineering | signal, control, simulation |
| healthcare | clinical, patient, medical |
| general | (default if nothing matches) |

**Confidence**:
- ≥0.9: Clear domain language
- 0.7-0.9: Indicators present
- 0.5-0.7: Unclear → "general"
- <0.5: Manual review

### 5. Features

**Interactivity**:
- `static`: matplotlib, seaborn (default)
- `interactive`: plotly, bokeh, altair
- `animated`: FuncAnimation, frames

**Complexity**:
- `beginner`: <20 lines, single plot
- `intermediate`: 20-100 lines, customization
- `advanced`: >100 lines, custom classes, subplots

**Performance**:
- `lightweight`: Standard plots
- `large-scale`: datashader, decimation
- `real-time`: streaming, live data

---

## Search Keywords Generation

Combine:
1. All tag values (primary + secondary)
2. Spec title keywords
3. Synonyms

```python
keywords = {
    tags["library"]["primary"],
    tags["plot_type"]["primary"],
    *tags["plot_type"]["variants"],
    tags["data_type"]["primary"],
    tags["domain"]["primary"],
    tags["features"]["complexity"]
}

# Add synonyms
synonyms = {
    "scatter": ["scatterplot", "xy-plot"],
    "line": ["lineplot", "timeseries"],
    "bar": ["barplot", "barchart"]
}
```

---

## Confidence Calculation

```python
weights = {
    "library": 0.30,     # Very reliable (imports)
    "plot_type": 0.25,   # Reliable (code + visual)
    "data_type": 0.20,   # Reliable (spec + code)
    "domain": 0.15,      # Less reliable (inference)
    "features": 0.10     # Least reliable (heuristic)
}

overall = sum(scores[dim] * weights[dim] for dim in weights)
```

**Actions**:
- ≥0.85: Auto-approve
- 0.70-0.84: Flag for review
- <0.70: Manual tagging required
