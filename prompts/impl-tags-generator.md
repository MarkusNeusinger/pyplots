# Impl Tags Generator

AI rules for assigning Implementation-Level Tags.

These tags describe **HOW** the code is implemented, not **WHAT** is visualized.

---

## Naming Convention

**For ALL tags:**
- All lowercase
- Hyphens for multi-word: `twin-axes`, `data-generation`, `publication-ready`
- No underscores, no spaces
- Prefer established terms from the programming community

---

## The 5 Tag Dimensions

### 1. dependencies - "Which external packages are used?"

**Purpose:** Captures external libraries beyond the main plotting library.

**Question:** "Which additional packages are imported?"

**Recommended Values:**

| Tag | Description | Detection Pattern |
|-----|-------------|-------------------|
| `scipy` | scipy.stats, scipy.cluster, etc. | `from scipy import`, `import scipy` |
| `sklearn` | scikit-learn | `from sklearn import`, `import sklearn` |
| `statsmodels` | Statistical modeling | `import statsmodels` |
| `networkx` | Graph/network operations | `import networkx` |
| `selenium` | Browser automation for export | `from selenium import` |
| `pillow` | Image processing | `from PIL import` |
| `geopandas` | Geospatial data | `import geopandas` |
| `shapely` | Geometric operations | `from shapely import` |
| `wordcloud` | Wordcloud generation | `from wordcloud import` |

**Rules:**
- Only tag when library is actually imported
- Do NOT tag numpy, pandas, and the main plotting library
- Do NOT tag standard library (os, sys, datetime)

---

### 2. techniques - "Which visualization techniques are used?"

**Purpose:** Describes specific visualization and coding techniques.

**Question:** "Which techniques go beyond basic API usage?"

**Recommended Values:**

| Tag | Description | Detection Pattern |
|-----|-------------|-------------------|
| `twin-axes` | Secondary Y-axis | `ax.twinx()`, `ax.twiny()` |
| `manual-ticks` | Custom tick positions | `set_xticks()`, `set_yticks()` |
| `annotations` | Text annotations | `ax.annotate()`, `ax.text()` |
| `colorbar` | Color scale legend | `fig.colorbar()`, `plt.colorbar()` |
| `subplots` | Multiple plot panels | `plt.subplots(2, 2)`, `fig.add_subplot()` |
| `faceting` | Small multiples | `FacetGrid`, `alt.facet()` |
| `layer-composition` | Multiple geom layers | Multiple marks combined |
| `custom-legend` | Manually constructed legend | `ax.legend(handles=[...])` |
| `inset-axes` | Axes within axes | `inset_axes()` |
| `polar-projection` | Polar coordinate system | `projection='polar'` |
| `3d-projection` | 3D visualization | `projection='3d'` |
| `bezier-curves` | Custom curves | `Path()` with CURVE4 |
| `patches` | Custom shapes | `mpatches.Wedge`, `mpatches.Circle` |
| `hover-tooltips` | Interactive hover info | `HoverTool`, `tooltip` |
| `html-export` | Generates HTML output | `.save('plot.html')` |

**Rules:**
- Tag techniques that go beyond basic API usage
- Library-specific features count (e.g., Bokeh callbacks)

---

### 3. patterns - "Which code structure patterns are used?"

**Purpose:** Identifies coding patterns and data organization.

**Question:** "Which structural patterns are recognizable in the code?"

**Recommended Values:**

| Tag | Description | Detection Pattern |
|-----|-------------|-------------------|
| `data-generation` | Synthetic data creation | `np.random.randn()`, `np.random.seed()` |
| `dataset-loading` | Loads built-in dataset | `sns.load_dataset()`, `load_iris()` |
| `wide-to-long` | Data reshaping | `pd.melt()` |
| `long-to-wide` | Data pivoting | `df.pivot()` |
| `groupby-aggregation` | Group and aggregate | `df.groupby().agg()` |
| `iteration-over-groups` | Loops for multi-series | `for group in groups:` |
| `matrix-construction` | Builds 2D array | `np.zeros((n, m))`, `np.empty()` |
| `columndatasource` | Bokeh data pattern | `ColumnDataSource(data={...})` |
| `explicit-figure` | Creates figure explicitly | `fig, ax = plt.subplots()` |

