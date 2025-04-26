import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from tkinter import filedialog
import locale

# Import python-docx
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Try to set locale for currency formatting
try:
    locale.setlocale(locale.LC_ALL, 'vi_VN.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_ALL, 'Vietnamese_Vietnam.1258')
    except locale.Error:
        print("Warning: Could not set Vietnamese locale for currency formatting.")
        def format_currency(amount):
            return f"{amount:,.0f}".replace(",", ".") + " VND"
    else:
        def format_currency(amount):
            return locale.currency(amount, grouping=True, symbol=" VND")
else:
    def format_currency(amount):
        return locale.currency(amount, grouping=True, symbol=" VND")

if 'format_currency' not in locals():
     def format_currency(amount):
            return f"{amount:,.0f}".replace(",", ".") + " VND"

# (Your CustomerInfo class here - commented out)
# class CustomerInfo: ...


class Checkout(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#eef2f7")
        self.price_per_day = {"VIP": 400000, "Normal": 250000}

        # --- NEW: Fixed daily rates for additional costs ---
        self.additional_price_per_day = {
            "Tiền điện": 5000,  # Example: 5000 VND per day
            "Tiền nước": 3000,  # Example: 3000 VND per day
            "Internet": 10000, # Example: 10000 VND per day
            "Tiền rác": 1000,   # Example: 1000 VND per day
            "Vệ sinh": 2000,    # Example: 2000 VND per day
        }
        # --- End NEW ---

        self.controller = controller # Customer data object

        # Panels
        self.leftPanel = tk.Frame(self, bg="#eef2f7")
        self.rightPanel = tk.Frame(self, bg="#eef2f7")
        self.mainPanel = tk.Frame(self, bg="#ffffff", padx=30, pady=30, relief=tk.RAISED, borderwidth=1, highlightbackground="#cccccc", highlightthickness=1)

        # Configure grid weights
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=5)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)

        # Layout
        self.leftPanel.grid(row=0, column=0, sticky="nsew")
        self.mainPanel.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.rightPanel.grid(row=0, column=2, sticky="nsew")

        # --- Content inside mainPanel ---

        # Title
        self.invoice_label = tk.Label(
            self.mainPanel, text="HÓA ĐƠN THANH TOÁN", font=("Arial", 30, "bold"), bg="#ffffff", fg="#333333"
        )
        self.invoice_label.pack(pady=(0, 20))

        # Customer Info Frame
        self.info_frame = tk.LabelFrame(self.mainPanel, text="THÔNG TIN KHÁCH HÀNG", font=("Arial", 14, "bold"), bg="#f8f9fa", padx=20, pady=15, bd=1, relief=tk.GROOVE, fg="#555555")
        self.info_frame.pack(fill="x", padx=10, pady=10)

        info_grid_frame = tk.Frame(self.info_frame, bg="#f8f9fa")
        info_grid_frame.pack(fill="both", expand=True)

        self.labels = {} # Labels for customer info and room type (read-only)
        fields = [
            ("Họ tên", "name"),
            ("Giới tính", "sex"),
            ("Ngày sinh", "birthday"),
            ("Quốc tịch", "national"),
            ("Quê quán", "country"),
        ]

        for i, (title, field) in enumerate(fields):
            tk.Label(info_grid_frame, text=title + ":", font=("Arial", 12, "bold"), bg="#f8f9fa", fg="#333333").grid(row=i, column=0, sticky="w", padx=5, pady=3)
            self.labels[field] = tk.Label(info_grid_frame, text="Đang tải...", font=("Arial", 12), bg="#f8f9fa", fg="#000000")
            self.labels[field].grid(row=i, column=1, sticky="w", padx=5, pady=3)

        # Room Details Frame
        self.room_frame = tk.LabelFrame(self.mainPanel, text="CHI TIẾT THUÊ PHÒNG", font=("Arial", 14, "bold"), bg="#f8f9fa", padx=20, pady=15, bd=1, relief=tk.GROOVE, fg="#555555")
        self.room_frame.pack(fill="x", padx=10, pady=10)

        room_grid_frame = tk.Frame(self.room_frame, bg="#f8f9fa")
        room_grid_frame.pack(fill="both", expand=True)

        tk.Label(room_grid_frame, text="Loại phòng:", font=("Arial", 12, "bold"), bg="#f8f9fa", fg="#333333").grid(row=0, column=0, sticky="w", padx=5, pady=3)
        self.labels["room_type"] = tk.Label(room_grid_frame, text="Đang tải...", font=("Arial", 12), bg="#f8f9fa", fg="#000000") # room_type label is also stored here
        self.labels["room_type"].grid(row=0, column=1, sticky="w", padx=5, pady=3)

        tk.Label(room_grid_frame, text="Ngày nhận phòng:", font=("Arial", 12, "bold"), bg="#f8f9fa", fg="#333333").grid(row=1, column=0, sticky="w", padx=5, pady=3)
        self.checkin_date_label = tk.Label(room_grid_frame, text="Đang tải...", bg="#f8f9fa", font=("Arial", 12), fg="#000000")
        self.checkin_date_label.grid(row=1, column=1, sticky="w", padx=5, pady=3)

        tk.Label(room_grid_frame, text="Ngày trả phòng:", font=("Arial", 12, "bold"), bg="#f8f9fa", fg="#333333").grid(row=2, column=0, sticky="w", padx=5, pady=3)
        self.checkout_date_label = tk.Label(room_grid_frame, text="Đang tải...", bg="#f8f9fa", font=("Arial", 12), fg="#000000")
        self.checkout_date_label.grid(row=2, column=1, sticky="w", padx=5, pady=3)

        # Separator
        separator_room_to_additional = tk.Frame(self.mainPanel, height=1, bg="#cccccc")
        separator_room_to_additional.pack(fill="x", padx=10, pady=15)

        # Additional Costs Frame (Now displaying calculated values)
        self.additional_frame = tk.LabelFrame(self.mainPanel, text="CHI PHÍ PHỤ (Tính theo ngày thuê)", font=("Arial", 14, "bold"), bg="#f8f9fa", padx=20, pady=15, bd=1, relief=tk.GROOVE, fg="#555555")
        self.additional_frame.pack(fill="x", padx=10, pady=10)

        additional_grid_frame = tk.Frame(self.additional_frame, bg="#f8f9fa")
        additional_grid_frame.pack(fill="both", expand=True)

        # --- NEW: Labels to display calculated additional costs ---
        self.additional_cost_labels = {}
        # Use the keys from the additional_price_per_day dictionary for order and titles
        for i, (cost_name, daily_rate) in enumerate(self.additional_price_per_day.items()):
             tk.Label(additional_grid_frame, text=cost_name + ":", font=("Arial", 12, "bold"), bg="#f8f9fa", fg="#333333").grid(row=i, column=0, sticky="w", padx=5, pady=3)
             # Label to display the calculated amount
             self.additional_cost_labels[cost_name] = tk.Label(additional_grid_frame, text="Đang tính...", font=("Arial", 12), bg="#f8f9fa", fg="#000000")
             self.additional_cost_labels[cost_name].grid(row=i, column=1, sticky="ew", padx=5, pady=3)
             # We no longer need a separate VND label if the amount includes it,
             # but keeping it helps alignment if the amount label text varies
             # tk.Label(additional_grid_frame, text=" VND", font=("Arial", 12), bg="#f8f9fa", fg="#333333").grid(row=i, column=2, sticky="w", padx=0, pady=3)

        # Add weight to column 1 for the cost amount labels
        additional_grid_frame.columnconfigure(1, weight=1)
        # --- End NEW ---


        # Separator
        separator_additional_to_total = tk.Frame(self.mainPanel, height=1, bg="#cccccc")
        separator_additional_to_total.pack(fill="x", padx=10, pady=15)

        # Result Label (Total Cost)
        self.result_label = tk.Label(self.mainPanel, text="Tổng tiền: Đang tính...", font=("Arial", 20, "bold"), fg="#007bff", bg="#ffffff")
        self.result_label.pack(pady=(10, 20))

        # Button Frame
        self.button_frame = tk.Frame(self.mainPanel, bg="#ffffff")
        self.button_frame.pack(pady=(0, 10))

        # Calculate Button
        self.calculate_btn = tk.Button(
            self.button_frame, text="TÍNH TIỀN", font=("Arial", 12, "bold"), fg="white", bg="#28a745",
            activebackground="#218838", activeforeground="white",
            relief=tk.RAISED, padx=15, pady=8, cursor="hand2",
            command=self.load_and_calculate # This method now also calculates and displays additional costs
        )
        self.calculate_btn.pack(side=tk.LEFT, padx=5)

        # Export Button
        self.export_btn = tk.Button(
            self.button_frame, text="XUẤT FILE WORD", font=("Arial", 12, "bold"), fg="white", bg="#17a2b8",
            activebackground="#138496", activeforeground="white",
            relief=tk.RAISED, padx=15, pady=8, cursor="hand2",
            command=self.export_invoice_to_word
        )
        self.export_btn.pack(side=tk.LEFT, padx=5)


    # --- Update the load_and_calculate method ---
    def load_and_calculate(self):
        """Loads customer info, calculates costs (room + additional), and updates display."""
        customer_data = self.controller

        if not customer_data:
             messagebox.showwarning("Cảnh báo", "Không có dữ liệu khách hàng để tạo hóa đơn.")
             # Clear customer/room info labels
             for _, label_widget in self.labels.items():
                  label_widget.config(text="Không có dữ liệu")
             self.checkin_date_label.config(text="N/A")
             self.checkout_date_label.config(text="N/A")
             self.result_label.config(text="Tổng tiền: N/A", fg="#dc3545")
             # Clear additional cost display labels
             for _, label_widget in self.additional_cost_labels.items():
                  label_widget.config(text="N/A")
             return

        # Populate ALL info fields (customer details and room type) - Keep this part
        for attr_name, label_widget in self.labels.items():
            value = getattr(customer_data, attr_name, "Không có dữ liệu")
            label_widget.config(text=value if value else "Không có dữ liệu")

        # Get check-in date and room type
        checkin_date_str = getattr(customer_data, "checkin_date", None)
        room_type = getattr(customer_data, "room_type", "Normal")

        # --- Calculate Duration ---
        duration = 0
        checkin_display = "N/A"
        checkout_display = datetime.today().strftime("%d/%m/%Y") # Default to today's date formatted

        if checkin_date_str:
            try:
                checkin = datetime.strptime(checkin_date_str, "%Y-%m-%d")
                checkout = datetime.today() # Use today's date as checkout
                if checkout >= checkin:
                    duration = (checkout - checkin).days
                    if duration < 0: duration = 0 # Should not happen if checkout >= checkin
                checkin_display = checkin.strftime("%d/%m/%Y") # Format for display
            except ValueError:
                messagebox.showwarning("Cảnh báo", f"Ngày nhận phòng '{checkin_date_str}' có định dạng không hợp lệ.")
                checkin_display = "Lỗi định dạng"
                duration = 0 # Reset duration on error
        else:
            messagebox.showwarning("Cảnh báo", "Không có ngày nhận phòng để tính tiền.")

        # Update date display labels
        self.checkin_date_label.config(text=checkin_display)
        self.checkout_date_label.config(text=checkout_display)
        # --- End Calculate Duration ---


        # --- Calculate Base Room Cost ---
        # calculate_room_cost now only needs checkin_date_str and room_type,
        # it will calculate duration internally as before, or we could pass duration
        # Let's reuse the duration calculated above for consistency
        base_room_cost = self.calculate_room_cost_from_duration(duration, room_type)
        # --- End Calculate Base Room Cost ---


        # --- NEW: Calculate and display additional costs ---
        additional_cost_sum = 0
        for cost_name, daily_rate in self.additional_price_per_day.items():
            cost = daily_rate * duration # Calculate cost based on daily rate and duration
            additional_cost_sum += cost
            # Update the specific label for this additional cost
            if cost_name in self.additional_cost_labels:
                self.additional_cost_labels[cost_name].config(text=format_currency(cost))
            else:
                print(f"Warning: Label for {cost_name} not found.") # Debugging line
        # --- End NEW ---


        # Calculate final total
        final_total = base_room_cost + additional_cost_sum

        # Format the final total for display
        formatted_total = format_currency(final_total)

        self.result_label.config(text=f"TỔNG TIỀN: {formatted_total}", fg="#28a745" if final_total >= 0 else "#dc3545")


    # --- Modified calculate_room_cost to accept duration (optional, but cleaner) ---
    # Renaming for clarity as it now uses pre-calculated duration
    def calculate_room_cost_from_duration(self, duration, room_type):
        """Calculates the base room cost based on duration and room type."""
        if duration <= 0:
            return 0

        room_rate = self.price_per_day.get(room_type, 250000) # Default to normal rate
        return duration * room_rate

    # Keep the original calculate_room_cost if you need it elsewhere,
    # but the logic for load_and_calculate is updated to use duration directly.
    # Or just replace the old one if this is the only place it's used for calculation.
    # Let's replace the old one and rename it.
    # (The old calculate_room_cost is now replaced by calculate_room_cost_from_duration)


    # --- Update the export_invoice_to_word method ---
    def export_invoice_to_word(self):
        customer_data = self.controller

        if not customer_data:
            messagebox.showwarning("Cảnh báo", "Không có dữ liệu khách hàng để xuất hóa đơn.")
            return

        # Get file path from user
        filepath = filedialog.asksaveasfilename(
            defaultextension=".docx",
            filetypes=[("Word Documents", "*.docx"), ("All Files", "*.*")],
            title="Lưu Hóa Đơn Dạng Word"
        )

        if not filepath: # User cancelled the dialog
            return

        try:
            # Create a new Word document
            document = Document()

            # Add Title
            title = document.add_paragraph("HÓA ĐƠN THANH TOÁN")
            title.alignment = WD_ALIGN_PARAGRAPH.CENTER
            title.style = 'Heading 1'

            # Add Customer Info - Keep this part
            document.add_paragraph("THÔNG TIN KHÁCH HÀNG", style='Heading 2')
            fields = [
                ("Họ tên", "name"),
                ("Giới tính", "sex"),
                ("Ngày sinh", "birthday"),
                ("Quốc tịch", "national"),
                ("Quê quán", "country"),
            ]
            for title, field in fields:
                value = getattr(customer_data, field, "Không có dữ liệu")
                p = document.add_paragraph()
                p.add_run(title + ": ").bold = True
                p.add_run(str(value) if value else "Không có dữ liệu")

            # Add Room Details - Keep this part
            document.add_paragraph("CHI TIẾT THUÊ PHÒNG", style='Heading 2')

            room_type = getattr(customer_data, "room_type", "Không xác định")
            p_room = document.add_paragraph()
            p_room.add_run("Loại phòng: ").bold = True
            p_room.add_run(str(room_type) if room_type else "Không xác định")

            checkin_date_str = getattr(customer_data, "checkin_date", None)

            # --- Recalculate Duration for Document ---
            duration = 0
            checkin_display = "N/A"
            checkout_display = datetime.today().strftime("%d/%m/%Y")

            if checkin_date_str:
                 try:
                      checkin = datetime.strptime(checkin_date_str, "%Y-%m-%d")
                      checkout = datetime.today()
                      if checkout >= checkin:
                           duration = (checkout - checkin).days
                           if duration < 0: duration = 0
                      checkin_display = checkin.strftime("%d/%m/%Y")
                 except ValueError:
                      checkin_display = "Lỗi định dạng ngày"
                      duration = 0
            # --- End Recalculate Duration ---


            p_checkin = document.add_paragraph()
            p_checkin.add_run("Ngày nhận phòng: ").bold = True
            p_checkin.add_run(checkin_display)

            p_checkout = document.add_paragraph()
            p_checkout.add_run("Ngày trả phòng: ").bold = True
            p_checkout.add_run(checkout_display)

            p_duration = document.add_paragraph()
            p_duration.add_run("Tổng số ngày thuê: ").bold = True
            p_duration.add_run(f"{duration} ngày")

            # --- Calculate Base Room Cost for Document ---
            base_room_cost = self.calculate_room_cost_from_duration(duration, room_type)
            # --- End Calculate Base Room Cost ---


            # --- NEW: Calculate and add Additional Costs to Word ---
            document.add_paragraph("CHI PHÍ PHỤ", style='Heading 2')

            additional_cost_sum = 0
            for cost_name, daily_rate in self.additional_price_per_day.items():
                cost = daily_rate * duration # Calculate cost
                additional_cost_sum += cost

                p_cost = document.add_paragraph()
                p_cost.add_run(cost_name + ": ").bold = True
                p_cost.add_run(format_currency(cost)) # Format individual cost
            # --- End NEW ---


            # Add Total Cost (includes base room cost + additional costs)
            final_total = base_room_cost + additional_cost_sum

            document.add_paragraph("") # Add a blank line for spacing
            p_total = document.add_paragraph()
            p_total.add_run("TỔNG TIỀN: ").bold = True
            p_total.add_run(format_currency(final_total)).bold = True
            p_total.alignment = WD_ALIGN_PARAGRAPH.RIGHT

            # Save the document
            document.save(filepath)

            messagebox.showinfo("Thành công", f"Đã xuất hóa đơn ra file:\n{filepath}")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi xuất file Word:\n{e}")
