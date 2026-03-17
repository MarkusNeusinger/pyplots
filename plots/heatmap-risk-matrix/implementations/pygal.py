""" pyplots.ai
heatmap-risk-matrix: Risk Assessment Matrix (Probability vs Impact)
Library: pygal 3.1.0 | Python 3.14.3
Quality: 84/100 | Created: 2026-03-17
"""

import sys

import numpy as np


# Temporarily remove current directory from path to avoid name collision
_cwd = sys.path[0] if sys.path[0] else "."
if _cwd in sys.path:
    sys.path.remove(_cwd)

from pygal.graph.graph import Graph  # noqa: E402
from pygal.style import Style  # noqa: E402


sys.path.insert(0, _cwd)


# Risk matrix heatmap built on pygal's Graph base with tooltip support
class RiskMatrixHeatmap(Graph):
    _series_margin = 0

    def __init__(self, *args, **kwargs):
        self.risk_scores = kwargs.pop("risk_scores", [])
        self.risk_items = kwargs.pop("risk_items", [])
        self.row_labels = kwargs.pop("row_labels", [])
        self.col_labels = kwargs.pop("col_labels", [])
        self.zone_colors = kwargs.pop("zone_colors", [])
        super().__init__(*args, **kwargs)

    def _get_zone_color(self, score):
        for max_score, color in self.zone_colors:
            if score <= max_score:
                return color
        return self.zone_colors[-1][1]

    def _get_zone_label(self, score):
        if score <= 4:
            return "Low"
        elif score <= 9:
            return "Medium"
        elif score <= 16:
            return "High"
        return "Critical"

    def _text_color(self, bg_color):
        r, g, b = int(bg_color[1:3], 16), int(bg_color[3:5], 16), int(bg_color[5:7], 16)
        brightness = (r * 299 + g * 587 + b * 114) / 1000
        return "#ffffff" if brightness < 150 else "#222222"

    def _plot(self):
        if not self.risk_scores:
            return

        n_rows = len(self.row_labels)
        n_cols = len(self.col_labels)

        plot_width = self.view.width
        plot_height = self.view.height

        # Layout margins - increased bottom for rotated labels
        margin_left = 520
        margin_bottom = 320
        margin_top = 60
        margin_right = 520

        avail_w = plot_width - margin_left - margin_right
        avail_h = plot_height - margin_bottom - margin_top

        cell_size = min(avail_w / n_cols, avail_h / n_rows) * 0.94
        gap = cell_size * 0.04

        grid_w = n_cols * (cell_size + gap) - gap
        grid_h = n_rows * (cell_size + gap) - gap

        x0 = self.view.x(0) + margin_left + (avail_w - grid_w) / 2
        y0 = self.view.y(n_rows) + margin_top + (avail_h - grid_h) / 2

        plot_node = self.nodes["plot"]
        group = self.svg.node(plot_node, class_="risk-matrix")

        # Font sizes based on cell size
        score_font = int(cell_size * 0.24)
        zone_font = int(cell_size * 0.15)
        marker_font = int(cell_size * 0.12)
        marker_r = int(cell_size * 0.07)
        label_font = int(cell_size * 0.16)
        title_font = int(cell_size * 0.22)
        legend_font = int(cell_size * 0.15)
        legend_box = int(cell_size * 0.14)

        # --- Draw cells ---
        for i in range(n_rows):
            for j in range(n_cols):
                row_idx = n_rows - 1 - i
                score = self.risk_scores[row_idx][j]
                color = self._get_zone_color(score)
                tc = self._text_color(color)

                x = x0 + j * (cell_size + gap)
                y = y0 + i * (cell_size + gap)

                # Cell rectangle with pygal tooltip via title element
                cell_group = self.svg.node(group, "g", class_="cell")
                rect = self.svg.node(cell_group, "rect", x=x, y=y, width=cell_size, height=cell_size, rx=8, ry=8)
                rect.set("fill", color)
                rect.set("stroke", "#ffffff")
                rect.set("stroke-width", "4")

                # Add SVG title for tooltip
                zone_label = self._get_zone_label(score)
                title_el = self.svg.node(cell_group, "title")
                title_el.text = f"Risk Score: {score} ({zone_label})"

                # Score number
                txt = self.svg.node(cell_group, "text", x=x + cell_size / 2, y=y + cell_size * 0.38)
                txt.set("text-anchor", "middle")
                txt.set("fill", tc)
                txt.set("style", f"font-size:{score_font}px;font-weight:bold;font-family:sans-serif")
                txt.text = str(score)

                # Zone label
                zt = self.svg.node(cell_group, "text", x=x + cell_size / 2, y=y + cell_size * 0.58)
                zt.set("text-anchor", "middle")
                zt.set("fill", tc)
                zt.set("opacity", "0.75")
                zt.set("style", f"font-size:{zone_font}px;font-weight:500;font-family:sans-serif")
                zt.text = zone_label

        # --- Risk item markers ---
        np.random.seed(42)
        for item in self.risk_items:
            col_idx = item["impact"] - 1
            row_display = n_rows - item["likelihood"]
            color = item.get("color", "#306998")

            jitter_x = np.random.uniform(-cell_size * 0.18, cell_size * 0.18)
            jitter_y = np.random.uniform(-cell_size * 0.06, cell_size * 0.06)

            cx = x0 + col_idx * (cell_size + gap) + cell_size / 2 + jitter_x
            cy = y0 + row_display * (cell_size + gap) + cell_size * 0.76 + jitter_y

            # Marker group with tooltip
            mg = self.svg.node(group, "g", class_="risk-marker")
            circle = self.svg.node(mg, "circle", cx=cx, cy=cy, r=marker_r)
            circle.set("fill", color)
            circle.set("stroke", "#ffffff")
            circle.set("stroke-width", "2.5")
            circle.set("opacity", "0.92")

            # Shadow for better visibility on any background
            shadow = self.svg.node(mg, "text", x=cx, y=cy + marker_r + marker_font + 3)
            shadow.set("text-anchor", "middle")
            shadow.set("fill", "#ffffff")
            shadow.set("style", f"font-size:{marker_font}px;font-weight:700;font-family:sans-serif")
            shadow.set("stroke", "#ffffff")
            shadow.set("stroke-width", "6")
            shadow.set("paint-order", "stroke fill")
            shadow.text = item["name"]

            # Label text on top
            lbl = self.svg.node(mg, "text", x=cx, y=cy + marker_r + marker_font + 3)
            lbl.set("text-anchor", "middle")
            lbl.set("fill", "#1a1a1a")
            lbl.set("style", f"font-size:{marker_font}px;font-weight:700;font-family:sans-serif")
            lbl.text = item["name"]

            # SVG tooltip
            tip = self.svg.node(mg, "title")
            score = item["likelihood"] * item["impact"]
            tip.text = f"{item['name']} — L:{item['likelihood']} × I:{item['impact']} = {score}"

        # --- Y-axis labels ---
        for i in range(n_rows):
            row_idx = n_rows - 1 - i
            y = y0 + i * (cell_size + gap) + cell_size / 2

            num_node = self.svg.node(group, "text", x=x0 - 24, y=y + label_font * 0.15)
            num_node.set("text-anchor", "end")
            num_node.set("fill", "#333333")
            num_node.set("style", f"font-size:{label_font}px;font-weight:600;font-family:sans-serif")
            num_node.text = f"{row_idx + 1}. {self.row_labels[row_idx]}"

        # --- X-axis labels (rotated 35° to avoid crowding) ---
        for j in range(n_cols):
            x = x0 + j * (cell_size + gap) + cell_size / 2
            y = y0 + grid_h + 40

            num_node = self.svg.node(group, "text", x=x, y=y)
            num_node.set("text-anchor", "end")
            num_node.set("fill", "#333333")
            num_node.set("style", f"font-size:{label_font}px;font-weight:600;font-family:sans-serif")
            num_node.set("transform", f"rotate(-35, {x}, {y})")
            num_node.text = f"{j + 1}. {self.col_labels[j]}"

        # --- Axis titles ---
        # Y-axis title (rotated)
        mid_y = y0 + grid_h / 2
        yt = self.svg.node(group, "text", x=x0 - 470, y=mid_y)
        yt.set("text-anchor", "middle")
        yt.set("fill", "#333333")
        yt.set("style", f"font-size:{title_font}px;font-weight:bold;font-family:sans-serif;letter-spacing:3px")
        yt.set("transform", f"rotate(-90, {x0 - 470}, {mid_y})")
        yt.text = "LIKELIHOOD"

        # X-axis title
        mid_x = x0 + grid_w / 2
        xt = self.svg.node(group, "text", x=mid_x, y=y0 + grid_h + 260)
        xt.set("text-anchor", "middle")
        xt.set("fill", "#333333")
        xt.set("style", f"font-size:{title_font}px;font-weight:bold;font-family:sans-serif;letter-spacing:3px")
        xt.text = "IMPACT"

        # --- Zone legend (right side) ---
        lx = x0 + grid_w + 60
        ly = y0 + 10
        zone_items = [
            ("Low (1\u20134)", "#4caf50"),
            ("Medium (5\u20139)", "#ffc107"),
            ("High (10\u201316)", "#ff9800"),
            ("Critical (20\u201325)", "#d32f2f"),
        ]
        # Legend title
        lt = self.svg.node(group, "text", x=lx, y=ly)
        lt.set("fill", "#333333")
        lt.set("style", f"font-size:{legend_font}px;font-weight:bold;font-family:sans-serif")
        lt.text = "Risk Zones"
        ly += 36

        for label, color in zone_items:
            rect = self.svg.node(group, "rect", x=lx, y=ly, width=legend_box, height=legend_box, rx=4, ry=4)
            rect.set("fill", color)
            rect.set("stroke", "#ffffff")
            rect.set("stroke-width", "2")

            txt = self.svg.node(group, "text", x=lx + legend_box + 14, y=ly + legend_box * 0.78)
            txt.set("fill", "#333333")
            txt.set("style", f"font-size:{legend_font}px;font-weight:500;font-family:sans-serif")
            txt.text = label
            ly += legend_box + 26

        # --- Category legend ---
        ly += 30
        ct = self.svg.node(group, "text", x=lx, y=ly)
        ct.set("fill", "#333333")
        ct.set("style", f"font-size:{legend_font}px;font-weight:bold;font-family:sans-serif")
        ct.text = "Risk Categories"
        ly += 32

        category_colors = {
            "Technical": "#1565c0",
            "Financial": "#6a1b9a",
            "Operational": "#e65100",
            "External": "#00838f",
        }
        for cat, color in category_colors.items():
            circle = self.svg.node(group, "circle", cx=lx + legend_box / 2, cy=ly + legend_box / 2 - 2, r=marker_r)
            circle.set("fill", color)
            circle.set("stroke", "#ffffff")
            circle.set("stroke-width", "2")

            txt = self.svg.node(group, "text", x=lx + legend_box + 14, y=ly + legend_box * 0.6)
            txt.set("fill", "#333333")
            txt.set("style", f"font-size:{legend_font}px;font-weight:500;font-family:sans-serif")
            txt.text = cat
            ly += legend_box + 22

    def _compute(self):
        n_rows = len(self.row_labels) if self.row_labels else 1
        n_cols = len(self.col_labels) if self.col_labels else 1
        self._box.xmin = 0
        self._box.xmax = n_cols
        self._box.ymin = 0
        self._box.ymax = n_rows


