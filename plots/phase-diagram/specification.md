# phase-diagram: Phase Diagram (State Space Plot)

## Description

A phase diagram (or state space plot) displays the trajectory of a dynamical system by plotting a variable against its derivative (x vs dx/dt). This visualization reveals the qualitative behavior of systems including fixed points, limit cycles, stability, and oscillation patterns. It is essential for analyzing differential equations without solving them explicitly.

## Applications

- Analyzing simple harmonic oscillators and damped pendulum motion in physics education
- Studying predator-prey dynamics (Lotka-Volterra equations) in ecology
- Examining stability of electrical circuits with inductors and capacitors
- Visualizing attractors and bifurcations in nonlinear dynamics research

## Data

- `x` (numeric array) - Position or state variable values along the trajectory
- `dx_dt` (numeric array) - Derivative (velocity) values corresponding to each x
- `t` (numeric array, optional) - Time values for computing derivatives from raw position data
- Size: 200-2000 points for smooth trajectories
- Example: A simple pendulum with initial displacement, showing spiral convergence to equilibrium

## Notes

- Multiple trajectories from different initial conditions can reveal basin of attraction structure
- Fixed points (equilibria) occur where the trajectory crosses dx/dt = 0
- Closed loops indicate periodic oscillation (limit cycles or centers)
- Consider adding direction arrows or color gradient to show time evolution
- For damped systems, trajectories spiral inward; for driven systems, they may form limit cycles
