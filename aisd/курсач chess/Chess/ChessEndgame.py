from figures import *
from board import *
from typing import Union
import time
import pygame
import items as ci
import tkinter as tk
from cryptography.fernet import Fernet
from tkinter import ttk, messagebox
import os

pygame.font.init()
pygame.mixer.init()
status = False

# Генерация ключа для шифрования
def generation_key():
    return Fernet.generate_key()

# Сохранение ключа в файл
def save_key(key):
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# Загрузка ключа из файла
def load_key():
    return open("secret.key", "rb").read()

# Шифрование пароля
def encrypt_password(password):
    key = load_key()
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    return encrypted_password

# Расшифровка пароля
def decrypt_password(encrypted_password):
    key = load_key()
    f = Fernet(key)
    decrypted_password = f.decrypt(encrypted_password).decode()
    return decrypted_password

# Сохранение логина и пароля в файл
def save_credentials(username, password):
    with open("credentials.txt", "a") as f:
        f.write(f"{username}:{password.decode()}\n")

# Проверка учетных данных
def check_credentials(username, password):
    try:
        with open("credentials.txt", "r") as f:
            for line in f:
                stored_username, stored_password = line.strip().split(":")
                if stored_username == username and decrypt_password(stored_password.encode()) == password:
                    return True
    except FileNotFoundError:
        pass
    return False

# Функция для обработки регистрации
def register():
    username = entry_username.get()
    password = entry_password.get()
    if username and password:
        encrypted_password = encrypt_password(password)
        save_credentials(username, encrypted_password)
        messagebox.showinfo("Успех", "Регистрация успешна!")
    else:
        messagebox.showwarning("Предупреждение", "Пожалуйста, заполните все поля.")

# Функция для обработки входа
def login():
    global status
    username = entry_login_username.get()
    password = entry_login_password.get()
    if check_credentials(username, password):
        messagebox.showinfo("Успех", "Вход выполнен успешно!")
        status = True
        root.destroy()
    else:
        messagebox.showerror("Ошибка", "Пользователь не зарегистрирован или введены неверные учётные данные.")

# Создание ключа и его сохранение
if not os.path.exists("secret.key"):
    key = generation_key()
    save_key(key)

# Создание основного окна
root = tk.Tk()
root.title("Шахматы - Вход и регистрация")
root.geometry('%dx%d+%d+%d' % (500, 500, 670, 290))
root.configure(bg='#2c3e50')
root.resizable(False, False)

style = ttk.Style()
style.theme_use('clam')

# Добавляем стили
style.configure('TNotebook', background='#34495e', borderwidth=0)
style.configure('TNotebook.Tab',
                background='#95a5a6',
                foreground='#2c3e50',
                padding=[20, 10],
                font=('Arial', 11, 'bold'))
style.map('TNotebook.Tab',
          background=[('selected', '#e74c3c')],
          foreground=[('selected', 'white')])
style.configure('TFrame', background='#34495e')
style.configure('TLabel', background='#34495e', foreground='#ecf0f1', font=('Arial', 11))
style.configure('TEntry', fieldbackground='#ecf0f1', foreground='#2c3e50', font=('Arial', 11))
style.configure('TButton',
                background='#e74c3c',
                foreground='white',
                font=('Arial', 11, 'bold'),
                borderwidth=0,
                focuscolor='none')
style.map('TButton',
          background=[('active', '#c0392b'), ('pressed', '#c0392b')])

# Заголовок приложения
header_frame = tk.Frame(root, bg='#2c3e50', height=80)
header_frame.pack(fill='x', pady=(0, 10))
title_label = tk.Label(header_frame,
                       text="ШАХМАТЫ",
                       font=('Arial', 24, 'bold'),
                       fg='#e74c3c',
                       bg='#2c3e50')
title_label.pack(pady=20)
subtitle_label = tk.Label(header_frame,
                          text="Эндшпиль: Король+2 пешки vs Король+слон",
                          font=('Arial', 12),
                          fg='#bdc3c7',
                          bg='#2c3e50')
subtitle_label.pack()

