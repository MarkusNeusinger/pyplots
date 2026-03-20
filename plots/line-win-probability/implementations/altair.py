""" pyplots.ai
line-win-probability: Win Probability Chart
Library: altair 6.0.0 | Python 3.14.3
Quality: 85/100 | Created: 2026-03-20
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Simulated NFL game: Eagles vs Cowboys
np.random.seed(42)

quarters = [0, 15, 30, 45, 60]
quarter_labels = ["Kickoff", "Q2", "Q3", "Q4", "Final"]

plays = np.linspace(0, 60, 200)
prob = np.full_like(plays, 0.5)
events = []

scoring_plays = [
    (5, -0.10, "FG Cowboys 0-3"),
    (12, 0.20, "TD Eagles 7-3"),
    (18, -0.18, "TD Cowboys 7-10"),
    (24, 0.15, "FG Eagles 10-10"),
    (31, 0.18, "TD Eagles 17-10"),
    (37, -0.22, "TD Cowboys 17-17"),
    (40, -0.12, "FG Cowboys 17-20"),
    (48, 0.28, "TD Eagles 24-20"),
    (53, 0.10, "FG Eagles 27-20"),
    (58, 0.08, "INT Eagles seal it"),
]

for i in range(1, len(plays)):
    dt = plays[i] - plays[i - 1]
    drift = 0.0
    for event_time, shift, label in scoring_plays:
        if plays[i - 1] < event_time <= plays[i]:
            drift += shift
            events.append((event_time, label))
    noise = np.random.normal(0, 0.008)
    prob[i] = np.clip(prob[i - 1] + drift + noise, 0.01, 0.99)

prob[-1] = 1.0
prob[-2] = 0.98
prob[-3] = 0.95

df = pd.DataFrame({"minute": plays, "win_prob": prob})
df["win_pct"] = df["win_prob"] * 100
df["above_50"] = df["win_pct"].clip(lower=50)
df["below_50"] = df["win_pct"].clip(upper=50)

df_events = pd.DataFrame(events, columns=["minute", "label"])
df_events["win_pct"] = [np.interp(m, df["minute"], df["win_pct"]) for m in df_events["minute"]]

df_quarters = pd.DataFrame({"minute": quarters, "label": quarter_labels})

# Plot
base = alt.Chart(df)

baseline = base.mark_rule(strokeDash=[6, 4], strokeWidth=2, color="#888888").encode(y=alt.datum(50))

area_home = base.mark_area(interpolate="monotone", opacity=0.4, color="#004C54").encode(
    x=alt.X("minute:Q", title="Game Time (minutes)", scale=alt.Scale(domain=[0, 60])),
    y=alt.Y("above_50:Q", title="Win Probability (%)", scale=alt.Scale(domain=[0, 100])),
    y2=alt.datum(50),
)

area_away = base.mark_area(interpolate="monotone", opacity=0.4, color="#7B2D26").encode(
    x="minute:Q", y=alt.Y("below_50:Q", scale=alt.Scale(domain=[0, 100])), y2=alt.datum(50)
)

line = base.mark_line(interpolate="monotone", strokeWidth=3, color="#306998").encode(
    x="minute:Q",
    y=alt.Y("win_pct:Q"),
    tooltip=[
        alt.Tooltip("minute:Q", title="Minute", format=".1f"),
        alt.Tooltip("win_pct:Q", title="Win Prob %", format=".1f"),
    ],
)

event_points = (
    alt.Chart(df_events)
    .mark_circle(size=200, color="#E84855", stroke="white", strokeWidth=2)
    .encode(
        x="minute:Q",
        y="win_pct:Q",
        tooltip=[alt.Tooltip("label:N", title="Event"), alt.Tooltip("minute:Q", title="Minute", format=".0f")],
    )
)

event_labels = (
    alt.Chart(df_events)
    .mark_text(fontSize=13, fontWeight="bold", align="left", dx=10, dy=-12, color="#333")
    .encode(x="minute:Q", y="win_pct:Q", text="label:N")
)

quarter_rules = (
    alt.Chart(df_quarters[1:-1]).mark_rule(strokeDash=[4, 3], strokeWidth=1.5, color="#aaaaaa").encode(x="minute:Q")
)

quarter_text = (
    alt.Chart(df_quarters)
    .mark_text(fontSize=16, fontWeight="bold", dy=-14, color="#666666")
    .encode(x="minute:Q", y=alt.datum(100), text="label:N")
)

chart = (
    (area_home + area_away + baseline + line + event_points + event_labels + quarter_rules + quarter_text)
    .properties(
        width=1600,
        height=900,
        title=alt.Title(
            "Eagles vs Cowboys · line-win-probability · altair · pyplots.ai",
            fontSize=28,
            subtitle="Final Score: Eagles 27 - Cowboys 20",
            subtitleFontSize=20,
            subtitleColor="#555555",
        ),
    )
    .configure_axis(labelFontSize=18, titleFontSize=22, grid=False, domainColor="#cccccc")
    .configure_view(strokeWidth=0)
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
