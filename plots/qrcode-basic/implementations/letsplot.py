""" pyplots.ai
qrcode-basic: Basic QR Code Generator
Library: letsplot 4.8.2 | Python 3.14.3
Quality: 85/100 | Updated: 2026-04-07
"""

import pandas as pd
import qrcode
from lets_plot import (
    LetsPlot,
    aes,
    coord_fixed,
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

# Convert QR matrix to dataframe
matrix = qr.get_matrix()
size = len(matrix)
rows = []
for y, row in enumerate(matrix):
    for x, cell in enumerate(row):
        rows.append({"x": x, "y": size - 1 - y, "module": "black" if cell else "white"})
df = pd.DataFrame(rows)

# Plot
plot = (
    ggplot(df, aes(x="x", y="y", fill="module"))
    + geom_tile(width=1, height=1, show_legend=False)
    + scale_fill_manual(values={"black": "#000000", "white": "#FFFFFF"})
    + coord_fixed()
    + labs(
        title="qrcode-basic \u00b7 letsplot \u00b7 pyplots.ai",
        subtitle="Encoded: https://pyplots.ai | Error Correction: M (15%)",
    )
    + ggsize(1200, 1200)
    + theme(
        plot_title=element_text(size=24, hjust=0.5),
        plot_subtitle=element_text(size=16, hjust=0.5, color="#666666"),
        axis_title=element_blank(),
        axis_text=element_blank(),
        axis_ticks=element_blank(),
        axis_line=element_blank(),
        panel_background=element_blank(),
        panel_grid=element_blank(),
        plot_background=element_blank(),
    )
)

# Save
ggsave(plot, "plot.png", path=".", scale=3)
