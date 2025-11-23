# Tagging Rules v1.0.0-draft

## Metadata
- **Version**: v1.0.0-draft
- **Type**: Auto-Tagging Process
- **Status**: draft
- **Last Updated**: 2025-01-23
- **Purpose**: Guide AI in automatically generating tags for plot implementations

---

## Overview

After generating plot code (via `code-generation-rules.md`), the AI must automatically tag the implementation across 5 dimensions:

1. **Library** (Level 1)
2. **Plot Type** (Level 2)
3. **Data Type** (Level 3)
4. **Domain** (Level 4)
5. **Features** (Level 5)

**Trigger**: After code generation + preview creation + quality check (≥85)

**Input**:
- `code`: Generated Python implementation file
- `spec`: Markdown specification
- `preview_image`: Plot preview (PNG, base64 or URL)

**Output**: JSON structure with tags + confidence scores

---

## Tagging Process (5 Steps)

### Step 1: Extract Library Tags

**Source**: Python code imports

**Method**: Parse import statements

```python
# Example code analysis
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
```

**Logic**:
```python
def extract_library_tag(code: str) -> dict:
    """
    Identify primary and secondary libraries from imports

    Priority order (if multiple libraries present):
    1. The library used for main plotting function (e.g., plt.scatter, sns.scatterplot)
    2. The library with most import statements
    3. Explicit library mentioned in docstring
    """

    import_patterns = {
        "matplotlib": r"import matplotlib",
        "seaborn": r"import seaborn",
        "plotly": r"import plotly",
        "bokeh": r"import bokeh",
        "altair": r"import altair"
    }

    # Find all libraries
    found_libraries = []
    for lib, pattern in import_patterns.items():
        if re.search(pattern, code):
            found_libraries.append(lib)

    # Determine primary library (most plotting calls)
    primary = detect_primary_from_function_calls(code, found_libraries)

    # Secondary libraries (used but not primary)
    secondary = [lib for lib in found_libraries if lib != primary]

    return {
        "library": {
            "primary": primary,
            "secondary": secondary
        }
    }
```

**Example Output**:
```json
{
  "library": {
    "primary": "matplotlib",
    "secondary": []
  }
}
```

**Confidence Score**:
- 1.0: Only one library imported
- 0.9: Multiple libraries but clear primary (>80% of plot calls)
- 0.7: Multiple libraries, unclear primary
- 0.5: Multiple libraries, no clear pattern (FLAG FOR REVIEW)

---

### Step 2: Analyze Plot Type

**Source**: Code structure + Preview image (Vision AI)

**Method**: Multi-modal analysis

**Code Analysis**:
```python
def detect_plot_type_from_code(code: str) -> str:
    """
    Identify plot type from function calls

    Matplotlib patterns:
    - ax.scatter() → "scatter"
    - ax.plot() → "line"
    - ax.bar() → "bar"
    - ax.imshow() + colorbar → "heatmap"

    Seaborn patterns:
    - sns.scatterplot() → "scatter"
    - sns.lineplot() → "line"
    - sns.heatmap() → "heatmap"

    Plotly patterns:
    - px.scatter() → "scatter"
    - px.line() → "line"
    - px.bar() → "bar"
    """

    # Extract main plotting function
    plot_function = extract_main_plot_call(code)

    # Map to plot_type
    function_to_type = {
        "scatter": "scatter",
        "scatterplot": "scatter",
        "plot": "line",
        "lineplot": "line",
        "bar": "bar",
        "barplot": "bar",
        "imshow": "heatmap",
        "heatmap": "heatmap",
        # ... full mapping in appendix
    }

    return function_to_type.get(plot_function, "unknown")
```

**Visual Analysis** (if code analysis unclear):
```python
async def analyze_plot_type_visual(preview_image: str) -> dict:
    """
    Use Vision AI to classify plot type from preview

    Prompt to Vision AI:
    "Analyze this data visualization and classify it as one of:
    - line (connected points)
    - bar (vertical/horizontal bars)
    - scatter (discrete points)
    - heatmap (colored grid)
    - pie (circular sectors)
    - 3d (three-dimensional)
    - network (nodes and edges)

    Also identify visual family (basic, statistical, advanced, specialized)
    and any variants (e.g., grouped-bar, bubble-scatter)"
    """

    response = await vision_api.analyze(
        image=preview_image,
        task="classify_plot_type",
        options={
            "types": ["line", "bar", "scatter", "heatmap", "pie", "3d", "network"],
            "families": ["basic", "statistical", "advanced", "specialized"],
            "detect_variants": True
        }
    )

    return {
        "plot_type": {
            "primary": response.type,
            "family": response.family,
            "variants": response.variants
        }
    }
```

