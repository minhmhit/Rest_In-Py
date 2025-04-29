import tkinter as tk
from tkinter import ttk
import locale
from datetime import datetime

from view.db.database import DB_Connector
from view.models import RevenueData

# --- Vietnamese Locale and Currency Formatting ---
def format_currency_fallback(amount):
    """Fallback formatting if locale setting fails (Vietnamese style)."""
    # Formats number with commas as thousands separators and no decimal places, adds " VND"
    # Then replaces comma with dot for Vietnamese style
    return f"{amount:,.0f}".replace(",", ".") + " VND"

# Try setting locale for proper currency formatting
try:
    # Common locale names for Vietnamese
    locale.setlocale(locale.LC_ALL, 'vi_VN.UTF-8')
    # Define the function using locale.currency
    def format_currency(amount):
        # locale.currency might add a space or have different symbol placement,
        # adjust if needed or stick to manual formatting for consistency.
        # Using manual formatting for consistent "X.XXX.XXX VND" style
        return f"{amount:,.0f}".replace(",", ".") + " VND"

except locale.Error:
    try:
        locale.setlocale(locale.LC_ALL, 'Vietnamese_Vietnam.1258')
         # Define the function using locale.currency or manual
        def format_currency(amount):
             return f"{amount:,.0f}".replace(",", ".") + " VND"
            # Alternative using locale (might look different):
            # return locale.currency(amount, grouping=True, symbol=" VND")

    except locale.Error:
        print("Warning: Could not set Vietnamese locale for currency formatting. Using fallback.")
        # If both fail, use the manual fallback function
        format_currency = format_currency_fallback

# Ensure format_currency is defined even if all locale setting fails
if 'format_currency' not in locals():
    format_currency = format_currency_fallback

# --- End Vietnamese Locale and Currency Formatting ---