# Data
likelihood_labels = ["Rare", "Unlikely", "Possible", "Likely", "Almost Certain"]
impact_labels = ["Negligible", "Minor", "Moderate", "Major", "Catastrophic"]

risk_scores = [[li * im for im in range(1, 6)] for li in range(1, 6)]

zone_colors = [(4, "#4caf50"), (9, "#ffc107"), (16, "#ff9800"), (25, "#d32f2f")]

# Changed External color from green (#2e7d32) to teal (#00838f) for better contrast on green cells
category_colors = {"Technical": "#1565c0", "Financial": "#6a1b9a", "Operational": "#e65100", "External": "#00838f"}

risk_items = [
    {"name": "Server Outage", "likelihood": 3, "impact": 4, "category": "Technical", "color": "#1565c0"},
    {"name": "Data Breach", "likelihood": 2, "impact": 5, "category": "Technical", "color": "#1565c0"},
    {"name": "Budget Overrun", "likelihood": 4, "impact": 3, "category": "Financial", "color": "#6a1b9a"},
    {"name": "Currency Risk", "likelihood": 3, "impact": 2, "category": "Financial", "color": "#6a1b9a"},
    {"name": "Vendor Delay", "likelihood": 4, "impact": 2, "category": "Operational", "color": "#e65100"},
    {"name": "Staff Turnover", "likelihood": 4, "impact": 1, "category": "Operational", "color": "#e65100"},
    {"name": "Scope Creep", "likelihood": 5, "impact": 2, "category": "Operational", "color": "#e65100"},
    {"name": "Reg. Change", "likelihood": 2, "impact": 4, "category": "External", "color": "#00838f"},
    {"name": "Supply Chain", "likelihood": 3, "impact": 5, "category": "External", "color": "#00838f"},
    {"name": "Market Shift", "likelihood": 2, "impact": 3, "category": "Financial", "color": "#6a1b9a"},
    {"name": "Tech Debt", "likelihood": 4, "impact": 4, "category": "Technical", "color": "#1565c0"},
    {"name": "Cyber Attack", "likelihood": 1, "impact": 4, "category": "Technical", "color": "#1565c0"},
    {"name": "Key Person", "likelihood": 4, "impact": 5, "category": "Operational", "color": "#e65100"},
    {"name": "Pandemic", "likelihood": 1, "impact": 5, "category": "External", "color": "#00838f"},
]