**Validation**:
```python
# Code says "scatter", Vision AI says "scatter" → Confidence 1.0
# Code says "scatter", Vision AI says "bubble" → Confidence 0.9 (bubble is scatter variant)
# Code says "scatter", Vision AI says "line" → Confidence 0.5 (FLAG FOR REVIEW)
```

**Example Output**:
```json
{
  "plot_type": {
    "primary": "scatter",
    "family": "basic",
    "variants": ["2d", "colored"]
  }
}
```

---

### Step 3: Detect Data Type

**Source**: Specification + Code (function signature)

**Method**: NLP analysis of spec + parameter types

**Spec Analysis**:
```python
def detect_data_type_from_spec(spec: str) -> dict:
    """
    Extract data type from spec description

    Keywords to look for:
    - "time series", "temporal" → timeseries
    - "categories", "categorical" → categorical
    - "latitude", "geospatial" → geospatial
    - "network", "graph", "nodes" → network
    - "table", "dataframe", "rows" → tabular
    - "hierarchy", "tree" → hierarchical
    """

    # NLP keyword extraction
    keywords = extract_keywords_from_spec(spec)

    # Mapping
    keyword_to_datatype = {
        "timeseries": ["time series", "temporal", "datetime", "timestamp"],
        "categorical": ["categories", "categorical", "groups", "factors"],
        "tabular": ["table", "dataframe", "rows", "columns", "csv"],
        "geospatial": ["latitude", "longitude", "map", "geographic"],
        "network": ["network", "graph", "nodes", "edges"],
        "hierarchical": ["hierarchy", "tree", "parent-child"]
    }

    # Find best match
    detected_types = []
    for dtype, kw_list in keyword_to_datatype.items():
        if any(kw in keywords for kw in kw_list):
            detected_types.append(dtype)

    # Primary = most specific, Secondary = additional characteristics
    primary = select_most_specific(detected_types)
    secondary = [dt for dt in detected_types if dt != primary]

    return {
        "data_type": {
            "primary": primary,
            "secondary": secondary,
            "format": detect_format_from_code(code)  # e.g., "dataframe", "json"
        }
    }
```

**Code Analysis** (parameter types):
```python
def detect_format_from_code(code: str) -> str:
    """
    Look at function signature for data format

    def create_plot(data: pd.DataFrame, ...) → "dataframe"
    def create_plot(data: dict, ...) → "json"
    def create_plot(data: gpd.GeoDataFrame, ...) → "geodataframe"
    """

    # Extract type hint from 'data' parameter
    type_hint = extract_type_hint(code, param_name="data")

    type_to_format = {
        "pd.DataFrame": "dataframe",
        "DataFrame": "dataframe",
        "dict": "json",
        "list": "array",
        "np.ndarray": "array",
        "gpd.GeoDataFrame": "geodataframe",
        # ...
    }

    return type_to_format.get(type_hint, "unknown")
```

**Example Output**:
```json
{
  "data_type": {
    "primary": "tabular",
    "secondary": ["numerical"],
    "format": "dataframe"
  }
}
```

---

### Step 4: Classify Domain

**Source**: Specification description + Spec filename + Keywords

**Method**: LLM classification with predefined categories