**Rules:**
- Most simple plots have no patterns (empty list is OK)
- Only tag distinctive structural patterns

---

### 4. dataprep - "Which data transformations are performed?"

**Purpose:** Captures statistical or mathematical transformations.

**Question:** "Which significant data processing steps are there?"

**Recommended Values:**

| Tag | Description | Detection Pattern |
|-----|-------------|-------------------|
| `hierarchical-clustering` | Linkage/dendrogram | `linkage()`, `dendrogram()` |
| `kde` | Kernel Density Estimation | `gaussian_kde()`, `kdeplot` |
| `binning` | Data discretization | `np.histogram()`, `pd.cut()` |
| `normalization` | Scaling | `MinMaxScaler`, manual scaling |
| `correlation-matrix` | Correlation calculation | `df.corr()` |
| `cumulative-sum` | Running sums | `np.cumsum()` |
| `time-series` | Date/time index handling | `pd.date_range()` |
| `interpolation` | Value interpolation | `scipy.interpolate` |
| `rolling-window` | Moving averages | `df.rolling()` |
| `pca` | Dimensionality reduction | `PCA(n_components=2)` |
| `regression` | Regression calculation | `linregress()`, `polyfit()` |

**Rules:**
- Tag significant data transformations
- Simple array creation = no tag

---

### 5. styling - "Which visual style is used?"

**Purpose:** Describes the visual/aesthetic approach.

**Question:** "What makes the visual style distinctive?"

**Recommended Values:**

| Tag | Description | Detection Pattern |
|-----|-------------|-------------------|
| `publication-ready` | High quality, print-ready | Large fonts, clean layout |
| `minimal-chrome` | Reduced visual elements | `ax.axis('off')`, `theme_void()` |
| `custom-colormap` | Non-standard color scheme | `cmap='viridis'` or custom |
| `alpha-blending` | Transparency for density | `alpha=0.7` |
| `edge-highlighting` | Marker/bar edges | `edgecolor='white'` |
| `gradient-fill` | Color gradients in fills | Gradient-based styling |
| `grid-styling` | Custom grid | `ax.grid(alpha=0.3, linestyle='--')` |
| `dark-theme` | Dark background | `plt.style.use('dark_background')` |

**Rules:**
- Most plots use standard styling (empty list is OK)
- Only tag distinctive styling decisions

---

## Output Format

```json
{
  "dependencies": ["scipy", "sklearn"],
  "techniques": ["twin-axes", "colorbar"],
  "patterns": ["data-generation", "matrix-construction"],
  "dataprep": ["correlation-matrix"],
  "styling": ["publication-ready", "alpha-blending"]
}
```

Or as YAML in the metadata file:

```yaml
impl_tags:
  dependencies:
    - scipy
    - sklearn
  techniques:
    - twin-axes
    - colorbar
  patterns:
    - data-generation
    - matrix-construction
  dataprep:
    - correlation-matrix
  styling:
    - publication-ready
    - alpha-blending
```

---

## Examples

### matplotlib Chord Diagram
```yaml
impl_tags:
  dependencies: []
  techniques:
    - bezier-curves
    - patches
    - manual-ticks
  patterns:
    - data-generation
    - matrix-construction
    - iteration-over-groups
  dataprep: []
  styling:
    - publication-ready
    - alpha-blending
```

### highcharts Dendrogram
```yaml
impl_tags:
  dependencies:
    - scipy
    - selenium
  techniques:
    - html-export
    - manual-ticks
  patterns:
    - data-generation
    - iteration-over-groups
  dataprep:
    - hierarchical-clustering
  styling:
    - publication-ready
```

### seaborn Heatmap
```yaml
impl_tags:
  dependencies: []
  techniques:
    - colorbar
    - annotations
  patterns:
    - data-generation
  dataprep:
    - correlation-matrix
  styling:
    - custom-colormap
```

---

## Best Practices

1. **Tag conservatively** - Only tag what is clearly recognizable
2. **Empty arrays are OK** - Simple implementations have few tags
3. **Use established terms** - Prefer vocabulary from this list, but use any recognized term from the programming/data-viz community when appropriate (e.g., a new library not listed above should still be tagged)
4. **Typically 3-8 tags total** - Per implementation
5. **patterns is almost always filled** - At least `data-generation` or `dataset-loading`
6. **dependencies only when imported** - Not available, but actually used
