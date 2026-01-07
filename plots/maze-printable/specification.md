# maze-printable: Printable Maze Puzzle

## Description

A rectangular maze puzzle visualization with clearly marked start and goal positions. The maze is algorithmically generated to guarantee exactly one solution path from start to finish. The clean black-and-white design is optimized for printing, allowing users to solve the puzzle with a pen or pencil.

## Applications

- Printable activity sheets for children's entertainment and education
- Puzzle books and newspapers requiring programmatically generated mazes
- Educational materials teaching algorithmic thinking and problem-solving
- Restaurant placemats and waiting room entertainment

## Data

- `width` (int) - Number of cells horizontally (recommended: 15-40)
- `height` (int) - Number of cells vertically (recommended: 15-40)
- `seed` (int, optional) - Random seed for reproducible maze generation
- Size: Grid dimensions determine complexity (larger = harder)
- Example: 25x25 grid with start at top-left, goal at bottom-right

## Notes

- Use maze generation algorithms (DFS, Prim's, Kruskal's) that guarantee a single solution
- Start position typically marked with "S" or arrow, goal with "G" or star
- Wall thickness should be consistent and print-friendly (not too thin)
- Include adequate margins for printing
- Black walls on white background for maximum contrast and ink efficiency
- Passage width should accommodate pen/pencil marking