# Создание вкладок
notebook = ttk.Notebook(root)
notebook.pack(expand=1, fill="both", padx=20, pady=10)

# Вкладка регистрации
register_tab = ttk.Frame(notebook)
notebook.add(register_tab, text="Регистрация")
register_container = tk.Frame(register_tab, bg='#34495e')
register_container.pack(expand=True, fill='both', padx=30, pady=30)
label_username = ttk.Label(register_container, text="Имя пользователя:")
label_username.grid(row=0, column=0, sticky='w', pady=(0, 10))
entry_username = ttk.Entry(register_container, width=25)
entry_username.grid(row=0, column=1, sticky='w', pady=(0, 10), padx=(10, 0))
label_password = ttk.Label(register_container, text="Пароль:")
label_password.grid(row=1, column=0, sticky='w', pady=(0, 20))
entry_password = ttk.Entry(register_container, show="*", width=25)
entry_password.grid(row=1, column=1, sticky='w', pady=(0, 20), padx=(10, 0))
button_register = ttk.Button(register_container, text="Создать аккаунт", command=register)
button_register.grid(row=2, column=0, columnspan=2, pady=10)

# Вкладка входа
login_tab = ttk.Frame(notebook)
notebook.add(login_tab, text="Вход")
login_container = tk.Frame(login_tab, bg='#34495e')
login_container.pack(expand=True, fill='both', padx=30, pady=30)
label_login_username = ttk.Label(login_container, text="Имя пользователя:")
label_login_username.grid(row=0, column=0, sticky='w', pady=(0, 10))
entry_login_username = ttk.Entry(login_container, width=25)
entry_login_username.grid(row=0, column=1, sticky='w', pady=(0, 10), padx=(10, 0))
label_login_password = ttk.Label(login_container, text="Пароль:")
label_login_password.grid(row=1, column=0, sticky='w', pady=(0, 20))
entry_login_password = ttk.Entry(login_container, show="*", width=25)
entry_login_password.grid(row=1, column=1, sticky='w', pady=(0, 20), padx=(10, 0))
button_login = ttk.Button(login_container, text="Войти в игру", command=login)
button_login.grid(row=2, column=0, columnspan=2, pady=10)

# Футер с декоративными элементами
footer_frame = tk.Frame(root, bg='#2c3e50', height=50)
footer_frame.pack(fill='x', side='bottom')
chess_chars = ["♔", "♙", "♗"]
chess_text = " ".join(chess_chars)
footer_label = tk.Label(footer_frame,
                        text=chess_text,
                        font=('Arial', 16),
                        fg='#7f8c8d',
                        bg='#2c3e50')
footer_label.pack(pady=10)

root.mainloop()

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Эндшпиль 'Король + 2 пешки vs Король + слон'")

