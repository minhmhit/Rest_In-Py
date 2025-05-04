import tkinter as tk
from tkinter import ttk
import locale
from datetime import datetime, timedelta
import random # Import random for sample data

from view.models import RevenueData

# --- Vietnamese Locale and Currency Formatting ---
def format_currency_fallback(amount):
    """Fallback formatting if locale setting fails (Vietnamese style)."""
    return f"{amount:,.0f}".replace(",", ".") + " VND"

try:
    # Try setting Vietnamese locale
    locale.setlocale(locale.LC_ALL, 'vi_VN.UTF-8')
    def format_currency(amount):
        # Format as X.XXX.XXX VND
        return f"{amount:,.0f}".replace(",", ".") + " VND"
except locale.Error:
    try:
        # Try alternative Vietnamese locale
        locale.setlocale(locale.LC_ALL, 'Vietnamese_Vietnam.1258')
        def format_currency(amount):
             # Format as X.XXX.XXX VND
             return f"{amount:,.0f}".replace(",", ".") + " VND"
    except locale.Error:
        print("Warning: Could not set Vietnamese locale for currency formatting. Using fallback.")
        format_currency = format_currency_fallback # Use the fallback function

# Ensure format_currency is defined even if all locale setting fails
if 'format_currency' not in locals():
    format_currency = format_currency_fallback

# --- End Vietnamese Locale and Currency Formatting ---


