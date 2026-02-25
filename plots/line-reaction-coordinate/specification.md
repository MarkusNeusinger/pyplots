# line-reaction-coordinate: Reaction Coordinate Energy Diagram

## Description

A reaction coordinate diagram plots potential energy against reaction progress, showing the energy landscape of a chemical transformation. The smooth curve traces the path from reactants through the transition state (energy maximum) to products, clearly depicting the activation energy barrier and overall enthalpy change. This fundamental chemistry visualization is essential for understanding reaction kinetics and thermodynamics.

## Applications

- Teaching activation energy and transition state theory in general chemistry courses
- Comparing catalyzed vs uncatalyzed reaction pathways to illustrate how catalysts lower activation energy
- Illustrating exothermic vs endothermic reactions by showing the relative energy levels of reactants and products
- Visualizing multi-step reaction mechanisms with intermediate species and multiple energy barriers

## Data

- `reaction_coordinate` (numeric) — Progress along the reaction path (arbitrary units, 0 to 1 or similar)
- `energy` (numeric) — Potential energy values in kJ/mol
- Size: 100-500 points for a smooth curve
- Example: A single-step exothermic reaction with reactants at 50 kJ/mol, transition state at 120 kJ/mol, and products at 20 kJ/mol

## Notes

- Label reactants, products, and transition state directly on the plot
- Show activation energy (Ea) with a double-headed arrow from reactant level to transition state peak
- Show enthalpy change (ΔH) with a double-headed arrow between reactant and product energy levels
- Use a smooth curve with a clear maximum at the transition state
- Horizontal dashed lines at reactant and product energy levels improve readability
- Use a clean, minimal style appropriate for scientific and educational contexts
