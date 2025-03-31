import tkinter as tk
from datetime import datetime
from tkinter import messagebox

class Checkout(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f5f5f5")  # gray background
        self.price_per_day = {"VIP": 400000, "Normal": 250000}
        self.controller = controller

        # Panels
        self.leftPanel = tk.Frame(self, bg="#f5f5f5")
        self.rightPanel = tk.Frame(self, bg="#f5f5f5")
        self.mainPanel = tk.Frame(self, bg="white", padx=20, pady=20, relief=tk.RIDGE, borderwidth=2)

        # Configure grid weights
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)

        # Layout
        self.leftPanel.grid(row=0, column=0, sticky="nsew")
        self.mainPanel.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.rightPanel.grid(row=0, column=2, sticky="nsew")

        # Title
        self.customer_info_label = tk.Label(
            self.mainPanel, text="Thông tin khách hàng", font=("Arial", 24, "bold"), bg="white"
        )
        self.customer_info_label.pack(pady=10)

        # Customer Info Frame
        self.info_frame = tk.Frame(self.mainPanel, bg="#e0e0e0", padx=15, pady=15)
        self.info_frame.pack(fill="x", padx=10, pady=5)
        
        self.info_text = tk.Label(self.info_frame, font=("Arial", 16), text="", justify="left", bg="#e0e0e0", anchor="w")
        self.info_text.pack(fill="x")

        # Dates
        date_frame = tk.Frame(self.mainPanel, bg="white")
        date_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(date_frame, text="Ngày nhận phòng:", font=("Arial", 14), bg="white").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.checkin_date = tk.Label(date_frame, bg="white", font=("Arial", 14))
        self.checkin_date.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        tk.Label(date_frame, text="Ngày trả phòng:", font=("Arial", 14), bg="white").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.checkout_date = tk.Label(date_frame, bg="white", font=("Arial", 14))
        self.checkout_date.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        # Result
        self.result_label = tk.Label(self.mainPanel, text="", font=("Arial", 18, "bold"), fg="green", bg="white")
        self.result_label.pack(pady=10)

        # Calculate Button
        self.calculate_btn = tk.Button(
            self.mainPanel, text="Tính Tiền", font=("Arial", 14, "bold"), fg="white", bg="#007BFF", 
            relief=tk.RAISED, padx=10, pady=5, command=self.load_customer_info
        )
        self.calculate_btn.pack(pady=10)

    def load_customer_info(self):
        customer_data = self.controller
        if not customer_data or self.info_text["text"] == "":
            self.info_text.config(text="Không có dữ liệu khách hàng.")
            return
        
        info_text = f"Họ tên: {customer_data.name}\nGiới tính: {customer_data.sex}\n"
        info_text += f"Ngày sinh: {customer_data.birthday}\nQuốc tịch: {customer_data.national}\n"
        info_text += f"Quê quán: {customer_data.country}\nLoại phòng: {customer_data.room_type}"
        
        self.info_text.config(text=info_text)
        self.checkin_date.config(text=customer_data.checkin_date)
        self.checkout_date.config(text=datetime.today().strftime("%d/%m/%Y"))
        self.result_label.config(text=f"Tổng tiền: {self.calculate_room_cost(customer_data.checkin_date, customer_data.room_type)} VND")
    
    def calculate_room_cost(self, checkin_date, room_type):
        try:
            checkin = datetime.strptime(checkin_date, "%d/%m/%Y")
            checkout = datetime.today()
            if checkout < checkin:
                raise ValueError("Ngày trả phòng không hợp lệ.")
            duration = (checkout - checkin).days
            room_rate = self.price_per_day.get(room_type, 250000)
            return duration * room_rate
        except ValueError:
            return 0
