from figures import *
from typing import Union


class Board:
    squares: list

    def __init__(self):
        self.squares = [[None for _ in range(8)] for _ in range(8)]
        # Белые: Король e1, пешки d2 e2
        self.squares[7][4] = King("e1", Color.WHITE)
        self.squares[6][3] = Pawn("d2", Color.WHITE)
        self.squares[6][4] = Pawn("e2", Color.WHITE)
        # Черные: Король e8, слон c8
        self.squares[0][4] = King("e8", Color.BLACK)
        self.squares[0][2] = Bishop("c8", Color.BLACK)



    def __repr__(self):
        board = "=" * 25 + "\n"
        for row in range(8):
            board += f"{8 - row} "
            for col in range(8):
                piece: Piece = self.squares[row][col]
                if piece is not None:
                    board += f"{piece.symbol} "
                else:
                    board += "   "
            board += "\n"
        board += "  a  b  c  d  e  f  g  h" + "\n" + "=" * 25
        return board

    def get_piece(self, pos: str) -> Union[Piece, None]:
        row, col = get_row_col(pos)
        return self.squares[row][col]

    def match_color(self, target: str, current_color: Color) -> bool:
        piece = self.get_piece(target)
        if piece is None:
            return False
        return piece.color == current_color



    def pawn_move(
        self, pos: str, target: str, color: Color, is_active: bool = True
    ) -> Union[str, bool]:
        pawn: Pawn = self.get_piece(pos)
        if pawn.move_diagonal(target, color):
            if not is_active:
                return target
            if color == Color.WHITE:
                if (
                    self.get_piece(target) is not None
                ):
                    if not self.match_color(target, pawn.color):
                        return target
                elif int(target[1]) - 1 == 5:  # Which is the only way to en passant
                    en_passant: str = target[0] + str(int(target[1]) - 1)
                    en_passant_square: Union[Pawn, None] = self.get_piece(en_passant)
                    if en_passant_square is not None and isinstance(
                        en_passant_square, Pawn
                    ):
                        if en_passant_square.jump and en_passant_square.color != color:
                            return en_passant
                return False
            else:
                if self.get_piece(target) is not None:
                    if not self.match_color(target, pawn.color):
                        return target
                elif int(target[1]) + 1 == 4:
                    en_passant: str = target[0] + str(int(target[1]) + 1)
                    en_passant_square: Union[Pawn, None] = self.get_piece(en_passant)
                    if en_passant_square is not None and isinstance(
                        en_passant_square, Pawn
                    ):
                        if en_passant_square.jump and en_passant_square.color != color:
                            return en_passant
                return False
        if not is_active:
            return False
        target_piece: Piece = self.get_piece(target)
        if target_piece is not None:
            return False
        return target

    def king_move(
        self, pos: str, target: str, color: Color, is_active: bool = True
    ) -> bool:
        return True

    def keep_checking_for_squares(
        self,
        color: Color,
        index: tuple[int],
        direction: tuple[int],
        is_active: bool = True,
        is_king: bool = False,
    ) -> list[str]:
        original_pos: str = get_square_name(*index)
        row_target: int
        col_target: int
        row_target, col_target = index
        valid_squares: list = []
        has_eaten: bool = False
        while not has_eaten:
            row_target += direction[0]
            col_target += direction[1]
            if row_target < 0 or row_target > 7 or col_target < 0 or col_target > 7:
                break
            else:
                target: str = get_square_name(row_target, col_target)
                target_piece: Union[Piece, None] = self.get_piece(target)
                if not self.get_piece(original_pos).can_move(target):
                    break
                elif isinstance(self.get_piece(original_pos), Pawn):
                    if self.pawn_move(original_pos, target, color, is_active) is False:
                        break
                elif target_piece is not None:
                    if self.match_color(target, color) and is_active:
                        break
                    else:
                        if is_active and is_king:
                            if target in self.get_all_valid_moves(
                                get_opposite_color(self.get_piece(original_pos).color),
                                is_active=False,
                            ):
                                break
                        has_eaten = True
                if is_active and is_king:
                    king: King = self.get_piece(original_pos)
                    if king.castle(target):
                        if (
                            self.get_piece("b" + king.pos[1]) is not None
                            and target == "c" + king.pos[1]
                        ):
                            break
                    if target in self.get_all_valid_moves(
                        get_opposite_color(self.get_piece(original_pos).color),
                        is_active=False,
                    ):
                        break
                valid_squares.append(target)
        return valid_squares

    def get_valid_moves_for_knights(self, pos: str, is_active: bool = True) -> list[str]:
        valid_squares: list = []
        knight: Knight = self.get_piece(pos)
        for i in range(8):
            for j in range(8):
                target: str = get_square_name(i, j)
                if knight.can_move(target):
                    if is_active:
                        if not self.match_color(target, knight.color):
                            valid_squares.append(target)
                    else:
                        valid_squares.append(target)
        return valid_squares

    def get_valid_moves(self, pos: str, is_active: bool = True) -> list[str]:
        if isinstance(self.get_piece(pos), Knight):
            return self.get_valid_moves_for_knights(pos, is_active)
        orders: list[list[int]] = [
            [-1, 0],
            [-1, 1],
            [0, 1],
            [1, 1],
            [1, 0],
            [1, -1],
            [0, -1],
            [-1, -1],
        ]
        row: int
        col: int
        row, col = get_row_col(pos)
        piece: Piece = self.squares[row][col]
        available_squares: list = []

        for order in orders:
            row_order = row + order[0]
            col_order = col + order[1]
            if row_order < 0 or row_order > 7 or col_order < 0 or col_order > 7:
                continue
            target: str = get_square_name(row_order, col_order)
            if piece is not None and piece.can_move(target):
                if isinstance(piece, Pawn):  # Check for en passant case
                    if self.pawn_move(pos, target, piece.color, is_active) is not False:
                        available_squares.extend(
                            self.keep_checking_for_squares(
                                piece.color,
                                (row, col),
                                (order[0], order[1]),
                                is_active,
                            )
                        )
                elif isinstance(piece, King):  # Check for castle case
                    if self.king_move(pos, target, piece.color, is_active):
                        available_squares.extend(
                            self.keep_checking_for_squares(
                                piece.color,
                                (row, col),
                                (order[0], order[1]),
                                is_active,
                                is_king=True,
                            )
                        )
                else:
                    available_squares.extend(
                        self.keep_checking_for_squares(
                            piece.color,
                            (row, col),
                            (order[0], order[1]),
                            is_active,
                        )
                    )
        return available_squares

    def update(
        self,
        pos: str,
        target: str,
        is_pawn: bool = False,
        do_castle: bool = False,
    ) -> None:
        if is_pawn:
            captured_square = self.pawn_move(pos, target, self.get_piece(pos).color)
            captured_row, captured_col = get_row_col(captured_square)
            self.squares[captured_row][captured_col] = None
        if do_castle:
            rook_pos = "a" if target[0] == "c" else "h"
            rook_pos += target[1]
            rook: Rook = self.get_piece(rook_pos)
            rook_target = "d" if target[0] == "c" else "f"
            rook_target += target[1]
            rook.pos = rook_target
            rook.has_castled = True
            self.get_piece(pos).has_castled = True
            self.update(rook_pos, rook_target)

        pos_row, pos_col = get_row_col(pos)
        target_row, target_col = get_row_col(target)
        self.squares[target_row][target_col] = self.squares[pos_row][pos_col]
        self.squares[pos_row][pos_col] = None

    def get_all_valid_moves(self, color: Color, is_active: bool = True) -> list[str]:
        valid_moves: list[str] = []
        for row in range(8):
            for col in range(8):
                pos: str = get_square_name(row, col)
                piece: Piece = self.get_piece(pos)
                if piece is not None and piece.color == color:
                    valid_moves.extend(self.get_valid_moves(pos, is_active))
        return list(set(valid_moves))

    def can_check(self, piece: Piece) -> bool:
        piece_moves = self.get_valid_moves(piece.pos)
        return self.get_king_pos(get_opposite_color(piece.color)) in piece_moves

    def get_king_pos(self, color: Color) -> str:
        for row in range(8):
            for col in range(8):
                pos: str = get_square_name(row, col)
                piece: Piece = self.get_piece(pos)
                if piece is not None and isinstance(piece, King) and piece.color == color:
                    return pos

    def move_to_avoid_mate(self, color: Color) -> list[str]:
        moves: list[str] = []
        for row in range(8):
            for col in range(8):
                pos: str = get_square_name(row, col)
                piece: Piece = self.get_piece(pos)
                if (
                    piece is not None
                    and piece.color == color
                    and not isinstance(piece, King)
                ):
                    valid_moves = self.get_valid_moves(pos, is_active=True)
                    moves.extend(
                        keep_wanted(
                            valid_moves, self.move_to_cover_check(piece, valid_moves)
                        )
                    )
        return list(set(moves))

    def move_to_cover_check(self, piece: Piece, piece_moves: list[str]) -> list[str]:
        moves_can_cover: list[str] = []
        for move in piece_moves:
            copy_of_board: Board = generate_cases(self.squares, Board())
            copy_of_board.update(piece.pos, move)
            if not copy_of_board.can_be_checked(piece.color):
                moves_can_cover.append(move)
        return moves_can_cover

    def can_be_checked(self, color: Color) -> bool:
        for row in range(8):
            for col in range(8):
                pos: str = get_square_name(row, col)
                piece: Piece = self.get_piece(pos)
                if piece is not None and piece.color != color:
                    if self.can_check(piece):
                        return True
        return False

    def stalemate(self, color: Color) -> bool:
        if len(self.get_all_valid_moves(color)) == 0:
            return True
        num_of_pieces: int = self.count_piece_on_board()
        if num_of_pieces <= 2:
            return True
        elif num_of_pieces == 3:
            piece: Piece = self.get_pieces_not_king(num_of_pieces)[0]
            if isinstance(piece, Knight) or isinstance(piece, Bishop):
                return True
        elif num_of_pieces == 4:
            piece_1: Piece
            piece_2: Piece
            piece_1, piece_2 = self.get_pieces_not_king(num_of_pieces)
            if piece_1.color != piece_2.color:
                if type(piece_1) == type(piece_2):
                    if isinstance(piece_1, Bishop) or isinstance(piece_1, Knight):
                        return True
        return False

    def get_pieces_not_king(self, num_pieces: int) -> list[Piece]:
        pieces: list[Piece] = []
        for row in range(8):
            for col in range(8):
                if len(pieces) == num_pieces:
                    return pieces
                pos: str = get_square_name(row, col)
                piece: Piece = self.get_piece(pos)
                if piece is not None and not isinstance(piece, King):
                    pieces.append(piece)
        return pieces

    def count_piece_on_board(self) -> int:
        count = 0
        for row in range(8):
            for col in range(8):
                if self.squares[row][col] is not None:
                    count += 1
        return count

    def get_checked_when_move(self, piece: Piece, target: str) -> bool:
        copy_of_board: Board = generate_cases(self.squares, Board())
        copy_of_board.update(piece.pos, target, is_pawn=isinstance(piece, Pawn))
        if copy_of_board.can_be_checked(piece.color):
            return True
        return False

    def moves_to_not_in_check(self, piece: Piece, piece_moves: list[str]) -> list[str]:
        moves_can_move: list[str] = []
        for move in piece_moves:
            copy_of_board: Board = generate_cases(self.squares, Board())
            copy_of_board.update(piece.pos, move, is_pawn=isinstance(piece, Pawn))
            if not copy_of_board.can_be_checked(piece.color):
                moves_can_move.append(move)
        return moves_can_move


def generate_cases(squares: list[Piece], board: Board) -> Board:
    for row in range(8):
        for col in range(8):
            board.squares[row][col] = squares[row][col]
    return board


def get_row_col(pos: str) -> tuple[int]:
    col = ord(pos[0]) - ord("a")
    row = 8 - int(pos[1])
    return row, col


def get_square_name(row: int, col: int) -> str:
    return chr(ord("a") + col) + str(8 - row)


def get_opposite_color(color: Color) -> Color:
    if color == Color.WHITE:
        return Color.BLACK
    else:
        return Color.WHITE


def keep_wanted(moves: list[str], wanted: list[str]) -> list[str]:
    return [move for move in moves if move in wanted]
