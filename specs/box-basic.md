# box-basic

## Description
A basic box plot (box-and-whisker plot) showing the statistical distribution of multiple groups. The plot displays quartiles (Q1, median, Q3) as boxes, whiskers extending to show the range within 1.5 * IQR (interquartile range), and individual points for outliers beyond the whiskers.

## Data Requirements
- **Structure**: One numeric column for values and one categorical column for groups
- **Minimum Data**: At least 5 data points per group for meaningful statistics
- **Data Types**:
  - Values: Numeric (float or int)
  - Groups: Categorical (string or numeric)

## Visual Requirements
### Core Elements
- **Boxes**: Rectangle from Q1 to Q3 for each group
- **Median Line**: Horizontal line at median within each box
- **Whiskers**: Lines extending from box to min(Q3 + 1.5*IQR, max_value) and max(Q1 - 1.5*IQR, min_value)
- **Outliers**: Individual points for values beyond whiskers
- **X-axis**: Categorical groups
- **Y-axis**: Value scale

### Styling
- **Colors**: Different colors for each box (optional, but enhances readability)
- **Box Width**: Proportional to available space, with gaps between boxes
- **Grid**: Horizontal grid lines for value reference
- **Labels**: Clear axis labels and title

## Implementation Requirements
### Data Generation
Generate sample data with:
- 4-5 groups (e.g., "Group A", "Group B", "Group C", "Group D")
- 30-50 data points per group
- Different distributions per group (e.g., different means and spreads)
- Some outliers in at least 2 groups
- Use deterministic random seed for reproducibility

### Key Features
1. **Statistical Display**: Show quartiles, median, range, and outliers
2. **Multiple Groups**: Compare distributions across categories
3. **Clear Labeling**: Title, axis labels, and group names
4. **Visual Clarity**: Distinguish boxes, whiskers, and outliers

## Example Use Cases
- Comparing performance metrics across different teams
- Analyzing price distributions across product categories
- Examining test scores across different classes
- Visualizing sensor readings from multiple devices
- Comparing response times across server regions

## Notes
- Box plots are excellent for comparing distributions and identifying outliers
- They provide a compact summary of data distribution
- Particularly useful when sample sizes vary across groups
- Non-parametric visualization (doesn't assume normal distribution)