**Classification Prompt**:
```python
async def classify_domain(spec_description: str, spec_id: str) -> dict:
    """
    Use LLM to classify into primary domain

    Domains (from tagging-system.md):
    - finance (stock, trading, portfolio, crypto)
    - research (experiment, hypothesis, publication, academic)
    - data-science (ML, EDA, feature-engineering, model-evaluation)
    - business (KPI, dashboard, sales, marketing, operations)
    - engineering (signal-processing, control, simulation, technical)
    - healthcare (clinical, epidemiology, genomics, medical)
    - general (if none of above fit)
    """

    prompt = f"""
Classify this plot specification into a primary domain:

Spec ID: {spec_id}
Description: {spec_description}

Domains:
1. finance - Financial markets, trading, portfolio analysis
2. research - Academic research, experiments, publications
3. data-science - Machine learning, data analysis, modeling
4. business - Business intelligence, KPIs, dashboards
5. engineering - Technical analysis, simulations, control systems
6. healthcare - Medical data, clinical trials, epidemiology
7. general - General-purpose, no specific domain

Instructions:
- Choose PRIMARY domain (best fit)
- List SECONDARY domains (if applicable)
- If domain-specific: identify INDUSTRY subcategory
- Confidence score 0-1

Example response:
{{
  "domain": {{
    "primary": "finance",
    "secondary": ["data-science"],
    "industry": "fintech"
  }},
  "confidence": 0.9,
  "reasoning": "Spec mentions stock prices, candlestick charts, and trading - clearly finance domain"
}}
"""

    response = await llm_api.classify(prompt, model="claude-3-haiku")
    return response
```

**Confidence Thresholds**:
- ≥0.9: Clear domain-specific language (e.g., "candlestick", "OHLC" → finance)
- 0.7-0.9: Domain indicators present but not explicit
- 0.5-0.7: Unclear domain, could fit multiple (use "general")
- <0.5: FLAG FOR MANUAL REVIEW

**Example Output**:
```json
{
  "domain": {
    "primary": "data-science",
    "secondary": ["research"],
    "industry": null
  }
}
```

---

### Step 5: Identify Features

**Source**: Code structure + Spec requirements + Preview

**Method**: Code analysis + inference

**Interactivity Detection**:
```python
def detect_interactivity(code: str, library: str) -> str:
    """
    Determine if plot is static, interactive, or animated

    Static:
    - matplotlib (default) → static
    - Output: plt.savefig() → static

    Interactive:
    - plotly, bokeh, altair → interactive
    - matplotlib with widgets → interactive

    Animated:
    - matplotlib.animation → animated
    - plotly with frames → animated
    """

    if library in ["plotly", "bokeh", "altair"]:
        # Check if animation frames present
        if "frames=" in code or "animate(" in code:
            return "animated"
        return "interactive"

    elif library == "matplotlib":
        if "animation." in code or "FuncAnimation" in code:
            return "animated"
        elif "widgets." in code or "ipywidgets" in code:
            return "interactive"
        else:
            return "static"

    # Seaborn inherits matplotlib behavior
    elif library == "seaborn":
        return "static"

    return "static"  # default
```

**Complexity Detection**:
```python
def calculate_complexity(code: str) -> str:
    """
    Determine complexity level based on code characteristics

    Beginner (<20 lines):
    - Single plot function
    - Minimal customization
    - No custom classes

    Intermediate (20-100 lines):
    - Multiple customization options
    - Some styling
    - Parameter validation

    Advanced (>100 lines):
    - Custom classes
    - Complex algorithms
    - Multiple subplots/panels
    """

    # Count lines (excluding comments/blanks)
    code_lines = count_code_lines(code)

    # Count complexity indicators
    complexity_score = 0

    if has_custom_classes(code):
        complexity_score += 30

    if has_multiple_subplots(code):
        complexity_score += 20

    if has_advanced_styling(code):
        complexity_score += 15

    if code_lines > 100:
        complexity_score += 40

    # Classification
    if complexity_score < 30 or code_lines < 20:
        return "beginner"
    elif complexity_score < 60 or code_lines < 100:
        return "intermediate"
    else:
        return "advanced"
```

**Performance Detection**:
```python
def detect_performance_features(code: str, spec: str) -> list[str]:
    """
    Identify performance-related features

    Features to detect:
    - real-time: Mentions streaming, live data, FuncAnimation
    - large-scale: Mentions datashader, decimation, >1M points
    - lightweight: No heavy dependencies, small memory footprint
    """

    features = []

    # Real-time indicators
    if any(kw in code.lower() for kw in ["stream", "live", "funcanimation", "real-time"]):
        features.append("real-time")

    # Large-scale indicators
    if any(kw in code.lower() for kw in ["datashader", "decimation", "resample"]):
        features.append("large-scale")

    if any(kw in spec.lower() for kw in ["million", "large dataset", "big data"]):
        features.append("large-scale")

    # Lightweight (default if no heavy features)
    if not features:
        features.append("lightweight")

    return features
```

**Example Output**:
```json
{
  "features": {
    "interactivity": "static",
    "complexity": "beginner",
    "performance": ["lightweight"],
    "special": ["export-ready", "publication-quality"]
  }
}
```

