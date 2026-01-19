""" pyplots.ai
chart-export-menu: Chart with Built-in Export Menu
Library: matplotlib 3.10.8 | Python 3.13.11
Quality: 91/100 | Created: 2026-01-19
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button


# Data - Monthly sales data for demonstration
np.random.seed(42)
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
product_a = np.random.randint(150, 300, 12) + np.arange(12) * 8
product_b = np.random.randint(100, 250, 12) + np.arange(12) * 5

# Create figure with extra space for export menu buttons
fig, ax = plt.subplots(figsize=(16, 9))
plt.subplots_adjust(bottom=0.18)

# Plot data as line chart with markers
x = np.arange(len(months))
(line_a,) = ax.plot(x, product_a, marker="o", markersize=12, linewidth=3, color="#306998", label="Product A")
(line_b,) = ax.plot(x, product_b, marker="s", markersize=10, linewidth=3, color="#FFD43B", label="Product B")

# Styling
ax.set_xlabel("Month", fontsize=20)
ax.set_ylabel("Units Sold", fontsize=20)
ax.set_title("chart-export-menu · matplotlib · pyplots.ai", fontsize=24)
ax.set_xticks(x)
ax.set_xticklabels(months, fontsize=14)
ax.tick_params(axis="y", labelsize=16)
ax.legend(fontsize=16, loc="upper left")
ax.grid(True, alpha=0.3, linestyle="--")
ax.set_ylim(0, max(max(product_a), max(product_b)) * 1.15)

# Export menu buttons - positioned at bottom of chart
button_style = {"color": "#306998", "hovercolor": "#4a90c2"}

# Create button axes
ax_png = plt.axes([0.15, 0.04, 0.12, 0.05])
ax_svg = plt.axes([0.30, 0.04, 0.12, 0.05])
ax_pdf = plt.axes([0.45, 0.04, 0.12, 0.05])
ax_csv = plt.axes([0.60, 0.04, 0.15, 0.05])

# Create buttons with export icons/labels
btn_png = Button(ax_png, "Export PNG", **button_style)
btn_svg = Button(ax_svg, "Export SVG", **button_style)
btn_pdf = Button(ax_pdf, "Export PDF", **button_style)
btn_csv = Button(ax_csv, "Export Data (CSV)", **button_style)

# Style button text
for btn in [btn_png, btn_svg, btn_pdf, btn_csv]:
    btn.label.set_fontsize(12)
    btn.label.set_color("white")


# Export callback functions
def export_png(event):
    fig.savefig("chart_export.png", dpi=300, bbox_inches="tight", facecolor="white")
    print("Exported to chart_export.png")


def export_svg(event):
    fig.savefig("chart_export.svg", format="svg", bbox_inches="tight", facecolor="white")
    print("Exported to chart_export.svg")


def export_pdf(event):
    fig.savefig("chart_export.pdf", format="pdf", bbox_inches="tight", facecolor="white")
    print("Exported to chart_export.pdf")


def export_csv(event):
    import csv

    with open("chart_data.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Month", "Product A", "Product B"])
        for m, a, b in zip(months, product_a, product_b, strict=True):
            writer.writerow([m, a, b])
    print("Exported to chart_data.csv")


# Connect buttons to callbacks
btn_png.on_clicked(export_png)
btn_svg.on_clicked(export_svg)
btn_pdf.on_clicked(export_pdf)
btn_csv.on_clicked(export_csv)

# Add export menu label
fig.text(0.03, 0.055, "Export Menu:", fontsize=14, fontweight="bold", color="#333333")

plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
