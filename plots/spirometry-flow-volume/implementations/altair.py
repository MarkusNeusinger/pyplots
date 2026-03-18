""" pyplots.ai
spirometry-flow-volume: Spirometry Flow-Volume Loop
Library: altair 6.0.0 | Python 3.14.3
Quality: 85/100 | Created: 2026-03-18
"""

import altair as alt
import numpy as np
import pandas as pd


# Data
np.random.seed(42)

fvc_measured = 4.8
fev1_measured = 3.2
pef_measured = 9.5

fvc_predicted = 5.2
pef_predicted = 10.5

n_points = 150


def generate_loop(fvc, pef, insp_depth, add_noise=False):
    """Generate expiratory + inspiratory limb data for a flow-volume loop."""
    vol_exp = np.linspace(0, fvc, n_points)
    pef_idx = int(n_points * 0.12)
    flow_rise = np.linspace(0, pef, pef_idx + 1)
    vol_remaining = vol_exp[pef_idx:] - vol_exp[pef_idx]
    vol_range = fvc - vol_exp[pef_idx]
    flow_decline = pef * (1 - (vol_remaining / vol_range) ** 0.85)
    flow_exp = np.concatenate([flow_rise, flow_decline[1:]])
    if add_noise:
        flow_exp += np.random.normal(0, 0.03, len(flow_exp))
    flow_exp = np.clip(flow_exp, 0, None)
    flow_exp[0] = 0
    flow_exp[-1] = 0

    vol_insp = np.linspace(fvc, 0, n_points)
    t_insp = np.linspace(0, np.pi, n_points)
    flow_insp = -insp_depth * np.sin(t_insp)
    if add_noise:
        flow_insp += np.random.normal(0, 0.03, len(flow_insp))
    flow_insp[0] = 0
    flow_insp[-1] = 0

    return vol_exp, flow_exp, vol_insp, flow_insp


vol_exp, flow_exp, vol_insp, flow_insp = generate_loop(fvc_measured, pef_measured, 5.5, add_noise=True)
vol_pred_exp, flow_pred_exp, vol_pred_insp, flow_pred_insp = generate_loop(
    fvc_predicted, pef_predicted, 6.2, add_noise=False
)

# Combine into dataframes with curve type for legend
df_measured = pd.concat(
    [pd.DataFrame({"volume": vol_exp, "flow": flow_exp}), pd.DataFrame({"volume": vol_insp, "flow": flow_insp})],
    ignore_index=True,
)
df_measured["curve"] = "Measured"
df_measured["order"] = range(len(df_measured))

df_predicted = pd.concat(
    [
        pd.DataFrame({"volume": vol_pred_exp, "flow": flow_pred_exp}),
        pd.DataFrame({"volume": vol_pred_insp, "flow": flow_pred_insp}),
    ],
    ignore_index=True,
)
df_predicted["curve"] = "Predicted"
df_predicted["order"] = range(len(df_predicted))

# Merge all curve data for unified legend encoding
df_all = pd.concat([df_measured, df_predicted], ignore_index=True)

# PEF annotation point
pef_vol = vol_exp[np.argmax(flow_exp)]
pef_flow = float(flow_exp.max())
df_pef = pd.DataFrame({"volume": [pef_vol], "flow": [pef_flow], "label": [f"PEF = {pef_flow:.1f} L/s"]})

# Clinical values annotation
df_clinical = pd.DataFrame(
    {
        "volume": [5.5],
        "flow": [8.5],
        "label": [f"FVC = {fvc_measured:.1f} L\nFEV\u2081 = {fev1_measured:.1f} L\nPEF = {pef_flow:.1f} L/s"],
    }
)

# Plot - unified encoding for proper legend
color_scale = alt.Scale(domain=["Measured", "Predicted"], range=["#306998", "#888888"])
dash_scale = alt.Scale(domain=["Measured", "Predicted"], range=[[0], [8, 6]])

# Nearest selection for interactive tooltip on hover (Altair-distinctive)
nearest = alt.selection_point(nearest=True, on="pointerover", fields=["order"], empty=False)

# Main curves with legend via color + strokeDash encoding
curves = (
    alt.Chart(df_all)
    .mark_line(strokeWidth=2.5)
    .encode(
        x=alt.X("volume:Q", title="Volume (L)", scale=alt.Scale(domain=[-0.3, 6.5])),
        y=alt.Y("flow:Q", title="Flow (L/s)", scale=alt.Scale(domain=[-8, 12])),
        order="order:Q",
        color=alt.Color(
            "curve:N",
            title=None,
            scale=color_scale,
            legend=alt.Legend(labelFontSize=16, symbolSize=300, symbolStrokeWidth=3, orient="top-right", offset=-10),
        ),
        strokeDash=alt.StrokeDash("curve:N", title=None, scale=dash_scale, legend=None),
        strokeWidth=alt.condition(alt.datum.curve == "Measured", alt.value(3), alt.value(2)),
    )
)

# Interactive tooltip layer (Altair-distinctive: hover reveals flow/volume values)
tooltip_points = (
    alt.Chart(df_measured)
    .mark_point(opacity=0, size=80)
    .encode(
        x="volume:Q",
        y="flow:Q",
        tooltip=[
            alt.Tooltip("volume:Q", title="Volume (L)", format=".2f"),
            alt.Tooltip("flow:Q", title="Flow (L/s)", format=".2f"),
        ],
    )
    .add_params(nearest)
)

hover_rule = (
    alt.Chart(df_measured)
    .mark_rule(color="#666666", strokeWidth=1, strokeDash=[3, 3])
    .encode(x="volume:Q")
    .transform_filter(nearest)
)

hover_point = (
    alt.Chart(df_measured)
    .mark_point(size=120, filled=True, color="#306998")
    .encode(x="volume:Q", y="flow:Q")
    .transform_filter(nearest)
)

# PEF marker and label
pef_point = alt.Chart(df_pef).mark_point(size=280, filled=True, color="#C0392B").encode(x="volume:Q", y="flow:Q")

pef_label = (
    alt.Chart(df_pef)
    .mark_text(align="left", dx=16, dy=-16, fontSize=18, fontWeight="bold", color="#C0392B")
    .encode(x="volume:Q", y="flow:Q", text="label:N")
)

# Clinical values text
clinical_text = (
    alt.Chart(df_clinical)
    .mark_text(align="left", fontSize=17, lineBreak="\n", lineHeight=22, color="#444444", fontWeight="bold")
    .encode(x="volume:Q", y="flow:Q", text="label:N")
)

# Zero flow reference line
df_zero = pd.DataFrame({"volume": [-0.3, 6.5], "flow": [0, 0]})
zero_line = (
    alt.Chart(df_zero).mark_line(strokeWidth=1, strokeDash=[4, 4], color="#bbbbbb").encode(x="volume:Q", y="flow:Q")
)

chart = (
    (zero_line + curves + tooltip_points + hover_rule + hover_point + pef_point + pef_label + clinical_text)
    .properties(
        width=1600,
        height=900,
        title=alt.Title(
            "spirometry-flow-volume · altair · pyplots.ai",
            fontSize=28,
            anchor="start",
            color="#222222",
            subtitleColor="#666666",
        ),
    )
    .configure_axis(
        labelFontSize=18,
        titleFontSize=22,
        gridOpacity=0.15,
        gridColor="#cccccc",
        domainColor="#444444",
        tickColor="#888888",
        labelColor="#333333",
        titleColor="#222222",
    )
    .configure_view(strokeWidth=0)
    .configure_legend(padding=10, cornerRadius=4, strokeColor="#dddddd")
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
