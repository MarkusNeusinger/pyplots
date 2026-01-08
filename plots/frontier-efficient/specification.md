# frontier-efficient: Efficient Frontier for Portfolio Optimization

## Description

The efficient frontier is a fundamental visualization in Modern Portfolio Theory (MPT) that displays a curve of optimal portfolios offering the highest expected return for each level of risk (standard deviation). Portfolios on the frontier are "efficient" because no other portfolio exists with higher return for the same risk, or lower risk for the same return. This plot is essential for asset allocation decisions and understanding the risk-return tradeoff in investment portfolios.

## Applications

- Portfolio managers selecting optimal asset allocations based on client risk tolerance
- Financial advisors demonstrating the benefits of diversification to investors
- Quantitative analysts comparing actual portfolio positions against theoretical optimums
- Academic research in finance and economics illustrating mean-variance optimization concepts

## Data

- `return` (numeric) - Expected portfolio return (annualized, typically 0.0-0.3)
- `risk` (numeric) - Portfolio risk as standard deviation (annualized, typically 0.0-0.4)
- `weight` (optional, list) - Asset weights for each portfolio point
- Size: 50-500 simulated portfolios plus the efficient frontier curve
- Example: Randomly generated portfolios from 5-10 asset universe with historical return/covariance data

## Notes

- X-axis should show risk (standard deviation), Y-axis should show expected return
- The efficient frontier curve should be clearly distinguished (thicker line, distinct color)
- Include random portfolio scatter points to show suboptimal portfolios below the frontier
- Mark key points: minimum variance portfolio, maximum Sharpe ratio (tangency) portfolio
- Optional: Show capital market line from risk-free rate tangent to frontier
- Color coding can indicate Sharpe ratio for scatter points