---

## Tag Validation

### Validation Checklist

Before storing tags, validate:

```python
def validate_tags(tags: dict) -> ValidationResult:
    """
    Validate generated tags against taxonomy

    Checks:
    1. All required dimensions present (library, plot_type, data_type, domain, features)
    2. Values match allowed taxonomy (from tagging-system.md)
    3. Confidence scores within range [0, 1]
    4. No conflicting tags (e.g., "static" + "animated")
    5. Primary + secondary tags make sense together
    """

    errors = []

    # Check 1: Required dimensions
    required = ["library", "plot_type", "data_type", "domain", "features"]
    for dim in required:
        if dim not in tags:
            errors.append(f"Missing dimension: {dim}")

    # Check 2: Valid taxonomy values
    taxonomy = load_taxonomy()  # From tagging-system.md

    if tags["library"]["primary"] not in taxonomy["libraries"]:
        errors.append(f"Invalid library: {tags['library']['primary']}")

    if tags["plot_type"]["primary"] not in taxonomy["plot_types"]:
        errors.append(f"Invalid plot_type: {tags['plot_type']['primary']}")

    # Check 3: Confidence scores
    if "confidence_scores" in tags:
        for dim, score in tags["confidence_scores"].items():
            if not 0 <= score <= 1:
                errors.append(f"Invalid confidence score for {dim}: {score}")

    # Check 4: Conflicting tags
    if tags["features"]["interactivity"] in ["static", "interactive", "animated"]:
        # Valid
        pass
    else:
        errors.append(f"Invalid interactivity: {tags['features']['interactivity']}")

    # Check 5: Primary/secondary consistency
    if tags["library"]["primary"] in tags["library"]["secondary"]:
        errors.append("Primary library cannot be in secondary")

    return ValidationResult(
        valid=len(errors) == 0,
        errors=errors
    )
```

### Validation Actions

```python
if validation.valid:
    # Store tags
    store_tags_in_firestore(tags)
else:
    if all_critical_errors(validation.errors):
        # Critical: Cannot store
        raise TagValidationError(validation.errors)
    else:
        # Non-critical: Store with warning flag
        tags["metadata"]["validation_warnings"] = validation.errors
        store_tags_in_firestore(tags)
```

---

## Output Format

### Complete Tag Structure

```json
{
  "plot_id": "scatter-basic-001",
  "spec_id": "scatter-basic-001",
  "implementation_path": "plots/matplotlib/scatter/scatter-basic-001/default.py",

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
      "primary": "data-science",
      "secondary": ["research"],
      "industry": null
    },
    "features": {
      "interactivity": "static",
      "complexity": "beginner",
      "performance": ["lightweight"],
      "special": ["export-ready"]
    }
  },

  "search_keywords": [
    "scatter", "matplotlib", "basic", "2d",
    "data-science", "dataframe", "simple", "beginner"
  ],

  "similarity_clusters": {
    "visual_cluster": "scatter-family",
    "technical_cluster": "basic-plots",
    "domain_cluster": "data-science-eda"
  },

  "confidence_scores": {
    "library": 1.0,
    "plot_type": 0.95,
    "data_type": 0.9,
    "domain": 0.75,
    "features": 0.85,
    "overall": 0.89
  },

  "metadata": {
    "tagged_by": "claude-auto-tagger-v1.0.0",
    "tagging_rules_version": "v1.0.0-draft",
    "created": "2025-01-23T10:30:00Z",
    "human_verified": false,
    "validation_warnings": []
  }
}
```

---

## Search Keywords Generation

Auto-generate search keywords from tags:

```python
def generate_search_keywords(tags: dict, spec: dict) -> list[str]:
    """
    Generate comprehensive search keywords

    Sources:
    1. All tag values (primary + secondary)
    2. Spec title words
    3. Spec description keywords
    4. Library-specific terms
    5. Domain-specific terms
    """

    keywords = set()

    # Add all tag values
    keywords.add(tags["library"]["primary"])
    keywords.update(tags["library"]["secondary"])
    keywords.add(tags["plot_type"]["primary"])
    keywords.update(tags["plot_type"].get("variants", []))
    keywords.add(tags["data_type"]["primary"])
    keywords.update(tags["data_type"]["secondary"])
    keywords.add(tags["domain"]["primary"])

    # Add spec-derived keywords
    spec_keywords = extract_keywords_from_text(spec["description"])
    keywords.update(spec_keywords[:10])  # Top 10 keywords

    # Add synonyms
    synonyms = {
        "scatter": ["scatterplot", "point-cloud", "xy-plot"],
        "line": ["lineplot", "timeseries", "trend"],
        "bar": ["barplot", "barchart", "column"],
        # ... full mapping
    }

    for kw in list(keywords):
        if kw in synonyms:
            keywords.update(synonyms[kw])

    # Remove generic words
    stop_words = {"plot", "chart", "graph", "visualization", "data"}
    keywords = keywords - stop_words

    return sorted(list(keywords))
```

