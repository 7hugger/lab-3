import tkinter as tk
from tkinter import filedialog, messagebox

class Contract:
    def __init__(self, name, course_type, student):
        self.name = name
        self.course_type = course_type
        self.student = student

class DrivingSchoolApp:
    def __init__(self, master):
        self.master = master
        self.contracts = []
        master.title("Курсы вождения - Договоры")
        master.geometry("900x900")
        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.master)
        frame.pack(padx=10, pady=10)

        self.load_button = tk.Button(frame, text="Загрузить договоры", command=self.load_contracts)
        self.load_button.pack(pady=5, fill=tk.X)

        self.segment_by_course_button = tk.Button(
            frame, text="Сегментация по типам курсов", command=self.segment_by_course
        )
        self.segment_by_course_button.pack(pady=5, fill=tk.X)

        self.segment_by_student_button = tk.Button(
            frame, text="Сегментация по обучающимся", command=self.segment_by_student
        )
        self.segment_by_student_button.pack(pady=5, fill=tk.X)

        self.delete_contracts_button = tk.Button(
            frame, text="Удалить все договоры", command=self.delete_contracts
        )
        self.delete_contracts_button.pack(pady=5, fill=tk.X)

        self.show_stats_button = tk.Button(
            frame, text="Показать статистику", command=self.show_statistics
        )
        self.show_stats_button.pack(pady=5, fill=tk.X)

        self.canvas = tk.Canvas(self.master, width=800, height=500, bg="white")
        self.canvas.pack(pady=20)

    def load_contracts(self):
        file_path = filedialog.askopenfilename(filetypes=[("TXT файлы", "*.txt"), ("Все файлы", "*.*")])
        if not file_path:
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                
                self.contracts.clear()
                line_count = 0
                
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                        
                    parts = line.split()
                    
                    if len(parts) < 3:
                        messagebox.showwarning("Предупреждение", 
                                              f"Строка {line_count + 1} содержит недостаточно данных: {line}")
                        continue
                    
                    name = parts[0]
                    course_type = parts[1]
                    student = ' '.join(parts[2:])
                    
                    contract = Contract(name, course_type, student)
                    self.contracts.append(contract)
                    line_count += 1

                messagebox.showinfo("Успех", f"Загружено {len(self.contracts)} договоров.")
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл:\n{e}")

    def delete_contracts(self):
        """Удаляет все загруженные договоры"""
        if not self.contracts:
            messagebox.showinfo("Информация", "Нет договоров для удаления.")
            return
            
        result = messagebox.askyesno(
            "Подтверждение удаления", 
            f"Вы уверены, что хотите удалить все {len(self.contracts)} договоров?"
        )
        
        if result:
            self.contracts.clear()
            self.canvas.delete("all")
            messagebox.showinfo("Успех", "Все договоры удалены.")

    def show_statistics(self):
        """Показывает общую статистику по договорам"""
        if not self.contracts:
            messagebox.showwarning("Нет данных", "Сначала загрузите договоры.")
            return
            
        course_stats = {}
        student_stats = {}
        
        for contract in self.contracts:
            if contract.course_type not in course_stats:
                course_stats[contract.course_type] = 0
            course_stats[contract.course_type] += 1
            
            if contract.student not in student_stats:
                student_stats[contract.student] = 0
            student_stats[contract.student] += 1
        
        stats_text = f"Общее количество договоров: {len(self.contracts)}\n\n"
        stats_text += "Статистика по типам курсов:\n"
        
        for course_type, count in course_stats.items():
            percentage = (count / len(self.contracts)) * 100
            stats_text += f"  {course_type}: {count} ({percentage:.1f}%)\n"
        
        stats_text += "\nСтатистика по обучающимся:\n"
        for student, count in student_stats.items():
            percentage = (count / len(self.contracts)) * 100
            stats_text += f"  {student}: {count} ({percentage:.1f}%)\n"
        
        messagebox.showinfo("Статистика договоров", stats_text)

    def segment_by_course(self):
        if not self.contracts:
            messagebox.showwarning("Нет данных", "Сначала загрузите договоры.")
            return

        stats = {}
        for contract in self.contracts:
            if contract.course_type not in stats:
                stats[contract.course_type] = 0
            stats[contract.course_type] += 1

        self.plot_pie_chart(stats, "Сегментация по типам курсов")

    def segment_by_student(self):
        if not self.contracts:
            messagebox.showwarning("Нет данных", "Сначала загрузите договоры.")
            return

        stats = {}
        for contract in self.contracts:
            if contract.student not in stats:
                stats[contract.student] = 0
            stats[contract.student] += 1

        self.plot_pie_chart(stats, "Сегментация по обучающимся")

    def plot_pie_chart(self, data, title):
        self.canvas.delete("all")

        self.canvas.create_text(400, 30, text=title, font=("Arial", 14, "bold"), fill="black")

        labels = list(data.keys())
        values = list(data.values())
        total = sum(values)
        cx, cy, radius = 300, 260, 200

        start_angle = 0

        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7", 
                 "#DDA0DD", "#98D8C8", "#F7DC6F", "#BB8FCE", "#85C1E9",
                 "#F8C471", "#82E0AA", "#F1948A", "#85C1E9", "#D7BDE2"]

        for i, (label, value) in enumerate(zip(labels, values)):
            angle = (value / total) * 360
            end_angle = start_angle + angle

            self.canvas.create_arc(
                cx - radius, cy - radius,
                cx + radius, cy + radius,
                start=start_angle, extent=angle,
                fill=colors[i % len(colors)], outline="black"
            )

            start_angle = end_angle

        legend_x = cx + radius + 20
        legend_y_start = cy - (len(labels) * 20) // 2

        for i, label in enumerate(labels):
            color = colors[i % len(colors)]
            percentage = (data[label] / total) * 100

            self.canvas.create_rectangle(legend_x, legend_y_start + i*25,
                                         legend_x + 15, legend_y_start + i*25 + 15,
                                         fill=color, outline="black")

            self.canvas.create_text(legend_x + 20, legend_y_start + i*25 + 8,
                                    text=f"{label} ({data[label]}, {percentage:.1f}%)", 
                                    anchor="w", font=("Arial", 10), fill="black")


if __name__ == "__main__":
    root = tk.Tk()
    app = DrivingSchoolApp(root)
    root.mainloop()
