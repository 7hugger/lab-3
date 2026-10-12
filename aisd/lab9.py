from tkinter import Tk, Button, Label, messagebox, Frame, Radiobutton, IntVar

ROWS = 3
COLS = 3

class TicTacToe:
    def __init__(self):
        self.window = Tk()
        self.window.title("Крестики-Нолики")
        self.buttons = []
        self.turn_count = 0
        self.board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]
        self.create_start_screen()

    def create_start_screen(self):
        """Начальный экран с выбором первого игрока"""
        self.clear_window()

        frame = Frame(self.window)
        frame.pack(pady=20)

        label = Label(frame, text="Кто ходит первым?", font=('Arial', 16))
        label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        self.first_player_var = IntVar(value=1)
        human_radio = Radiobutton(frame, text="Человек", variable=self.first_player_var, value=1)
        human_radio.grid(row=1, column=0, padx=10)
        computer_radio = Radiobutton(frame, text="Компьютер", variable=self.first_player_var, value=2)
        computer_radio.grid(row=1, column=1, padx=10)

        start_button = Button(frame, text="Начать игру", command=self.start_game)
        start_button.grid(row=2, column=0, columnspan=2, pady=(10, 0))

    def clear_window(self):
        """Удаляет все виджеты из окна"""
        for widget in self.window.winfo_children():
            widget.destroy()

    def start_game(self):
        """Создает игровое поле"""
        self.current_player = 'X' if self.first_player_var.get() == 1 else 'O'
        self.clear_window()
        self.buttons.clear()
        self.turn_count = 0
        self.board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]

        for i in range(ROWS):
            row_buttons = []
            for j in range(COLS):
                btn = Button(
                    self.window,
                    text=" ",
                    font=('Arial', 20),
                    width=6,
                    height=3,
                    command=lambda x=i, y=j: self.click_button(x, y)
                )
                btn.grid(row=i, column=j)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

        if self.current_player == 'O':
            self.computer_move()

    def click_button(self, x, y):
        if self.board[x][y] != ' ':
            return

        self.board[x][y] = self.current_player
        self.buttons[x][y].config(text=self.current_player)
        self.turn_count += 1

        if self.check_win():
            messagebox.showinfo("Победитель!", f"Победил {self.current_player}")
            self.ask_to_replay()
        elif self.turn_count >= ROWS * COLS:
            messagebox.showinfo("Ничья!", "Игра закончилась вничью!")
            self.ask_to_replay()
        else:
            self.change_player()
            if self.current_player == 'O':
                self.computer_move()

    def ask_to_replay(self):
        if messagebox.askyesno("Продолжить?", "Хотите сыграть еще раз?"):
            self.create_start_screen()
        else:
            self.window.destroy()

    def computer_move(self):
        best_score = float('-inf')
        best_move = None

        for i in range(ROWS):
            for j in range(COLS):
                if self.board[i][j] == ' ':
                    self.board[i][j] = 'O'
                    score = self.minimax(self.board, False)
                    self.board[i][j] = ' '
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)

        if best_move:
            i, j = best_move
            self.board[i][j] = 'O'
            self.buttons[i][j].config(text='O')
            self.turn_count += 1

            if self.check_win():
                messagebox.showinfo("Победитель!", "Выиграл компьютер!")
                self.ask_to_replay()
            elif self.turn_count >= ROWS * COLS:
                messagebox.showinfo("Ничья!", "Игра закончилась вничью!")
                self.ask_to_replay()
            else:
                self.change_player()

    def minimax(self, board, maximizing):
        winner = self.get_winner(board)
        if winner == 'X': return -1
        if winner == 'O': return 1
        if self.is_board_full(board): return 0

        if maximizing:
            best_score = float('-inf')
            for i in range(ROWS):
                for j in range(COLS):
                    if board[i][j] == ' ':
                        board[i][j] = 'O'
                        score = self.minimax(board, False)
                        board[i][j] = ' '
                        best_score = max(best_score, score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(ROWS):
                for j in range(COLS):
                    if board[i][j] == ' ':
                        board[i][j] = 'X'
                        score = self.minimax(board, True)
                        board[i][j] = ' '
                        best_score = min(best_score, score)
            return best_score

    def get_winner(self, board):
        for i in range(ROWS):
            if board[i][0] != ' ' and all(board[i][j] == board[i][0] for j in range(COLS)):
                return board[i][0]
        for j in range(COLS):
            if board[0][j] != ' ' and all(board[i][j] == board[0][j] for i in range(ROWS)):
                return board[0][j]
        if board[0][0] != ' ' and all(board[i][i] == board[0][0] for i in range(ROWS)):
            return board[0][0]
        if board[0][COLS-1] != ' ' and all(board[i][COLS-i-1] == board[0][COLS-1] for i in range(ROWS)):
            return board[0][COLS-1]
        return None

    def check_win(self):
        return self.get_winner(self.board) is not None

    def change_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def is_board_full(self, board):
        return all(board[i][j] != ' ' for i in range(ROWS) for j in range(COLS))

    def start(self):
        self.window.mainloop()


if __name__ == "__main__":
    game = TicTacToe()
    game.start()

