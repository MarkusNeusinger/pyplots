# mohr-circle: Mohr's Circle for Stress Analysis

## Description

Mohr's Circle is a graphical method used to determine principal stresses, maximum shear stress, and stress transformations from a given 2D stress state. A circle is drawn on a normal stress (σ) vs. shear stress (τ) plane, with the center at ((σx + σy) / 2, 0) and a radius derived from the stress components. It is an essential tool in mechanical and civil engineering for visualizing how stress components change under coordinate rotation.

## Applications

- Determining principal stresses (σ1, σ2) in structural members under combined loading
- Finding maximum shear stress for failure analysis and material yielding criteria
- Visualizing stress transformation under arbitrary rotation angles in solid mechanics
- Teaching mechanics of materials concepts such as stress invariants and principal planes

## Data

- `sigma_x` (numeric) — normal stress in the x-direction (MPa)
- `sigma_y` (numeric) — normal stress in the y-direction (MPa)
- `tau_xy` (numeric) — shear stress on the xy-plane (MPa)
- Size: single stress state (3 values) defining the circle

## Notes

- Draw the circle with center at ((σx + σy) / 2, 0) and radius √(((σx − σy) / 2)² + τxy²)
- Mark the principal stresses (σ1, σ2) where the circle intersects the horizontal axis
- Show maximum shear stress (τ_max) at the top and bottom of the circle
- Plot the stress points A(σx, τxy) and B(σy, −τxy) on the circle
- Annotate the angle of the principal planes (2θp) as the angle from the reference points to the principal stress axis
- Use equal aspect ratio so the circle appears as a true circle
- Label axes: horizontal as "Normal Stress σ (MPa)", vertical as "Shear Stress τ (MPa)"
- Include a light grid and reference lines through the center for readability
