import tkinter as tk
from datetime import datetime, date, timedelta # Import timedelta for date calculations
from tkinter import messagebox, ttk
from tkinter import filedialog
import locale
from typing import Callable # Import Callable for type hinting

from view.db.database import DB_Connector
from view.models import CustomerInfo, RevenueData
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
DOCX_AVAILABLE = True

# Import python-docx (ensure you have it installed: pip install python-docx)
# try:
#     from docx import Document
#     from docx.shared import Inches
#     from docx.enum.text import WD_ALIGN_PARAGRAPH
#     DOCX_AVAILABLE = True
# except ImportError:
#     print("Warning: python-docx library not found. Export to Word will be disabled.")
#     DOCX_AVAILABLE = False
#

# --- Define colors --- (Keep consistent)
COLOR_PRIMARY_BLUE = "#3B82F6"
COLOR_ACCENT_GREEN = "#28a745"
COLOR_ACCENT_RED = "#dc3545"
COLOR_ACCENT_TEAL = "#17a2b8"
COLOR_BACKGROUND_LIGHT = "#eef2f7"
COLOR_FRAME_BACKGROUND = "#f8f9fa"
COLOR_MAIN_PANEL_BG = "#ffffff"
COLOR_TEXT_DARK = "#333333"
COLOR_TEXT_MEDIUM = "#555555"
COLOR_BORDER_GRAY = "#cccccc"

# --- Currency Formatting ---
# Ensure consistent formatting function is available
try:
    locale.setlocale(locale.LC_ALL, 'vi_VN.UTF-8')
    def format_currency(amount):
        # Format as X.XXX.XXX VND
        return f"{amount:,.0f}".replace(",", ".") + " VND"
except locale.Error:
    try:
        locale.setlocale(locale.LC_ALL, 'Vietnamese_Vietnam.1258')
        def format_currency(amount):
             # Format as X.XXX.XXX VND
             return f"{amount:,.0f}".replace(",", ".") + " VND"
    except locale.Error:
        print("Warning: Could not set Vietnamese locale for currency formatting. Using fallback.")
        def format_currency(amount):
            # Fallback format
            return f"{amount:,.0f}".replace(",", ".") + " VND"

# Ensure format_currency is defined even if all locale setting fails
if 'format_currency' not in locals():
     def format_currency(amount):
            return f"{amount:,.0f}".replace(",", ".") + " VND"
# --- End Currency Formatting ---


