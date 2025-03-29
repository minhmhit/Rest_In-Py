import tkinter as tk
from datetime import datetime
from tkinter import messagebox

class Checkout(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#F5F5F5")
        self.price_per_day = 250000
        self.controller = controller

        # Thông tin khách hàng
        self.customer_info_label = tk.Label(self, text="Thông tin khách hàng", font=("Arial", 14, "bold"), bg="#F5F5F5")
        self.customer_info_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        self.info_text = tk.Label(self, text="", justify="left", bg="#F5F5F5", anchor="w")
        self.info_text.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        tk.Label(self, text="Ngày nhận phòng (dd/mm/yyyy):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.checkin_date = tk.Label(self,bg="#F5F5F5")
        self.checkin_date.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self, text="Ngày trả phòng (dd/mm/yyyy):").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.checkout_date = tk.Label(self,bg="#F5F5F5")
        self.checkout_date.grid(row=3, column=1, padx=10, pady=5)

        self.calculate_btn = tk.Button(self, text="Tính tiền", command=self.load_customer_info)
        self.calculate_btn.grid(row=4, column=0, columnspan=2, pady=10)

        self.result_label = tk.Label(self, text="", font=("Arial", 12, "bold"), fg="red")
        self.result_label.grid(row=5, column=0, columnspan=2, pady=10)

    # def get_data_from_customerlist(self):
    #     shared_data = self.controller.shared_data
    #     if shared_data.datetime_value:
    #         self.display_label.config(text=str(shared_data))
    #     else:
    #         self.display_label.config(text="No data received")

    def load_customer_info(self):
        customer_data = self.controller
        if not customer_data:
            self.info_text.config(text="Không có dữ liệu khách hàng.")
            return
        
        info_text = f"Họ tên: {customer_data.name}\n"
        info_text += f"Giới tính: {customer_data.sex}\n"
        info_text += f"Ngày sinh: {customer_data.birthday}\n"
        info_text += f"Quốc tịch: {customer_data.national}\n"
        info_text += f"Quê quán: {customer_data.country}\n"
        info_text += f"Loại phòng: {customer_data.room_type}"
        
        self.info_text.config(text=info_text)
        self.checkin_date.config(text=customer_data.checkin_date)
        self.checkout_date.config(text=datetime.today().strftime("%d/%m/%Y"))
        
        # self.calculate_room_cost(customer_data.checkin_date)
        self.result_label.config(text=f"Tổng tiền phải trả là: {self.calculate_room_cost(customer_data.checkin_date)}")
        # self.calculate_payment()

    # def calculate_payment(self):
    #     checkin_date =  datetime.strptime(self.controller.customer_controller.checkin_date, "%d/%m/%Y")
    #     checkout_date = datetime.today().strftime("%d/%m/%Y")
    #
    #     if not checkin_date or not checkout_date:
    #         self.result_label.config(text="Vui lòng nhập đủ thông tin ngày.")
    #         return
    #
    #     try:
    #         # checkin = datetime.strptime(checkin_date, "%d/%m/%Y")
    #         checkin = "20/11/2020"
    #         checkout = datetime.strptime(checkout_date, "%d/%m/%Y")
    #
    #         if checkout <= checkin:
    #             messagebox.showerror("Lỗi", "Ngày trả phòng phải sau ngày nhận phòng.")
    #             return
    #
    #         num_days = (checkout - checkin).days
    #         total_cost = num_days * self.price_per_day
    #
    #         self.result_label.config(text=f"Tổng tiền: {total_cost:,} VND")
    #     except ValueError:
    #         messagebox.showerror("Lỗi định dạng", "Vui lòng nhập ngày theo định dạng dd/mm/yyyy.")

    
    def calculate_room_cost(self,checkin_date):
        cost_per_day = 250000
        checkout_date = datetime.today().strftime("%d/%m/%Y")
        try:
            checkin = datetime.strptime(checkin_date, "%d/%m/%Y")
            checkout = datetime.strptime(checkout_date, "%d/%m/%Y")

            if checkout < checkin:
                raise ValueError("Checkout date cannot be earlier than check-in date.")

            duration = (checkout - checkin).days

            total_cost = duration * cost_per_day
            return total_cost

        except ValueError as e:
            print(f"Error: {e}")
            return 0  # Return 0 on error
