# barcode-ean13: EAN-13 Barcode

## Description

A standard EAN-13 barcode visualization commonly used for retail products worldwide. The plot renders a scannable linear barcode encoding a 13-digit number with proper bar widths, guard patterns, and human-readable digits. This visualization is essential for product identification, inventory management, and point-of-sale systems.

## Applications

- Product labeling for retail and e-commerce inventory management
- Supply chain tracking and logistics identification
- Educational demonstrations of barcode encoding technology
- Generating scannable labels for custom product catalogs

## Data

- `code` (string) - 12 or 13 digit numeric string; check digit auto-calculated if 12 digits provided
- Structure: First 2-3 digits = country code, next 4-5 digits = manufacturer code, next 5 digits = product code, final digit = check digit
- Size: Exactly 12 or 13 numeric characters
- Example: "5901234123457" (Polish product) or "4006381333931" (German product)

## Notes

- Include quiet zones (white space) of at least 9 module widths on left and 9 on right
- Render start guard (101), center guard (01010), and end guard (101) patterns
- Use standard bar width ratios: bars are 1, 2, 3, or 4 modules wide
- Display human-readable digits below the barcode with the first digit outside left guard
- Recommended output size: at least 200 pixels wide for reliable scanning
- Libraries: `python-barcode`, `treepoem`, or manual rendering with matplotlib
- Print resolution should be 300 DPI minimum for physical labels
