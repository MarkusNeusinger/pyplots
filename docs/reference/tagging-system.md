# Tagging System

A 4-dimensional tagging system for plot specifications. Tags are assigned by the spec-create workflow and help users find plots by type, data, domain, and features.

---

## The 4 Tag Dimensions

### 1. plot_type - "What is being visualized?"

**Purpose:** Describes the visual form and structure. Answers: "What kind of chart is this?"

**Principle:** Use established data visualization vocabulary. If a plot type has a known name, use it. Combine multiple tags when applicable.

**Typical values:**
- Basic shapes: `scatter`, `line`, `bar`, `pie`, `area`
- Distributions: `histogram`, `density`, `box`, `violin`, `strip`, `swarm`
- Matrices: `heatmap`, `contour`, `hexbin`
- Hierarchies: `treemap`, `sunburst`, `dendrogram`, `icicle`
- Networks: `network`, `chord`, `arc`, `sankey`
- Specialized: `candlestick`, `gauge`, `funnel`, `waterfall`, `radar`

**How to derive:** Ask yourself: "How would a data visualization expert name this plot?" Use terminology from matplotlib/seaborn/plotly documentation.

---

### 2. data_type - "What data is being visualized?"

**Purpose:** Describes the structure and type of input data. Answers: "What kind of data does this plot need?"

**Principle:** Focus on logical data structure, not technical format. A user wanting to "visualize time series" should find this plot.

**Typical values:**
- Numbers: `numeric`, `continuous`, `discrete`
- Categories: `categorical`, `ordinal`
- Time: `timeseries`, `datetime`
- Structure: `hierarchical`, `network`, `relational`
- Space: `geospatial`, `spatial`
- Text: `text`, `frequency`

**How to derive:** Ask yourself: "If someone has this type of data, would they search for this plot?" Think about the typical use case.

---

### 3. domain - "Where is it used?"

**Purpose:** Describes typical application areas. Answers: "In which industry/discipline is this plot commonly used?"

**Principle:** `general` is the default for universally applicable plots. Use specific domains only when the plot is particularly established there.

**Typical values:**
- Universal: `general`
- Science: `statistics`, `science`, `research`
- Business: `business`, `finance`, `marketing`
- Technical: `engineering`, `technology`
- Other: `healthcare`, `education`, `energy`, `environment`

**How to derive:** Ask yourself: "Is there an industry where this plot type is particularly common?" Candlestick → finance. Forest plot → healthcare/research. If unclear → `general`.

---

### 4. features - "What are special characteristics?"

**Purpose:** Describes variants, modifications, and special attributes. Answers: "What distinguishes this variant from the basic version?"

**Principle:** Describe what makes the plot SPECIAL. Multiple tags allowed. Consider what a user would search for.

**Typical values:**
- Complexity: `basic`, `advanced`
- Layout: `grouped`, `stacked`, `horizontal`, `multi`
- Dimensions: `2d`, `3d`
- Interaction: `interactive`, `animated`, `static`
- Function: `comparison`, `distribution`, `correlation`, `ranking`
- Display: `annotated`, `color-mapped`, `proportional`

**How to derive:** Ask yourself: "What adjectives describe this plot?" and "What would someone type into a search engine to find exactly this variant?"

---

## Example

**For `sankey-basic`:**

```yaml
tags:
  plot_type:
    - sankey          # Established name
    - flow            # Alternative term
  data_type:
    - categorical     # Nodes are categories
    - numeric         # Flows have values
  domain:
    - general         # Universally applicable
    - business        # Common for process analysis
    - energy          # Classic for energy flows
  features:
    - basic           # Base variant
    - flow-visualization
    - proportional    # Width shows quantity
```

---

## Format in specification.yaml

```yaml
tags:
  plot_type:
    - {primary type}
    - {secondary type if applicable}
  data_type:
    - {primary data type}
    - {secondary if applicable}
  domain:
    - general         # Always include if universally applicable
    - {specific domain if applicable}
  features:
    - basic           # Or specific features
    - {additional features}
```

---

## Best Practices

1. **Be specific but not excessive** - 2-4 tags per dimension is typical
2. **Think like a user** - What would someone search for?
3. **Use established vocabulary** - Standard data viz terminology
4. **general is fine** - Not every plot needs a specialized domain
5. **basic is informative** - It tells users this is the foundational variant
