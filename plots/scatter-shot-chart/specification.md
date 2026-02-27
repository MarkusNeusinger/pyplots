# scatter-shot-chart: Basketball Shot Chart

## Description

A basketball shot chart overlays shooting data on a half-court diagram, plotting each shot attempt as a point colored by outcome (made or missed). The court drawing includes the three-point arc, free-throw line, paint/key area, and basket, providing spatial context for analyzing shooting patterns and efficiency. Essential for basketball analytics and player evaluation.

## Applications

- Analyzing a player's shooting tendencies and field-goal percentage by court zone
- Scouting opposing players to identify their preferred and weakest shooting locations
- Evaluating team offensive strategies and shot selection patterns
- Sports journalism and broadcast graphics summarizing game or season performance

## Data

- `x` (numeric) — horizontal court position in feet from the basket center
- `y` (numeric) — vertical court position in feet from the basket center
- `made` (boolean) — shot outcome (True = made, False = missed)
- `shot_type` (categorical) — type of shot: "2-pointer", "3-pointer", "free-throw"
- Size: 200-500 shot attempts per player

## Notes

- Draw an accurate NBA half-court outline using standard dimensions (50 ft wide x 47 ft deep): three-point arc (23.75 ft at top, 22 ft in corners), free-throw line (15 ft from backboard), paint/key area (16 ft wide), restricted area arc, and basket/backboard
- Plot each shot as a point: green for made, red for missed
- Court lines should be drawn in a neutral color (gray or black) so shot markers stand out
- The court should fill the plot area with minimal padding; axis ticks and labels are optional since the court geometry provides spatial reference
- Use a 1:1 aspect ratio so the court is not distorted
- Optionally include a legend for made/missed and shot type
