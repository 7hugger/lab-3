import tkinter as tk
from tkinter import messagebox
import random

# GAME LOGIC
class Vessel:
    def __init__(self, coords):
        self.coords = set(coords)
        self.damaged = set()
    def is_destroyed(self):
        return self.damaged == self.coords

class Field:
    def __init__(self):
        self.matrix = [[0]*10 for _ in range(10)]
        self.vessels = []
        self.attacks = set()
    def can_fit(self, row, col, length, horizontal):
        coords = [(row, col+i) if horizontal else (row+i, col) for i in range(length)]
        if any(r<0 or r>9 or c<0 or c>9 for r,c in coords):
            return False
        for r, c in coords:
            for dr in [-1,0,1]:
                for dc in [-1,0,1]:
                    nr, nc = r+dr, c+dc
                    if 0<=nr<10 and 0<=nc<10 and self.matrix[nr][nc]==1:
                        return False
        return True
    def add_vessel(self, row, col, length, horizontal):
        if not self.can_fit(row, col, length, horizontal): return False
        coords = [(row, col+i) if horizontal else (row+i, col) for i in range(length)]
        self.vessels.append(Vessel(coords))
        for r,c in coords: self.matrix[r][c]=1
        return True
    def auto_place(self, lengths):
        self.matrix = [[0]*10 for _ in range(10)]
        self.vessels = []
        for length in lengths:
            for attempt in range(1000):
                row, col = random.randint(0,9), random.randint(0,9)
                orientation = random.choice([True, False])
                if self.add_vessel(row, col, length, orientation): break
    def fire(self, row, col):
        if (row, col) in self.attacks: return None
        self.attacks.add((row, col))
        if self.matrix[row][col] == 1:
            self.matrix[row][col] = 2
            for vessel in self.vessels:
                if (row, col) in vessel.coords:
                    vessel.damaged.add((row, col))
                    return 'sunk' if vessel.is_destroyed() else 'hit'
        self.matrix[row][col] = 3
        return 'miss'
    def all_destroyed(self): 
        return all(vessel.is_destroyed() for vessel in self.vessels)

class Session:
    def __init__(self):
        self.lengths = [4,3,3,2,2,2,1,1,1,1]
        self.user = Field()
        self.opponent = Field()
        self.potential_targets = []
        self.hunt_mode = False
        self.hunt_coords = []
        self.hit_history = []
        self.stage = 'setup'; self.user_turn = True
        self.setup_index = 0; self.horizontal = True
    def place_user_vessel(self, row, col):
        if self.setup_index >= len(self.lengths): return False
        if self.user.add_vessel(row, col, self.lengths[self.setup_index], self.horizontal):
            self.setup_index += 1
            if self.setup_index >= len(self.lengths): self.initiate_game()
            return True
        return False
    def auto_user_setup(self):
        self.user.auto_place(self.lengths)
        self.setup_index = len(self.lengths)
        self.initiate_game()
    def initiate_game(self):
        self.opponent.auto_place(self.lengths)
        self.potential_targets = [(r,c) for r in range(10) for c in range(10)]
        random.shuffle(self.potential_targets)
        self.hunt_mode = False
        self.hunt_coords = []
        self.hit_history = []
        self.stage = 'playing'; self.user_turn = True
    def user_fire(self, row, col):
        if not self.user_turn or self.stage != 'playing': return None
        result = self.opponent.fire(row, col)
        if result and self.opponent.all_destroyed(): self.stage = 'ended'; return 'win'
        if result == 'miss': self.user_turn = False
        return result
    def opponent_fire(self):
        if self.user_turn: return None, None
        if self.hunt_mode and self.hunt_coords:
            row, col = self.hunt_coords.pop(0)
        else:
            if not self.potential_targets: return None, None
            row, col = self.potential_targets.pop(0)
        result = self.user.fire(row, col)
        if result == 'hit':
            self.hunt_mode = True
            self.hit_history.append((row, col))
            if len(self.hit_history) == 2:
                r1, c1 = self.hit_history[0]
                r2, c2 = self.hit_history[1]
                self.hunt_coords = []
                if r1 == r2:
                    min_col, max_col = min(c1, c2), max(c1, c2)
                    for new_col in [min_col-1, max_col+1]:
                        if 0 <= new_col < 10 and (r1, new_col) not in self.user.attacks:
                            if (r1, new_col) in self.potential_targets: self.potential_targets.remove((r1, new_col))
                            self.hunt_coords.append((r1, new_col))
                else:
                    min_row, max_row = min(r1, r2), max(r1, r2)
                    for new_row in [min_row-1, max_row+1]:
                        if 0 <= new_row < 10 and (new_row, c1) not in self.user.attacks:
                            if (new_row, c1) in self.potential_targets: self.potential_targets.remove((new_row, c1))
                            self.hunt_coords.append((new_row, c1))
            elif len(self.hit_history) == 1:
                for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < 10 and 0 <= nc < 10 and (nr, nc) not in self.user.attacks:
                        if (nr, nc) in self.potential_targets: self.potential_targets.remove((nr, nc))
                        if (nr, nc) not in self.hunt_coords: self.hunt_coords.append((nr, nc))
            else:
                if len(self.hit_history) >= 3:
                    self.hit_history.sort()
                    if self.hit_history[0][0] == self.hit_history[-1][0]:
                        row_base = self.hit_history[0][0]
                        min_col = min(h[1] for h in self.hit_history)
                        max_col = max(h[1] for h in self.hit_history)
                        self.hunt_coords = []
                        for new_col in [min_col-1, max_col+1]:
                            if 0 <= new_col < 10 and (row_base, new_col) not in self.user.attacks:
                                if (row_base, new_col) in self.potential_targets: self.potential_targets.remove((row_base, new_col))
                                self.hunt_coords.append((row_base, new_col))
                    else:
                        col_base = self.hit_history[0][1]
                        min_row = min(h[0] for h in self.hit_history)
                        max_row = max(h[0] for h in self.hit_history)
                        self.hunt_coords = []
                        for new_row in [min_row-1, max_row+1]:
                            if 0 <= new_row < 10 and (new_row, col_base) not in self.user.attacks:
                                if (new_row, col_base) in self.potential_targets: self.potential_targets.remove((new_row, col_base))
                                self.hunt_coords.append((new_row, col_base))
        elif result == 'sunk':
            self.hunt_mode = False
            self.hunt_coords = []
            self.hit_history = []
        if self.user.all_destroyed(): self.stage = 'ended'; return (row, col), 'lose'
        if result == 'miss': self.user_turn = True
        return (row, col), result

