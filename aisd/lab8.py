'''17. Объекты – товар в магазине
Функции:	сегментация полного списка товара по категориям
визуализация предыдущей функции в форме круговой диаграммы
сегментация полного списка товара по продажам
визуализация предыдущей функции в форме круговой диаграммы
'''

import csv
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt

# Класс для представления товара
class Product:
    def __init__(self, name, category, price, quantity):
        self.name = name
        self.category = category
        if price:
            self.price = float(price)
        else:
            self.price = None
        if quantity:
            self.quantity = int(quantity)
        else:
            self.quantity = None

    # Метод для вывода информации о товаре
    def __str__(self):
        return f'{self.name}: Категория - {self.category}, Цена - {self.price}'

# Функция для чтения данных из CSV файла
def read_csv_file():
    try:
        with open('products.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)  # Пропускаем заголовок
            products = []
            for row in reader:
                if len(row) >= 4:
                    name = row[0].strip()
                    category = row[1].strip()
                    price_str = row[2].strip() if len(row) > 2 and row[2].strip() else None
                    quantity_str = row[3].strip() if len(row) > 3 and row[3].strip() else None
                    product = Product(name, category, price_str, quantity_str)
                    products.append(product)
            return products
    except FileNotFoundError:
        print("Файл не найден!")
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")
    return []

# Функция для выполнения сегментации по категориям и последующей визуализации
def perform_segmentation_by_categories():
    if not products:
        print("Данные не загружены!")
        return
    
    # Сбор уникальных категорий
    unique_categories = []
    for product in products:
        if product.category not in unique_categories:
            unique_categories.append(product.category)
    
    # Подсчет количества товаров в каждой категории
    labels = unique_categories[:]
    sizes = []
    for category in labels:
        count = 0
        for product in products:
            if product.category == category:
                count += 1
        sizes.append(count)
    
    visualize_segmentation_by_categories(labels, sizes)

# Функция для выполнения сегментации по продажам и последующей визуализации
def perform_segmentation_by_sales():
    if not products:
        print("Данные не загружены!")
        return
    
    # Сбор значений продаж
    sales_values = []
    for product in products:
        if product.price is not None and product.quantity is not None:
            total_sales = product.price * product.quantity
            sales_values.append(total_sales)
    
    # Сбор уникальных значений продаж
    unique_sales = []
    for value in sales_values:
        if value not in unique_sales:
            unique_sales.append(value)
    
    # Подсчет количества товаров для каждого значения продаж
    labels = [f"{value:.2f}" for value in unique_sales]
    counts = []
    for unique_value in unique_sales:
        count = 0
        for sales_value in sales_values:
            if sales_value == unique_value:
                count += 1
        counts.append(count)
    
    visualize_segmentation_by_sales(labels, counts)

# Функция для визуализации распределения товаров по категориям
def visualize_segmentation_by_categories(labels, sizes):
    if not labels or not sizes:
        print("Нет данных для визуализации!")
        return
    explode = [0.1] * len(labels)
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')  # Для получения равномерной диаграммы
    plt.title("Сегментация товаров по категориям")
    plt.show()

# Функция для визуализации распределения товаров по продажам
def visualize_segmentation_by_sales(labels, counts):
    if not labels or not counts:
        print("Нет данных для визуализации!")
        return
    explode = [0.1] * len(labels)
    fig2, ax2 = plt.subplots()
    ax2.pie(counts, explode=explode, labels=labels, autopct='%1.1f%%', startangle=90)
    ax2.axis('equal')  # Для получения равномерной диаграммы
    plt.title("Сегментация товаров по продажам")
    plt.show()

# Создаем графический интерфейс с помощью библиотеки tkinter
root = tk.Tk()
root.title("Анализ товаров")

# Окно с информацией о товарах
info_frame = tk.Frame(root)
info_frame.pack(padx=10, pady=10)
tk.Label(info_frame, text="Информация о товарах").pack()

# Кнопка для загрузки данных из CSV файла
load_button = tk.Button(info_frame, text="Загрузить данные", command=lambda: load_data())
load_button.pack(pady=(10, 0))

# Метка для отображения статуса загрузки данных
info_label = tk.Label(info_frame, text="Нажмите кнопку для загрузки данных.")
info_label.pack(pady=(10, 0))

# Виджет для отображения результатов сегментации по категориям
segment_categories_frame = tk.Frame(root)
segment_categories_frame.pack(padx=10, pady=10)
tk.Label(segment_categories_frame, text="Сегментация по категориям").pack()

# Кнопка для запуска сегментации по категориям
segment_categories_button = tk.Button(segment_categories_frame, text="Выполнить сегментацию", command=lambda: perform_segmentation_by_categories())
segment_categories_button.pack(pady=(10, 0))

# Виджет для отображения результатов сегментации по продажам
segment_sales_frame = tk.Frame(root)
segment_sales_frame.pack(padx=10, pady=10)
tk.Label(segment_sales_frame, text="Сегментация по продажам").pack()

# Кнопка для запуска сегментации по продажам
segment_sales_button = tk.Button(segment_sales_frame, text="Выполнить сегментацию", command=lambda: perform_segmentation_by_sales())
segment_sales_button.pack(pady=(10, 0))

# Глобальная переменная для хранения продуктов
products = []

# Функция для загрузки данных
def load_data():
    global products
    products = read_csv_file()
    if products:
        info_label.config(text=f"Успешная загрузка данных: {len(products)} товаров.")
    else:
        info_label.config(text="Ошибка при загрузке данных.")

# Запуск главного цикла приложения
root.mainloop()

