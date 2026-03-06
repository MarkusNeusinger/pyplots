"""pyplots.ai
tree-decision: Decision Tree Visualization with Probabilities
Library: letsplot | Python 3.13
Quality: pending | Created: 2026-03-06
"""

import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_text,
    geom_point,
    geom_segment,
    geom_text,
    ggplot,
    ggsize,
    labs,
    scale_x_continuous,
    scale_y_continuous,
    theme,
    theme_void,
)
from lets_plot.export import ggsave


LetsPlot.setup_html()

# Data - Two-stage product launch decision
# EMV rollback:
#   C2: 0.6 × $600K + 0.4 × $200K = $440K
#   D2: max($440K, $350K) = $440K → "Maintain" pruned
#   C1: 0.3 × $900K + 0.5 × $440K + 0.2 × (-$200K) = $450K
#   D1: max($450K, $250K) = $450K → "License Tech" pruned

node_records = [
    {"id": "D1", "type": "decision", "x": 0, "y": 4.5, "value": "EMV $450K"},
    {"id": "C1", "type": "chance", "x": 5, "y": 7.0, "value": "EMV $450K"},
    {"id": "T6", "type": "terminal", "x": 5, "y": 1.5, "value": "$250K"},
    {"id": "T1", "type": "terminal", "x": 10, "y": 9.0, "value": "$900K"},
    {"id": "D2", "type": "decision", "x": 10, "y": 7.0, "value": "EMV $440K"},
    {"id": "T2", "type": "terminal", "x": 10, "y": 4.5, "value": "-$200K"},
    {"id": "C2", "type": "chance", "x": 15, "y": 8.0, "value": "EMV $440K"},
    {"id": "T3", "type": "terminal", "x": 15, "y": 6.0, "value": "$350K"},
    {"id": "T4", "type": "terminal", "x": 20, "y": 8.5, "value": "$600K"},
    {"id": "T5", "type": "terminal", "x": 20, "y": 7.5, "value": "$200K"},
]

branch_records = [
    {"from_id": "D1", "to_id": "C1", "label": "Launch Product", "pruned": False},
    {"from_id": "D1", "to_id": "T6", "label": "License Tech", "pruned": True},
    {"from_id": "C1", "to_id": "T1", "label": "Strong (0.3)", "pruned": False},
    {"from_id": "C1", "to_id": "D2", "label": "Moderate (0.5)", "pruned": False},
    {"from_id": "C1", "to_id": "T2", "label": "Weak (0.2)", "pruned": False},
    {"from_id": "D2", "to_id": "C2", "label": "Scale Up", "pruned": False},
    {"from_id": "D2", "to_id": "T3", "label": "Maintain", "pruned": True},
    {"from_id": "C2", "to_id": "T4", "label": "Success (0.6)", "pruned": False},
    {"from_id": "C2", "to_id": "T5", "label": "Setback (0.4)", "pruned": False},
]

node_lookup = {r["id"]: r for r in node_records}

# Build segment dataframes for branches (elbow connectors: horizontal then vertical then horizontal)
active_segs = []
pruned_segs = []
for b in branch_records:
    f = node_lookup[b["from_id"]]
    t = node_lookup[b["to_id"]]
    mid_x = (f["x"] + t["x"]) / 2
    seg1 = {"x": f["x"], "y": f["y"], "xend": mid_x, "yend": f["y"]}
    seg2 = {"x": mid_x, "y": f["y"], "xend": mid_x, "yend": t["y"]}
    seg3 = {"x": mid_x, "y": t["y"], "xend": t["x"], "yend": t["y"]}
    target = pruned_segs if b["pruned"] else active_segs
    target.extend([seg1, seg2, seg3])

df_active = pd.DataFrame(active_segs)
df_pruned = pd.DataFrame(pruned_segs)

# Branch labels placed along the horizontal portion near the parent
branch_label_records = []
for b in branch_records:
    f = node_lookup[b["from_id"]]
    t = node_lookup[b["to_id"]]
    mid_x = (f["x"] + t["x"]) / 2
    label_x = mid_x
    label_y = t["y"] + 0.35
    branch_label_records.append({"x": label_x, "y": label_y, "label": b["label"]})
df_branch_labels = pd.DataFrame(branch_label_records)

