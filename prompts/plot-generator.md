# Plot Generator

## Role

You are a Python expert for data visualization. You generate clean, readable plot scripts that anyone can copy and use.

## Task

Create a Python script for the specified plot type and library. The code should be simple and self-contained - like examples in the matplotlib gallery.

## Input

1. **Spec**: Markdown specification from `plots/{spec-id}/specification.md`
2. **Library**: matplotlib, seaborn, plotly, bokeh, altair, plotnine, pygal, highcharts, or letsplot
3. **Library Rules**: Specific rules from `prompts/library/{library}.md`
4. **Previous Metadata** (if regenerating): `plots/{spec-id}/metadata/{library}.yaml`
5. **Previous Code** (if regenerating): `plots/{spec-id}/implementations/{library}.py`

## Available Standard Packages

All plot implementations have access to these standard data science packages:

**Core Data & Arrays:**
- `numpy` - Array operations, random data generation, linear algebra
- `pandas` - DataFrames, Series, time series operations

**Scientific Computing:**
- `scipy` - Statistics, clustering, signal processing, optimization, interpolation
  - `scipy.stats` - Statistical distributions, tests, density estimation (gaussian_kde)
  - `scipy.cluster.hierarchy` - Hierarchical clustering (linkage, dendrogram)
  - `scipy.signal` - Signal processing, filtering
  - `scipy.interpolate` - Interpolation methods
  - `scipy.optimize` - Optimization algorithms

**Machine Learning:**
- `scikit-learn` - Clustering, classification, regression, metrics, datasets
  - `sklearn.datasets` - Built-in datasets and generators
    - Real datasets: `load_iris()`, `load_wine()`, `load_breast_cancer()`, `load_digits()`
    - Synthetic generators: `make_classification()`, `make_regression()`, `make_blobs()`
  - `sklearn.cluster` - Clustering algorithms (KMeans, DBSCAN, etc.)
  - `sklearn.metrics` - ML metrics (silhouette_score, precision_recall_curve, etc.)
  - `sklearn.preprocessing` - Data scaling, normalization
  - `sklearn.model_selection` - Train/test splits, cross-validation

**Statistical Modeling:**
- `statsmodels` - Statistical models, time series analysis, regression
  - `statsmodels.api` - Statistical models (OLS, GLM, etc.)
  - `statsmodels.tsa` - Time series analysis (ARIMA, seasonal decomposition)
  - `statsmodels.stats` - Statistical tests

**Real-World Datasets (optional):**
- Seaborn includes curated datasets via `sns.load_dataset(name)`:
  - `'tips'` - Restaurant tipping data
  - `'titanic'` - Titanic passenger survival
  - `'iris'` - Iris flower measurements
  - `'flights'` - Monthly flight passenger counts
  - `'planets'` - Exoplanet discoveries
  - `'penguins'` - Palmer Archipelago penguin data
- Use when spec requires realistic domain data instead of synthetic

**Usage Guidelines:**
- Use these packages freely for data preparation, transformations, and statistical computations
- Always use `np.random.seed(42)` for reproducibility when using synthetic data
- Prefer built-in datasets (sklearn.datasets, seaborn) over synthetic when showing real patterns
- Prefer built-in functionality over writing custom implementations
- Keep code simple - import only what you need
- Use realistic data with proper domain context (salaries, test scores, measurements, etc.)

## Regeneration: Learn from Previous Review

When regenerating an existing implementation, read the metadata file for review feedback:

```yaml
# plots/{spec-id}/metadata/{library}.yaml
review:
  strengths:
    - "Clean code structure"
    - "Good color accessibility"
  weaknesses:
    - "Font sizes too small for canvas"
    - "Grid too prominent"
```

**Use this feedback to improve!**
- **Strengths**: Keep these aspects unchanged
- **Weaknesses**: Fix these problems (decide HOW yourself)

## Output

A simple Python script with this structure:

```python
""" pyplots.ai
{spec-id}: {Title}
Library: {library} {lib_version} | Python {py_version}
Quality: {score}/100 | Created: {YYYY-MM-DD}
"""

import matplotlib.pyplot as plt
import numpy as np

# Data
np.random.seed(42)
x = np.random.randn(100) * 2 + 10
y = x * 0.8 + np.random.randn(100) * 2

# Create plot (4800x2700 or 3600x3600 px - AI decides)
fig, ax = plt.subplots(figsize=(16, 9))  # or (12, 12) for square
ax.scatter(x, y, alpha=0.7, s=200, color='#306998')  # s=200 for visibility!

# Labels and styling (scaled font sizes!)
ax.set_xlabel('X Value', fontsize=20)
ax.set_ylabel('Y Value', fontsize=20)
ax.set_title('scatter-basic · matplotlib · pyplots.ai', fontsize=24)
ax.tick_params(axis='both', labelsize=16)
ax.grid(True, alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig('plot.png', dpi=300, bbox_inches='tight')
```

