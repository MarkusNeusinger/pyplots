# timeseries-forecast-uncertainty: Time Series Forecast with Uncertainty Band

## Description

A time series plot that displays historical observed data followed by a forecast projection with confidence intervals or uncertainty bands. The plot clearly distinguishes between the historical period and the forecast period using a vertical line marker, with shaded bands representing different confidence levels (typically 80% and 95%). This visualization is essential for communicating prediction uncertainty in forecasting applications, helping stakeholders understand both the expected values and the range of possible outcomes.

## Applications

- Visualizing sales and demand forecasting with confidence intervals for inventory planning
- Displaying stock price or financial indicator predictions with uncertainty ranges for risk assessment
- Communicating weather forecast uncertainty with multiple confidence bands
- Presenting economic projections with confidence intervals for policy decisions
- Illustrating capacity planning forecasts with uncertainty bounds for resource allocation

## Data

- `date` (datetime) - Time index covering both historical and forecast periods
- `actual` (numeric) - Historical observed values (null/NaN for forecast period)
- `forecast` (numeric) - Predicted values (typically starts where actual ends, may overlap slightly)
- `lower_80` (numeric) - Lower bound of 80% confidence interval
- `upper_80` (numeric) - Upper bound of 80% confidence interval
- `lower_95` (numeric) - Lower bound of 95% confidence interval
- `upper_95` (numeric) - Upper bound of 95% confidence interval
- Size: 50-200 total points (30-150 historical + 10-50 forecast)
- Example: Monthly sales data with 3 years history and 6-month forecast from Prophet or ARIMA model

## Notes

- Use a solid line for historical data and a distinct style (dashed or different color) for forecast
- Mark the forecast start with a vertical line or shaded region
- Use nested shaded bands for confidence intervals: darker for 80%, lighter for 95%
- Semi-transparent fills (alpha 0.2-0.4) allow bands to overlap without obscuring data
- Include a clear legend identifying historical data, forecast, and confidence levels
- Consider using a consistent color family (e.g., blue for historical, orange for forecast)
