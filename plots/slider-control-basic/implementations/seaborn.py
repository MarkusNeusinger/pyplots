"""pyplots.ai
slider-control-basic: Interactive Plot with Slider Control
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 86/100 | Created: 2025-12-31
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.widgets import Slider


# Data - Sales data across multiple years
np.random.seed(42)
years = np.arange(2018, 2025)

# Generate sales data for each year with realistic patterns
sales_data = {}
for year in years:
    base = 50000 + (year - 2018) * 5000  # Growing trend over years
    seasonal = 10000 * np.sin(np.linspace(0, 2 * np.pi, 12))  # Seasonal pattern
    noise = np.random.normal(0, 3000, 12)
    sales_data[year] = base + seasonal + noise

# Create figure with space for slider
fig, ax = plt.subplots(figsize=(16, 9))
plt.subplots_adjust(bottom=0.22)

# Initial year to display
initial_year = 2022

# Style settings
sns.set_style("whitegrid")

# Month names for x-axis
month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Initial plot using seaborn
bars = sns.barplot(x=month_names, y=sales_data[initial_year], ax=ax, color="#306998", edgecolor="white", linewidth=2)

# Styling
ax.set_xlabel("Month", fontsize=20)
ax.set_ylabel("Sales ($)", fontsize=20)
ax.set_title("slider-control-basic · seaborn · pyplots.ai", fontsize=24, fontweight="bold")
ax.tick_params(axis="both", labelsize=16)
ax.set_ylim(0, 100000)

# Format y-axis with dollar signs
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x / 1000:.0f}K"))

# Store text annotations for updating
value_texts = []
for bar, val in zip(ax.patches, sales_data[initial_year], strict=True):
    txt = ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 1500,
        f"${val / 1000:.0f}K",
        ha="center",
        va="bottom",
        fontsize=12,
        fontweight="bold",
    )
    value_texts.append(txt)

# Create slider axis with proper positioning
slider_ax = plt.axes([0.2, 0.06, 0.6, 0.04])
year_slider = Slider(
    ax=slider_ax, label="Year", valmin=2018, valmax=2024, valinit=initial_year, valstep=1, color="#306998"
)
year_slider.label.set_fontsize(18)
year_slider.valtext.set_fontsize(18)


# Slider update callback function
def update_plot(val):
    year = int(year_slider.val)
    new_data = sales_data[year]

    # Update bar heights
    for bar, height in zip(ax.patches, new_data, strict=True):
        bar.set_height(height)

    # Update value labels
    for txt, bar, val in zip(value_texts, ax.patches, new_data, strict=True):
        txt.set_position((bar.get_x() + bar.get_width() / 2, bar.get_height() + 1500))
        txt.set_text(f"${val / 1000:.0f}K")

    fig.canvas.draw_idle()


# Connect slider to update function
year_slider.on_changed(update_plot)

# Add instructional text for slider interaction
fig.text(
    0.5,
    0.015,
    "Drag the slider to explore monthly sales data from 2018-2024",
    ha="center",
    fontsize=16,
    style="italic",
    color="#666666",
)

plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