class Checkout(tk.Frame):
    # Accept the CustomerInfo object and a callback function in __init__
    def __init__(self, parent, customer_info_controller: CustomerInfo, add_revenue_callback: Callable[[RevenueData], None], db_conn: DB_Connector):
        super().__init__(parent, bg=COLOR_BACKGROUND_LIGHT)

        # --- Price Definitions ---
        self.price_per_day = {"VIP": 400000, "Thường": 250000} # Assuming "Thường" is the term
        self.db_conn = db_conn

        self.additional_price_per_day = {
            "Tiền điện": 5000,
            "Tiền nước": 3000,
            "Internet": 10000,
            "Tiền rác": 1000,
            "Vệ sinh": 2000,
        }

        # --- Motel Information (for Word Export) ---
        self.motel_name = "Fake Motel"
        self.motel_city = "Thành Phố Hồ Chí Minh"
        self.motel_phone = "0528471087"


        # --- Data and Callback Storage ---
        # Store the CustomerInfo object representing the current customer
        self.customer_info_controller = customer_info_controller
        # Store the callback function provided by the App to add revenue data
        self.add_revenue_callback = add_revenue_callback

        # --- Variables to store calculated values ---
        self.current_duration = 0
        self.current_base_room_cost = 0
        self.current_additional_cost_sum = 0
        self.current_final_total = 0.0
        self.current_checkout_dt = datetime.today() # Store checkout datetime object (defaults to today)


        # --- UI Panels ---
        self.leftPanel = tk.Frame(self, bg=COLOR_BACKGROUND_LIGHT)
        self.rightPanel = tk.Frame(self, bg=COLOR_BACKGROUND_LIGHT)
        self.mainPanel = tk.Frame(self, bg=COLOR_MAIN_PANEL_BG, padx=30, pady=30, relief=tk.RAISED, borderwidth=1, highlightbackground=COLOR_BORDER_GRAY, highlightthickness=1)

        # Configure grid weights for the main frame
        self.columnconfigure(0, weight=1) # Left padding/spacer
        self.columnconfigure(1, weight=5) # Main content area
        self.columnconfigure(2, weight=1) # Right padding/spacer
        self.rowconfigure(0, weight=1) # Main row expands

        # Layout panels using grid
        self.leftPanel.grid(row=0, column=0, sticky="nsew")
        self.mainPanel.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.rightPanel.grid(row=0, column=2, sticky="nsew")

        # --- Content inside mainPanel ---
        self.mainPanel.columnconfigure(0, weight=1) # Make the single column in mainPanel expandable

        # Title
        self.invoice_label = tk.Label(
            self.mainPanel, text="HÓA ĐƠN THANH TOÁN", font=("Arial", 30, "bold"), bg=COLOR_MAIN_PANEL_BG, fg=COLOR_TEXT_DARK
        )
        self.invoice_label.pack(pady=(0, 20))

        # --- Customer Info Frame ---
        self.info_frame = tk.LabelFrame(self.mainPanel, text="THÔNG TIN KHÁCH HÀNG", font=("Arial", 14, "bold"), bg=COLOR_FRAME_BACKGROUND, padx=20, pady=15, bd=1, relief=tk.GROOVE, fg=COLOR_TEXT_MEDIUM)
        self.info_frame.pack(fill="x", padx=10, pady=10)

        info_grid_frame = tk.Frame(self.info_frame, bg=COLOR_FRAME_BACKGROUND)
        info_grid_frame.pack(fill="both", expand=True)
        info_grid_frame.columnconfigure(1, weight=1) # Make value column expandable

        self.labels = {} # Dictionary to store labels for dynamic updates

        # --- Info fields definition ---
        # Define the fields to display from the CustomerInfo object
        self.info_fields = [
            ("Mã khách hàng", "id"), # Assuming CustomerInfo has an 'id' attribute
            ("Họ tên", "name"),
            ("Giới tính", "sex"),
            ("Ngày Sinh", "birthday"),
            ("Quốc tịch", "national"), # Use 'nationality' as per previous discussion
            ("Quê quán", "country"),
        ]
        # --- End Info fields definition ---

        # Create labels for customer info fields
        for i, (title, field) in enumerate(self.info_fields):
            tk.Label(info_grid_frame, text=title + ":", font=("Arial", 12, "bold"), bg=COLOR_FRAME_BACKGROUND, fg=COLOR_TEXT_DARK).grid(row=i, column=0, sticky="w", padx=5, pady=3)
            # Use anchor="w" for left alignment and sticky="ew" to fill horizontally
            self.labels[field] = tk.Label(info_grid_frame, text="...", font=("Arial", 12), bg=COLOR_FRAME_BACKGROUND, fg=COLOR_TEXT_DARK, anchor="w")
            self.labels[field].grid(row=i, column=1, sticky="ew", padx=5, pady=3)

        # --- Room Details Frame ---
        self.room_frame = tk.LabelFrame(self.mainPanel, text="CHI TIẾT THUÊ PHÒNG", font=("Arial", 14, "bold"), bg=COLOR_FRAME_BACKGROUND, padx=20, pady=15, bd=1, relief=tk.GROOVE, fg=COLOR_TEXT_MEDIUM)
        self.room_frame.pack(fill="x", padx=10, pady=10)

        room_grid_frame = tk.Frame(self.room_frame, bg=COLOR_FRAME_BACKGROUND)
        room_grid_frame.pack(fill="both", expand=True)
        room_grid_frame.columnconfigure(1, weight=1) # Make value column expandable

        # Labels for room details
        tk.Label(room_grid_frame, text="Loại phòng:", font=("Arial", 12, "bold"), bg=COLOR_FRAME_BACKGROUND, fg=COLOR_TEXT_DARK).grid(row=0, column=0, sticky="w", padx=5, pady=3)
        self.labels["room_type"] = tk.Label(room_grid_frame, text="...", font=("Arial", 12), bg=COLOR_FRAME_BACKGROUND, fg=COLOR_TEXT_DARK, anchor="w") # room_type label
        self.labels["room_type"].grid(row=0, column=1, sticky="ew", padx=5, pady=3)

        tk.Label(room_grid_frame, text="Số phòng:", font=("Arial", 12, "bold"), bg=COLOR_FRAME_BACKGROUND, fg=COLOR_TEXT_DARK).grid(row=1, column=0, sticky="w", padx=5, pady=3)
        self.labels["room_number"] = tk.Label(room_grid_frame, text="...", font=("Arial", 12), bg=COLOR_FRAME_BACKGROUND, fg=COLOR_TEXT_DARK, anchor="w") # room_number label
        self.labels["room_number"].grid(row=1, column=1, sticky="ew", padx=5, pady=3)

        tk.Label(room_grid_frame, text="Ngày nhận phòng:", font=("Arial", 12, "bold"), bg=COLOR_FRAME_BACKGROUND, fg=COLOR_TEXT_DARK).grid(row=2, column=0, sticky="w", padx=5, pady=3)
        self.checkin_date_label = tk.Label(room_grid_frame, text="...", bg=COLOR_FRAME_BACKGROUND, font=("Arial", 12), fg=COLOR_TEXT_DARK, anchor="w")
        self.checkin_date_label.grid(row=2, column=1, sticky="ew", padx=5, pady=3)

        tk.Label(room_grid_frame, text="Ngày trả phòng:", font=("Arial", 12, "bold"), bg=COLOR_FRAME_BACKGROUND, fg=COLOR_TEXT_DARK).grid(row=3, column=0, sticky="w", padx=5, pady=3)
        self.checkout_date_label = tk.Label(room_grid_frame, text="...", bg=COLOR_FRAME_BACKGROUND, font=("Arial", 12), fg=COLOR_TEXT_DARK, anchor="w")
        self.checkout_date_label.grid(row=3, column=1, sticky="ew", padx=5, pady=3)

        tk.Label(room_grid_frame, text="Tổng số ngày thuê:", font=("Arial", 12, "bold"), bg=COLOR_FRAME_BACKGROUND, fg=COLOR_TEXT_DARK).grid(row=4, column=0, sticky="w", padx=5, pady=3)
        self.duration_label = tk.Label(room_grid_frame, text="...", bg=COLOR_FRAME_BACKGROUND, font=("Arial", 12), fg=COLOR_TEXT_DARK, anchor="w")
        self.duration_label.grid(row=4, column=1, sticky="ew", padx=5, pady=3)


        # Separator
        separator_room_to_additional = ttk.Separator(self.mainPanel, orient='h') # Use ttk.Separator
        separator_room_to_additional.pack(fill="x", padx=10, pady=15)

        # --- Additional Costs Frame ---
        self.additional_frame = tk.LabelFrame(self.mainPanel, text="CHI PHÍ PHỤ (Tính theo ngày thuê)", font=("Arial", 14, "bold"), bg=COLOR_FRAME_BACKGROUND, padx=20, pady=15, bd=1, relief=tk.GROOVE, fg=COLOR_TEXT_MEDIUM)
        self.additional_frame.pack(fill="x", padx=10, pady=10)

        additional_grid_frame = tk.Frame(self.additional_frame, bg=COLOR_FRAME_BACKGROUND)
        additional_grid_frame.pack(fill="both", expand=True)
        additional_grid_frame.columnconfigure(1, weight=1) # Make value column expandable

        self.additional_cost_labels = {}
        for i, (cost_name, daily_rate) in enumerate(self.additional_price_per_day.items()):
             tk.Label(additional_grid_frame, text=cost_name + ":", font=("Arial", 12, "bold"), bg=COLOR_FRAME_BACKGROUND, fg=COLOR_TEXT_DARK).grid(row=i, column=0, sticky="w", padx=5, pady=3)
             self.additional_cost_labels[cost_name] = tk.Label(additional_grid_frame, text="...", font=("Arial", 12), bg=COLOR_FRAME_BACKGROUND, fg=COLOR_TEXT_DARK, anchor="w")
             self.additional_cost_labels[cost_name].grid(row=i, column=1, sticky="ew", padx=5, pady=3)


        # Separator
        separator_additional_to_total = ttk.Separator(self.mainPanel, orient='h') # Use ttk.Separator
        separator_additional_to_total.pack(fill="x", padx=10, pady=15)

        # --- Result Label (Total Cost) ---
        self.result_label = tk.Label(self.mainPanel, text="TỔNG TIỀN: ...", font=("Arial", 20, "bold"), fg=COLOR_PRIMARY_BLUE, bg=COLOR_MAIN_PANEL_BG)
        self.result_label.pack(pady=(10, 20))

        # --- Button Frame ---
        self.button_frame = tk.Frame(self.mainPanel, bg=COLOR_MAIN_PANEL_BG)
        self.button_frame.pack(pady=(0, 10))

        button_font = ("Arial", 12, "bold")
        button_pady = 8
        button_padx = 15

        # Calculate Button
        self.calculate_btn = tk.Button(
            self.button_frame, text="TÍNH TIỀN", font=button_font, fg="white", bg=COLOR_ACCENT_GREEN,
            activebackground="#1e7e34", activeforeground="white",
            relief=tk.RAISED, padx=button_padx, pady=button_pady, cursor="hand2",
            command=self.calculate_and_display_costs # Call the calculation method
        )
        self.calculate_btn.pack(side=tk.LEFT, padx=5)

        # Export Button (Enabled only if python-docx is available)
        self.export_btn = tk.Button(
            self.button_frame, text="XUẤT FILE WORD", font=button_font, fg="white", bg=COLOR_ACCENT_TEAL,
            activebackground="#117a8b", activeforeground="white",
            relief=tk.RAISED, padx=button_padx, pady=button_pady, cursor="hand2",
            command=self.export_invoice_to_word,
            state=tk.NORMAL if DOCX_AVAILABLE else tk.DISABLED # Enable/Disable based on docx availability
        )
        self.export_btn.pack(side=tk.LEFT, padx=5)

        # --- Finalize Checkout Button ---
        self.finalize_btn = tk.Button(
            self.button_frame, text="THANH TOÁN & LƯU", font=button_font, fg="white", bg=COLOR_PRIMARY_BLUE,
            activebackground="#3060c0", activeforeground="white",
            relief=tk.RAISED, padx=button_padx, pady=button_pady, cursor="hand2",
            command=self.finalize_checkout # Call the finalize method
        )
        self.finalize_btn.pack(side=tk.LEFT, padx=5)
        # --- End Finalize Checkout Button ---


    # --- Helper to process raw date input (string or datetime) into datetime object ---
    def _process_date_input_to_datetime(self, raw_date_value):
        """Converts raw date input (string or datetime) to a datetime object or None."""
        if isinstance(raw_date_value, datetime):
             return raw_date_value # Already a datetime object
        elif isinstance(raw_date_value, date): # Handle date objects too
             # Combine date object with min time to get a datetime object
             return datetime.combine(raw_date_value, datetime.min.time())
        elif isinstance(raw_date_value, str) and raw_date_value:
             try:
                 # Try parsing from YYYY-MM-DD string
                 return datetime.strptime(raw_date_value, "%Y-%m-%d")
             except ValueError:
                 print(f"Warning: Could not parse date string '{raw_date_value}'. Expected YYYY-MM-DD.")
                 return None
        else:
             return None # None, empty string, or other types are treated as no date


    # --- Calculate Base Room Cost from Duration ---
    def calculate_room_cost_from_duration(self, duration, room_type):
        """Calculates the base room cost based on duration and room type."""
        if duration is None or duration < 0: # Duration should not be negative
            return 0

        # Use .get() with a default value in case room_type is unexpected
        # Default to "Thường" price or 0 if "Thường" isn't in the dict either
        room_rate = self.price_per_day.get(room_type, self.price_per_day.get("Thường", 0))
        return duration * room_rate

    # --- Method to load and display customer/room info (called by App when tab is shown) ---
    def load_customer_data(self):
        """Loads customer and room info from the controller and updates the display labels."""
        customer_data = self.customer_info_controller

        # Reset stored calculated values when loading new customer data
        self.current_duration = 0
        self.current_base_room_cost = 0
        self.current_additional_cost_sum = 0
        self.current_final_total = 0.0
        self.current_checkout_dt = datetime.today() # Reset checkout date to today

        if not customer_data:
            # Clear all display labels if no customer data
            print("[*] No customer data available in controller. Clearing display.")
            for field in self.labels.keys():
                 self.labels[field].config(text="...") # Use "..." or "N/A"

            self.checkin_date_label.config(text="...")
            self.checkout_date_label.config(text="...")
            self.duration_label.config(text="...")

            for _, label_widget in self.additional_cost_labels.items():
                 label_widget.config(text="...")

            self.result_label.config(text="TỔNG TIỀN: ...", fg=COLOR_PRIMARY_BLUE)
            return

        print("[*] Loading customer data for display...")

        # --- Update GUI display labels for customer info, room type, and room number ---
        # Use self.info_fields to iterate through fields including birthday
        for title, field in self.info_fields:
             value = getattr(customer_data, field, None) # Use None as default

             if field == "birthday": # Handle birthday formatting here
                  birthday_dt = self._process_date_input_to_datetime(value)
                  display_value = birthday_dt.strftime("%Y-%m-%d") if birthday_dt else "N/A"
             else:
                 # For other info fields (id, name, sex, nationality, country)
                 # Use getattr to safely access attributes, provide "N/A" if None
                 display_value = str(value) if value is not None else "N/A"

             if field in self.labels: # Ensure label exists before config
                  self.labels[field].config(text=display_value)
             else:
                  print(f"Warning: Label widget not found for field '{field}'.")


        # Handle Room Type and Room Number labels (assuming these are attributes of customer_data)
        room_type_value = getattr(customer_data, "room_type", None)
        room_number_value = getattr(customer_data, "room_number", None)

        self.labels["room_type"].config(text=str(room_type_value) if room_type_value is not None else "N/A")
        self.labels["room_number"].config(text=str(room_number_value) if room_number_value is not None else "N/A")


        # Check-in date label is updated during calculation, initially set to "..."
        self.checkin_date_label.config(text="...")
        self.checkout_date_label.config(text="...")
        self.duration_label.config(text="...")

        # Clear additional costs and total initially
        for _, label_widget in self.additional_cost_labels.items():
             label_widget.config(text="...")
        self.result_label.config(text="TỔNG TIỀN: ...", fg=COLOR_PRIMARY_BLUE)

        print("[✓] Customer data display updated.")


    # --- Method to calculate costs and update display (called by "TÍNH TIỀN" button) ---
    def calculate_and_display_costs(self):
        """Calculates room and additional costs and updates the display."""
        customer_data = self.customer_info_controller

        if not customer_data:
             messagebox.showwarning("Cảnh báo", "Không có dữ liệu khách hàng để tính tiền.")
             # Clear calculated fields if no customer data
             self.checkin_date_label.config(text="N/A")
             self.checkout_date_label.config(text="N/A")
             self.duration_label.config(text="N/A")
             for _, label_widget in self.additional_cost_labels.items():
                  label_widget.config(text="N/A")
             self.result_label.config(text="TỔNG TIỀN: N/A", fg=COLOR_ACCENT_RED)
             # Reset stored calculated values
             self.current_duration = 0
             self.current_base_room_cost = 0
             self.current_additional_cost_sum = 0
             self.current_final_total = 0.0
             self.current_checkout_dt = datetime.today() # Reset checkout date to today
             return # Do not proceed if no customer data

        # Get raw check-in date data and room type from the controller object
        raw_checkin_date = getattr(customer_data, "checkin_date", None)
        room_type = getattr(customer_data, "room_type", "Thường") # Default to "Thường"

        # --- Process Raw Check-in Date ---
        checkin_dt = self._process_date_input_to_datetime(raw_checkin_date)
        self.current_checkout_dt = datetime.today() # Use today's date for checkout calculation

        self.current_duration = 0
        checkin_display = "N/A"
        checkout_display = self.current_checkout_dt.strftime("%Y-%m-%d") # Format as YYYY-MM-DD for display

        if checkin_dt:
            if self.current_checkout_dt >= checkin_dt:
                 time_difference = self.current_checkout_dt - checkin_dt
                 self.current_duration = time_difference.days # Duration in days
                 # If duration is 0, it means less than a full day, often charged as 1 day
                 if self.current_duration == 0 and time_difference.total_seconds() > 0:
                     self.current_duration = 1 # Charge for at least one day if checkin/out are same day but different times
                 elif self.current_duration < 0: # Should not happen with checkout_dt = today()
                     self.current_duration = 0

            else:
                 messagebox.showwarning("Lỗi", "Ngày trả phòng không hợp lệ (trước ngày nhận phòng).")
                 self.current_duration = 0 # Reset duration on invalid date range

            checkin_display = checkin_dt.strftime("%Y-%m-%d") # Format as YYYY-MM-DD for display
        else:
             messagebox.showwarning("Cảnh báo", "Ngày nhận phòng không hợp lệ hoặc không có dữ liệu.")
             # checkin_display remains "N/A"


        # --- Update GUI display labels for dates and duration ---
        self.checkin_date_label.config(text=checkin_display)
        self.checkout_date_label.config(text=checkout_display)
        self.duration_label.config(text=f"{self.current_duration} ngày")


        # --- Calculate Base Room Cost --- (Using calculated duration)
        self.current_base_room_cost = self.calculate_room_cost_from_duration(self.current_duration, room_type)


        # --- Calculate and display additional costs --- (Using calculated duration)
        self.current_additional_cost_sum = 0
        for cost_name, daily_rate in self.additional_price_per_day.items():
             cost = daily_rate * self.current_duration
             self.current_additional_cost_sum += cost
             if cost_name in self.additional_cost_labels:
                 self.additional_cost_labels[cost_name].config(text=format_currency(cost))
             else:
                 print(f"Warning: Label for '{cost_name}' not found in additional_cost_labels.")


        # Calculate final total
        self.current_final_total = self.current_base_room_cost + self.current_additional_cost_sum

        # Format the final total for display
        formatted_total = format_currency(self.current_final_total)

        # Update the result label
        self.result_label.config(text=f"TỔNG TIỀN: {formatted_total}", fg=COLOR_ACCENT_GREEN if self.current_final_total >= 0 else COLOR_ACCENT_RED)

        print("[✓] Costs calculated and displayed.")


    # --- Method to finalize checkout and pass data (called by "THANH TOÁN & LƯU" button) ---
    def finalize_checkout(self):
        """Creates the RevenueData object and calls the callback to add/save the record."""
        customer_data = self.customer_info_controller

        # Ensure costs have been calculated at least once and there's a valid duration
        if self.current_final_total is None or self.current_duration <= 0:
             messagebox.showwarning("Cảnh báo", "Vui lòng tính tiền trước khi thanh toán.")
             return

        if not customer_data:
             messagebox.showwarning("Cảnh báo", "Không có dữ liệu khách hàng để tạo bản ghi doanh thu.")
             return

        # --- Create the RevenueData object ---
        # Get check-in date again to include in the RevenueData object
        raw_checkin_date = getattr(customer_data, "checkin_date", None)
        checkin_dt = self._process_date_input_to_datetime(raw_checkin_date)
        # Format dates as YYYY-MM-DD strings for the RevenueData object
        checkin_date_str = checkin_dt.strftime("%Y-%m-%d") if checkin_dt else "N/A"
        checkout_date_str = self.current_checkout_dt.strftime("%Y-%m-%d") # Use the stored checkout datetime object

        # Use getattr with default values for safety when accessing customer_data attributes
        revenue_record = RevenueData(
            id=getattr(customer_data, 'id', None), # Assuming customer_data has an 'id'
            name=getattr(customer_data, 'name', 'Unknown'),
            sex=getattr(customer_data, 'sex', 'N/A'),
            birthday=getattr(customer_data, 'birthday', 'N/A'), # Pass raw birthday, models.py should handle format if needed
            national=getattr(customer_data, 'national', 'N/A'), # Use national
            country=getattr(customer_data, 'country', 'N/A'),
            checkin_date=checkin_date_str, # Use formatted string
            checkout_date=checkout_date_str, # Use formatted string
            room_type=getattr(customer_data, 'room_type', 'N/A'),
            room_number=getattr(customer_data, 'room_number', 'N/A'),
            total_price=int(self.current_final_total) # Use the calculated total
        )

        # --- Call the callback provided by the App ---
        if self.add_revenue_callback:
            try:
                # Pass the newly created RevenueData object to the callback
                self.add_revenue_callback(revenue_record)
                messagebox.showinfo("Thành công", "Đã lưu hóa đơn và thêm vào danh sách doanh thu.")
                print("[✓] Finalized checkout and called add_revenue_callback.")
                # Optional: Clear the checkout display after successful finalization
                # This prepares the tab for the next customer

                # add to revenue_record: RevenueData sql table
                self.db_conn.setRevenueToDatabase(revenue_record)

                self.load_customer_data() # Clears the display and resets values
            except Exception as e:
                 messagebox.showerror("Lỗi Callback", f"Đã xảy ra lỗi khi gọi hàm lưu dữ liệu:\n{e}")
                 print(f"[!] Error calling add_revenue_callback: {e}")
        else:
            messagebox.showwarning("Cảnh báo", "Không có hàm lưu dữ liệu được cung cấp.")
            print("[!] add_revenue_callback is not set.")


    # --- export_invoice_to_word method ---
    def export_invoice_to_word(self):
        """Exports the current invoice details to a Word document."""
        # Check if python-docx is available
        if not DOCX_AVAILABLE:
             messagebox.showwarning("Cảnh báo", "Thư viện 'python-docx' chưa được cài đặt. Không thể xuất file Word.")
             return

        customer_data = self.customer_info_controller

        # Ensure costs have been calculated before exporting
        if self.current_final_total is None or self.current_duration <= 0:
             messagebox.showwarning("Cảnh báo", "Vui lòng tính tiền trước khi xuất hóa đơn.")
             return

        if not customer_data:
             messagebox.showwarning("Cảnh báo", "Không có dữ liệu khách hàng để xuất hóa đơn.")
             return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".docx",
            filetypes=[("Word Documents", "*.docx"), ("All Files", "*.*")],
            title="Lưu Hóa Đơn Dạng Word"
        )

        if not filepath:
            return

        try:
            document = Document()

            # --- Add Motel Information at the top ---
            motel_info_paragraph = document.add_paragraph()
            motel_info_paragraph.add_run(f"{self.motel_name}\n").bold = True
            motel_info_paragraph.add_run(f"Địa chỉ: {self.motel_city}\n")
            motel_info_paragraph.add_run(f"Điện thoại: {self.motel_phone}\n")
            motel_info_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER # Center align motel info
            document.add_paragraph("") # Add some space

            # --- Add Invoice Title ---
            title = document.add_paragraph("HÓA ĐƠN THANH TOÁN")
            title.alignment = WD_ALIGN_PARAGRAPH.CENTER
            title.style = 'Heading 1'
            document.add_paragraph("") # Add some space

            # Add Customer Info
            document.add_paragraph("THÔNG TIN KHÁCH HÀNG", style='Heading 2')
            # Use self.info_fields to iterate and get values
            for title, field in self.info_fields:
                 value = getattr(customer_data, field, None) # Use None as default
                 # Format dates for document (expecting datetime or date objects, or strings)
                 if field in ["birthday"] and isinstance(value, (datetime, date)):
                      display_value = value.strftime("%Y-%m-%d") # Format as YYYY-MM-DD for document
                 else:
                      # For other info fields (id, name, sex, nationality, country)
                      display_value = str(value) if value is not None else "N/A"


                 p = document.add_paragraph()
                 p.add_run(title + ": ").bold = True
                 p.add_run(display_value)

            document.add_paragraph("") # Add some space

            # Add Room Details (using the stored calculated duration/dates)
            document.add_paragraph("CHI TIẾT THUÊ PHÒNG", style='Heading 2')

            room_type_value = getattr(customer_data, "room_type", None)
            room_number_value = getattr(customer_data, "room_number", None)

            p_room = document.add_paragraph()
            p_room.add_run("Loại phòng: ").bold = True
            p_room.add_run(str(room_type_value) if room_type_value is not None else "N/A")

            p_room_num = document.add_paragraph()
            p_room_num.add_run("Số phòng: ").bold = True
            p_room_num.add_run(str(room_number_value) if room_number_value is not None else "N/A")


            # Use the formatted date strings from the last calculation/display
            # Or use the stored datetime objects for more accuracy if needed
            checkin_display = self.checkin_date_label.cget("text")
            checkout_display = self.checkout_date_label.cget("text")
            duration_display = self.duration_label.cget("text")


            p_checkin = document.add_paragraph()
            p_checkin.add_run("Ngày nhận phòng: ").bold = True
            p_checkin.add_run(checkin_display)

            p_checkout = document.add_paragraph()
            p_checkout.add_run("Ngày trả phòng: ").bold = True
            p_checkout.add_run(checkout_display)

            p_duration = document.add_paragraph()
            p_duration.add_run("Tổng số ngày thuê: ").bold = True
            p_duration.add_run(duration_display)

            document.add_paragraph("") # Add some space

            # --- Add Additional Costs to Word (using stored calculated costs) ---
            document.add_paragraph("CHI PHÍ PHỤ", style='Heading 2')

            # Iterate through the additional cost labels to get the displayed values
            for cost_name, label_widget in self.additional_cost_labels.items():
                 displayed_cost = label_widget.cget("text") # Get the formatted string from the label

                 p_cost = document.add_paragraph()
                 p_cost.add_run(cost_name + ": ").bold = True
                 p_cost.add_run(displayed_cost) # Use the formatted string

            document.add_paragraph("") # Add some space

            # Add Total Cost (using the stored final total)
            document.add_paragraph("") # Add some space before total
            p_total = document.add_paragraph()
            p_total.add_run("TỔNG TIỀN: ").bold = True
            # Format the stored total again for safety/consistency in the document
            p_total.add_run(format_currency(self.current_final_total)).bold = True
            p_total.alignment = WD_ALIGN_PARAGRAPH.RIGHT

            document.save(filepath)
            messagebox.showinfo("Thành công", f"Đã xuất hóa đơn ra file:\n{filepath}")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi xuất file Word:\n{e}")

    # --- Method to be called by App when the tab is shown ---
    def refresh_display(self):
        """Method called by the App to refresh the display when the tab is shown."""
        print("[*] Checkout tab refreshing display...")
        self.load_customer_data() # Load and display customer info
        # Costs are calculated when the button is clicked, not automatically on refresh
        print("[✓] Checkout tab display refreshed.")

