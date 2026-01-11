# crossword-basic: Crossword Puzzle Grid

## Description

A crossword puzzle grid visualization with white entry cells for letters, black blocking cells, and numbered starting positions for across and down words. The symmetric black cell pattern follows traditional newspaper-style crossword conventions, creating a clean and recognizable puzzle layout suitable for printing or digital display.

## Applications

- Printable crossword puzzles for newspapers and puzzle books
- Educational vocabulary exercises and language learning tools
- Custom puzzle generation for events or themed activities
- Interactive puzzle games and mobile applications

## Data

- `grid` (2D array) - Binary pattern indicating blocked (1) and entry (0) cells
- `numbers` (dict) - Mapping of cell positions to clue numbers for word starts
- Size: 10x10 to 15x15 cells typical for standard crosswords
- Example: 15x15 grid with symmetric black cell pattern and numbered word positions

## Notes

- White cells for letter entry, black cells for blocking
- Numbers placed in top-left corner of cells that start words (across or down)
- Traditional 180-degree rotational symmetry for black cell placement
- Clean, uniform grid lines separating all cells
- Monochrome design optimized for printing
- Cell aspect ratio should be 1:1 (square cells)