class Revenue(tk.Frame):
    def __init__(self, parent, revenue_list, db_conn: DB_Connector):
        super().__init__(parent, bg="#F5F5F5")

        self.revenue_list = revenue_list
        # if revenue_list is None:
        #     self.revenue_list = [
        #         RevenueData(1, "Nguyễn Văn An", "Nam", "1990-05-20", "Việt Nam", "Long An", "2005-08-16", "Thường", 301, 500000),
        #         RevenueData(2, "Trần Thị Hoa", "Nữ", "1985-12-15", "Việt Nam", "Tra Vinh", "2015-02-20", "VIP", 102, 400000),
        #         RevenueData(3, "Lê Minh Tú", "Nam", "1992-07-30", "Việt Nam", "Ho Chi Minh", "2010-02-10", "VIP", 103, 482945),
        #         RevenueData(4, "Phạm Thùy Dung", "Nữ", "1998-09-05", "Việt Nam", "Ha Noi", "2018-11-15", "Thường", 104, 109842),
        #         RevenueData(5, "Hoàng Quốc Bảo", "Nam", "1987-11-22", "Việt Nam", "Bac Lieu", "2020-01-01", "Thường", 105, 98247),
        #         RevenueData(6, "Đặng Thu Hằng", "Nữ", "1995-04-18", "Việt Nam", "Hai Phong", "2015-02-20", "VIP", 205, 100004),
        #         RevenueData(7, "Bùi Quang Huy", "Nam", "1989-08-12", "Việt Nam", "Vĩnh Long", "2015-02-23", "Thường", 201, 738883)
        #     ]
        # else:
        #      self.customer_list = [c for c in customer_list if isinstance(c, RevenueData)]


        # LabelFrame for the Table - Translated
        table_frame = tk.LabelFrame(self, text="Doanh Thu Nhà Nghỉ", bg="#F5F5F5", font=("Arial", 12, "bold"))
        table_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Columns Definition - Translated
        column_identifiers = ("Mã", "Tên", "Giới tính", "Ngày sinh", "Quốc tịch", "Quê quán", "Ngày nhận phòng", "Loại phòng", "Số phòng", "Tổng tiền")

        # Treeview Widget
        self.tree = ttk.Treeview(table_frame, columns=column_identifiers, show="headings")

        # Configure columns - Use translated identifiers
        for col_id in column_identifiers:
            self.tree.heading(col_id, text=col_id)
            self.tree.column(col_id, anchor="center", width=100) # Default width

        # Adjust width and alignment for the price column
        self.tree.column("Tổng tiền", anchor="e", width=100) # 'e' for east (right) alignment

        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", padx=10, pady=5, fill="both", expand=True)

        # insert initial data
        self.load_customer_data()

        # LabelFrame for Total Revenue - Translated
        revenue_frame = tk.LabelFrame(self, text="Tổng Doanh Thu 30 Ngày Gần Nhất", bg="#F5F5F5", font=("Arial", 12, "bold"))
        revenue_frame.pack(padx=10, pady=10, fill="x")

        # Total Revenue Label - Translated
        self.total_revenue_label = tk.Label(revenue_frame, text="Tổng Doanh Thu: " + format_currency(0), font=("Arial", 12, "bold"), bg="#F5F5F5")
        self.total_revenue_label.pack(padx=10, pady=5)

        # update total revenue
        self.update_total_revenue()

    def load_customer_data(self):
        """Clears the treeview and loads data from self.customer_list."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert data from the list
        for revenue in self.revenue_list:
            # Extract attributes into a tuple for the Treeview
            # Make sure the order matches column_identifiers
            revenue_values = (
                revenue.id,
                revenue.name,
                revenue.sex,
                revenue.birthday,
                revenue.national,
                revenue.country,
                revenue.checkin_date,
                revenue.room_type,
                revenue.room_number,
                revenue.total_price # Include the total price
            )
            # The treeview uses the column identifiers defined during setup,
            # the order of values in the tuple must match the order of identifiers.
            self.tree.insert("", "end", values=revenue_values)

    def update_total_revenue(self):
        """Calculates and updates the total revenue displayed."""
        total = 0.0
        # Get the column index for "Tổng tiền" dynamically
        # This is safer than hardcoding index 9
        try:
            price_col_index = list(self.tree["columns"]).index("Tổng tiền")
        except ValueError:
             print("Error: 'Tổng tiền' column not found in treeview columns.")
             self.total_revenue_label.config(text="Error calculating revenue.")
             return

        # Iterate through all items in the treeview
        for item_id in self.tree.get_children():
            # Get the values for the current item
            values = self.tree.item(item_id, "values")

            # Check if the values tuple is long enough
            if len(values) > price_col_index:
                try:
                    # Convert the price to float and add to total
                    price = float(values[price_col_index])
                    total += price
                except ValueError:
                    # Handle cases where the price isn't a number in that column
                    print(f"Warning: Could not convert price to float for item values: {values}")
                    pass # Skip this row
            else:
                 print(f"Warning: Item values too short, missing price column: {values}")


        # Format the total revenue using the configured format_currency function
        formatted_total = format_currency(total)

        # Update the label
        self.total_revenue_label.config(text=f"Tổng Doanh Thu: {formatted_total}")


    def add_record(self, customer: RevenueData):
        customer_values = (
            customer.id,
            customer.name,
            customer.sex,
            customer.birthday,
            customer.national,
            customer.country,
            customer.checkin_date,
            customer.room_type,
            customer.room_number,
            customer.total_price # Include the total price
        )

        # Insert the record and get its item ID
        # The values are matched to columns based on the order defined when creating the treeview
        item_id = self.tree.insert("", "end", values=customer_values)

        # Move the new record to the top (index 0) if desired
        # self.tree.move(item_id, "", 0) # Keep or remove

        # Add the customer object to the internal list
        self.revenue_list.append(customer)

        # Update total revenue
        self.update_total_revenue()
