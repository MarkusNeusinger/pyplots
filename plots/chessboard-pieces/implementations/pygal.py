"""pyplots.ai
chessboard-pieces: Chess Board with Pieces for Position Diagrams
Library: pygal | Python 3.13
Quality: pending | Created: 2026-01-08
"""

import pygal
from pygal.style import Style


# Map piece codes to Unicode chess symbols for value_formatter
# Using simple integer codes: 1-6 for white, 11-16 for black
PIECE_CODE_MAP = {
    1: "\u2654",  # White King
    2: "\u2655",  # White Queen
    3: "\u2656",  # White Rook
    4: "\u2657",  # White Bishop
    5: "\u2658",  # White Knight
    6: "\u2659",  # White Pawn
    11: "\u265a",  # Black King
    12: "\u265b",  # Black Queen
    13: "\u265c",  # Black Rook
    14: "\u265d",  # Black Bishop
    15: "\u265e",  # Black Knight
    16: "\u265f",  # Black Pawn
}

PIECE_TO_CODE = {"K": 1, "Q": 2, "R": 3, "B": 4, "N": 5, "P": 6, "k": 11, "q": 12, "r": 13, "b": 14, "n": 15, "p": 16}

# Scholar's Mate position - a famous quick checkmate
# After 1.e4 e5 2.Bc4 Nc6 3.Qh5 Nf6?? 4.Qxf7#
pieces = {
    # White pieces
    "a1": "R",
    "b1": "N",
    "c1": "B",
    "d1": "K",
    "h1": "R",
    "a2": "P",
    "b2": "P",
    "c2": "P",
    "d2": "P",
    "f2": "P",
    "g2": "P",
    "h2": "P",
    "c4": "B",
    "e4": "P",
    "f7": "Q",
    # Black pieces
    "a8": "r",
    "b8": "n",
    "c8": "b",
    "d8": "q",
    "e8": "k",
    "h8": "r",
    "a7": "p",
    "b7": "p",
    "c7": "p",
    "d7": "p",
    "g7": "p",
    "h7": "p",
    "c6": "n",
    "e5": "p",
    "f6": "n",
}

# Chess board configuration
columns = ["a", "b", "c", "d", "e", "f", "g", "h"]
col_to_idx = {col: i for i, col in enumerate(columns)}

# Classic chess board colors
light_color = "#F0D9B5"  # Cream/tan for light squares
dark_color = "#B58863"  # Brown for dark squares

# Convert pieces dict to a grid for easier access
piece_grid = {}
for square, piece in pieces.items():
    col_idx = col_to_idx[square[0]]
    row_num = int(square[1])
    piece_grid[(col_idx, row_num)] = PIECE_TO_CODE[piece]


# Value formatter to display chess pieces
# Values are encoded as: base_value + piece_code/1000
# e.g., 1.005 = row value 1, piece code 5 (white knight)
# Using /1000 to keep values close to 1.0 and avoid visible stacking issues
def piece_formatter(x):
    if isinstance(x, (int, float)) and x >= 0.9:
        # Extract piece code from decimal part (scaled by 1000)
        decimal = round((x % 1) * 1000)
        if decimal in PIECE_CODE_MAP:
            return PIECE_CODE_MAP[decimal]
    return ""


# Create custom style with large fonts for pieces
custom_style = Style(
    background="#FFFFFF",
    plot_background="#FFFFFF",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#555555",
    title_font_size=72,
    label_font_size=52,
    major_label_font_size=48,
    legend_font_size=0,
    value_font_size=100,
    font_family="DejaVu Sans",
    opacity=1.0,
    opacity_hover=1.0,
    transition="0s",
)

# Create the board using stacked bars with pieces encoded in values
board = pygal.StackedBar(
    style=custom_style,
    width=3600,
    height=3600,
    title="Scholar's Mate · chessboard-pieces · pygal · pyplots.ai",
    show_legend=False,
    show_y_guides=False,
    show_x_guides=False,
    spacing=0,
    margin=180,
    margin_left=180,
    margin_right=180,
    margin_bottom=180,
    print_values=True,
    print_values_position="center",
    print_zeroes=False,
    truncate_label=-1,
    show_y_labels=False,
    range=(0, 8),
    value_formatter=piece_formatter,
)

# X-axis labels (columns a-h at bottom)
board.x_labels = columns

# Build data for each row from row 1 (bottom) to row 8 (top)
for row_num in range(1, 9):
    row_data = []
    for col_idx in range(8):
        # Standard chess: a1 is dark (col_idx=0, row=1: 0+1=1 odd -> dark)
        # h1 is light (col_idx=7, row=1: 7+1=8 even -> light)
        is_light = (col_idx + row_num) % 2 == 0
        color = light_color if is_light else dark_color

        # Encode piece in the value: 1 + piece_code/1000
        piece_code = piece_grid.get((col_idx, row_num), 0)
        value = 1 + piece_code / 1000

        row_data.append({"value": value, "color": color})

    board.add(str(row_num), row_data)

# Render to files
board.render_to_file("plot.svg")
board.render_to_png("plot.png")
board.render_to_file("plot.html")
