# pie-portfolio-interactive: Interactive Portfolio Allocation Chart

## Description

An interactive visualization showing portfolio weight allocation across assets, with the ability to explore holdings and sub-allocations through hover interactions and drill-down navigation. This chart enables investors and analysts to quickly understand portfolio composition at multiple levels of granularity, from high-level asset class breakdown to individual holdings. Ideal for portfolio reporting, rebalancing analysis, and investment fund communication.

## Applications

- Portfolio composition visualization for wealth management dashboards
- Asset allocation reporting in quarterly investment reports
- Investment fund breakdown for prospectus materials
- Rebalancing analysis comparing current vs target allocations

## Data

- `asset` (string) - Asset or holding name (e.g., "Apple Inc.", "US Treasury 10Y")
- `weight` (numeric) - Percentage allocation (0-100, must sum to 100)
- `category` (string, optional) - Asset class grouping (e.g., "Equities", "Fixed Income", "Alternatives")
- Size: 5-20 holdings typical, supports drill-down for larger portfolios

## Notes

- Pie or donut chart as primary visualization
- Interactive hover tooltips showing exact weights and values
- Group by asset class with click-to-drill-down into sub-holdings
- Display both percentage and absolute values where applicable
- Color-code by asset class or risk level for quick identification
- Include legend with asset class categories
- Support return-to-overview navigation from drill-down views