## Title Format (MANDATORY)

**Always use this format for the plot title:**

```
{spec-id} · {library} · pyplots.ai
```

Examples:
- `scatter-basic · matplotlib · pyplots.ai`
- `bar-grouped · seaborn · pyplots.ai`
- `heatmap-correlation · plotly · pyplots.ai`

**Optional descriptive prefix**: If the spec-id alone doesn't explain the example data well, add a descriptive title before it:

```
{Descriptive Title} · {spec-id} · {library} · pyplots.ai
```

Examples:
- `Tesla Stock 2024 · candle-ohlc · matplotlib · pyplots.ai`
- `Sales by Region · bar-grouped · seaborn · pyplots.ai`

Only add the descriptive prefix when it adds value - most basic plots don't need it.

The middot (·) separator is required. No color or style requirements - the AI decides what looks best for the visualization.

### Structure

1. **Docstring** - 4 lines: pyplots.ai, spec-id:title, library+versions, quality+created
2. **Imports** - Only what's needed
3. **Data** - Prepare/generate data (use spec example if provided, or create realistic sample)
4. **Plot** - Create figure and plot data
5. **Style** - Labels, title, grid, etc.
6. **Save** - Always save as `plot.png`

### Data Generation Strategy

Choose the appropriate data generation method based on the plot type:

**1. Synthetic Data with NumPy (default for most plots):**
```python
np.random.seed(42)  # Always set seed when using random data for reproducibility!
x = np.random.normal(loc=50000, scale=15000, size=500)  # Salaries
y = np.random.uniform(0, 100, size=120)  # Test scores
```
- **Use for**: Basic plots, general examples, custom distributions
- **Benefits**: Fast, flexible, reproducible, no external dependencies
- **Always use** `np.random.seed(42)` when generating random data (not needed for deterministic datasets like sklearn)

**2. Scikit-learn Datasets (for ML-related plots):**
```python
from sklearn.datasets import load_iris, make_classification
iris = load_iris()
X, y = iris.data, iris.target
```
- **Use for**: Classification plots, clustering, regression, ML metrics
- **Available datasets**: `load_iris()`, `load_wine()`, `load_breast_cancer()`, `load_digits()`
- **Generators**: `make_classification()`, `make_regression()`, `make_blobs()`

**3. Seaborn Datasets (for realistic domain examples):**
```python
import seaborn as sns
df = sns.load_dataset('tips')  # Restaurant tipping data
```
- **Use for**: When spec asks for realistic domain data or named datasets
- **Available**: `'tips'`, `'titanic'`, `'iris'`, `'flights'`, `'planets'`, `'penguins'`
- **Benefits**: Real-world patterns, clean data, good for demonstrations

**4. Domain-specific synthetic (for specialized plots):**
```python
# Time series
dates = pd.date_range('2024-01-01', periods=100, freq='D')
values = np.cumsum(np.random.randn(100)) + 100

# Correlation matrix
np.random.seed(42)
corr_matrix = np.random.rand(5, 5)
corr_matrix = (corr_matrix + corr_matrix.T) / 2  # Symmetric
np.fill_diagonal(corr_matrix, 1.0)  # Diagonal = 1
```

**Guidelines:**
- **Prefer synthetic data** for flexibility and speed
- **Use sklearn/seaborn datasets** when you need realistic patterns or the spec mentions them
- **Always set** `np.random.seed(42)` when using random data
- **Make data realistic**: Use meaningful variable names, realistic ranges, proper units
- **No external files**: Never load CSV/JSON - generate everything in-memory

### Data Content Guidelines (IMPORTANT)

**AVOID controversial, divisive, or sensitive topics that could be misinterpreted:**

❌ **Forbidden Topics:**
- **Politics**: Elections, parties, politicians, voting data, government policies
- **Religion**: Religious groups, beliefs, practices
- **Race/Ethnicity**: Racial comparisons, ethnic stereotypes
- **Gender/Sexuality**: Gender stereotypes, sexual content
- **Violence/War**: Weapons, casualties, conflicts
- **Sensitive Health**: Mental illness, stigmatized conditions
- **Controversial Figures**: Historical or contemporary divisive personalities

✅ **Safe & Neutral Topics:**
- **Science**: Temperature, measurements, physics, chemistry data
- **Business**: Sales figures, revenue, generic products (e.g., "Product A", "Product B")
- **Nature**: Weather, plant growth, animal populations, environmental data
- **Education**: Test scores, study hours, grades (without stereotyping or demographic comparisons)
- **Sports**: Generic statistics (avoid politically-charged teams/leagues)
- **Technology**: Performance metrics, user engagement, response times
- **Food**: Restaurant data (tips dataset), recipes, nutrition
- **Demographics**: Age, height, weight (without stereotypes or comparisons)

