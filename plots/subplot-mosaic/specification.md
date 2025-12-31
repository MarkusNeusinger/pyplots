# subplot-mosaic: Mosaic Subplot Layout with Varying Sizes

## Description

A complex subplot layout where different subplots can have varying sizes and arrangements using intuitive ASCII-art style string definitions. Unlike GridSpec approaches that require explicit row/column spanning, mosaic layouts allow defining layouts through visual string patterns (e.g., "AB;CC" creates A and B on top, C spanning below), making complex configurations more readable and maintainable.

## Applications

- Dashboard layouts with a dominant visualization surrounded by smaller supporting charts
- Scientific figures where related plots need non-uniform visual emphasis
- Multi-panel reports combining wide time series with stacked detail panels
- Exploratory data analysis layouts with flexible panel arrangements

## Data

- `x` (numeric or categorical) - Primary variable for each subplot
- `y` (numeric) - Secondary variable for each subplot
- `z` (numeric, optional) - Tertiary variable for color or size encoding
- Size: Varies per subplot, typically 20-500 points per cell
- Example: Dashboard with wide overview chart (top), two medium detail charts (middle), and three small metric panels (bottom)

## Notes

- Layout defined using string patterns where repeated characters indicate spanning
- Support patterns like "AAB;AAB;CCC" for complex asymmetric layouts
- Allow empty cells using placeholder characters (e.g., "." for gaps)
- Maintain consistent spacing between all subplots
- Clear visual hierarchy with larger cells for primary data
- Each cell can contain a different plot type (line, bar, scatter, etc.)