---

## Confidence Scoring

### Overall Confidence Calculation

```python
def calculate_overall_confidence(dimension_scores: dict) -> float:
    """
    Weighted average of dimension confidence scores

    Weights:
    - library: 0.3 (most reliable - clear from imports)
    - plot_type: 0.25 (very reliable - code + visual)
    - data_type: 0.2 (reliable - spec + code)
    - domain: 0.15 (less reliable - inference)
    - features: 0.1 (least reliable - heuristic)
    """

    weights = {
        "library": 0.3,
        "plot_type": 0.25,
        "data_type": 0.2,
        "domain": 0.15,
        "features": 0.1
    }

    overall = sum(
        dimension_scores[dim] * weights[dim]
        for dim in weights
    )

    return round(overall, 2)
```

### Action Based on Confidence

```python
if overall_confidence >= 0.85:
    # High confidence - auto-approve
    action = "auto_approve"

elif overall_confidence >= 0.70:
    # Medium confidence - flag for human review
    action = "flag_for_review"

else:
    # Low confidence - require human tagging
    action = "manual_tagging_required"
```

---

## Examples

### Example 1: Simple Scatter Plot

**Input**:
```python
# Code
def create_plot(data: pd.DataFrame, x: str, y: str) -> Figure:
    fig, ax = plt.subplots()
    ax.scatter(data[x], data[y])
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    return fig

# Spec
"Basic 2D scatter plot for visualizing relationship between two numerical variables"
```

**Output Tags**:
```json
{
  "library": {"primary": "matplotlib", "secondary": []},
  "plot_type": {"primary": "scatter", "family": "basic", "variants": ["2d"]},
  "data_type": {"primary": "tabular", "secondary": ["numerical"], "format": "dataframe"},
  "domain": {"primary": "general", "secondary": [], "industry": null},
  "features": {
    "interactivity": "static",
    "complexity": "beginner",
    "performance": ["lightweight"]
  },
  "confidence_scores": {
    "library": 1.0,
    "plot_type": 1.0,
    "data_type": 0.95,
    "domain": 0.6,
    "features": 0.9,
    "overall": 0.89
  }
}
```

---

### Example 2: Financial Candlestick

**Input**:
```python
# Code
import plotly.graph_objects as go

def create_plot(data: pd.DataFrame) -> go.Figure:
    fig = go.Figure(data=[go.Candlestick(
        x=data['date'],
        open=data['open'],
        high=data['high'],
        low=data['low'],
        close=data['close']
    )])
    return fig

# Spec
"Interactive candlestick chart for financial market analysis (OHLC data)"
```

**Output Tags**:
```json
{
  "library": {"primary": "plotly", "secondary": []},
  "plot_type": {"primary": "candlestick", "family": "financial", "variants": ["ohlc"]},
  "data_type": {"primary": "timeseries", "secondary": ["tabular"], "format": "dataframe"},
  "domain": {"primary": "finance", "secondary": ["trading"], "industry": "fintech"},
  "features": {
    "interactivity": "interactive",
    "complexity": "intermediate",
    "performance": ["real-time"],
    "special": ["responsive"]
  },
  "confidence_scores": {
    "library": 1.0,
    "plot_type": 1.0,
    "data_type": 1.0,
    "domain": 0.95,
    "features": 0.9,
    "overall": 0.97
  }
}
```

---

## Quality Criteria for Tags

Tags are considered high-quality if:

- ✅ All 5 dimensions present
- ✅ Overall confidence ≥ 0.85
- ✅ No validation errors
- ✅ Primary tags are specific (not "general", "unknown")
- ✅ Search keywords include spec-specific terms (not just generic)
- ✅ Similarity clusters assigned

