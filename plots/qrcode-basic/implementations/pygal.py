"""pyplots.ai
qrcode-basic: Basic QR Code Generator
Library: pygal | Python 3.13
Quality: pending | Created: 2025-01-07
"""

import sys

import qrcode


# Temporarily remove current directory from path to avoid name collision
_cwd = sys.path[0] if sys.path[0] else "."
if _cwd in sys.path:
    sys.path.remove(_cwd)

from pygal.graph.graph import Graph  # noqa: E402
from pygal.style import Style  # noqa: E402


# Restore path
sys.path.insert(0, _cwd)


class QRCodeChart(Graph):
    """Custom QR Code visualization for pygal - renders QR matrix as SVG squares."""

    def __init__(self, *args, **kwargs):
        self.qr_data = kwargs.pop("qr_data", "https://pyplots.ai")
        self.error_correction = kwargs.pop("error_correction", qrcode.constants.ERROR_CORRECT_M)
        self.box_size = kwargs.pop("box_size", 10)
        self.border = kwargs.pop("border", 4)
        self.fill_color = kwargs.pop("fill_color", "#000000")
        self.back_color = kwargs.pop("back_color", "#FFFFFF")
        super().__init__(*args, **kwargs)
        self._qr_matrix = None

    def _generate_qr_matrix(self):
        """Generate QR code matrix using qrcode library."""
        qr = qrcode.QRCode(version=None, error_correction=self.error_correction, box_size=1, border=0)
        qr.add_data(self.qr_data)
        qr.make(fit=True)
        return qr.get_matrix()

    def _plot(self):
        """Draw the QR code as SVG rectangles."""
        # Generate QR matrix
        self._qr_matrix = self._generate_qr_matrix()
        if not self._qr_matrix:
            return

        matrix_size = len(self._qr_matrix)
        total_size = matrix_size + 2 * self.border  # Add quiet zone

        # Get plot dimensions
        plot_width = self.view.width
        plot_height = self.view.height

        # Calculate cell size to fit QR code in view with margins
        margin = 150  # Space for title
        available_size = min(plot_width, plot_height) - 2 * margin
        cell_size = available_size / total_size

        # Calculate offset to center the QR code
        qr_total_size = total_size * cell_size
        x_offset = self.view.x(0) + (plot_width - qr_total_size) / 2
        y_offset = self.view.y(total_size) + (plot_height - qr_total_size) / 2 + 50

        # Create group for the QR code
        plot_node = self.nodes["plot"]
        qr_group = self.svg.node(plot_node, class_="qr-code")

        # Draw background (quiet zone included)
        bg_rect = self.svg.node(qr_group, "rect", x=x_offset, y=y_offset, width=qr_total_size, height=qr_total_size)
        bg_rect.set("fill", self.back_color)
        bg_rect.set("stroke", "#CCCCCC")
        bg_rect.set("stroke-width", "2")

        # Draw QR code modules (black squares)
        for row_idx, row in enumerate(self._qr_matrix):
            for col_idx, cell in enumerate(row):
                if cell:  # Black module
                    x = x_offset + (col_idx + self.border) * cell_size
                    y = y_offset + (row_idx + self.border) * cell_size

                    rect = self.svg.node(qr_group, "rect", x=x, y=y, width=cell_size, height=cell_size)
                    rect.set("fill", self.fill_color)

        # Add encoded data label below the QR code
        label_y = y_offset + qr_total_size + 80
        label_x = x_offset + qr_total_size / 2
        font_size = 42

        # URL label
        text_node = self.svg.node(qr_group, "text", x=label_x, y=label_y)
        text_node.set("text-anchor", "middle")
        text_node.set("fill", "#306998")
        text_node.set("style", f"font-size:{font_size}px;font-weight:bold;font-family:sans-serif")
        text_node.text = self.qr_data

        # Error correction level label
        ec_labels = {
            qrcode.constants.ERROR_CORRECT_L: "Error Correction: L (7%)",
            qrcode.constants.ERROR_CORRECT_M: "Error Correction: M (15%)",
            qrcode.constants.ERROR_CORRECT_Q: "Error Correction: Q (25%)",
            qrcode.constants.ERROR_CORRECT_H: "Error Correction: H (30%)",
        }
        ec_label = ec_labels.get(self.error_correction, "")

        ec_node = self.svg.node(qr_group, "text", x=label_x, y=label_y + 60)
        ec_node.set("text-anchor", "middle")
        ec_node.set("fill", "#666666")
        ec_node.set("style", f"font-size:{int(font_size * 0.7)}px;font-family:sans-serif")
        ec_node.text = ec_label

        # Matrix size info
        size_node = self.svg.node(qr_group, "text", x=label_x, y=label_y + 110)
        size_node.set("text-anchor", "middle")
        size_node.set("fill", "#666666")
        size_node.set("style", f"font-size:{int(font_size * 0.7)}px;font-family:sans-serif")
        size_node.text = f"Matrix: {matrix_size} x {matrix_size} modules"

    def _compute(self):
        """Compute the box for rendering."""
        # Generate matrix to get size
        if self._qr_matrix is None:
            self._qr_matrix = self._generate_qr_matrix()

        matrix_size = len(self._qr_matrix) if self._qr_matrix else 21
        total_size = matrix_size + 2 * self.border

        self._box.xmin = 0
        self._box.xmax = total_size
        self._box.ymin = 0
        self._box.ymax = total_size


# Custom style for 3600x3600 square canvas (best for QR code)
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B"),
    title_font_size=72,
    legend_font_size=48,
    label_font_size=42,
    value_font_size=36,
    font_family="sans-serif",
)

# Data - URL to encode in QR code
qr_content = "https://pyplots.ai"

# Create QR code chart
chart = QRCodeChart(
    width=3600,
    height=3600,
    style=custom_style,
    title="qrcode-basic \u00b7 pygal \u00b7 pyplots.ai",
    qr_data=qr_content,
    error_correction=qrcode.constants.ERROR_CORRECT_M,
    border=4,
    fill_color="#000000",
    back_color="#FFFFFF",
    show_legend=False,
    margin=120,
    margin_top=200,
    margin_bottom=200,
    show_x_labels=False,
    show_y_labels=False,
)

# Add a dummy series to trigger _plot (pygal requires at least one series)
chart.add("", [0])

# Save output
chart.render_to_file("plot.svg")
chart.render_to_png("plot.png")

# Also save HTML for interactivity
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>qrcode-basic - pygal</title>
    <style>
        body {{ margin: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; background: #f5f5f5; }}
        .chart {{ max-width: 100%; height: auto; }}
    </style>
</head>
<body>
    <figure class="chart">
        {chart.render(is_unicode=True)}
    </figure>
</body>
</html>
"""

with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)
