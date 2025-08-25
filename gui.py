"""
GUI приложение на tkinter для клиентов и заказов с простыми формами и списками.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from models import Client, Product, Order
import re

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Менеджер интернет-магазина")
        self.geometry("700x600")

        self.clients = []  # список клиентов
        self.orders = []   # список заказов
        self.products_catalog = [Product("Сахар", 50), Product("Соль", 20), Product("Перец черный, молотый", 30), Product("Перец красный, молотый", 35), Product("Куркума", 50)]

        self.create_widgets()

    def create_widgets(self):
        tabControl = ttk.Notebook(self)
        self.clients_tab = ttk.Frame(tabControl)
        self.orders_tab = ttk.Frame(tabControl)
        tabControl.add(self.clients_tab, text='Клиенты')
        tabControl.add(self.orders_tab, text='Заказы')
        tabControl.pack(expand=1, fill="both")

        self.setup_clients_tab()
        self.setup_orders_tab()

    # Клиенты
    def setup_clients_tab(self):
        frm = ttk.Frame(self.clients_tab)
        frm.pack(padx=10, pady=10, fill='x')

        ttk.Label(frm, text="Номер клиента:").grid(row=0, column=0)
        self.client_number_var = tk.IntVar()
        ttk.Entry(frm, textvariable=self.client_number_var).grid(row=0, column=1)

        ttk.Label(frm, text="ФИО:").grid(row=1, column=0)
        self.client_fio_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.client_fio_var).grid(row=1, column=1)

        ttk.Label(frm, text="Телефон (+79000000000):").grid(row=2, column=0)
        self.client_phone_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.client_phone_var).grid(row=2, column=1)

        ttk.Label(frm, text="Email:").grid(row=3, column=0)
        self.client_email_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.client_email_var).grid(row=3, column=1)

        ttk.Button(frm, text="Добавить клиента", command=self.add_client).grid(row=4, column=0,columnspan=2,pady=10)

        self.clients_list = tk.Listbox(self.clients_tab)
        self.clients_list.pack(padx=10, pady=10, fill='both', expand=True)

    def add_client(self):
        try:
            number = self.client_number_var.get()
            fio = self.client_fio_var.get().strip()
            phone = self.client_phone_var.get().strip()
            email = self.client_email_var.get().strip()
            client = Client(number, fio, phone, email)
            self.clients.append(client)
            self.refresh_clients_list()
            messagebox.showinfo("Успех", "Клиент добавлен")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def refresh_clients_list(self):
        self.clients_list.delete(0, tk.END)
        for c in self.clients:
            self.clients_list.insert(tk.END, f"{c.number}: {c.fio}, тел:{c.phone}, email:{c.email}")

    # Заказы
    def refresh_orders_list(self):
        self.orders_list.delete(0, tk.END)
        # Сортируем список заказов, например, по номеру заказа или сумме
        sorted_orders = sorted(self.orders, key=lambda o: o.number)  # сортировка по номеру заказа

        for o in sorted_orders:
            products_str = ", ".join(p.name for p in o.products)
            self.orders_list.insert(tk.END,
                                    f"Заказ #{o.number} для {o.client.fio}, Товары: {products_str}, Сумма: {o.total_cost:.2f} руб.")

    def setup_orders_tab(self):
        frm = ttk.Frame(self.orders_tab)
        frm.pack(padx=10, pady=10, fill='x')

        ttk.Label(frm, text="Номер заказа:").grid(row=0, column=0)
        self.order_number_var = tk.IntVar()
        ttk.Entry(frm, textvariable=self.order_number_var).grid(row=0, column=1)

        ttk.Label(frm, text="Клиент (номер):").grid(row=1, column=0)
        self.order_client_number_var = tk.IntVar()
        ttk.Entry(frm, textvariable=self.order_client_number_var).grid(row=1, column=1)

        ttk.Label(frm, text="Выберите товары:").grid(row=2, column=0, sticky='w')
        self.product_vars = {}
        for i, p in enumerate(self.products_catalog):
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(frm, text=f"{p.name} ({p.price} руб.)", variable=var)
            cb.grid(row=3+i, column=0, columnspan=2, sticky='w')
            self.product_vars[p] = var

        ttk.Button(frm, text="Добавить заказ", command=self.add_order).grid(row=6, column=2,columnspan=2,pady=10)

        self.orders_list = tk.Listbox(self.orders_tab)
        self.orders_list.pack(padx=10, pady=10, fill='both', expand=True)

    def add_order(self):
        try:
            number = self.order_number_var.get()
            client_number = self.order_client_number_var.get()
            client = next((c for c in self.clients if c.number == client_number), None)
            if client is None:
                raise ValueError("Клиент с таким номером не найден")
            products = [p for p, v in self.product_vars.items() if v.get()]
            if not products:
                raise ValueError("Не выбраны товары")
            order = Order(number, client, products)
            self.orders.append(order)
            self.refresh_orders_list()
            messagebox.showinfo("Успех", "Заказ добавлен")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def refresh_orders_list(self):
        self.orders_list.delete(0, tk.END)
        for o in self.orders:
            products_str = ", ".join(p.name for p in o.products)
            self.orders_list.insert(tk.END,
                f"Заказ #{o.number} для {o.client.fio}, Товары: {products_str}, Сумма: {o.total_cost:.2f} руб.")