Tags need review if:

- ⚠️ Confidence 0.70 - 0.84
- ⚠️ Validation warnings present
- ⚠️ Domain = "general" (could be more specific?)
- ⚠️ Low confidence on multiple dimensions

Tags are rejected if:

- ❌ Overall confidence < 0.70
- ❌ Critical validation errors
- ❌ Missing required dimensions
- ❌ Contradictory tags

---

## Integration with Generation Workflow

### Workflow Position

```
1. Generate Code (code-generation-rules.md)
   ↓
2. Self-Review (self-review-checklist.md)
   ↓
3. Quality Check (quality-criteria.md)
   ↓
4. Generate Preview (execute code, save PNG)
   ↓
5. AUTO-TAG (tagging-rules.md) ← THIS STEP
   ↓
6. Store in Database (with tags)
   ↓
7. Publish
```

### When to Tag

**Trigger**: After quality check passes (score ≥ 85)

**Rationale**: Only tag plots that meet quality standards. Low-quality plots will be regenerated anyway, so don't waste resources tagging them.

---

## Appendix: Function Mapping

### Matplotlib

```python
MATPLOTLIB_FUNCTION_TO_TYPE = {
    "scatter": "scatter",
    "plot": "line",
    "bar": "bar",
    "barh": "bar",
    "hist": "histogram",
    "boxplot": "boxplot",
    "violinplot": "violin",
    "imshow": "heatmap",
    "contour": "contour",
    "contourf": "contour",
    "pie": "pie",
    "polar": "polar",
    "fill_between": "area",
    "stem": "stem",
    "step": "step",
    "quiver": "quiver",
    "streamplot": "streamplot"
}
```

### Seaborn

```python
SEABORN_FUNCTION_TO_TYPE = {
    "scatterplot": "scatter",
    "lineplot": "line",
    "barplot": "bar",
    "countplot": "bar",
    "boxplot": "boxplot",
    "violinplot": "violin",
    "stripplot": "strip",
    "swarmplot": "swarm",
    "pointplot": "point",
    "heatmap": "heatmap",
    "clustermap": "heatmap",
    "kdeplot": "kde",
    "histplot": "histogram",
    "ecdfplot": "ecdf",
    "rugplot": "rug",
    "pairplot": "pairplot",
    "jointplot": "jointplot",
    "lmplot": "regression",
    "regplot": "regression",
    "residplot": "residual"
}
```

### Plotly

```python
PLOTLY_FUNCTION_TO_TYPE = {
    "scatter": "scatter",
    "line": "line",
    "bar": "bar",
    "histogram": "histogram",
    "box": "boxplot",
    "violin": "violin",
    "strip": "strip",
    "scatter_3d": "3d",
    "line_3d": "3d",
    "surface": "3d",
    "mesh_3d": "3d",
    "heatmap": "heatmap",
    "contour": "contour",
    "pie": "pie",
    "sunburst": "sunburst",
    "treemap": "treemap",
    "funnel": "funnel",
    "scatter_geo": "geospatial",
    "choropleth": "geospatial",
    "density_heatmap": "heatmap",
    "candlestick": "candlestick",
    "ohlc": "ohlc",
    "waterfall": "waterfall",
    "sankey": "sankey",
    "parallel_coordinates": "parallel",
    "parallel_categories": "parallel"
}
```

---

## Known Limitations (v1.0.0-draft)

1. **Domain classification**: Relies on keyword matching and LLM inference - may misclassify ambiguous specs
2. **Visual analysis**: Requires Vision AI - adds latency and cost
3. **Multi-library plots**: Code that uses multiple libraries may have unclear primary library
4. **Custom plot types**: New/unusual plot types not in taxonomy will be tagged as "unknown"
5. **No user feedback loop**: Tags cannot be corrected by users (yet)

---

## Future Improvements (v1.1.0+)

1. **User feedback**: Allow manual tag correction → retrain classification model
2. **Custom taxonomy**: Support project-specific tag categories
3. **Cross-library equivalence**: Tag "matplotlib scatter" ≈ "seaborn scatterplot"
4. **Automatic cluster discovery**: ML identifies new visual clusters
5. **Confidence calibration**: Improve scoring based on real-world validation data

---

*Version: v1.0.0-draft*
*Status: Draft - Not yet implemented*
*Last Updated: 2025-01-23*
