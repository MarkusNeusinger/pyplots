# scatter-text: Scatter Plot with Text Labels Instead of Points

## Description

A scatter plot where data points are represented by text labels instead of markers. Each label is positioned at its corresponding coordinates, making the text itself the visual element. This visualization is particularly useful for displaying named entities in 2D space, such as word embeddings, dimensionality reduction outputs, or any scenario where identifying individual items by name is more important than seeing their relative density.

## Applications

- Visualizing word embeddings or document embeddings after t-SNE or UMAP dimensionality reduction
- Displaying product or brand positioning in a competitive landscape analysis
- Showing author or journal relationships in bibliometric studies
- Mapping company positions based on two business metrics where company names matter

## Data

- `x` (numeric) - Horizontal coordinate for each text label
- `y` (numeric) - Vertical coordinate for each text label
- `label` (string) - The text to display at each coordinate position
- Size: 20-100 points recommended to balance readability and visual density
- Example: Named entities with 2D coordinates from dimensionality reduction

## Notes

- Text labels should be legible with appropriate font size
- Consider using alpha transparency when labels overlap
- Font size may need adjustment based on the number of labels
- For dense regions, consider rotating text or using smaller fonts
- Color can encode additional categorical or numeric information
