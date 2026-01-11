# barcode-code128: Code 128 Barcode

## Description

A Code 128 barcode visualization that encodes alphanumeric data into a high-density linear barcode pattern. Code 128 is a widely-used 1D barcode format that supports the full 128 ASCII character set, with three code subsets (A, B, C) that can be switched dynamically for optimal encoding efficiency. This visualization generates scannable barcodes commonly found on shipping labels, industrial parts, and healthcare specimens.

## Applications

- Generating shipping labels and package tracking codes for logistics operations
- Creating asset identification tags for inventory and equipment management
- Producing specimen and sample labels for healthcare and laboratory workflows
- Labeling industrial parts and components for manufacturing traceability
- Generating membership cards and badge barcodes for access control systems

## Data

- `content` (string) - The alphanumeric text to encode in the barcode
- `subset` (string, optional) - Preferred code subset: A (control + uppercase), B (ASCII printable), C (numeric pairs), or Auto
- Size: Up to 48 characters recommended for standard label width; supports full ASCII range
- Example: "SHIP-2024-ABC123" or "https://pyplots.ai"

## Notes

- Include quiet zones (white space) on left and right sides for reliable scanning
- Start pattern indicates the code subset (A, B, or C)
- Check digit is mandatory and calculated using modulo 103 algorithm
- Stop pattern is required at the end of every Code 128 barcode
- Human-readable text should appear below the barcode for visual verification
- Use high contrast black bars on white background for maximum scan reliability
- Recommended bar width ratio maintains standard Code 128 proportions
- Libraries: `python-barcode`, `reportlab`, or manual rendering with PIL/matplotlib
