# {spec-id}: {Title}

## Description

{2-4 sentences describing what this plot visualizes and when to use it.
What makes it useful? What insights does it reveal?}

## Data

**Required columns:**
- `{column_name}` (numeric) - {what this column represents}
- `{column_name}` (categorical) - {what this column represents}

**Example:** *(optional - provide inline data, dataset reference, or omit for AI to generate)*
```python
# Option A: Inline data for simple plots
data = pd.DataFrame({
    "category": ["A", "B", "C", "D"],
    "value": [25, 40, 30, 35]
})

# Option B: Standard dataset reference
import seaborn as sns
data = sns.load_dataset('tips')

# Option C: Omit this section - AI generates appropriate sample data
```

## Tags

{type}, {purpose}, {complexity}

## Use Cases

- {Realistic scenario with domain context}
- {Another use case}
- {Third use case}