# Цвета
DARK_GREEN = (0, 204, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
DARK_BROWN = (124, 115, 115)
LIGHT_GRAY = (173, 170, 166)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
DARK_RED = (199, 0, 0)
LIGHT_BROWN = (210, 180, 140)

# Шрифты
FONT = pygame.font.SysFont("Tahoma", 24)
sml_font = pygame.font.SysFont("Tahoma", 20)
mate_font = pygame.font.SysFont("Verdana", 40)
win_font = pygame.font.SysFont("Tahoma", 72)
check_text = FONT.render("Шах!", True, DARK_RED)
stlmt_text = mate_font.render("Ничья!", True, DARK_GREEN)
prmt_text = FONT.render("Выберите фигуру", True, BLACK)

class ChessClock:
    def __init__(self, minutes=5):
        self.white_time = minutes * 60  # В секундах
        self.black_time = minutes * 60  # В секундах
        self.current_player = Color.WHITE
        self.last_update_time = time.time()
        self.is_running = False

    def start(self, starting_player=Color.WHITE):
        self.current_player = starting_player
        self.last_update_time = time.time()
        self.is_running = True

    def switch_player(self):
        current_time = time.time()
        elapsed = current_time - self.last_update_time
        # Уменьшаем время текущего игрока
        if self.current_player == Color.WHITE:
            self.white_time = max(0, self.white_time - elapsed)
        else:
            self.black_time = max(0, self.black_time - elapsed)
        # Переключаем игрока
        self.current_player = Color.BLACK if self.current_player == Color.WHITE else Color.WHITE
        self.last_update_time = current_time

    def update(self):
        if self.is_running:
            current_time = time.time()
            elapsed = current_time - self.last_update_time
            if self.current_player == Color.WHITE:
                self.white_time = max(0, self.white_time - elapsed)
            else:
                self.black_time = max(0, self.black_time - elapsed)
            self.last_update_time = current_time

    def format_time(self, seconds):
        minutes = int(seconds) // 60
        secs = int(seconds) % 60
        return f"{minutes:02d}:{secs:02d}"

    def get_white_time(self):
        return self.format_time(self.white_time)

    def get_black_time(self):
        return self.format_time(self.black_time)

    def is_time_up(self):
        return self.white_time <= 0 or self.black_time <= 0

    def get_winner_by_time(self):
        if self.white_time <= 0 and self.black_time > 0:
            return Color.BLACK
        elif self.black_time <= 0 and self.white_time > 0:
            return Color.WHITE
        return None

class MoveLogger:
    def __init__(self):
        self.moves = []
        self.current_move_number = 1

    def add_move(self, white_move, black_move=None):
        if black_move is None:
            self.moves.append(f"{self.current_move_number}. {white_move}")
            self.current_move_number += 1
        else:
            self.moves.append(f"{self.current_move_number}. {white_move} {black_move}")
            self.current_move_number += 1

    def get_last_moves(self, max_lines=10):
        """Возвращает последние ходы для отображения"""
        return self.moves[-max_lines:] if len(self.moves) > max_lines else self.moves

# [Все функции отрисовки остаются БЕЗ ИЗМЕНЕНИЙ - draw_screen, draw_pieces, draw_options и т.д.]
def draw_screen(
    board: Board,
    current_player: Color,
    piece_moves: list[str],
    draw_moves: bool,
    check: bool,
    is_flipped: bool,
    clock: ChessClock,
    move_logger: MoveLogger
) -> None:
    SCREEN.fill(BLACK)
    SCREEN.blit(ci.CHESS_BOARD, (0, 0))
    # Панель для ходов (выше часов)
    pygame.draw.rect(SCREEN, LIGHT_GRAY, (600, 0, 400, 200))
    pygame.draw.rect(SCREEN, DARK_BROWN, (600, 200, 400, 5))  # Разделительная линия
    # Панель для часов и информации
    pygame.draw.rect(SCREEN, DARK_BROWN, (600, 205, 400, 195))
    # Рисуем информацию о текущем игроке
    draw_current_player(current_player)
    # Перемещаем сообщение о шахе вниз
    SCREEN.blit(check_text, (650, 530)) if check else None
    draw_pieces(board, is_flipped)
    if draw_moves:
        draw_available_moves(piece_moves, is_flipped)
    draw_options(clock, current_player)
    draw_move_log(move_logger)
    pygame.display.update()

def draw_move_log(move_logger: MoveLogger):
    # Заголовок таблицы ходов
    moves_title = sml_font.render("Ходы партии:", True, BLACK)
    SCREEN.blit(moves_title, (610, 10))
    # Отображаем последние ходы
    last_moves = move_logger.get_last_moves(8)  # Показываем до 8 строк
    for i, move in enumerate(last_moves):
        move_text = sml_font.render(move, True, BLACK)
        SCREEN.blit(move_text, (610, 40 + i * 20))

def draw_pieces(board: Board, is_flipped: bool) -> None:
    squares = board.squares
    for row in range(len(squares)):
        for col in range(len(squares[row])):
            piece: Union[Piece, None] = squares[row][col]
            if piece is not None:
                r, c = get_row_col_with_flip(row, col, is_flipped)
                if piece.is_clicked:
                                    pygame.draw.rect(SCREEN, YELLOW, (c * 75, r * 75, 75, 75))
                SCREEN.blit(piece.img, (c * 75, r * 75))

def draw_options(clock: ChessClock, current_player: Color) -> None:
    draw_clock_with_frame(610, 320, "Белые:", clock.get_white_time(),
                         current_player == Color.WHITE, Color.WHITE)
    draw_clock_with_frame(610, 250, "Чёрные:", clock.get_black_time(),
                         current_player == Color.BLACK, Color.BLACK)

def draw_clock_with_frame(x, y, player_name, time_str, is_active, color):
    clock_width = 180
    clock_height = 60
    frame_color = YELLOW if is_active else LIGHT_BROWN
    bg_color = LIGHT_GRAY
    pygame.draw.rect(SCREEN, frame_color, (x, y, clock_width, clock_height), 3)
    pygame.draw.rect(SCREEN, bg_color, (x + 2, y + 2, clock_width - 4, clock_height - 4))
    name_color = BLACK if color == Color.WHITE else WHITE
    player_text = sml_font.render(player_name, True, name_color)
    SCREEN.blit(player_text, (x + 10, y + 8))
    time_color = DARK_RED if is_active else BLACK
    time_text = FONT.render(time_str, True, time_color)
    SCREEN.blit(time_text, (x + 70, y + 30))

def draw_winner(current_player: Color, is_checkmate: bool, time_winner: Union[Color, None] = None) -> None:
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    SCREEN.blit(overlay, (0, 0))
    text_rect = pygame.Rect(0, 0, 500, 150)
    text_rect.center = (WIDTH // 2, HEIGHT // 2)
    pygame.draw.rect(SCREEN, WHITE, text_rect)
    pygame.draw.rect(SCREEN, BLACK, text_rect, 3)
    if time_winner:
        winner_color = "Чёрные" if time_winner == Color.WHITE else "Белые"
        winner_text = mate_font.render(f"{winner_color} победили по времени!", True, GREEN)
        text_rect_surface = winner_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        SCREEN.blit(winner_text, text_rect_surface)
    elif is_checkmate:
        winner_color = "Чёрные" if current_player == Color.WHITE else "Белые"
        winner_text = win_font.render(f"{winner_color} победили!!!", True, GREEN)
        text_rect_surface = winner_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        SCREEN.blit(winner_text, text_rect_surface)
    else:
        stlmt_text = mate_font.render("Ничья!", True, DARK_GREEN)
        text_rect_surface = stlmt_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        SCREEN.blit(stlmt_text, text_rect_surface)
    continue_text = sml_font.render("Игра завершится через 5 секунд...", True, BLACK)
    continue_rect = continue_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
    SCREEN.blit(continue_text, continue_rect)
    pygame.display.update()

def draw_available_moves(piece_moves: list[str], is_flipped: bool) -> None:
    for move in piece_moves:
        row, col = get_row_col(move)
        row, col = get_row_col_with_flip(row, col, is_flipped)
        pygame.draw.circle(SCREEN, DARK_BROWN, (col * 75 + 37, row * 75 + 37), 10)

def draw_current_player(current_player: Color) -> None:
    panel_rect = pygame.Rect(600, 400, 200, 120)
    pygame.draw.rect(SCREEN, WHITE, panel_rect)
    pygame.draw.rect(SCREEN, BLACK, panel_rect, 2)
    current_text = FONT.render("Текущий ход:", True, BLACK)
    SCREEN.blit(current_text, (610, 410))
    player_bg_rect = pygame.Rect(610, 450, 180, 50)
    bg_color = LIGHT_GRAY if current_player == Color.WHITE else DARK_BROWN
    text_color = BLACK if current_player == Color.WHITE else WHITE
    player_text = "БЕЛЫЕ" if current_player == Color.WHITE else "ЧЁРНЫЕ"
    pygame.draw.rect(SCREEN, bg_color, player_bg_rect)
    pygame.draw.rect(SCREEN, BLACK, player_bg_rect, 2)
    current_player_text = FONT.render(player_text, True, text_color)
    text_rect = current_player_text.get_rect(center=player_bg_rect.center)
    SCREEN.blit(current_player_text, text_rect)

def draw_promote_options() -> None:
    pygame.draw.rect(SCREEN, LIGHT_GRAY, (600, 0, 400, 150))
    SCREEN.blit(prmt_text, (610, 20))
    SCREEN.blit(ci.WHITE_QUEEN, (630, 50))
    SCREEN.blit(ci.WHITE_ROOK, (720, 50))
    SCREEN.blit(ci.WHITE_KNIGHT, (630, 100))
    SCREEN.blit(ci.WHITE_BISHOP, (720, 100))
    pygame.display.update()

def get_row_col_with_flip(row: int, col: int, is_flipped: bool) -> tuple[int]:
    if is_flipped:
        return 7 - row, 7 - col
    return row, col

def validate_chosen_piece(current_player: Color, board: Board, index: tuple[int]) -> bool:
    piece: Union[Piece, None] = board.squares[index[0]][index[1]]
    if piece is None:
        return False
    elif piece.color != current_player:
        return False
    else:
        piece_moves: list[str] = board.get_valid_moves(piece.pos)
        actual_piece_moves: list[str] = board.moves_to_not_in_check(piece, piece_moves)
        if len(actual_piece_moves) == 0:
            return False
        return True

def get_piece_moves(board: Board, piece: Piece) -> list[str]:
    piece_moves: list[str] = board.get_valid_moves(piece.pos)
    actual_piece_moves: list[str] = board.moves_to_not_in_check(piece, piece_moves)
    return actual_piece_moves

def validate_target_piece(
    board: Board, piece: Piece, piece_moves: list[str], index: tuple[int]
) -> bool:
    target_square: str = get_square_name(index[0], index[1])
    if target_square == piece.pos:
        return False
    if target_square not in piece_moves:
        return False
    if board.get_checked_when_move(piece, target_square):
        return False
    return True

def get_piece_symbol(piece: Piece) -> str:
    if isinstance(piece, Pawn):
        return ""
    elif isinstance(piece, Knight):
        return "N"
    elif isinstance(piece, Bishop):
        return "B"
    elif isinstance(piece, Rook):
        return "R"
    elif isinstance(piece, Queen):
        return "Q"
    elif isinstance(piece, King):
        return "K"
    return ""

def format_move(piece: Piece, target_square: str, is_capture: bool = False) -> str:
    symbol = get_piece_symbol(piece)
    capture_symbol = "x" if is_capture else ""
    return f"{symbol}{capture_symbol}{target_square}"

def promotion() -> Union[type, None]:
    draw_promote_options()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if 630 <= pos[0] <= 690:
                    if 50 <= pos[1] <= 100:
                        return Queen
                    elif 100 <= pos[1] <= 150:
                        return Knight
                elif 720 <= pos[0] <= 780:
                    if 50 <= pos[1] <= 100:
                        return Rook
                    elif 100 <= pos[1] <= 150:
                        return Bishop

def move(board: Board, piece: Piece, chosen_square: str, target_square: str, move_logger: MoveLogger,
         current_player: Color) -> str:
    is_a_pawn: bool = isinstance(piece, Pawn)
    is_a_king: bool = isinstance(piece, King)
    promote_type = None
    is_capture = board.squares[get_row_col(target_square)[0]][get_row_col(target_square)[1]] is not None
    move_notation = format_move(piece, target_square, is_capture)
    
    if is_a_pawn:
        if piece.can_promote(target_square):
            promote_type = promotion()
            move_notation += "=" + get_piece_symbol(promote_type(target_square, piece.color))
    
    if is_a_king:
        do_castle: bool = piece.castle(target_square)
        if do_castle:
            if target_square == "g1" or target_square == "g8":
                move_notation = "O-O"
            else:
                move_notation = "O-O-O"
    
    board.update(
        chosen_square,
        target_square,
        is_pawn=is_a_pawn,
        do_castle=(is_a_king and do_castle),
    )
    piece.pos = target_square
    
    if promote_type is not None:
        promote_piece_row, promote_piece_col = get_row_col(target_square)
        board.squares[promote_piece_row][promote_piece_col] = promote_type(
            target_square, piece.color
        )
    
    ci.MOVE_SOUND.play()
    return move_notation

def start():
    board: Board = Board()
    clock = ChessClock(minutes=5)  # 5 минут на каждого игрока
    move_logger = MoveLogger()
    is_flipped: bool = False
    current_player: Color = Color.WHITE
    is_choosing_target: bool = False
    can_move_piece: bool = False
    check: bool = False
    is_mate: bool = False
    is_checkmate: bool = False
    piece_moves: list[str] = []
    white_move = None
    running = True

    # Запуск шахматных часов
    clock.start(current_player)

    while running:
        # Обновление времени на часах
        clock.update()

        # Проверка на окончание времени
        if clock.is_time_up():
            time_winner = clock.get_winner_by_time()
            draw_winner(current_player, False, time_winner)
            time.sleep(5)
            running = False
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                row, col = pygame.mouse.get_pos()
                row = row // 75
                col = col // 75
                row, col = get_row_col_with_flip(row, col, is_flipped)
                if 0 <= row < 8 and 0 <= col < 8:
                    if not is_choosing_target:
                        if validate_chosen_piece(current_player, board, (col, row)):
                            piece: Piece = board.squares[col][row]
                            piece.is_clicked = True
                            piece_moves: list[str] = get_piece_moves(
                                board, board.squares[col][row]
                            )
                            is_choosing_target = True
                    else:
                        is_choosing_target = False
                        if validate_target_piece(board, piece, piece_moves, (col, row)):
                            can_move_piece = True
                            target: str = get_square_name(col, row)

                            # Записываем ход
                            move_notation = move(board, piece, piece.pos, target, move_logger, current_player)

                            if current_player == Color.WHITE:
                                white_move = move_notation
                            else:
                                if white_move:
                                    move_logger.add_move(white_move, move_notation)
                                    white_move = None
                                else:
                                    move_logger.add_move(move_notation)

                            # Переключаем часы при успешном ходе
                            clock.switch_player()
                            current_player = (
                                Color.BLACK
                                if current_player == Color.WHITE
                                else Color.WHITE
                            )
                        else:
                            piece.is_clicked = False
        if can_move_piece:
            king_pos: str = board.get_king_pos(get_opposite_color(piece.color))
            king: King = board.get_piece(king_pos)

            # If check
            if board.can_check(board.get_piece(target)):
                king.in_check = True
                check = True
                moves_to_cover_check: list = board.move_to_avoid_mate(
                    get_opposite_color(piece.color)
                )
                king_moves_to_live: list = board.get_valid_moves(king_pos)
                if moves_to_cover_check:
                    moves_to_cover_check.extend(king_moves_to_live)
                else:
                    if not king_moves_to_live:
                        is_mate = True
                        is_checkmate = True
            else:
                king.in_check = False
                check = False
                if board.stalemate(get_opposite_color(piece.color)):
                    is_mate = True
            can_move_piece = False
            piece.is_clicked = False

        draw_screen(
            board,
            current_player,
            piece_moves,
            is_choosing_target,
            check,
            is_flipped,
            clock,
            move_logger
        )
        if current_player == Color.BLACK and not is_choosing_target:
            import random
            # Берем случайную фигуру черных с валидными ходами
            for r in range(8):
                for c in range(8):
                    pos = get_square_name(r, c)
                    black_piece = board.get_piece(pos)
                    if black_piece and black_piece.color == Color.BLACK:
                        valid_moves = get_piece_moves(board, black_piece)  # ← ГОТОВАЯ ФУНКЦИЯ
                        if valid_moves:
                            target_pos = random.choice(valid_moves)
                            # Делаем ход
                            ai_move_notation = format_move(black_piece, target_pos)
                            if white_move:
                                move_logger.add_move(white_move, ai_move_notation)
                                white_move = None
                            else:
                                move_logger.add_move(ai_move_notation)
                            
                            board.update(pos, target_pos, is_pawn=isinstance(black_piece, Pawn))
                            black_piece.pos = target_pos
                            ci.MOVE_SOUND.play()
                            clock.switch_player()
                            current_player = Color.WHITE
                            break  # Ход сделан - выходим
                else:
                    continue
                break
        
        if is_mate:
            draw_winner(current_player, is_checkmate)
            time.sleep(5)
            running = False
    
    pygame.quit()

if __name__ == "__main__":
    if status:
        start()