# Style
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#999999",
    colors=("#306998",),
    title_font_size=64,
    legend_font_size=40,
    label_font_size=38,
    value_font_size=34,
    font_family="sans-serif",
    tooltip_font_size=28,
)

# Plot
chart = RiskMatrixHeatmap(
    width=4800,
    height=2700,
    style=custom_style,
    title="heatmap-risk-matrix \u00b7 pygal \u00b7 pyplots.ai",
    risk_scores=risk_scores,
    risk_items=risk_items,
    row_labels=likelihood_labels,
    col_labels=impact_labels,
    zone_colors=zone_colors,
    show_legend=False,
    margin=100,
    margin_top=200,
    margin_bottom=140,
    margin_left=120,
    margin_right=120,
    show_x_labels=False,
    show_y_labels=False,
    tooltip_border_radius=6,
)

chart.add("", [0])

# Save
chart.render_to_file("plot.svg")
chart.render_to_png("plot.png")

html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>heatmap-risk-matrix - pygal</title>
    <style>
        body {{ margin: 0; display: flex; justify-content: center; align-items: center;
               min-height: 100vh; background: #f5f5f5; }}
        .chart {{ max-width: 100%; height: auto; }}
    </style>
</head>
<body>
    <figure class="chart">
        {chart.render(is_unicode=True)}
    </figure>
</body>
</html>
"""

with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)