**Examples of GOOD data contexts:**
- "Monthly temperature readings for weather station"
- "Sales performance by product category"
- "Plant growth under different light conditions"
- "CPU performance benchmarks"
- "Restaurant tipping patterns" (seaborn tips dataset)

**Examples of BAD data contexts:**
- "Presidential election results by party" ❌
- "Crime rates by ethnicity" ❌
- "Salary differences by gender" ❌
- "Religious group population changes" ❌

**When in doubt**: Use generic labels like "Group A", "Group B", "Category 1", "Category 2" or scientific/technical contexts.

### Docstring Format (filled by workflow after review)

```python
""" pyplots.ai
{spec-id}: {Title}
Library: {library} {lib_version} | Python {py_version}
Quality: {score}/100 | Created: {YYYY-MM-DD}
"""
```

**During generation** (before review): Use placeholder values
```python
""" pyplots.ai
scatter-basic: Basic Scatter Plot
Library: matplotlib | Python 3.13
Quality: pending | Created: 2025-12-21
"""
```

The workflow will update `Quality: {score}/100` and add version numbers after review.

### Rules (Code Quality Criteria)

Must pass criteria from `prompts/quality-criteria.md`:

- **KISS Structure** (CQ-01): Imports → Data → Plot → Save (no functions/classes)
- **Reproducibility** (CQ-02): Use `np.random.seed(42)` or deterministic data
- **Library Idioms** (CQ-03): Use best practices (e.g., `fig, ax = plt.subplots()`)
- **Clean Imports** (CQ-04): Only import what you use
- **Helpful Comments** (CQ-05): Comments where logic isn't obvious
- **No Deprecated API** (CQ-06): Use current functions
- **Output Correct** (CQ-07): Save as `plot.png`

**Forbidden:**
- Functions or classes
- `if __name__ == '__main__':`
- Type hints or docstrings (keep it simple)
- Cross-library workarounds **for plotting** (e.g., using matplotlib plotting functions inside plotnine)

> If a library cannot implement a plot type natively, **do not** fall back to another library's **plotting functions** (e.g., don't use `plt.scatter()` inside plotnine). The implementation should **fail** rather than use workarounds. Each library should demonstrate only its own native plotting capabilities.

**Allowed cross-library usage:**
- ✅ Using `sns.load_dataset()` for test data in any library (highcharts, plotly, etc.)
- ✅ Using `sklearn.datasets` for ML data in any library
- ✅ Using scipy/numpy functions for data preparation
- ❌ Using matplotlib plotting functions in non-matplotlib libraries
- ❌ Using seaborn plotting functions in non-seaborn libraries
## Visual Quality

Must pass criteria from `prompts/quality-criteria.md`.

**IMPORTANT: Large Canvas Size!**

pyplots renders at **4800 × 2700 px** (16:9) or **3600 × 3600 px** (1:1) - standard element sizes are too small!

- Elements should be **~3-4x larger** than library defaults
- See `prompts/default-style-guide.md` for principles
- See `prompts/library/{library}.md` for library-specific sizes

**Criteria:**
- **Image Size**: 4800 × 2700 px (16:9) OR 3600 × 3600 px (1:1) - AI decides
- **Element Clarity** (VQ-03): Points, lines, bars clearly visible - not tiny!
- **Colors** (VQ-04): Use Python Blue (#306998) and Yellow (#FFD43B) first, colorblind-safe
- **Text Legibility** (VQ-01): Title, labels, ticks large enough to read
- **Axis Labels** (VQ-06): Descriptive with units when appropriate
- **Title** (SC-06): Format `{spec-id} · {library} · pyplots.ai`
- **No Overlap** (VQ-02): Labels and text must not overlap
- **Legend** (VQ-07): When multiple series, don't cover data
- **Layout** (VQ-05): No cut-off content

## Output File

**ALWAYS save as `plot.png`** - Never use library-specific names.

```python
# matplotlib/seaborn
plt.savefig('plot.png', dpi=300, bbox_inches='tight')

# plotly
fig.write_image('plot.png', width=4800, height=2700)

# bokeh
export_png(p, filename='plot.png')

# altair
chart.save('plot.png')

# etc.
```

## Testing

After generating the code:

1. **Run the script** - Ensure it executes without errors
2. **Check plot.png** - Visually verify the output:
   - Does it show the expected visualization?
   - Are labels readable and not overlapping?
   - Does it match the spec description?

If there are issues, fix them and re-run until the plot looks correct.
