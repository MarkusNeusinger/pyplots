""" pyplots.ai
scatter-text: Scatter Plot with Text Labels Instead of Points
Library: plotly 6.5.1 | Python 3.13.11
Quality: 85/100 | Created: 2026-01-09
"""

import numpy as np
import plotly.graph_objects as go


# Data - Programming languages positioned by paradigm characteristics
np.random.seed(42)

# Language names as labels
labels = [
    "Python",
    "JavaScript",
    "Java",
    "C++",
    "Ruby",
    "Go",
    "Rust",
    "Kotlin",
    "Swift",
    "TypeScript",
    "Scala",
    "Haskell",
    "Elixir",
    "Clojure",
    "F#",
    "R",
    "Julia",
    "MATLAB",
    "Perl",
    "PHP",
    "C#",
    "Dart",
    "Lua",
    "Erlang",
    "OCaml",
    "Fortran",
    "COBOL",
    "Assembly",
    "Lisp",
    "Prolog",
]

# Position based on: x = Level of abstraction, y = Type safety
# Coordinates adjusted to avoid text overlaps
x = np.array(
    [
        8.5,  # Python
        6.5,  # JavaScript - shifted left (was 7.0, avoid Perl overlap)
        6.0,  # Java
        3.0,  # C++
        8.0,  # Ruby
        5.5,  # Go
        4.0,  # Rust
        5.8,  # Kotlin - shifted left (was 6.5, avoid Dart overlap)
        7.0,  # Swift
        7.5,  # TypeScript
        7.0,  # Scala
        9.0,  # Haskell
        8.5,  # Elixir
        9.5,  # Clojure - shifted right (was 9.0, avoid Prolog overlap)
        8.0,  # F#
        8.0,  # R
        7.5,  # Julia
        7.0,  # MATLAB
        7.8,  # Perl - shifted right (was 7.0, avoid JavaScript overlap)
        7.5,  # PHP
        6.0,  # C#
        7.5,  # Dart - shifted right (was 7.0, avoid Kotlin overlap)
        6.5,  # Lua
        8.0,  # Erlang
        8.5,  # OCaml
        3.0,  # Fortran - shifted left (was 3.5, avoid COBOL overlap)
        4.5,  # COBOL - shifted right (was 4.0, avoid Fortran overlap)
        1.0,  # Assembly
        9.0,  # Lisp
        8.5,  # Prolog - shifted left (was 9.0, avoid Clojure overlap)
    ]
)

y = np.array(
    [
        3.0,  # Python
        2.0,  # JavaScript - shifted down (was 2.5, avoid Perl overlap)
        8.0,  # Java
        6.0,  # C++
        2.0,  # Ruby
        7.0,  # Go
        9.0,  # Rust
        8.0,  # Kotlin - shifted up (was 7.5, avoid Dart overlap)
        8.5,  # Swift - shifted up (was 8.0, avoid TypeScript overlap)
        7.5,  # TypeScript - shifted down (was 8.0)
        8.5,  # Scala - shifted up (was 8.0, avoid TypeScript overlap)
        9.5,  # Haskell
        6.0,  # Elixir
        5.8,  # Clojure - shifted down (was 6.5, avoid Prolog overlap)
        8.5,  # F#
        2.5,  # R
        4.0,  # Julia
        3.5,  # MATLAB
        2.8,  # Perl - shifted up (was 2.0, avoid JavaScript overlap)
        2.0,  # PHP - shifted down (was 2.5, avoid R overlap)
        8.0,  # C#
        6.5,  # Dart - shifted down (was 7.0, avoid Kotlin overlap)
        3.0,  # Lua
        6.0,  # Erlang
        9.0,  # OCaml
        4.5,  # Fortran - shifted down (was 5.0, avoid COBOL overlap)
        6.0,  # COBOL - shifted up (was 5.5, avoid Fortran overlap)
        3.0,  # Assembly
        4.0,  # Lisp
        7.5,  # Prolog - shifted up (was 7.0, avoid Clojure overlap)
    ]
)

# Add small noise for visual interest (reduced to avoid creating new overlaps)
x = x + np.random.uniform(-0.15, 0.15, len(x))
y = y + np.random.uniform(-0.15, 0.15, len(y))

# Color by category (functional, OOP, multi-paradigm, systems)
categories = [
    "Multi-paradigm",
    "Multi-paradigm",
    "OOP",
    "Systems",
    "OOP",
    "Systems",
    "Systems",
    "OOP",
    "OOP",
    "Multi-paradigm",
    "Functional",
    "Functional",
    "Functional",
    "Functional",
    "Functional",
    "Statistical",
    "Scientific",
    "Scientific",
    "Scripting",
    "Scripting",
    "OOP",
    "OOP",
    "Scripting",
    "Functional",
    "Functional",
    "Scientific",
    "Legacy",
    "Systems",
    "Functional",
    "Functional",
]

# Color mapping (improved distinction between categories)
color_map = {
    "Multi-paradigm": "#1E88E5",  # Bright Blue
    "OOP": "#FFC107",  # Amber Yellow
    "Systems": "#D32F2F",  # Red
    "Functional": "#43A047",  # Green
    "Statistical": "#8E24AA",  # Deep Purple (more distinct from blue)
    "Scientific": "#00ACC1",  # Cyan (more distinct from blue)
    "Scripting": "#FB8C00",  # Orange
    "Legacy": "#757575",  # Gray
}

colors = [color_map[cat] for cat in categories]

# Create figure with text labels as data points
fig = go.Figure()

# Add text labels grouped by category for legend
for category in color_map:
    mask = [c == category for c in categories]
    if any(mask):
        x_cat = [x[i] for i in range(len(x)) if mask[i]]
        y_cat = [y[i] for i in range(len(y)) if mask[i]]
        labels_cat = [labels[i] for i in range(len(labels)) if mask[i]]
        # Create hover text with detailed information
        hover_cat = [
            f"<b>{labels[i]}</b><br>Paradigm: {category}<br>Abstraction: {x[i]:.1f}<br>Type Safety: {y[i]:.1f}"
            for i in range(len(labels))
            if mask[i]
        ]

        fig.add_trace(
            go.Scatter(
                x=x_cat,
                y=y_cat,
                mode="text",
                text=labels_cat,
                textfont=dict(size=16, color=color_map[category]),
                textposition="middle center",
                name=category,
                showlegend=True,
                hovertext=hover_cat,
                hoverinfo="text",
            )
        )

# Update layout
fig.update_layout(
    title=dict(text="scatter-text · plotly · pyplots.ai", font=dict(size=32), x=0.5, xanchor="center"),
    xaxis=dict(
        title=dict(text="Level of Abstraction", font=dict(size=24)),
        tickfont=dict(size=18),
        range=[0, 10.5],
        gridcolor="rgba(0,0,0,0.1)",
        gridwidth=1,
    ),
    yaxis=dict(
        title=dict(text="Type Safety", font=dict(size=24)),
        tickfont=dict(size=18),
        range=[0, 10.5],
        gridcolor="rgba(0,0,0,0.1)",
        gridwidth=1,
    ),
    template="plotly_white",
    legend=dict(
        title=dict(text="Paradigm", font=dict(size=18)),
        font=dict(size=16),
        x=1.02,
        y=0.98,
        xanchor="left",
        yanchor="top",
    ),
    margin=dict(l=80, r=180, t=100, b=80),
)

# Save as PNG and HTML
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html")
