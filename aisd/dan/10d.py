import tkinter as tk
from tkinter import messagebox

okno = tk.Tk()
pole = [' '] * 9
current_player = 'X'
buttons = []

def create_pole():
    okno.title("Крестики-нолики")
    for i in range(3):
        for j in range(3):
            index = 3 * i + j
            button = tk.Button(okno, text='', font=('Arial', 20), width=5, height=2,
                             command=lambda idx=index: make_move(idx))
            button.grid(row=i, column=j)
            buttons.append(button)
def make_move(index):
    global current_player
    if pole[index] == ' ' and current_player == 'X':
        pole[index] = 'X'
        buttons[index].config(text='X', state='disabled')
        if not check_winner():
            current_player = 'O'
            bot_move()
def bot_move():
    global current_player
    for i in range(9):
        if pole[i] == ' ':
            pole[i] = 'O'
            if check_winner_bot() == 'O':
                buttons[i].config(text='O', state='disabled')
                check_winner()
                current_player = 'X'
                return
            pole[i] = ' '
    for i in range(9):
        if pole[i] == ' ':
            pole[i] = 'X'
            if check_winner_bot() == 'X':
                pole[i] = 'O'
                buttons[i].config(text='O', state='disabled')
                check_winner()
                current_player = 'X'
                return
            pole[i] = ' '
    ugol_pairs = [(0, 8), (2, 6)]
    for a, b in ugol_pairs:
        if pole[a] == 'X' and pole[b] == 'X':
            for move in [1, 3, 5, 7]:  
                if pole[move] == ' ':
                    pole[move] = 'O'
                    buttons[move].config(text='O', state='disabled')
                    check_winner()
                    current_player = 'X'
                    return
    for move in [4, 0, 2, 6, 8, 1, 3, 5, 7]:
        if pole[move] == ' ':
            pole[move] = 'O'
            buttons[move].config(text='O', state='disabled')
            break
    check_winner()
    current_player = 'X'
def check_winner_bot():
    wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    for a,b,c in wins:
        if pole[a] == pole[b] == pole[c] != ' ':
            return pole[a]
    return 'tie' if ' ' not in pole else None
def check_winner():
    winner = check_winner_bot()
    if winner == 'X':
        messagebox.showinfo("Победа!", "Вы победили!")
        reset_game()
        return True
    elif winner == 'O':
        messagebox.showinfo("Поражение", "Бот победил!")
        reset_game()
        return True
    elif winner == 'tie':
        messagebox.showinfo("Ничья", "Ничья!")
        reset_game()
        return True
    return False
def reset_game():
    global pole, current_player
    pole = [' '] * 9
    current_player = 'X'
    for button in buttons:
        button.config(text='', state='normal')
def main():
    create_pole()
    okno.mainloop()
if __name__ == "__main__":
    main()
