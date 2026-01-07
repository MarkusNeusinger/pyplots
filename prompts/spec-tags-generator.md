# Spec Tags Generator

AI rules for assigning Specification-Level Tags.

---

## Naming Convention

**For ALL tags:**
- All lowercase
- Hyphens for multi-word: `color-mapped`, `time-series`, `flow-visualization`
- No underscores, no spaces
- Prefer established terms from the data visualization community

---

## The 4 Tag Dimensions

### 1. plot_type - "What is visualized?"

**Purpose:** Describes the visual form and structure of the plot.

**Question:** "How would a data visualization expert name this plot?"

**Recommended Values:**

| Category | Tags |
|----------|------|
| Basic Forms | `scatter`, `line`, `bar`, `pie`, `area`, `point` |
| Distributions | `histogram`, `density`, `box`, `violin`, `strip`, `swarm`, `rug` |
| Matrices | `heatmap`, `contour`, `hexbin` |
| Hierarchies | `treemap`, `sunburst`, `dendrogram`, `icicle`, `circlepacking` |
| Networks | `network`, `chord`, `arc`, `sankey`, `alluvial` |
| Specialized | `candlestick`, `gauge`, `funnel`, `waterfall`, `radar`, `polar` |
| Geospatial | `choropleth`, `map` |
| Statistical | `qq`, `ecdf`, `calibration`, `bland-altman` |

**Rules:**
- Use established names from matplotlib/seaborn/plotly documentation
- Multiple tags allowed when plot combines multiple types
- Example: Sankey is also a `flow` plot

---

### 2. data_type - "What data is visualized?"

**Purpose:** Describes the structure and nature of the input data.

**Question:** "If someone has this type of data, would they search for this plot?"

**Recommended Values:**

| Category | Tags |
|----------|------|
| Numbers | `numeric`, `continuous`, `discrete` |
| Categories | `categorical`, `ordinal` |
| Time | `timeseries`, `datetime` |
| Structure | `hierarchical`, `network`, `relational` |
| Space | `geospatial`, `spatial` |
| Text | `text`, `frequency` |
| Matrix | `matrix`, `correlation` |

**Rules:**
- Focus on logical data structure, not technical format
- Multiple tags when different data types are combined
- Example: Scatter needs `numeric` for both axes

---

### 3. domain - "Where is it used?"

**Purpose:** Describes typical application areas.

**Question:** "Is there an industry where this plot is particularly common?"

**Recommended Values:**

| Category | Tags |
|----------|------|
| Universal | `general` |
| Science | `statistics`, `science`, `research` |
| Business | `business`, `finance`, `marketing` |
| Technology | `engineering`, `technology` |
| Other | `healthcare`, `education`, `energy`, `environment` |
| ML/AI | `machine-learning`, `model-evaluation` |

**Rules:**
- `general` is default for universally applicable plots
- Specific domains only when plot is particularly established there
- Example: Candlestick → `finance`, Forest Plot → `healthcare`

---

### 4. features - "What are special properties?"

**Purpose:** Describes variants, modifications, and special attributes.

**Question:** "What distinguishes this variant from the base version?"

**Recommended Values:**

| Category | Tags |
|----------|------|
| Complexity | `basic`, `advanced` |
| Layout | `grouped`, `stacked`, `horizontal`, `multi`, `faceted` |
| Dimensions | `2d`, `3d` |
| Interaction | `interactive`, `animated`, `static` |
| Function | `comparison`, `distribution`, `correlation`, `ranking` |
| Display | `annotated`, `color-mapped`, `proportional` |
| Special | `flow`, `temporal`, `cumulative`, `stepwise` |

**Rules:**
- Describe what makes the plot SPECIAL
- Multiple tags allowed
- `basic` is informative - indicates base variant

---

## Output Format

```yaml
tags:
  plot_type:
    - {primary-type}
    - {secondary-type}  # optional
  data_type:
    - {primary-datatype}
    - {secondary-datatype}  # optional
  domain:
    - general  # always when universally applicable
    - {specific-domain}  # optional
  features:
    - basic  # or specific features
    - {additional-features}
```

---

## Examples

### scatter-basic
```yaml
tags:
  plot_type:
    - scatter
  data_type:
    - numeric
    - continuous
  domain:
    - statistics
    - general
  features:
    - basic
    - 2d
    - correlation
```

### sankey-basic
```yaml
tags:
  plot_type:
    - sankey
    - flow
  data_type:
    - categorical
    - numeric
  domain:
    - general
    - business
  features:
    - basic
    - flow
    - proportional
```

### heatmap-calendar
```yaml
tags:
  plot_type:
    - heatmap
    - calendar
  data_type:
    - datetime
    - numeric
  domain:
    - general
    - business
  features:
    - basic
    - temporal
    - color-mapped
```

---

## Best Practices

1. **Specific but not excessive** - 2-4 tags per dimension is typical
2. **Think like a user** - What would someone type in a search?
3. **Use established terms** - Prefer listed vocabulary, but any recognized term from the data-viz community is valid
4. **general is OK** - Not every plot needs a specialized domain
5. **basic is informative** - Indicates this is the base variant
