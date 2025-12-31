""" pyplots.ai
tree-phylogenetic: Phylogenetic Tree Diagram
Library: pygal 3.1.0 | Python 3.13.11
Quality: 82/100 | Created: 2025-12-31
"""

import pygal
from pygal.style import Style


# Primate phylogenetic tree based on mitochondrial DNA divergence (simplified)
# Tree structure: ((((Human, Chimpanzee), Gorilla), Orangutan), (Gibbon, Macaque))
species_data = [
    ("Human", 0.70),
    ("Chimpanzee", 0.70),
    ("Gorilla", 0.60),
    ("Orangutan", 0.45),
    ("Gibbon", 0.70),
    ("Macaque", 0.70),
]

# Tree structure with internal nodes (y positions for species, x = evolutionary distance)
# Y positions: spread species vertically
n_species = len(species_data)
species_y = {name: i for i, (name, _) in enumerate(species_data)}

# Define tree connections: each internal node connects to its children
# Format: (x_position, y_center, children_y_positions)
tree_segments = []

# Human-Chimpanzee clade (most recent common ancestor at x=0.60)
hc_ancestor_x = 0.60
hc_ancestor_y = (species_y["Human"] + species_y["Chimpanzee"]) / 2
tree_segments.append([(hc_ancestor_x, species_y["Human"]), (0.70, species_y["Human"])])
tree_segments.append([(hc_ancestor_x, species_y["Chimpanzee"]), (0.70, species_y["Chimpanzee"])])
tree_segments.append([(hc_ancestor_x, species_y["Human"]), (hc_ancestor_x, species_y["Chimpanzee"])])

# Human-Chimp-Gorilla clade (ancestor at x=0.45)
hcg_ancestor_x = 0.45
hcg_ancestor_y = (hc_ancestor_y + species_y["Gorilla"]) / 2
tree_segments.append([(hcg_ancestor_x, hc_ancestor_y), (hc_ancestor_x, hc_ancestor_y)])
tree_segments.append([(hcg_ancestor_x, species_y["Gorilla"]), (0.60, species_y["Gorilla"])])
tree_segments.append([(hcg_ancestor_x, hc_ancestor_y), (hcg_ancestor_x, species_y["Gorilla"])])

# Great apes clade including Orangutan (ancestor at x=0.30)
great_apes_x = 0.30
great_apes_y = (hcg_ancestor_y + species_y["Orangutan"]) / 2
tree_segments.append([(great_apes_x, hcg_ancestor_y), (hcg_ancestor_x, hcg_ancestor_y)])
tree_segments.append([(great_apes_x, species_y["Orangutan"]), (0.45, species_y["Orangutan"])])
tree_segments.append([(great_apes_x, hcg_ancestor_y), (great_apes_x, species_y["Orangutan"])])

# Gibbon-Macaque clade (ancestor at x=0.50)
gm_ancestor_x = 0.50
gm_ancestor_y = (species_y["Gibbon"] + species_y["Macaque"]) / 2
tree_segments.append([(gm_ancestor_x, species_y["Gibbon"]), (0.70, species_y["Gibbon"])])
tree_segments.append([(gm_ancestor_x, species_y["Macaque"]), (0.70, species_y["Macaque"])])
tree_segments.append([(gm_ancestor_x, species_y["Gibbon"]), (gm_ancestor_x, species_y["Macaque"])])

# Root: connects great apes and gibbon-macaque clades (x=0)
root_x = 0.0
root_y = (great_apes_y + gm_ancestor_y) / 2
tree_segments.append([(root_x, great_apes_y), (great_apes_x, great_apes_y)])
tree_segments.append([(root_x, gm_ancestor_y), (gm_ancestor_x, gm_ancestor_y)])
tree_segments.append([(root_x, great_apes_y), (root_x, gm_ancestor_y)])

# Custom style for pyplots - larger fonts for 4800x2700 canvas
# Use single color for consistent branch appearance
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333",
    foreground_strong="#333",
    foreground_subtle="#999",
    colors=("#306998",),  # Python Blue for all branches
    title_font_size=56,
    label_font_size=40,
    major_label_font_size=36,
    legend_font_size=32,
    value_font_size=28,
    tooltip_font_size=24,
    stroke_width=5,
    opacity=1.0,
    guide_stroke_color="#ddd",
)

# Create XY chart for phylogenetic tree
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="Primate Evolution · tree-phylogenetic · pygal · pyplots.ai",
    x_title="Evolutionary Distance (substitutions per site)",
    y_title="",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=8,
    show_dots=False,
    stroke_style={"width": 5},
    fill=False,
    show_x_guides=True,
    show_y_guides=False,
    show_y_labels=False,
    range=(-0.8, n_species - 0.5),
    xrange=(-0.05, 0.85),
    print_values=False,
)

# Add all tree branches as unnamed series (all use Python Blue)
for seg in tree_segments:
    chart.add(None, seg, show_dots=False, stroke_style={"width": 5})

# Add species markers at the tips
# Use colorblind-friendly colors for species points
species_colors = ["#E63946", "#457B9D", "#2A9D8F", "#E9C46A", "#F4A261", "#9C6644"]
for i, (name, x_pos) in enumerate(species_data):
    y_pos = species_y[name]
    color = species_colors[i % len(species_colors)]
    chart.add(
        name,
        [{"value": (x_pos, y_pos), "label": name, "color": color}],
        show_dots=True,
        dots_size=16,
        stroke_style={"width": 0},
        color=color,
    )

# Add scale bar below the plot area
scale_bar_y = -0.6
chart.add(
    "Scale: 0.1 subs/site",
    [(0.35, scale_bar_y), (0.45, scale_bar_y)],
    show_dots=False,
    stroke_style={"width": 8},
    color="#333",
)

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
