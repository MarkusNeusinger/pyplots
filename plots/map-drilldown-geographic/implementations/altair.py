"""pyplots.ai
map-drilldown-geographic: Drillable Geographic Map
Library: altair | Python 3.13
Quality: pending | Created: 2025-01-20
"""

import altair as alt
import pandas as pd


# Data - hierarchical sales data for US states with drill-down by region
# US TopoJSON from vega-datasets CDN
us_states_url = "https://cdn.jsdelivr.net/npm/vega-datasets@v1.29.0/data/us-10m.json"

states_data = pd.DataFrame(
    {
        "id": [
            1,
            2,
            4,
            5,
            6,
            8,
            9,
            10,
            11,
            12,
            13,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
            25,
            26,
            27,
            28,
            29,
            30,
            31,
            32,
            33,
            34,
            35,
            36,
            37,
            38,
            39,
            40,
            41,
            42,
            44,
            45,
            46,
            47,
            48,
            49,
            50,
            51,
            53,
            54,
            55,
            56,
        ],
        "state": [
            "Alabama",
            "Alaska",
            "Arizona",
            "Arkansas",
            "California",
            "Colorado",
            "Connecticut",
            "Delaware",
            "District of Columbia",
            "Florida",
            "Georgia",
            "Hawaii",
            "Idaho",
            "Illinois",
            "Indiana",
            "Iowa",
            "Kansas",
            "Kentucky",
            "Louisiana",
            "Maine",
            "Maryland",
            "Massachusetts",
            "Michigan",
            "Minnesota",
            "Mississippi",
            "Missouri",
            "Montana",
            "Nebraska",
            "Nevada",
            "New Hampshire",
            "New Jersey",
            "New Mexico",
            "New York",
            "North Carolina",
            "North Dakota",
            "Ohio",
            "Oklahoma",
            "Oregon",
            "Pennsylvania",
            "Rhode Island",
            "South Carolina",
            "South Dakota",
            "Tennessee",
            "Texas",
            "Utah",
            "Vermont",
            "Virginia",
            "Washington",
            "West Virginia",
            "Wisconsin",
            "Wyoming",
        ],
        "value": [
            145,
            78,
            210,
            98,
            520,
            185,
            165,
            72,
            95,
            380,
            275,
            88,
            62,
            310,
            155,
            92,
            88,
            125,
            142,
            48,
            195,
            225,
            245,
            168,
            85,
            155,
            45,
            68,
            175,
            52,
            285,
            78,
            425,
            265,
            35,
            295,
            112,
            145,
            320,
            42,
            135,
            38,
            195,
            485,
            95,
            28,
            255,
            215,
            58,
            165,
            25,
        ],
    }
)

# Region assignments for hierarchical drill-down
regions = {
    "West": [
        "California",
        "Oregon",
        "Washington",
        "Nevada",
        "Arizona",
        "Utah",
        "Colorado",
        "New Mexico",
        "Wyoming",
        "Montana",
        "Idaho",
        "Alaska",
        "Hawaii",
    ],
    "Midwest": [
        "Illinois",
        "Indiana",
        "Iowa",
        "Kansas",
        "Michigan",
        "Minnesota",
        "Missouri",
        "Nebraska",
        "North Dakota",
        "Ohio",
        "South Dakota",
        "Wisconsin",
    ],
    "South": [
        "Texas",
        "Florida",
        "Georgia",
        "North Carolina",
        "Virginia",
        "Tennessee",
        "Louisiana",
        "Kentucky",
        "South Carolina",
        "Alabama",
        "Oklahoma",
        "Arkansas",
        "Mississippi",
        "West Virginia",
        "Maryland",
        "Delaware",
        "District of Columbia",
    ],
    "Northeast": [
        "New York",
        "Pennsylvania",
        "New Jersey",
        "Massachusetts",
        "Connecticut",
        "Rhode Island",
        "Vermont",
        "New Hampshire",
        "Maine",
    ],
}

# Add region column to states data
region_map = {state: region for region, states in regions.items() for state in states}
states_data["region"] = states_data["state"].map(region_map).fillna("Other")

# Create regional aggregation for the overview level
region_data = (
    states_data.groupby("region").agg(total_value=("value", "sum"), num_states=("state", "count")).reset_index()
)
region_data["avg_value"] = region_data["total_value"] / region_data["num_states"]