# Node dataframes by type for different shapes
df_decision = pd.DataFrame([r for r in node_records if r["type"] == "decision"])
df_chance = pd.DataFrame([r for r in node_records if r["type"] == "chance"])
df_terminal = pd.DataFrame([r for r in node_records if r["type"] == "terminal"])

# Value labels positioned near nodes
value_label_records = []
for r in node_records:
    if r["type"] == "terminal":
        value_label_records.append({"x": r["x"] + 0.6, "y": r["y"], "label": r["value"]})
    else:
        value_label_records.append({"x": r["x"], "y": r["y"] - 0.6, "label": r["value"]})
df_values = pd.DataFrame(value_label_records)

# Pruning cross marks (double-strike at 30% along pruned branch)
prune_mark_records = []
for b in branch_records:
    if b["pruned"]:
        f = node_lookup[b["from_id"]]
        t = node_lookup[b["to_id"]]
        cx = f["x"] + (t["x"] - f["x"]) * 0.4
        cy = f["y"] + (t["y"] - f["y"]) * 0.4
        d = 0.25
        prune_mark_records.append({"x": cx - d, "y": cy - d, "xend": cx + d, "yend": cy + d})
        prune_mark_records.append({"x": cx - d, "y": cy + d, "xend": cx + d, "yend": cy - d})
df_prune_marks = pd.DataFrame(prune_mark_records)

# Plot
plot = (
    ggplot()
    + geom_segment(aes(x="x", y="y", xend="xend", yend="yend"), data=df_active, size=1.5, color="#555555")
    + geom_segment(
        aes(x="x", y="y", xend="xend", yend="yend"), data=df_pruned, size=1.2, color="#AAAAAA", linetype="dashed"
    )
    + geom_segment(aes(x="x", y="y", xend="xend", yend="yend"), data=df_prune_marks, size=1.5, color="#CC3333")
    + geom_point(aes(x="x", y="y"), data=df_decision, shape=22, size=14, fill="#306998", color="#1A3D5C", stroke=1.5)
    + geom_point(aes(x="x", y="y"), data=df_chance, shape=21, size=14, fill="#E8A838", color="#B8841A", stroke=1.5)
    + geom_point(aes(x="x", y="y"), data=df_terminal, shape=24, size=10, fill="#6AAB6A", color="#4A8B4A", stroke=1.5)
    + geom_text(aes(x="x", y="y", label="label"), data=df_branch_labels, size=9, color="#333333")
    + geom_text(aes(x="x", y="y", label="label"), data=df_values, size=9, color="#222222", fontface="bold")
    + geom_point(
        aes(x="x", y="y"),
        data=pd.DataFrame([{"x": 14.5, "y": 1.8}]),
        shape=22,
        size=10,
        fill="#306998",
        color="#1A3D5C",
        stroke=1.2,
    )
    + geom_point(
        aes(x="x", y="y"),
        data=pd.DataFrame([{"x": 14.5, "y": 1.2}]),
        shape=21,
        size=10,
        fill="#E8A838",
        color="#B8841A",
        stroke=1.2,
    )
    + geom_point(
        aes(x="x", y="y"),
        data=pd.DataFrame([{"x": 14.5, "y": 0.6}]),
        shape=24,
        size=8,
        fill="#6AAB6A",
        color="#4A8B4A",
        stroke=1.2,
    )
    + geom_text(
        aes(x="x", y="y", label="label"),
        data=pd.DataFrame(
            [
                {"x": 15.2, "y": 1.8, "label": "Decision Node"},
                {"x": 15.2, "y": 1.2, "label": "Chance Node"},
                {"x": 15.2, "y": 0.6, "label": "Terminal Node"},
            ]
        ),
        size=8,
        color="#555555",
        hjust=0,
    )
    + scale_x_continuous(limits=[-1.5, 23])
    + scale_y_continuous(limits=[0.5, 10])
    + labs(title="Product Launch Strategy · tree-decision · letsplot · pyplots.ai")
    + theme_void()
    + theme(plot_title=element_text(size=24, hjust=0.5), plot_margin=[40, 20, 20, 20])
    + ggsize(1600, 900)
)

# Save
ggsave(plot, "plot.png", path=".", scale=3)
ggsave(plot, "plot.html", path=".")
