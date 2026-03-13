""" pyplots.ai
swimmer-clinical-timeline: Swimmer Plot for Clinical Trial Timelines
Library: bokeh 3.9.0 | Python 3.14.3
Quality: 82/100 | Created: 2026-03-13
"""

import numpy as np
from bokeh.io import export_png, save
from bokeh.models import ColumnDataSource, FactorRange, Legend, LegendItem, Range1d
from bokeh.plotting import figure
from bokeh.resources import CDN


# Data - Simulated Phase II oncology trial with 25 patients across two treatment arms
np.random.seed(42)

n_patients = 25
patient_ids = [f"PT-{i + 1:03d}" for i in range(n_patients)]
arms = np.random.choice(["Arm A (Combo)", "Arm B (Mono)"], size=n_patients, p=[0.52, 0.48])
durations = np.round(np.random.exponential(scale=18, size=n_patients) + 4, 1)
durations = np.clip(durations, 4, 52)

# Generate clinical events for each patient
events_time = []
events_type = []
events_patient = []
ongoing_patients = set()

for i in range(n_patients):
    dur = durations[i]
    patient_events = []

    if np.random.random() < 0.6:
        t = np.round(np.random.uniform(4, min(dur * 0.4, 12)), 1)
        patient_events.append((t, "partial_response"))

    if np.random.random() < 0.3 and dur > 16:
        t = np.round(np.random.uniform(12, min(dur * 0.6, 24)), 1)
        patient_events.append((t, "complete_response"))

    if np.random.random() < 0.35:
        t = np.round(np.random.uniform(2, dur * 0.8), 1)
        patient_events.append((t, "adverse_event"))

    if np.random.random() < 0.4 and dur < 30:
        t = np.round(dur - np.random.uniform(0, 2), 1)
        patient_events.append((t, "progressive_disease"))

    if dur > 25 and not any(e[1] == "progressive_disease" for e in patient_events):
        ongoing_patients.add(i)

    for t, etype in patient_events:
        events_time.append(t)
        events_type.append(etype)
        events_patient.append(patient_ids[i])

# Sort patients by duration (longest at top)
sort_idx = np.argsort(durations)[::-1]
sorted_patient_ids = [patient_ids[i] for i in sort_idx]
sorted_durations = [durations[i] for i in sort_idx]
sorted_arms = [arms[i] for i in sort_idx]

# Bar colors by treatment arm
arm_colors = {"Arm A (Combo)": "#306998", "Arm B (Mono)": "#FFD43B"}

# Plot
p = figure(
    y_range=FactorRange(*sorted_patient_ids),
    width=4800,
    height=2700,
    title="swimmer-clinical-timeline · bokeh · pyplots.ai",
    x_axis_label="Time on Study (Weeks)",
    toolbar_location=None,
)

# Horizontal bars per treatment arm
bars_a = p.hbar(
    y=[sorted_patient_ids[i] for i, a in enumerate(sorted_arms) if a == "Arm A (Combo)"],
    right=[sorted_durations[i] for i, a in enumerate(sorted_arms) if a == "Arm A (Combo)"],
    left=0,
    height=0.6,
    color=arm_colors["Arm A (Combo)"],
    alpha=0.85,
    line_color="white",
    line_width=1,
)

bars_b = p.hbar(
    y=[sorted_patient_ids[i] for i, a in enumerate(sorted_arms) if a == "Arm B (Mono)"],
    right=[sorted_durations[i] for i, a in enumerate(sorted_arms) if a == "Arm B (Mono)"],
    left=0,
    height=0.6,
    color=arm_colors["Arm B (Mono)"],
    alpha=0.85,
    line_color="white",
    line_width=1,
)

# Event marker definitions
event_marker_config = {
    "partial_response": {"marker": "triangle", "color": "#2ca02c", "size": 22},
    "complete_response": {"marker": "star", "color": "#e377c2", "size": 26},
    "progressive_disease": {"marker": "diamond", "color": "#d62728", "size": 22},
    "adverse_event": {"marker": "square", "color": "#ff7f0e", "size": 18},
}

# Plot event markers using scatter() with marker parameter
event_renderers = {}
for etype, config in event_marker_config.items():
    mask = [j for j in range(len(events_type)) if events_type[j] == etype]
    if not mask:
        continue
    ex = [events_time[j] for j in mask]
    ey = [events_patient[j] for j in mask]
    source_evt = ColumnDataSource(data={"x": ex, "y": ey})

    r = p.scatter(
        x="x",
        y="y",
        source=source_evt,
        marker=config["marker"],
        size=config["size"],
        color=config["color"],
        line_color="#333333",
        line_width=1.5,
    )
    event_renderers[etype] = r

# Ongoing indicators (right-pointing triangles at bar ends)
ongoing_idx_sorted = [i for i in range(n_patients) if sort_idx[i] in ongoing_patients]
ongoing_r = None
if ongoing_idx_sorted:
    arrow_x = [sorted_durations[i] + 1.0 for i in ongoing_idx_sorted]
    arrow_y = [sorted_patient_ids[i] for i in ongoing_idx_sorted]
    arrow_source = ColumnDataSource(data={"x": arrow_x, "y": arrow_y})
    ongoing_r = p.scatter(
        x="x",
        y="y",
        source=arrow_source,
        marker="triangle",
        size=24,
        color="#333333",
        angle=np.pi / 2 * 3,
        line_color="#333333",
    )

# Style
p.title.text_font_size = "36pt"
p.title.text_color = "#333333"

p.xaxis.axis_label_text_font_size = "28pt"
p.xaxis.major_label_text_font_size = "20pt"
p.x_range = Range1d(0, max(sorted_durations) + 6)

p.yaxis.axis_label = "Patient"
p.yaxis.axis_label_text_font_size = "28pt"
p.yaxis.major_label_text_font_size = "16pt"

p.xgrid.grid_line_color = None
p.ygrid.grid_line_alpha = 0.15
p.ygrid.grid_line_dash = "dashed"

p.background_fill_color = "#fafafa"
p.border_fill_color = "#ffffff"
p.outline_line_color = None

# Legend
legend_items = [
    LegendItem(label="Arm A (Combo)", renderers=[bars_a]),
    LegendItem(label="Arm B (Mono)", renderers=[bars_b]),
]
for etype, label in [
    ("partial_response", "Partial Response"),
    ("complete_response", "Complete Response"),
    ("progressive_disease", "Progressive Disease"),
    ("adverse_event", "Adverse Event"),
]:
    if etype in event_renderers:
        legend_items.append(LegendItem(label=label, renderers=[event_renderers[etype]]))

if ongoing_r is not None:
    legend_items.append(LegendItem(label="Ongoing", renderers=[ongoing_r]))

legend = Legend(items=legend_items, location="bottom_right", orientation="vertical")
legend.label_text_font_size = "22pt"
legend.glyph_height = 35
legend.glyph_width = 35
legend.spacing = 14
legend.padding = 30
legend.background_fill_alpha = 0.85
p.add_layout(legend)

# Save
export_png(p, filename="plot.png")
save(p, filename="plot.html", resources=CDN, title="Swimmer Clinical Timeline")
