# maze-circular: Circular Maze Puzzle

## Description

A circular maze puzzle visualization featuring concentric rings connected by radial passages. Unlike rectangular mazes, this design creates a unique solving experience where the player navigates inward through ring-shaped corridors. The maze has an entry point on the outer edge and a goal at the center, with algorithmically generated walls ensuring exactly one solvable path.

## Applications

- Printable puzzle sheets with a distinctive circular aesthetic
- Decorative maze art for posters, coasters, or wall prints
- Game level design for maze-based video games or apps
- Educational activities teaching spatial reasoning and problem-solving

## Data

- `rings` (int) - Number of concentric rings (recommended: 5-10)
- `difficulty` (string) - Difficulty level affecting passage density: "easy", "medium", or "hard"
- `seed` (int, optional) - Random seed for reproducible maze generation
- Size: More rings and higher difficulty increase complexity
- Example: 7 rings with medium difficulty, entry at outer edge, goal at center

## Notes

- Concentric circular walls form ring-shaped corridors
- Radial walls divide each ring into sectors
- Radial passages connect adjacent rings at strategic points
- Entry point clearly marked on the outer perimeter
- Goal/finish clearly marked at the center
- Maze generation algorithm must guarantee exactly one solution
- Black walls on white background for print-friendly output
- Wall thickness should be consistent and suitable for pen/pencil solving
