# survival-kaplan-meier: Kaplan-Meier Survival Plot

## Description

A Kaplan-Meier survival plot visualizes the probability of survival (or event-free time) over a time period using a step function. It is the standard method for estimating survival functions from time-to-event data, handling censored observations where the event has not yet occurred. The plot shows how survival probability decreases over time, with optional confidence intervals and comparison between groups.

## Applications

- Medical research tracking patient survival rates after diagnosis or treatment
- Reliability engineering analyzing time-to-failure for equipment or components
- Customer analytics measuring time-to-churn or subscription retention
- Clinical trials comparing survival outcomes between treatment and control groups

## Data

- `time` (numeric) - Time to event or censoring (e.g., days, months, years)
- `event` (binary) - Event indicator (1 = event occurred, 0 = censored)
- `group` (categorical, optional) - Grouping variable for comparing survival curves
- Size: 50-1000 observations
- Example: Clinical trial data with patient survival times and treatment groups

## Notes

- Use step function (not smooth curves) to accurately represent discrete event times
- Include 95% confidence intervals as shaded bands around the survival curve
- Mark censored observations with tick marks on the curve
- When comparing groups, use distinct colors and include a legend
- Consider adding median survival time annotation and at-risk table below the plot
- Log-rank test p-value can be included when comparing groups