# Selection parameter for drill-down interaction (defined once)
region_select = alt.selection_point(fields=["region"], name="drill")

# Base US states map with topojson
states_map = alt.topo_feature(us_states_url, "states")

# Main choropleth map - states colored by value, highlighted when region selected
choropleth = (
    alt.Chart(states_map)
    .mark_geoshape(stroke="white", strokeWidth=1.5)
    .encode(
        color=alt.condition(
            region_select,
            alt.Color(
                "value:Q",
                scale=alt.Scale(scheme="blues", domain=[0, 550]),
                legend=alt.Legend(
                    title="Sales Value",
                    titleFontSize=18,
                    labelFontSize=14,
                    orient="right",
                    gradientLength=400,
                    gradientThickness=25,
                ),
            ),
            alt.value("lightgray"),
        ),
        opacity=alt.condition(region_select, alt.value(1), alt.value(0.4)),
        tooltip=[
            alt.Tooltip("state:N", title="State"),
            alt.Tooltip("region:N", title="Region"),
            alt.Tooltip("value:Q", title="Sales Value", format=",.0f"),
        ],
    )
    .transform_lookup(lookup="id", from_=alt.LookupData(states_data, "id", ["state", "value", "region"]))
    .properties(width=1200, height=700)
)

# Region bar chart - click to drill down and filter states
region_bars = (
    alt.Chart(region_data)
    .mark_bar(cornerRadiusTopRight=5, cornerRadiusBottomRight=5)
    .encode(
        y=alt.Y("region:N", sort="-x", title=None, axis=alt.Axis(labelFontSize=16, labelFontWeight="bold")),
        x=alt.X("total_value:Q", title="Total Sales", axis=alt.Axis(labelFontSize=14, titleFontSize=16)),
        color=alt.condition(
            region_select,
            alt.Color(
                "region:N",
                scale=alt.Scale(
                    domain=["West", "South", "Midwest", "Northeast"], range=["#306998", "#FFD43B", "#6B8E23", "#CD5C5C"]
                ),
                legend=None,
            ),
            alt.value("lightgray"),
        ),
        opacity=alt.condition(region_select, alt.value(1), alt.value(0.4)),
        tooltip=[
            alt.Tooltip("region:N", title="Region"),
            alt.Tooltip("total_value:Q", title="Total Sales", format=",.0f"),
            alt.Tooltip("num_states:Q", title="States"),
            alt.Tooltip("avg_value:Q", title="Avg per State", format=",.0f"),
        ],
    )
    .add_params(region_select)
    .properties(width=350, height=200, title=alt.Title("Click to Drill Down by Region", fontSize=18))
)

# State detail chart - shows states when region is selected
state_bars = (
    alt.Chart(states_data)
    .mark_bar(cornerRadiusTopRight=5, cornerRadiusBottomRight=5)
    .encode(
        y=alt.Y("state:N", sort="-x", title=None, axis=alt.Axis(labelFontSize=12)),
        x=alt.X("value:Q", title="Sales Value", axis=alt.Axis(labelFontSize=14, titleFontSize=16)),
        color=alt.Color("value:Q", scale=alt.Scale(scheme="blues"), legend=None),
        tooltip=[
            alt.Tooltip("state:N", title="State"),
            alt.Tooltip("value:Q", title="Sales", format=",.0f"),
            alt.Tooltip("region:N", title="Region"),
        ],
    )
    .transform_filter(region_select)
    .properties(width=350, height=400, title=alt.Title("States in Selected Region", fontSize=18))
)

# Combine charts with layout
sidebar = alt.vconcat(region_bars, state_bars, spacing=30)

# Final composition
chart = (
    alt.hconcat(choropleth, sidebar, spacing=40)
    .properties(
        title=alt.Title(
            "map-drilldown-geographic · altair · pyplots.ai",
            fontSize=28,
            anchor="middle",
            subtitle="Click a region bar to drill down and highlight states on the map",
            subtitleFontSize=16,
            subtitlePadding=10,
        )
    )
    .configure_view(strokeWidth=0)
    .configure_axis(grid=False)
)

# Save outputs
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
