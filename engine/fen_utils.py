"""
Utils to load and save FEN strings
"""

from typing import Dict

from engine.constants import BOARD_SIZE
from engine.board import Board
from engine.game import Game
from engine.types import Color, Location, Piece, PieceType

FEN_MAPPING: Dict[str, Piece] = {
    "p": Piece(Color.BLACK, PieceType.PAWN),
    "r": Piece(Color.BLACK, PieceType.ROOK),
    "n": Piece(Color.BLACK, PieceType.KNIGHT),
    "b": Piece(Color.BLACK, PieceType.BISHOP),
    "q": Piece(Color.BLACK, PieceType.QUEEN),
    "k": Piece(Color.BLACK, PieceType.KING),
    "P": Piece(Color.WHITE, PieceType.PAWN),
    "R": Piece(Color.WHITE, PieceType.ROOK),
    "N": Piece(Color.WHITE, PieceType.KNIGHT),
    "B": Piece(Color.WHITE, PieceType.BISHOP),
    "Q": Piece(Color.WHITE, PieceType.QUEEN),
    "K": Piece(Color.WHITE, PieceType.KING)
}

INV_FEN_MAPPING = {v: k for k, v in FEN_MAPPING.items()}


def from_fen(fen_string: str, game: Game) -> None:
    fen_data: list[str] = fen_string.strip().split(sep=" ")

    if len(fen_data) == 1:
        placement_string: str = fen_data[0]
    elif len(fen_data) == 6:
        placement_string, active_color_data, _, _, _, _ = fen_data
        active_color: Color = Color.BLACK if active_color_data.lower() == "b"\
            else Color.WHITE
        game.active_color = active_color

    placement_data: list[str] = placement_string.split("/")
    if len(placement_data) != BOARD_SIZE:
        raise ValueError(f"Invalid number of rows in the FEN string: {len(placement_data)}")

    game.reset()
    for i, rank_data in enumerate(placement_data):
        rank_repr = "".join(
            int(c)*"x" if c.isdigit() else c for c in rank_data
        )
        for j, square_data in enumerate(rank_repr):
            if square_data != "x":
                piece: Piece = FEN_MAPPING[square_data]
                game.board.place_piece(piece, (i, j))
                game.active_pieces.add((piece, Location(i, j)))


def to_fen(board: Board) -> str:
    placement_string = ""
    for i, rank in enumerate(board.board):
        empty_counter = 0
        for j in range(len(rank)):
            if board.board[i, j, 3]:
                piece: Piece = board.get_piece((i, j))
                square_data = INV_FEN_MAPPING[piece]
                if empty_counter != 0:
                    placement_string += f"{empty_counter}"
                    empty_counter = 0
                    placement_string += f"{square_data}"
                else:
                    placement_string += f"{square_data}"
            else:
                empty_counter += 1

        if empty_counter != 0:
            placement_string += f"{empty_counter}"
        placement_string += "/"
    placement_string = placement_string.strip("/")
    return placement_string
