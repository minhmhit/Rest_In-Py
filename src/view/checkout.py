import tkinter as tk
from datetime import datetime
from tkinter import messagebox


class Checkout(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#F5F5F5")
        self.price_per_day = 250000

        tk.Label(self, text="Ngay lay phong (dd/mm/yyyy):").grid(
            row=0, column=0, padx=10, pady=5
        )
        self.checkin_entry = tk.Entry(self)
        self.checkin_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self, text="Ngay tra phong (dd/mm/yyyy):").grid(
            row=1, column=0, padx=10, pady=5
        )
        self.checkout_entry = tk.Entry(self)
        self.checkout_entry.grid(row=1, column=1, padx=10, pady=5)

        self.calculate_btn = tk.Button(
            self, text="Calculate", command=self.calculate_payment
        )
        self.calculate_btn.grid(row=2, column=0, columnspan=2, pady=10)

        self.result_label = tk.Label(self, text="")
        self.result_label.grid(row=3, column=0, columnspan=2)

    def calculate_payment(self):
        checkin_date = self.checkin_entry.get()
        checkout_date = self.checkout_entry.get()

        try:
            checkin = datetime.strptime(checkin_date, "%d/%m/%Y")
            checkout = datetime.strptime(checkout_date, "%d/%m/%Y")

            if checkout <= checkin:
                messagebox.showerror(
                    "Error", "Check-out date must be after check-in date."
                )
                return

            num_days = (checkout - checkin).days
            total_cost = num_days * self.price_per_day

            self.result_label.config(text=f"Tong tien: {total_cost:,} VND")
        except ValueError:
            messagebox.showerror("Vui long nhap format dd/mm/yyyy.")
