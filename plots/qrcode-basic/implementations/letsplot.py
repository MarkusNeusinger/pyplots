""" pyplots.ai
qrcode-basic: Basic QR Code Generator
Library: letsplot 4.8.2 | Python 3.13.11
Quality: 92/100 | Created: 2026-01-07
"""

import pandas as pd
import qrcode
from lets_plot import (
    LetsPlot,
    aes,
    element_blank,
    element_text,
    geom_tile,
    ggplot,
    ggsave,
    ggsize,
    labs,
    scale_fill_manual,
    theme,
)


LetsPlot.setup_html()

# Generate QR code data
content = "https://pyplots.ai"
qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=1, border=4)
qr.add_data(content)
qr.make(fit=True)

# Get the QR code matrix (list of lists with True/False)
matrix = qr.get_matrix()
size = len(matrix)

# Convert to dataframe for lets-plot
rows = []
for y, row in enumerate(matrix):
    for x, cell in enumerate(row):
        rows.append({"x": x, "y": size - 1 - y, "fill": 1 if cell else 0})
df = pd.DataFrame(rows)

# Create the QR code visualization
plot = (
    ggplot(df, aes(x="x", y="y", fill="fill"))
    + geom_tile(width=1, height=1, show_legend=False)
    + scale_fill_manual(values=["#FFFFFF", "#000000"])
    + labs(title="qrcode-basic · letsplot · pyplots.ai")
    + ggsize(1200, 1200)
    + theme(
        plot_title=element_text(size=24, hjust=0.5),
        axis_title=element_blank(),
        axis_text=element_blank(),
        axis_ticks=element_blank(),
        axis_line=element_blank(),
        panel_background=element_blank(),
        panel_grid=element_blank(),
        plot_background=element_blank(),
    )
)

# Save as PNG and HTML
ggsave(plot, "plot.png", path=".", scale=3)
ggsave(plot, "plot.html", path=".")
