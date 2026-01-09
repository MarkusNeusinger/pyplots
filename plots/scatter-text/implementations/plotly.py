"""pyplots.ai
scatter-text: Scatter Plot with Text Labels Instead of Points
Library: plotly | Python 3.13
Quality: pending | Created: 2025-01-09
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
x = np.array(
    [
        8.5,
        7.0,
        6.0,
        3.0,
        8.0,
        5.5,
        4.0,
        6.5,
        7.0,
        7.5,
        7.0,
        9.0,
        8.5,
        9.0,
        8.0,
        8.0,
        7.5,
        7.0,
        7.0,
        7.5,
        6.0,
        7.0,
        6.5,
        8.0,
        8.5,
        3.5,
        4.0,
        1.0,
        9.0,
        9.0,
    ]
)

y = np.array(
    [
        3.0,
        2.5,
        8.0,
        6.0,
        2.0,
        7.0,
        9.0,
        7.5,
        8.0,
        8.0,
        8.0,
        9.5,
        6.0,
        6.5,
        8.5,
        2.5,
        4.0,
        3.5,
        2.0,
        2.5,
        8.0,
        7.0,
        3.0,
        6.0,
        9.0,
        5.0,
        5.5,
        3.0,
        4.0,
        7.0,
    ]
)

# Add small noise for visual interest
x = x + np.random.uniform(-0.3, 0.3, len(x))
y = y + np.random.uniform(-0.3, 0.3, len(y))

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

# Color mapping
color_map = {
    "Multi-paradigm": "#306998",  # Python Blue
    "OOP": "#FFD43B",  # Python Yellow
    "Systems": "#E74C3C",  # Red
    "Functional": "#2ECC71",  # Green
    "Statistical": "#9B59B6",  # Purple
    "Scientific": "#3498DB",  # Light Blue
    "Scripting": "#F39C12",  # Orange
    "Legacy": "#95A5A6",  # Gray
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
