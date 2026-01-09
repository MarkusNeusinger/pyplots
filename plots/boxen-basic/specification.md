# boxen-basic: Basic Boxen Plot (Letter-Value Plot)

## Description

A boxen plot (also known as letter-value plot) extends the traditional box plot to show more quantile information, making it ideal for large datasets with 1000+ observations. Instead of just displaying the median and quartiles, it shows additional "letter values" (eighths, sixteenths, etc.) as nested boxes, revealing the full shape of the distribution including tail behavior. This makes outlier detection more meaningful and distribution comparison more detailed.

## Applications

- Analyzing response time distributions across server clusters with millions of requests
- Comparing gene expression levels in large-scale genomics studies
- Quality control in manufacturing with high-volume production data
- Exploring salary or income distributions in large census datasets

## Data

- `category` (string) - group labels for comparison (optional for single distribution)
- `value` (numeric) - numerical values to plot
- Size: 1000-100000+ points per category, 1-8 categories
- Example: Server response times by endpoint, test scores by school

## Notes

- Show nested boxes representing letter values (median, quartiles, eighths, sixteenths, etc.)
- Boxes should decrease in width for deeper quantiles
- Use contrasting colors or shading to distinguish quantile levels
- Display outliers beyond the deepest letter value as individual points
- Include clear axis labels and legend explaining quantile levels