class Revenue(tk.Frame):
    def __init__(self, parent, revenue_list=None, db_conn=None):
        super().__init__(parent, bg="#F5F5F5")

        self.revenue_list = revenue_list if revenue_list is not None else []
        self.db_conn = db_conn # Store the database connector (optional, depending on usage)

        # --- Table Frame ---
        table_frame = tk.LabelFrame(self, text="Doanh Thu Nhà Nghỉ", bg="#F5F5F5", font=("Arial", 12, "bold"))
        table_frame.pack(padx=10, pady=10, fill="both", expand=True)

        column_identifiers = ("Mã", "Tên", "Giới tính", "Ngày sinh", "Quốc tịch", "Quê quán", "Ngày nhận phòng", "Ngày trả phòng", "Loại phòng", "Số phòng", "Tổng tiền")

        # Treeview Widget
        self.tree = ttk.Treeview(table_frame, columns=column_identifiers, show="headings")

        # Configure columns
        for col_id in column_identifiers:
            self.tree.heading(col_id, text=col_id)
            # Adjust column widths as needed
            self.tree.column(col_id, anchor="center", width=80) # Default width

        # Specific column width adjustments
        self.tree.column("Mã", width=60) # Adjust ID width
        self.tree.column("Tên", width=150, anchor="w") # Wider for names, left-aligned
        self.tree.column("Giới tính", width=80)
        self.tree.column("Ngày sinh", width=100)
        self.tree.column("Quốc tịch", width=100)
        self.tree.column("Quê quán", width=150, anchor="w") # Wider for country, left-aligned
        self.tree.column("Ngày nhận phòng", width=120)
        self.tree.column("Ngày trả phòng", width=120)
        self.tree.column("Loại phòng", width=80)
        self.tree.column("Số phòng", width=80)
        self.tree.column("Tổng tiền", anchor="e", width=120) # Right-aligned for currency, slightly wider


        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", padx=10, pady=5, fill="both", expand=True)

        # --- Total Revenue Frame ---
        revenue_frame = tk.LabelFrame(self, text="Tổng Doanh Thu", bg="#F5F5F5", font=("Arial", 12, "bold")) # Simplified title
        revenue_frame.pack(padx=10, pady=10, fill="x")

        # Frame to hold Label and Button side-by-side
        total_display_frame = tk.Frame(revenue_frame, bg="#F5F5F5")
        total_display_frame.pack(fill="x", padx=10, pady=5)
        total_display_frame.columnconfigure(0, weight=1) # Make label column expandable

        # Total Revenue Label
        self.total_revenue_label = tk.Label(total_display_frame, text="Tổng Doanh Thu: " + format_currency(0), font=("Arial", 12, "bold"), bg="#F5F5F5")
        self.total_revenue_label.grid(row=0, column=0, sticky="w") # Use grid for side-by-side

        # Refresh List Button (Renamed and command updated)
        self.refresh_list_button = tk.Button(
            total_display_frame,
            text="Tải lại danh sách", # Button text
            command=self.refresh_display, # Call the refresh method
            font=("Arial", 10),
            bg="#4CAF50", # Green background
            fg="white", # White text
            activebackground="#45a049", # Darker green when active
            activeforeground="white",
            bd=0, # No border
            padx=10, # Padding
            pady=5,
            relief=tk.FLAT # Flat appearance
        )
        self.refresh_list_button.grid(row=0, column=1, sticky="e") # Use grid for side-by-side

        # --- Initial Load and Calculation ---
        self.load_revenue_data()
        self.update_total_revenue()


    def load_revenue_data(self):
        """Clears the treeview and loads data from self.revenue_list."""
        print("[*] Loading revenue data into Treeview...")
        # Clear existing items in the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert data from the internal list (self.revenue_list)
        for revenue in self.revenue_list:
            # Ensure revenue is RevenueData and has the necessary attributes
            if not isinstance(revenue, RevenueData):
                 print(f"Warning: Found non-RevenueData object in list: {revenue}. Skipping.")
                 continue # Skip non-RevenueData items

            # Use the get_values_for_treeview method from RevenueData if available
            if hasattr(revenue, 'get_values_for_treeview') and callable(revenue.get_values_for_treeview):
                 revenue_values = revenue.get_values_for_treeview()
            else:
                revenue_values = (
                    getattr(revenue, 'id', ''),
                    getattr(revenue, 'name', ''),
                    getattr(revenue, 'sex', ''),
                    getattr(revenue, 'birthday', ''),
                    getattr(revenue, 'national', ''), # Use nationality
                    getattr(revenue, 'country', ''),
                    getattr(revenue, 'checkin_date', ''),
                    getattr(revenue, 'checkout_date', ''), # Added checkout_date
                    getattr(revenue, 'room_type', ''),
                    getattr(revenue, 'room_number', ''),
                    getattr(revenue, 'total_price', 0.0) # Ensure price is treated as float
                )

            # Ensure the tuple length matches the number of columns
            if len(revenue_values) == len(self.tree["columns"]):
                 # Format the total_price for display in the treeview
                 formatted_values = list(revenue_values) # Convert to list to modify
                 # Find the index of the "Tổng tiền" column dynamically
                 try:
                      price_col_index = list(self.tree["columns"]).index("Tổng tiền")
                      # Format the price at the correct index
                      formatted_values[price_col_index] = format_currency(revenue_values[price_col_index])
                 except ValueError:
                      print("Warning: 'Tổng tiền' column not found for formatting in load_revenue_data.")
                      # If column not found, insert raw values (might not be formatted)

                 self.tree.insert("", "end", values=formatted_values) # Insert formatted values
            else:
                 print(f"Warning: Data tuple length mismatch for item {revenue}. Expected {len(self.tree['columns'])}, got {len(revenue_values)}. Skipping.")
                 print(f"Values: {revenue_values}")

        print("[✓] Revenue data loaded into Treeview.")


    def update_total_revenue(self):
        """Calculates and updates the total revenue displayed from the internal list."""
        print("[*] Calculating total revenue from list...")
        total = 0.0
        # Calculate total directly from the internal list (self.revenue_list)
        # This is more reliable than parsing from the Treeview strings
        for revenue in self.revenue_list:
             if isinstance(revenue, RevenueData):
                  # Safely get the total_price, default to 0.0 if not found or invalid
                  price = getattr(revenue, 'total_price', 0.0)
                  try:
                      total += float(price) # Ensure it's a float before adding
                  except (ValueError, TypeError):
                      print(f"Warning: Could not convert total_price '{price}' to float for item {revenue}. Skipping.")
                      pass # Skip this item's price if invalid
             else:
                  print(f"Warning: Found non-RevenueData object in list during total calculation: {revenue}. Skipping.")


        # Format the total revenue using the configured format_currency function
        formatted_total = format_currency(total)

        # Update the label
        self.total_revenue_label.config(text=f"Tổng Doanh Thu: {formatted_total}")
        print(f"[✓] Total revenue updated: {formatted_total}")


    # --- Method to refresh the display from the internal list ---
    def refresh_display(self):
        self.load_revenue_data() # Reload data from the internal list into Treeview
        self.update_total_revenue() # Recalculate and update total


    def add_sample_record(self):
        print("[*] Adding sample revenue record...")
        sample_id = len(self.revenue_list) + 1 # Simple way to get a unique ID
        sample_name = f"Khách Mẫu {sample_id}"
        sample_sex = random.choice(["Nam", "Nữ"])
        sample_birthday = "2000-01-01" # Example fixed date string
        sample_national = "Việt Nam"
        sample_country = "Hà Nội"
        # Generate sample dates
        start_date = datetime.now() - timedelta(days=random.randint(1, 30))
        end_date = start_date + timedelta(days=random.randint(1, 10))
        sample_checkin = start_date.strftime("%Y-%m-%d")
        sample_checkout = end_date.strftime("%Y-%m-%d")

        sample_room_type = random.choice(["Thường", "VIP"])
        sample_room_number = random.randint(101, 305)
        sample_price = random.randint(100000, 1000000) # Random price

        sample_revenue = RevenueData(
            id=sample_id,
            name=sample_name,
            sex=sample_sex,
            birthday=sample_birthday,
            national=sample_national, # Use nationality
            country=sample_country,
            checkin_date=sample_checkin,
            checkout_date=sample_checkout,
            room_type=sample_room_type,
            room_number=sample_room_number,
            total_price=int(sample_price) # Ensure total_price is a float
        )

        # Add the sample record to the internal list
        self.revenue_list.append(sample_revenue)
        print(f"[✓] Sample revenue record added to list: ID {sample_revenue.id}")

        # Refresh the display to show the new record and update the total
        self.refresh_display()
        print("[✓] Revenue tab display refreshed after adding sample record.")
