import tkinter as tk
from tkinter import filedialog, messagebox


def read_matrix(filename):
    matrix = []
    with open(filename, 'r') as file:
        for line in file:
            row = [int(x) for x in line.strip().split() if x]
            if row:  
                matrix.append(row)
    return matrix


def find_path(matrix, start, end):
    rows, cols = len(matrix), len(matrix[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    path = []

    def dfs(x, y):
      
        if x < 0 or x >= rows or y < 0 or y >= cols:
            return False
        if matrix[x][y] == 1 or visited[x][y]:
            return False
        if (x, y) == end:
            path.append((x, y))
            return True

        visited[x][y] = True
        path.append((x, y))

     
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in directions:
            if dfs(x + dx, y + dy):
                return True

      
        path.pop()
        return False

    if dfs(start[0], start[1]):
        return path
    return None


def visualize_labyrinth(matrix, path, start, end):
    visualization_window = tk.Toplevel()
    visualization_window.title("Лабиринт — визуализация пути")
    visualization_window.resizable(False, False)

    cell_size = 30
    rows, cols = len(matrix), len(matrix[0])
    canvas_width = cols * cell_size
    canvas_height = rows * cell_size

    canvas = tk.Canvas(visualization_window, width=canvas_width, height=canvas_height, bg='white')
    canvas.pack(padx=10, pady=10)

  
    for i in range(rows):
        for j in range(cols):
            x1, y1 = j * cell_size, i * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size
            if matrix[i][j] == 1:
                canvas.create_rectangle(x1, y1, x2, y2, fill='black', outline='gray')
            else:
                canvas.create_rectangle(x1, y1, x2, y2, fill='white', outline='lightgray')


    sx, sy = start
    ex, ey = end

  
    x1, y1 = sy * cell_size + 5, sx * cell_size + 5
    x2, y2 = x1 + 20, y1 + 20
    canvas.create_oval(x1, y1, x2, y2, fill='green', outline='darkgreen', width=2, tags="start")


    x1, y1 = ey * cell_size + 5, ex * cell_size + 5
    x2, y2 = x1 + 20, y1 + 20
    canvas.create_oval(x1, y1, x2, y2, fill='red', outline='darkred', width=2, tags="end")


    info_label = tk.Label(visualization_window, text="Анимация пути...", font=("Arial", 11))
    info_label.pack(pady=5)


    if not path:
        info_label.config(text=" Путь не найден")
        return


    step = 0
    path_objects = []  

    def animate_step():
        nonlocal step
        if step >= len(path):
            info_label.config(text=f" Путь найден! Длина: {len(path)} клеток")
            return

        i, j = path[step]
        x_center = j * cell_size + cell_size // 2
        y_center = i * cell_size + cell_size // 2

        if (i, j) != start and (i, j) != end:
            oval_id = canvas.create_oval(
                x_center - 4, y_center - 4,
                x_center + 4, y_center + 4,
                fill='blue', outline='navy'
            )
            path_objects.append(oval_id)

        if step > 0:
            prev_i, prev_j = path[step - 1]
            prev_x = prev_j * cell_size + cell_size // 2
            prev_y = prev_i * cell_size + cell_size // 2
            line_id = canvas.create_line(
                prev_x, prev_y, x_center, y_center,
                fill='blue', width=3, arrow=tk.LAST, arrowshape=(6, 7, 3)
            )
            path_objects.append(line_id)

        step += 1
       
        canvas.after(300, animate_step)

   
    animate_step()


def select_file():
    filename = filedialog.askopenfilename(
        title="Выберите файл с лабиринтом",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )

    if filename:
        file_label.config(text=f" {filename.split('/')[-1]}")
        solve_labyrinth(filename)


def solve_labyrinth(filename):
    try:
        matrix = read_matrix(filename)

        
        if len(matrix) != 15 or any(len(row) != 15 for row in matrix):
            messagebox.showerror("Ошибка", "Матрица должна быть размером 15×15")
            file_label.config(text="Файл не выбран")
            return

        start = (0, 0)
        end = (14, 14)

        if matrix[start[0]][start[1]] == 1:
            messagebox.showerror("Ошибка", "Стартовая клетка (0,0) заблокирована (значение 1)")
            return
        if matrix[end[0]][end[1]] == 1:
            messagebox.showerror("Ошибка", "Финишная клетка (14,14) заблокирована (значение 1)")
            return

        path = find_path(matrix, start, end)

        if path:
            messagebox.showinfo("Успех", f"Путь найден!\nДлина: {len(path)} клеток")
            visualize_labyrinth(matrix, path, start, end)
        else:
            messagebox.showwarning("Результат", "Путь не найден.")
            visualize_labyrinth(matrix, [], start, end)

    except FileNotFoundError:
        messagebox.showerror("Ошибка", "Файл не найден.")
    except ValueError as e:
        messagebox.showerror("Ошибка", f"Некорректные данные в файле (ожидались целые числа):\n{e}")
    except Exception as e:
        messagebox.showerror("Неизвестная ошибка", f"{type(e).__name__}: {e}")


def create_main_window():
    global file_label
    root = tk.Tk()
    root.title(" Решатель лабиринта (15×15)")
    root.geometry("420x220")
    root.resizable(False, False)

    title_label = tk.Label(root, text="Решатель лабиринта", font=("Arial", 16, "bold"))
    title_label.pack(pady=12)

    desc_label = tk.Label(
        root,
        text="Выберите текстовый файл с матрицей 15×15:\n• 0 — проход, 1 — стена\n• Старт: (0,0), Финиш: (14,14)",
        font=("Arial", 9), fg="gray", justify="center", wraplength=380
    )
    desc_label.pack(pady=5)

    select_button = tk.Button(
        root, text=" Выбрать файл", command=select_file,
        font=("Arial", 12), bg="#4CAF50", fg="white",
        padx=20, pady=8, relief="flat", cursor="hand2"
    )
    select_button.pack(pady=10)

    file_label = tk.Label(root, text="Файл не выбран", font=("Arial", 10), fg="#666")
    file_label.pack(pady=5)

    exit_button = tk.Button(
        root, text=" Выход", command=root.quit,
        font=("Arial", 10), bg="#f44336", fg="white",
        padx=15, pady=5, relief="flat", cursor="hand2"
    )
    exit_button.pack(pady=10)

    return root


def main():
    root = create_main_window()
    root.mainloop()


if __name__ == "__main__":
    main()
