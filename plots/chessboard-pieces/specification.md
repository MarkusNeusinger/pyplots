# chessboard-pieces: Chess Board with Pieces for Position Diagrams

## Description

A chess board visualization with pieces that can be positioned programmatically to display specific game positions, puzzles, or notable games. Pieces are defined using a dictionary mapping squares (e.g., 'e4': 'K') to standard chess notation where uppercase letters represent white pieces (K/Q/R/B/N/P) and lowercase represent black pieces (k/q/r/b/n/p). Unicode chess symbols provide clean, recognizable piece rendering.

## Applications

- Chess puzzle diagrams for tactics training and educational materials
- Game position documentation showing critical moments from famous matches
- Opening repertoire visualization for chess study and preparation
- Tournament analysis and annotated game publications

## Data

- `pieces` (dict) - Dictionary mapping square names to piece codes (e.g., {'e1': 'K', 'e8': 'k', 'd4': 'Q'})
- `square` (string) - Algebraic notation with column (a-h) and row (1-8)
- `piece` (string) - Single character: K/Q/R/B/N/P for white, k/q/r/b/n/p for black
- Example: Starting position, Scholar's Mate, or any custom arrangement

## Notes

- Use Unicode chess symbols: White pieces (U+2654 to U+2659), Black pieces (U+265A to U+265F)
- Board orientation follows standard convention with white at bottom (rows 1-2)
- Light square at h1 corner as per chess standards
- Piece symbols should be centered within their squares
- Consider slight size adjustment so pieces don't touch square edges
- Color scheme should provide good contrast for both board squares and piece visibility
