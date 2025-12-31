"""pyplots.ai
tree-phylogenetic: Phylogenetic Tree Diagram
Library: pygal 3.1.0 | Python 3.13.11
Quality: 82/100 | Created: 2025-12-31
"""

import pygal
from pygal.style import Style


# Primate phylogenetic tree based on mitochondrial DNA divergence (simplified)
# Tree structure: ((((Human, Chimpanzee), Gorilla), Orangutan), (Gibbon, Macaque))
# Using wider y-spacing for better vertical distribution
species_data = [
    ("Human", 0.70, 0),
    ("Chimpanzee", 0.70, 1.5),
    ("Gorilla", 0.60, 3),
    ("Orangutan", 0.45, 5),
    ("Gibbon", 0.70, 7),
    ("Macaque", 0.70, 8.5),
]

# Y positions from species data (now with wider spacing)
species_y = {name: y for name, _, y in species_data}
species_x = {name: x for name, x, _ in species_data}

# Define tree connections with improved spacing
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
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333",
    foreground_strong="#333",
    foreground_subtle="#999",
    colors=("#306998",),
    title_font_size=56,
    label_font_size=44,
    major_label_font_size=40,
    legend_font_size=36,
    value_font_size=32,
    tooltip_font_size=28,
    stroke_width=6,
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
    show_legend=False,
    show_dots=False,
    stroke_style={"width": 6},
    fill=False,
    show_x_guides=True,
    show_y_guides=False,
    show_y_labels=False,
    range=(-1.5, 10),
    xrange=(-0.05, 1.05),
    print_values=False,
)

# Add all tree branches as unnamed series
for seg in tree_segments:
    chart.add(None, seg, show_dots=False, stroke_style={"width": 6})

# Add species markers with labels at the tips
# Colorblind-friendly palette
species_colors = ["#E63946", "#457B9D", "#2A9D8F", "#E9C46A", "#F4A261", "#9C6644"]

# Add species as points and label points slightly to the right
for i, (name, x_pos, y_pos) in enumerate(species_data):
    color = species_colors[i % len(species_colors)]
    # Add larger species marker dot
    chart.add(
        None,
        [{"value": (x_pos, y_pos), "color": color}],
        show_dots=True,
        dots_size=24,
        stroke_style={"width": 0},
        color=color,
    )
    # Add species name label as a text point to the right of the marker
    chart.add(
        None,
        [{"value": (x_pos + 0.02, y_pos), "label": name}],
        show_dots=False,
        stroke_style={"width": 0},
        print_labels=True,
    )

# Add scale bar as standalone annotation at bottom
scale_bar_y = -1.0
# Scale bar line
chart.add(None, [(0.0, scale_bar_y), (0.1, scale_bar_y)], show_dots=False, stroke_style={"width": 10}, color="#333")
# Scale bar label
chart.add(None, [{"value": (0.05, scale_bar_y - 0.4), "label": "0.1"}], show_dots=False, print_labels=True)

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