class Display:
    def __init__(self, root):
        self.root = root; root.title("Морской бой")
        self.session = Session(); self.cell_size = 40
        self.colors = {0: 'seagreen', 1: 'darkgreen', 2: 'darkred', 3: 'cyan'}
        root.update_idletasks()
        width, height = 920, 550
        x_pos = (root.winfo_screenwidth() // 2) - (width // 2)
        y_pos = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f'{width}x{height}+{x_pos}+{y_pos}')
        
        # Кнопки размещены вертикально сверху
        button_frame = tk.Frame(root); button_frame.pack(pady=10)
        tk.Button(button_frame, text="Повернуть", command=self.toggle_orientation, bg='lightyellow', fg='black', font=('Arial', 10)).pack(side=tk.TOP, pady=2)
        tk.Button(button_frame, text="Авто-расстановка", command=self.random_setup, bg='lightcoral', fg='black', font=('Arial', 10)).pack(side=tk.TOP, pady=2)
        tk.Button(button_frame, text="Новая партия", command=self.new_session, bg='lightcyan', fg='black', font=('Arial', 10)).pack(side=tk.TOP, pady=2)
        
        self.info_label = tk.Label(root, text="Разместите корабли", font=('Arial', 14), bg='wheat')
        self.info_label.pack(pady=5)
        self.ships_label = tk.Label(root, text="", font=('Arial', 11), fg='darkblue', bg='wheat')
        self.ships_label.pack(pady=5)
        
        main_frame = tk.Frame(root); main_frame.pack(pady=10)
        user_side = tk.Frame(main_frame); user_side.pack(side=tk.LEFT, padx=30)
        tk.Label(user_side, text="Ваш флот", font=('Arial', 12, 'bold'), bg='wheat').pack()
        self.user_canvas = tk.Canvas(user_side, width=400, height=400, bg='wheat'); self.user_canvas.pack(pady=5)
        self.user_canvas.bind('<Button-1>', self.user_click); self.user_canvas.bind('<Motion>', self.user_hover)
        enemy_side = tk.Frame(main_frame); enemy_side.pack(side=tk.LEFT, padx=30)
        tk.Label(enemy_side, text="Воды противника", font=('Arial', 12, 'bold'), bg='wheat').pack()
        self.enemy_canvas = tk.Canvas(enemy_side, width=400, height=400, bg='wheat'); self.enemy_canvas.pack(pady=5)
        self.enemy_canvas.bind('<Button-1>', self.enemy_click)
        self.enemy_canvas.bind('<Motion>', self.enemy_hover)
        self.hover_preview = None
        self.draw_fields()
    
    def draw_fields(self):
        self.draw_field(self.user_canvas, self.session.user, True)
        self.draw_field(self.enemy_canvas, self.session.opponent, False)
    
    def draw_field(self, canvas, field, show_ships):
        canvas.delete('all')
        for row in range(10):
            for col in range(10):
                x1, y1 = col * self.cell_size, row * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                value = field.matrix[row][col]
                is_destroyed = any(vessel.is_destroyed() and (row, col) in vessel.coords for vessel in field.vessels)
                color = 'brown' if is_destroyed else (self.colors[0] if value == 1 and not show_ships else self.colors[value])
                canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='darkslategray')
                if is_destroyed:
                    pad = 8
                    canvas.create_line(x1 + pad, y1 + pad, x2 - pad, y2 - pad, fill='black', width=3)
                    canvas.create_line(x1 + pad, y2 - pad, x2 - pad, y1 + pad, fill='black', width=3)
    
    # Placement logic
    def user_click(self, event):
        if self.session.stage != 'setup': return
        row, col = event.y // self.cell_size, event.x // self.cell_size
        if 0 <= row < 10 and 0 <= col < 10 and self.session.place_user_vessel(row, col):
            self.draw_fields(); self.update_info()
    
    def user_hover(self, event):
        if self.session.stage != 'setup' or self.session.setup_index >= len(self.session.lengths): return
        row, col = event.y // self.cell_size, event.x // self.cell_size
        self.draw_field(self.user_canvas, self.session.user, True)
        length = self.session.lengths[self.session.setup_index]
        if 0 <= row < 10 and 0 <= col < 10:
            color = 'lime' if self.session.user.can_fit(row, col, length, self.session.horizontal) else 'magenta'
            for rr, cc in [(row, col + i) if self.session.horizontal else (row + i, col) for i in range(length)]:
                if 0 <= rr < 10 and 0 <= cc < 10:
                    x1, y1 = cc * self.cell_size, rr * self.cell_size
                    self.user_canvas.create_rectangle(x1, y1, x1 + self.cell_size, y1 + self.cell_size, 
                                                      fill=color, outline='darkslategray', stipple='gray50')
    
    # Game process
    def enemy_click(self, event):
        if self.session.stage != 'playing' or not self.session.user_turn: return
        row, col = event.y // self.cell_size, event.x // self.cell_size
        if 0 <= row < 10 and 0 <= col < 10:
            result = self.session.user_fire(row, col)
            if result:
                self.draw_fields()
                if result == 'win':
                    self.update_info()
                    messagebox.showinfo("Победа", "Вы победили!")
                    return
                self.update_info()
                if not self.session.user_turn: self.root.after(500, self.opponent_turn)
    
    def enemy_hover(self, event):
        if self.session.stage != 'playing' or not self.session.user_turn: return
        row, col = event.y // self.cell_size, event.x // self.cell_size
        self.draw_field(self.enemy_canvas, self.session.opponent, False)
        if 0 <= row < 10 and 0 <= col < 10 and (row, col) not in self.session.opponent.attacks:
            x1, y1 = col * self.cell_size, row * self.cell_size
            x2, y2 = x1 + self.cell_size, y1 + self.cell_size
            self.hover_preview = self.enemy_canvas.create_rectangle(x1, y1, x2, y2, 
                                                                     fill='orange', outline='darkslategray', stipple='gray50')
    
    def opponent_turn(self):
        if self.session.stage != 'playing' or self.session.user_turn: return
        self.update_info(); pos, result = self.session.opponent_fire()
        if pos:
            self.draw_fields()
            if result == 'lose':
                self.update_info()
                messagebox.showinfo("Поражение", "Противник победил!")
                return
            if not self.session.user_turn: self.root.after(500, self.opponent_turn)
            else: self.update_info()
    
    # Button actions
    def toggle_orientation(self): self.session.horizontal = not self.session.horizontal
    def random_setup(self): self.session.auto_user_setup(); self.draw_fields(); self.update_info()
    def new_session(self): self.session = Session(); self.draw_fields(); self.update_info()
    
    def update_info(self):
        if self.session.stage == 'setup' and self.session.setup_index < len(self.session.lengths):
            length = self.session.lengths[self.session.setup_index]
            remaining = len(self.session.lengths) - self.session.setup_index
            self.info_label.config(text=f"Разместите судно {length} ({remaining} осталось)")
            self.ships_label.config(text="")
        elif self.session.stage == 'playing' or self.session.stage == 'ended':
            if self.session.stage == 'playing':
                self.info_label.config(text="Ваш ход" if self.session.user_turn else "Ход противника")
            else:
                self.info_label.config(text="Игра окончена")
            user_remaining = sum(1 for v in self.session.user.vessels if not v.is_destroyed())
            opponent_remaining = sum(1 for v in self.session.opponent.vessels if not v.is_destroyed())
            self.ships_label.config(text=f"Ваши суда: {user_remaining}/10  |  Суда противника: {opponent_remaining}/10")
        else: 
            self.info_label.config(text="Игра окончена")
            self.ships_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk(); Display(root); root.mainloop()
