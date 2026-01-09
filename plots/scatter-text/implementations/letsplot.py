""" pyplots.ai
scatter-text: Scatter Plot with Text Labels Instead of Points
Library: letsplot 4.8.2 | Python 3.13.11
Quality: 84/100 | Created: 2026-01-09
"""

import numpy as np
import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_text,
    geom_text,
    ggplot,
    ggsave,
    ggsize,
    labs,
    scale_color_manual,
    theme,
    theme_minimal,
)


LetsPlot.setup_html()

# Data - Programming languages positioned by paradigm (functional vs object-oriented)
# and level of abstraction (low vs high)
np.random.seed(42)

languages = [
    "Python",
    "JavaScript",
    "Java",
    "C++",
    "Ruby",
    "Go",
    "Rust",
    "Swift",
    "Kotlin",
    "TypeScript",
    "Scala",
    "Haskell",
    "Clojure",
    "Elixir",
    "F#",
    "C#",
    "PHP",
    "Perl",
    "R",
    "Julia",
    "MATLAB",
    "Lua",
    "Dart",
    "Groovy",
    "OCaml",
    "Erlang",
    "Fortran",
    "COBOL",
    "Assembly",
    "Lisp",
]

# Position languages based on paradigm characteristics with some jitter
paradigm_scores = {
    "Python": (0.6, 0.8),
    "JavaScript": (0.5, 0.75),
    "Java": (0.3, 0.7),
    "C++": (0.2, 0.4),
    "Ruby": (0.7, 0.85),
    "Go": (0.25, 0.6),
    "Rust": (0.15, 0.5),
    "Swift": (0.4, 0.75),
    "Kotlin": (0.45, 0.78),
    "TypeScript": (0.5, 0.77),
    "Scala": (0.7, 0.72),
    "Haskell": (0.95, 0.85),
    "Clojure": (0.9, 0.8),
    "Elixir": (0.85, 0.82),
    "F#": (0.8, 0.75),
    "C#": (0.35, 0.72),
    "PHP": (0.4, 0.65),
    "Perl": (0.5, 0.6),
    "R": (0.65, 0.78),
    "Julia": (0.6, 0.7),
    "MATLAB": (0.55, 0.65),
    "Lua": (0.5, 0.55),
    "Dart": (0.4, 0.7),
    "Groovy": (0.5, 0.68),
    "OCaml": (0.88, 0.7),
    "Erlang": (0.82, 0.65),
    "Fortran": (0.1, 0.35),
    "COBOL": (0.05, 0.3),
    "Assembly": (0.0, 0.1),
    "Lisp": (0.92, 0.6),
}

# Add jitter for visual interest
jitter_x = np.random.normal(0, 0.02, len(languages))
jitter_y = np.random.normal(0, 0.02, len(languages))

x_coords = [paradigm_scores[lang][0] + jitter_x[i] for i, lang in enumerate(languages)]
y_coords = [paradigm_scores[lang][1] + jitter_y[i] for i, lang in enumerate(languages)]

# Categorize by primary use
categories = [
    "General",
    "Web",
    "General",
    "Systems",
    "Web",
    "Systems",
    "Systems",
    "Mobile",
    "Mobile",
    "Web",
    "General",
    "Functional",
    "Functional",
    "Functional",
    "Functional",
    "General",
    "Web",
    "Scripting",
    "Data Science",
    "Data Science",
    "Data Science",
    "Scripting",
    "Mobile",
    "General",
    "Functional",
    "Functional",
    "Scientific",
    "Legacy",
    "Systems",
    "Functional",
]

df = pd.DataFrame({"x": x_coords, "y": y_coords, "label": languages, "category": categories})

# Define colors for categories
color_palette = [
    "#306998",  # Python Blue - General
    "#FFD43B",  # Python Yellow - Web
    "#2E86AB",  # Systems
    "#A23B72",  # Mobile
    "#F18F01",  # Functional
    "#C73E1D",  # Scripting
    "#3A86A9",  # Data Science
    "#6B8E23",  # Scientific
    "#708090",  # Legacy
]

category_order = [
    "General",
    "Web",
    "Systems",
    "Mobile",
    "Functional",
    "Scripting",
    "Data Science",
    "Scientific",
    "Legacy",
]

# Create plot
plot = (
    ggplot(df, aes(x="x", y="y", label="label", color="category"))
    + geom_text(size=12, alpha=0.85, fontface="bold")
    + scale_color_manual(values=color_palette, limits=category_order)
    + labs(
        x="Object-Oriented ← Paradigm → Functional",
        y="Abstraction Level (Low → High)",
        title="scatter-text · letsplot · pyplots.ai",
        color="Primary Use",
    )
    + theme_minimal()
    + theme(
        plot_title=element_text(size=28, face="bold"),
        axis_title=element_text(size=22),
        axis_text=element_text(size=16),
        legend_title=element_text(size=18),
        legend_text=element_text(size=14),
    )
    + ggsize(1600, 900)
)

# Save as PNG (scale 3x for 4800 × 2700 px)
ggsave(plot, "plot.png", path=".", scale=3)

# Save interactive HTML version
ggsave(plot, "plot.html", path=".")
