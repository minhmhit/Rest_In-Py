import tkinter as tk
from datetime import datetime
from tkinter import messagebox

class Checkout(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f5f5f5")  # Light gray background
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
        self.invoice_label = tk.Label(
            self.mainPanel, text="Hóa Đơn", font=("Arial", 34, "bold"), bg="white"
        )
        self.invoice_label.pack(pady=10)

        # Customer Info Frame
        self.info_frame = tk.Frame(self.mainPanel, bg="#e0e0e0", padx=15, pady=15)
        self.info_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(self.info_frame, text="  Thông Tin Khách Hàng", font=("Arial", 18, "bold"), bg="#e0e0e0").grid(row=0, columnspan=2, pady=5)
        
        self.labels = {}
        fields = [
            ("Họ tên", "name"),
            ("Giới tính", "sex"),
            ("Ngày sinh", "birthday"),
            ("Quốc tịch", "national"),
            ("Quê quán", "country"),
        ]

        for i, (title, field) in enumerate(fields):
            tk.Label(self.info_frame, text=title + ":", font=("Arial", 14, "bold"), bg="#e0e0e0").grid(row=i+1, column=0, sticky="w", padx=5, pady=2)
            self.labels[field] = tk.Label(self.info_frame, text="", font=("Arial", 14), bg="#e0e0e0")
            self.labels[field].grid(row=i+1, column=1, sticky="w", padx=5, pady=2)

        # Room Details Frame
        self.room_frame = tk.Frame(self.mainPanel, bg="#e0e0e0", padx=15, pady=15)
        self.room_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(self.room_frame, text="Chi Tiết Phòng Thuê", font=("Arial", 18, "bold"), bg="#e0e0e0").grid(row=0, columnspan=2, pady=5)
        
        tk.Label(self.room_frame, text="Loại phòng:", font=("Arial", 14, "bold"), bg="#e0e0e0").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.labels["room_type"] = tk.Label(self.room_frame, text="", font=("Arial", 14), bg="#e0e0e0")
        self.labels["room_type"].grid(row=1, column=1, sticky="w", padx=5, pady=2)

        tk.Label(self.room_frame, text="Ngày nhận phòng:", font=("Arial", 14, "bold"), bg="#e0e0e0").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.checkin_date = tk.Label(self.room_frame, bg="#e0e0e0", font=("Arial", 14))
        self.checkin_date.grid(row=2, column=1, sticky="w", padx=5, pady=2)
        
        tk.Label(self.room_frame, text="Ngày trả phòng:", font=("Arial", 14, "bold"), bg="#e0e0e0").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.checkout_date = tk.Label(self.room_frame, bg="#e0e0e0", font=("Arial", 14))
        self.checkout_date.grid(row=3, column=1, sticky="w", padx=5, pady=2)

        # Result
        self.result_label = tk.Label(self.mainPanel, text="", font=("Arial", 18, "bold"), fg="green", bg="white")
        self.result_label.pack(pady=10)

        # Calculate Button
        self.calculate_btn = tk.Button(
            self.mainPanel, text="Tính Tiền", font=("Arial", 14, "bold"), fg="white", bg="#007BFF", 
            relief=tk.RAISED, padx=10, pady=5, command=self.load_customer_info
        )
        self.calculate_btn.pack(pady=10)

    # def load_customer_info(self):
    #     customer_data = self.controller
    #     if not customer_data or customer_data.isNotNull:
    #         for field in self.labels:
    #             self.labels[field].config(text="Không có dữ liệu")
    #         return
    #
    #     for field in self.labels:
    #         value = getattr(customer_data, field, "")
    #         if value:
    #             self.labels[field].config(text=value)
    #
    #     if customer_data.checkin_date:
    #         self.checkin_date.config(text=customer_data.checkin_date)
    #
    #     self.checkout_date.config(text=datetime.today().strftime("%d/%m/%Y"))
    #     self.result_label.config(text=f"Tổng tiền: {self.calculate_room_cost(customer_data.checkin_date, customer_data.room_type)} VND")

    def load_customer_info(self):
        customer_data = self.controller
        if not customer_data:
            messagebox.showwarning("Cảnh báo", "Không có dữ liệu khách hàng")
            return
        
        for field in self.labels:
            value = getattr(customer_data, field, "")
            self.labels[field].config(text=value if value else "Không có dữ liệu")
        
        if customer_data.getCheckinDate:
            self.checkin_date.config(text=customer_data.checkin_date)
        else:
            messagebox.showwarning("Cảnh báo", "Ngày nhận phòng không có dữ liệu")
            self.checkout_date.config(text="Không có dữ liệu khách hàng")
            self.result_label.config(text="Không có dữ liệu khách hàng")
            return
        
        self.checkout_date.config(text=datetime.today().strftime("%d/%m/%Y"))
        self.result_label.config(text=f"Tổng tiền: {self.calculate_room_cost(customer_data.checkin_date, customer_data.room_type)} VND")
    
    def calculate_room_cost(self, checkin_date, room_type):
        if checkin_date is None:
            return 0
        try:
            checkin = datetime.strptime(checkin_date, "%d/%m/%Y")
            checkout = datetime.today()
            if checkout < checkin:
                raise ValueError("Ngày trả phòng không hợp lệ.")
            duration = (checkout - checkin).days
            room_rate = self.price_per_day.get(room_type, 250000)  # Default to normal room rate
            return duration * room_rate
        except ValueError:
            return 0
