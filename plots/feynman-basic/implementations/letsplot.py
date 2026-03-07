"""pyplots.ai
feynman-basic: Feynman Diagram for Particle Interactions
Library: letsplot | Python 3.13
Quality: pending | Created: 2026-03-07
"""

import numpy as np
import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_blank,
    element_rect,
    element_text,
    geom_path,
    geom_point,
    geom_segment,
    geom_text,
    ggplot,
    ggsize,
    labs,
    scale_color_identity,
    theme,
    xlim,
    ylim,
)
from lets_plot.export import ggsave


LetsPlot.setup_html()

# Data - Electron-positron annihilation into muon pair: e⁻e⁺ → γ → μ⁻μ⁺
# Vertex positions
v1x, v1y = 0.35, 0.50
v2x, v2y = 0.65, 0.50

# Fermion line endpoints
fermion_ext = 0.22

# Fermion segments (particles: arrow forward in time, antiparticles: arrow backward)
# e⁻ incoming: top-left → v1 (particle, arrow toward vertex)
# e⁺ incoming: v1 → bottom-left (antiparticle, arrow away from vertex = backward in time)
# μ⁻ outgoing: v2 → top-right (particle, arrow away from vertex)
# μ⁺ outgoing: bottom-right → v2 (antiparticle, arrow toward vertex = backward in time)
fermion_df = pd.DataFrame(
    {
        "x": [v1x - fermion_ext, v1x, v2x, v2x + fermion_ext],
        "y": [v1y + fermion_ext, v1y, v2y, v2y - fermion_ext],
        "xend": [v1x, v1x - fermion_ext, v2x + fermion_ext, v2x],
        "yend": [v1y, v1y - fermion_ext, v2y + fermion_ext, v2y],
    }
)

# Arrowhead data (V-shaped, at the segment endpoint)
head_len = 0.025
head_width = 0.012

arrow_rows = []
for _, row in fermion_df.iterrows():
    dx = row["xend"] - row["x"]
    dy = row["yend"] - row["y"]
    length = np.sqrt(dx**2 + dy**2)
    ux, uy = dx / length, dy / length
    px, py = -uy, ux

    tip_x, tip_y = row["xend"], row["yend"]
    base_x, base_y = tip_x - head_len * ux, tip_y - head_len * uy

    arrow_rows.append(
        {
            "x_left": base_x - head_width * px,
            "x_right": base_x + head_width * px,
            "x_tip": tip_x,
            "y_left": base_y - head_width * py,
            "y_right": base_y + head_width * py,
            "y_tip": tip_y,
        }
    )

arrow_df = pd.DataFrame(arrow_rows)

# Photon line (wavy sinusoidal path from v1 to v2)
n_wave = 400
t = np.linspace(0, 1, n_wave)
wave_amplitude = 0.028
wave_freq = 7
photon_x = v1x + t * (v2x - v1x)
photon_y = v1y + wave_amplitude * np.sin(t * wave_freq * 2 * np.pi)
photon_df = pd.DataFrame({"x": photon_x, "y": photon_y, "group": [1] * n_wave})

# Vertex points
vertex_df = pd.DataFrame({"x": [v1x, v2x], "y": [v1y, v2y]})

# Particle labels
labels_df = pd.DataFrame(
    {
        "x": [
            v1x - fermion_ext - 0.03,
            v1x - fermion_ext - 0.03,
            v2x + fermion_ext + 0.03,
            v2x + fermion_ext + 0.03,
            0.50,
        ],
        "y": [
            v1y + fermion_ext + 0.025,
            v1y - fermion_ext - 0.025,
            v2y + fermion_ext + 0.025,
            v2y - fermion_ext - 0.025,
            v1y + 0.045,
        ],
        "label": ["e\u207b", "e\u207a", "\u03bc\u207b", "\u03bc\u207a", "\u03b3"],
    }
)

# Time arrow indicator
time_arrow_df = pd.DataFrame({"x": [0.35], "xend": [0.65], "y": [0.10], "yend": [0.10]})
time_label_df = pd.DataFrame({"x": [0.50], "y": [0.06], "label": ["time"]})

# Plot
plot = (
    ggplot()
    # Fermion lines
    + geom_segment(data=fermion_df, mapping=aes(x="x", y="y", xend="xend", yend="yend"), size=2.0, color="#306998")
    # Arrowheads (left side of V)
    + geom_segment(
        data=arrow_df, mapping=aes(x="x_left", y="y_left", xend="x_tip", yend="y_tip"), size=2.0, color="#306998"
    )
    # Arrowheads (right side of V)
    + geom_segment(
        data=arrow_df, mapping=aes(x="x_right", y="y_right", xend="x_tip", yend="y_tip"), size=2.0, color="#306998"
    )
    # Photon wavy line
    + geom_path(data=photon_df, mapping=aes(x="x", y="y", group="group"), size=2.0, color="#D4973B")
    # Vertices
    + geom_point(data=vertex_df, mapping=aes(x="x", y="y"), size=10, color="#1A1A1A", shape=16)
    # Particle labels
    + geom_text(data=labels_df, mapping=aes(x="x", y="y", label="label"), size=22, color="#1A1A1A", fontface="italic")
    # Time arrow
    + geom_segment(data=time_arrow_df, mapping=aes(x="x", y="y", xend="xend", yend="yend"), size=1.0, color="#AAAAAA")
    + geom_text(
        data=time_label_df, mapping=aes(x="x", y="y", label="label"), size=16, color="#AAAAAA", fontface="italic"
    )
    # Time arrowhead
    + geom_segment(
        data=pd.DataFrame({"x": [0.64, 0.64], "y": [0.11, 0.09], "xend": [0.65, 0.65], "yend": [0.10, 0.10]}),
        mapping=aes(x="x", y="y", xend="xend", yend="yend"),
        size=1.0,
        color="#AAAAAA",
    )
    # Legend for line types
    + geom_segment(
        data=pd.DataFrame(
            {
                "x": [0.78, 0.78],
                "xend": [0.86, 0.86],
                "y": [0.85, 0.78],
                "yend": [0.85, 0.78],
                "color": ["#306998", "#D4973B"],
            }
        ),
        mapping=aes(x="x", y="y", xend="xend", yend="yend", color="color"),
        size=2.0,
    )
    + scale_color_identity()
    + geom_text(
        data=pd.DataFrame({"x": [0.87, 0.87], "y": [0.85, 0.78], "label": ["Fermion", "Photon"]}),
        mapping=aes(x="x", y="y", label="label"),
        size=16,
        color="#1A1A1A",
        hjust=0,
    )
    # Styling
    + xlim(0.0, 1.0)
    + ylim(0.0, 0.95)
    + labs(
        title="feynman-basic \u00b7 letsplot \u00b7 pyplots.ai",
        subtitle="Electron\u2013Positron Annihilation: e\u207be\u207a \u2192 \u03b3 \u2192 \u03bc\u207b\u03bc\u207a",
    )
    + theme(
        axis_title=element_blank(),
        axis_text=element_blank(),
        axis_ticks=element_blank(),
        axis_line=element_blank(),
        panel_grid=element_blank(),
        panel_background=element_rect(fill="white", color="white"),
        plot_background=element_rect(fill="white", color="white"),
        plot_title=element_text(size=24, face="bold", color="#1A3A5C"),
        plot_subtitle=element_text(size=18, color="#4A6B82"),
        legend_position="none",
    )
    + ggsize(1600, 900)
)

# Save
ggsave(plot, filename="plot.png", path=".", scale=3)
ggsave(plot, filename="plot.html", path=".")
