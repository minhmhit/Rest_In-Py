import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, date # Import date
from view.models import CustomerInfo
from tkcalendar import Calendar
from view.db.database import DB_Connector
from typing import Callable # Import Callable for type hinting

try:
    from view.utils import capture_customer_image
    CAPTURE_AVAILABLE = True
except ImportError:
    print("Warning: src/view/utils.py or capture_customer_image function not found. Image capture will be disabled.")
    CAPTURE_AVAILABLE = False

# --- Define colors --- (Keep consistent with Checkout)
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

# --- Define all possible room numbers ---
# Pattern: 101-109, 201-209, ..., 901-909
ALL_ROOM_NUMBERS = [f"{floor * 100 + room}" for floor in range(1, 10) for room in range(1, 10)]


class Customer(tk.Frame):
    # Added refresh_room_management_callback parameter
    def __init__(self, parent,show_tab,controller,customer_list,db_conn: DB_Connector,refresh_room_management_callback):
        super().__init__(parent, bg=COLOR_BACKGROUND_LIGHT)
        self.show_tab = show_tab
        self.controller = controller # Assumed to be the object receiving customer data for checkout
        self.customer_list = customer_list # The list holding CustomerInfo objects
        self.db_conn = db_conn
        self.refresh_room_management_callback = refresh_room_management_callback


        # Define fields for consistency
        self.customer_fields = [
            ("ID", "id"), ("Họ Tên", "name"), ("Giới Tính", "sex"), ("Ngày Sinh", "birthday"),
            ("Quốc Tịch", "national"), ("Quê Quán", "country"), ("Ngày Thuê Phòng", "checkin_date"), # Changed 'national' to 'nationality'
            ("Loại Phòng", "room_type"), ("Số Phòng", "room_number"), # room_number field
        ]
        self.treeview_columns = [title for title, field in self.customer_fields]
        self.treeview_field_map = {title: field for title, field in self.customer_fields}


        # Create panels
        self.mainPanel = tk.LabelFrame(
            self, text="DANH SÁCH KHÁCH HÀNG", bg=COLOR_MAIN_PANEL_BG, fg=COLOR_TEXT_MEDIUM, font=("Arial", 14, "bold"), padx=15, pady=15, bd=1, relief=tk.GROOVE
        )
        self.functionPanel = tk.Frame(self, bg=COLOR_FRAME_BACKGROUND, padx=10, pady=10)

        self.mainPanel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.functionPanel.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Customer list (Treeview)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background=COLOR_PRIMARY_BLUE, foreground="white")
        style.configure("Treeview", font=("Arial", 10), rowheight=25, fieldbackground=COLOR_MAIN_PANEL_BG, foreground=COLOR_TEXT_DARK)
        style.map("Treeview", background=[("selected", COLOR_PRIMARY_BLUE)], foreground=[("selected", "white")])


        self.tree = ttk.Treeview(
            self.mainPanel, columns=self.treeview_columns, show="headings", style="Treeview"
        )

        for col in self.treeview_columns:
            self.tree.heading(col, text=col, anchor="center") # Center header text
            width_map = { # Adjust column widths as needed
                "ID": 60, "Họ Tên": 150, "Giới Tính": 80, "Ngày Sinh": 100, "Quốc Tịch": 100,
                "Quê Quán": 120, "Ngày Thuê Phòng": 100, "Loại Phòng": 80, "Số Phòng": 80 # room_number width
            }
            self.tree.column(col, width=width_map.get(col, 100), anchor="center") # Center cell text


        self.populate_treeview()


        scrollbar = ttk.Scrollbar(
            self.mainPanel, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.mainPanel.rowconfigure(0, weight=1)
        self.mainPanel.columnconfigure(0, weight=1)

        # buttons (placed in functionPanel)
        button_font = ("Arial", 10, "bold")
        button_pady = 8
        button_padx = 15

        self.addCustomer = tk.Button(
            self.functionPanel, text="Thêm khách hàng", font=button_font,
            bg=COLOR_ACCENT_GREEN, fg="white", activebackground="#1e7e34", activeforeground="white",
            relief=tk.RAISED, padx=button_padx, pady=button_pady, cursor="hand2",
            command=self.open_add_customer,
        )
        self.removeCustomer = tk.Button(
            self.functionPanel, text="Xóa khách hàng", font=button_font,
            bg=COLOR_ACCENT_RED, fg="white", activebackground="#c82333", activeforeground="white",
            relief=tk.RAISED, padx=button_padx, pady=button_pady, cursor="hand2",
            command=self.remove_customer,
        )
        self.changeInformation = tk.Button(
            self.functionPanel, text="Chỉnh sửa", font=button_font,
            bg=COLOR_ACCENT_TEAL, fg="white", activebackground="#117a8b", activeforeground="white",
            relief=tk.RAISED, padx=button_padx, pady=button_pady, cursor="hand2",
            command=self.change_customer_information,
        )
        self.customerPayment = tk.Button(
            self.functionPanel, text="Thanh toán", font=button_font,
            bg=COLOR_PRIMARY_BLUE, fg="white", activebackground="#0056b3", activeforeground="white",
            relief=tk.RAISED, padx=button_padx, pady=button_pady, cursor="hand2",
            command=self.sent_data_to_checkout,
        )

        self.addCustomer.pack(side="left", expand=True, fill=tk.X, padx=5)
        self.removeCustomer.pack(side="left", expand=True, fill=tk.X, padx=5)
        self.changeInformation.pack(side="left", expand=True, fill=tk.X, padx=5)
        self.customerPayment.pack(side="left", expand=True, fill=tk.X, padx=5)

    # --- Helper methods for room availability ---
    def _get_occupied_room_numbers(self):
        """Returns a set of room numbers currently occupied by customers in the list."""
        occupied_rooms = set()
        for customer in self.customer_list:
            room_num = getattr(customer, 'room_number', None)
            if room_num is not None and room_num != "":
                occupied_rooms.add(str(room_num)) # Ensure it's a string for comparison
        return occupied_rooms

    def _get_available_room_numbers(self):
        """Returns a sorted list of room numbers that are not currently occupied."""
        occupied_rooms = self._get_occupied_room_numbers()
        # Filter ALL_ROOM_NUMBERS to exclude occupied rooms
        available_rooms = [room for room in ALL_ROOM_NUMBERS if room not in occupied_rooms]
        # Sort numerically
        available_rooms.sort(key=int)
        return available_rooms


    def populate_treeview(self):
        """Clears and repopulates the treeview from self.customer_list."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Add data (expecting CustomerInfo objects with YYYY-MM-DD strings or None)
        for customer in self.customer_list:
            # Use the get_values_for_treeview method from CustomerInfo
            # Assume CustomerInfo has this method and returns YYYY-MM-DD strings or ""
            if hasattr(customer, 'get_values_for_treeview'):
                 values = customer.get_values_for_treeview()
                 # Ensure iid is a string and not empty
                 customer_id_str = str(getattr(customer, 'id', '')) if getattr(customer, 'id', None) is not None else f"temp_{hash(customer)}"
                 if customer_id_str == "":
                     customer_id_str = f"temp_{hash(customer)}" # Use temp iid if ID is empty string
                 self.tree.insert("", "end", iid=customer_id_str, values=values)
            else:
                 # Fallback logic if CustomerInfo doesn't have the method (less ideal)
                 print(f"Warning: Customer object {customer} does not have get_values_for_treeview method. Using fallback.")
                 try:
                     # Attempt to get values directly, format dates to YYYY-MM-DD strings
                     values = (
                         str(getattr(customer, 'id', '') if getattr(customer, 'id', None) is not None else ""),
                         str(getattr(customer, 'name', '') if getattr(customer, 'name', None) is not None else ""),
                         str(getattr(customer, 'sex', '') if getattr(customer, 'sex', None) is not None else ""),
                         getattr(customer, 'birthday', ''), # May be datetime or string
                         str(getattr(customer, 'national', '') if getattr(customer, 'national', None) is not None else ""), # Use nationality
                         str(getattr(customer, 'country', '') if getattr(customer, 'country', None) is not None else ""),
                         getattr(customer, 'checkin_date', ''), # May be datetime or string
                         str(getattr(customer, 'room_type', '') if getattr(customer, 'room_type', None) is not None else ""),
                         str(getattr(customer, 'room_number', '') if getattr(customer, 'room_number', None) is not None else ""), # room_number
                     )

                     # Ensure dates are YYYY-MM-DD strings for the Treeview
                     values_formatted = list(values)
                     # Indices for date fields: birthday (3), checkin_date (6)
                     date_indices = [i for i, (title, field) in enumerate(self.customer_fields) if field in ['birthday', 'checkin_date']]

                     for i in date_indices:
                          if i < len(values_formatted): # Prevent index error
                              if isinstance(values_formatted[i], (datetime, date)):
                                   values_formatted[i] = values_formatted[i].strftime("%Y-%m-%d")
                              elif values_formatted[i] is None:
                                   values_formatted[i] = "" # Ensure None becomes empty string
                              elif not isinstance(values_formatted[i], str):
                                   # Handle cases where it's not a date/datetime or string
                                   values_formatted[i] = str(values_formatted[i])


                     customer_id_str = values_formatted[0] if values_formatted[0] else f"temp_{hash(customer)}" # Use ID or temp
                     self.tree.insert("", "end", iid=customer_id_str, values=values_formatted)

                 except Exception as e:
                      print(f"Error inserting customer {customer} into treeview using fallback: {e}")


    # --- Helper to create calendar command closures (Outputs YYYY-MM-DD) ---
    def create_calendar_command(self, parent_window, entry_widget, field_name):
         """Helper to create calendar command closures."""
         def open_calendar():
              def select_date():
                   # get_date() returns string in date_pattern format (yyyy-mm-dd)
                   selected_date_str = cal.get_date()
                   # Temporarily set state to normal to allow insertion
                   entry_widget.config(state="normal")
                   entry_widget.delete(0, tk.END)
                   entry_widget.insert(0, selected_date_str) # Insert YYYY-MM-DD string
                   # Set state back to readonly
                   entry_widget.config(state="readonly")
                   top.destroy()

              top = tk.Toplevel(parent_window)
              top.title(f"Chọn Ngày {self.field_name_to_vietnamese(field_name)}")
              top.transient(parent_window.winfo_toplevel())
              top.grab_set()

              # Calendar widget - Use YYYY-MM-DD date_pattern
              cal = Calendar(top, date_pattern="yyyy-mm-dd", selectmode='day', font=("Arial", 10))
              cal.pack(pady=10, padx=10)

              btn_select = tk.Button(top, text="Xác Nhận", command=select_date, font=("Arial", 10, "bold"),
                                     bg=COLOR_PRIMARY_BLUE, fg="white", activebackground="#0056b3", activeforeground="white",
                                     relief=tk.RAISED, padx=10, pady=5, cursor="hand2")
              btn_select.pack(pady=5)

         return open_calendar

    def field_name_to_vietnamese(self, field_name):
        """Helper to map internal field name to Vietnamese title."""
        mapping = {field: title for title, field in self.customer_fields}
        return mapping.get(field_name, field_name)


    # --- open_add_customer method (UPDATED for Room Number Dropdown) ---
    # def open_add_customer(self):
    #     add_window = tk.Toplevel(self, bg=COLOR_BACKGROUND_LIGHT)
    #     add_window.title("Thêm khách hàng mới")
    #     # Adjusted geometry to fit potentially more fields/widgets
    #     add_window.geometry("450x500")
    #     add_window.transient(self.winfo_toplevel())
    #     add_window.grab_set()
    #
    #     padding_frame = tk.Frame(add_window, bg=COLOR_BACKGROUND_LIGHT, padx=20, pady=20)
    #     padding_frame.pack(fill="both", expand=True)
    #
    #     entries = {} # Use a dict to store Entry/Combobox widgets
    #
    #     # Use the fields defined in __init__ for consistency
    #     add_fields_and_titles = self.customer_fields
    #     field_title_map = {field: title for title, field in self.customer_fields}
    #
    #
    #     for i, (title, field) in enumerate(add_fields_and_titles):
    #         tk.Label(padding_frame, text=title + ":", font=("Arial", 10), bg=COLOR_BACKGROUND_LIGHT, fg=COLOR_TEXT_DARK).grid(
    #             row=i, column=0, padx=5, pady=5, sticky="w"
    #         )
    #
    #         if field == "sex":
    #              combobox_items = ["Nam", "Nữ", "Khác"]
    #              widget = ttk.Combobox(padding_frame, values=combobox_items, state="readonly", font=("Arial", 10))
    #              widget.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
    #              widget.current(0)
    #              entries[field] = widget # Store the Combobox widget
    #         elif field == "room_type":
    #              combobox_items = ["Thường", "VIP"]
    #              widget = ttk.Combobox(padding_frame, values=combobox_items, state="readonly", font=("Arial", 10))
    #              widget.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
    #              widget.current(0)
    #              entries[field] = widget # Store the Combobox widget
    #         elif field == "room_number":
    #              # --- Room Number Combobox ---
    #              available_rooms = self._get_available_room_numbers()
    #              widget = ttk.Combobox(padding_frame, values=available_rooms, state="readonly", font=("Arial", 10))
    #              widget.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
    #              # Optionally set the first available room as default
    #              if available_rooms:
    #                  widget.current(0)
    #              entries[field] = widget # Store the Combobox widget
    #              # --- End Room Number Combobox ---
    #         elif field in ["birthday", "checkin_date"]:
    #              # Use an Entry (readonly) and a button for dates (Calendar outputs YYYY-MM-DD)
    #              entry = tk.Entry(padding_frame, font=("Arial", 10), state="readonly")
    #              entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
    #              entries[field] = entry # Store entry reference
    #              date_button_command = self.create_calendar_command(padding_frame, entry, field)
    #              date_button = tk.Button(padding_frame, text="Chọn ngày", command=date_button_command, font=("Arial", 8), padx=2, pady=2)
    #              date_button.grid(row=i, column=2, padx=(0, 5), pady=5, sticky="w")
    #              # No need to store date_button in entries dict
    #         else:
    #              # Standard Entry for other fields (id, name, nationality, country)
    #              entry = tk.Entry(padding_frame, font=("Arial", 10))
    #              entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
    #              entries[field] = entry # Store the Entry widget
    #
    #
    #     padding_frame.columnconfigure(1, weight=1) # Entry/Combobox column expands
    #
    #
    #     def submit():
    #         new_customer_values = {}
    #         for field, widget in entries.items():
    #              # Get value from Entry or Combobox
    #              if isinstance(widget, (tk.Entry, ttk.Combobox)):
    #                   new_customer_values[field] = widget.get().strip() # Get value and strip whitespace
    #              elif isinstance(widget, tk.Label) and field == 'id':
    #                   # Should not happen in add window, but for consistency
    #                   new_customer_values[field] = widget.cget("text").strip()
    #
    #
    #         # Validation
    #         # room_number is now validated by the Combobox selection, but check if it's empty
    #         required_fields = ['id', 'name', 'checkin_date', 'room_type', 'room_number']
    #         for field in required_fields:
    #              if not new_customer_values.get(field):
    #                   messagebox.showerror("Lỗi", f"Trường '{field_title_map.get(field, field)}' không được để trống.")
    #                   return
    #
    #         # Validate ID is numeric
    #         if not new_customer_values['id'].isdigit():
    #             messagebox.showerror("Lỗi", "ID phải là số.")
    #             return
    #
    #         # Validate dates are in YYYY-MM-DD format if not empty
    #         for field in ['birthday', 'checkin_date']:
    #              date_str = new_customer_values.get(field)
    #              if date_str: # Only validate if not empty
    #                   try:
    #                        datetime.strptime(date_str, "%Y-%m-%d")
    #                   except ValueError:
    #                        messagebox.showerror("Lỗi định dạng ngày", f"Trường '{field_title_map.get(field, field)}' có định dạng không hợp lệ. Vui lòng dùng YYYY-MM-DD.")
    #                        return
    #
    #         # Check if room number is already occupied (should be handled by dropdown, but double check)
    #         if new_customer_values.get('room_number') in self._get_occupied_room_numbers():
    #              messagebox.showerror("Lỗi", f"Số phòng {new_customer_values.get('room_number')} đã có khách thuê.")
    #              return
    #
    #
    #         # Create CustomerInfo object (passing YYYY-MM-DD strings or empty strings)
    #         new_customer_info = CustomerInfo(
    #             id=new_customer_values.get('id'),
    #             name=new_customer_values.get('name'),
    #             sex=new_customer_values.get('sex'),
    #             birthday=new_customer_values.get('birthday'), # Store as YYYY-MM-DD string
    #             national=new_customer_values.get('national'), # Use nationality
    #             country=new_customer_values.get('country'),
    #             checkin_date=new_customer_values.get('checkin_date'), # Store as YYYY-MM-DD string
    #             room_type=new_customer_values.get('room_type'),
    #             room_number=new_customer_values.get('room_number') # Store the selected room number string
    #         )
    #
    #         # Add to customer_list and Treeview
    #         self.customer_list.append(new_customer_info)
    #         self.populate_treeview() # Repopulate to ensure data is fresh and sorted/ordered
    #
    #         # Add to database
    #         try:
    #             self.db_conn.setCustomerToDatabase(new_customer_info) # Expects CustomerInfo with YYYY-MM-DD strings
    #             messagebox.showinfo("Thành công", "Đã thêm khách hàng mới.")
    #             # Call the refresh callback after adding a customer
    #             if self.refresh_room_management_callback:
    #                  self.refresh_room_management_callback()
    #             add_window.destroy()
    #
    #         except Exception as e:
    #             messagebox.showerror("Lỗi Database", f"Không thể thêm khách hàng vào database:\n{e}")
    #             # Optional: remove the added customer from list/treeview if DB fails?
    #             # self.customer_list.pop()
    #             # self.populate_treeview()
    #
    #
    #     button_frame_bottom = tk.Frame(padding_frame, bg=COLOR_BACKGROUND_LIGHT)
    #     button_frame_bottom.grid(row=len(add_fields_and_titles), column=0, columnspan=3, pady=10)
    #     button_frame_bottom.columnconfigure(0, weight=1)
    #
    #     submit_btn = tk.Button(button_frame_bottom, text="LƯU KHÁCH HÀNG", command=submit,
    #                            font=("Arial", 10, "bold"), bg=COLOR_ACCENT_GREEN, fg="white",
    #                            activebackground="#1e7e34", activeforeground="white",
    #                            relief=tk.RAISED, padx=10, pady=5, cursor="hand2")
    #     submit_btn.pack(expand=True)

    def open_add_customer(self):
        add_window = tk.Toplevel(self, bg=COLOR_BACKGROUND_LIGHT)
        add_window.title("Thêm khách hàng mới")
        # Adjusted geometry to fit potentially more fields/widgets and the new button
        add_window.geometry("450x550") # Increased height slightly
        add_window.transient(self.winfo_toplevel())
        add_window.grab_set()

        padding_frame = tk.Frame(add_window, bg=COLOR_BACKGROUND_LIGHT, padx=20, pady=20)
        padding_frame.pack(fill="both", expand=True)

        entries = {} # Use a dict to store Entry/Combobox widgets

        # Use the fields defined in __init__ for consistency
        add_fields_and_titles = self.customer_fields
        field_title_map = {field: title for title, field in self.customer_fields}


        for i, (title, field) in enumerate(add_fields_and_titles):
            tk.Label(padding_frame, text=title + ":", font=("Arial", 10), bg=COLOR_BACKGROUND_LIGHT, fg=COLOR_TEXT_DARK).grid(
                row=i, column=0, padx=5, pady=5, sticky="w"
            )

            if field == "sex":
                 combobox_items = ["Nam", "Nữ", "Khác"]
                 widget = ttk.Combobox(padding_frame, values=combobox_items, state="readonly", font=("Arial", 10))
                 widget.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
                 widget.current(0)
                 entries[field] = widget # Store the Combobox widget
            elif field == "room_type":
                 combobox_items = ["Thường", "VIP"]
                 widget = ttk.Combobox(padding_frame, values=combobox_items, state="readonly", font=("Arial", 10))
                 widget.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
                 widget.current(0)
                 entries[field] = widget # Store the Combobox widget
            elif field == "room_number":
                 # --- Room Number Combobox ---
                 available_rooms = self._get_available_room_numbers()
                 widget = ttk.Combobox(padding_frame, values=available_rooms, state="readonly", font=("Arial", 10))
                 widget.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
                 # Optionally set the first available room as default
                 if available_rooms:
                     widget.current(0)
                 entries[field] = widget # Store the Combobox widget
                 # --- End Room Number Combobox ---
            elif field in ["birthday", "checkin_date"]:
                 # Use an Entry (readonly) and a button for dates (Calendar outputs JPanel-MM-DD)
                 entry = tk.Entry(padding_frame, font=("Arial", 10), state="readonly")
                 entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
                 entries[field] = entry # Store entry reference
                 date_button_command = self.create_calendar_command(padding_frame, entry, field)
                 date_button = tk.Button(padding_frame, text="Chọn ngày", command=date_button_command, font=("Arial", 8), padx=2, pady=2)
                 date_button.grid(row=i, column=2, padx=(0, 5), pady=5, sticky="w")
                 # No need to store date_button in entries dict
            else:
                 # Standard Entry for other fields (id, name, nationality, country)
                 entry = tk.Entry(padding_frame, font=("Arial", 10))
                 entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
                 entries[field] = entry # Store the Entry widget


        padding_frame.columnconfigure(1, weight=1) # Entry/Combobox column expands

        # --- Capture Image Button ---
        # Placed below the input fields
        capture_button_frame = tk.Frame(padding_frame, bg=COLOR_BACKGROUND_LIGHT)
        # Grid this frame below the last input field row
        capture_button_frame.grid(row=len(add_fields_and_titles), column=0, columnspan=3, pady=(15, 5))
        capture_button_frame.columnconfigure(0, weight=1) # Center the button

        def on_capture_click():
            """Handles the click event for the Capture Image button."""
            customer_name = entries.get('id').get().strip() # Get name from the 'name' entry widget

            if not customer_name:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập ID trước khi chụp ảnh.")
                return

            if not CAPTURE_AVAILABLE:
                 messagebox.showerror("Lỗi", "Chức năng chụp ảnh không khả dụng. Vui lòng kiểm tra file view/utils.py.")
                 return

            # Call the external capture function
            # This function should handle opening the camera, capturing, and saving
            print(f"[*] Attempting to capture image for customer: {customer_name}")
            success = capture_customer_image(customer_name) # Call the utility function

            if success:
                messagebox.showinfo("Thành công", f"Đã chụp và lưu ảnh cho khách hàng '{customer_name}'.")
            else:
                messagebox.showwarning("Thất bại", f"Không thể chụp hoặc lưu ảnh cho khách hàng '{customer_name}'. Vui lòng kiểm tra camera và quyền truy cập.")


        capture_btn = tk.Button(
            capture_button_frame, text="CHỤP ẢNH", command=on_capture_click,
            font=("Arial", 10, "bold"), bg=COLOR_ACCENT_TEAL, fg="white",
            activebackground="#117a8b", activeforeground="white",
            relief=tk.RAISED, padx=10, pady=5, cursor="hand2",
            state=tk.NORMAL if CAPTURE_AVAILABLE else tk.DISABLED # Enable/Disable based on utility availability
        )
        capture_btn.pack(expand=True) # Center the button


        def submit():
            new_customer_values = {}
            for field, widget in entries.items():
                 # Get value from Entry or Combobox
                 if isinstance(widget, (tk.Entry, ttk.Combobox)):
                      new_customer_values[field] = widget.get().strip() # Get value and strip whitespace
                 elif isinstance(widget, tk.Label) and field == 'id':
                      # Should not happen in add window, but for consistency
                      new_customer_values[field] = widget.cget("text").strip()


            # Validation
            # room_number is now validated by the Combobox selection, but check if it's empty
            required_fields = ['id', 'name', 'checkin_date', 'room_type', 'room_number']
            for field in required_fields:
                 if not new_customer_values.get(field):
                      messagebox.showerror("Lỗi", f"Trường '{field_title_map.get(field, field)}' không được để trống.")
                      return

            # Validate ID is numeric
            if not new_customer_values['id'].isdigit():
                messagebox.showerror("Lỗi", "ID phải là số.")
                return

            # Validate dates are in JPanel-MM-DD format if not empty
            for field in ['birthday', 'checkin_date']:
                 date_str = new_customer_values.get(field)
                 if date_str: # Only validate if not empty
                      try:
                           datetime.strptime(date_str, "%Y-%m-%d")
                      except ValueError:
                           messagebox.showerror("Lỗi định dạng ngày", f"Trường '{field_title_map.get(field, field)}' có định dạng không hợp lệ. Vui lòng dùng JPanel-MM-DD.")
                           return

            # Check if room number is already occupied (should be handled by dropdown, but double check)
            if new_customer_values.get('room_number') in self._get_occupied_room_numbers():
                 messagebox.showerror("Lỗi", f"Số phòng {new_customer_values.get('room_number')} đã có khách thuê.")
                 return


            # Create CustomerInfo object (passing JPanel-MM-DD strings or empty strings)
            new_customer_info = CustomerInfo(
                id=new_customer_values.get('id'),
                name=new_customer_values.get('name'),
                sex=new_customer_values.get('sex'),
                birthday=new_customer_values.get('birthday'), # Store as JPanel-MM-DD string
                national=new_customer_values.get('nationality'), # Use nationality
                country=new_customer_values.get('country'),
                checkin_date=new_customer_values.get('checkin_date'), # Store as JPanel-MM-DD string
                room_type=new_customer_values.get('room_type'),
                room_number=new_customer_values.get('room_number') # Store the selected room number string
            )

            # Add to customer_list and Treeview
            self.customer_list.append(new_customer_info)
            self.populate_treeview() # Repopulate to ensure data is fresh and sorted/ordered

            # Add to database
            try:
                self.db_conn.setCustomerToDatabase(new_customer_info) # Expects CustomerInfo with JPanel-MM-DD strings
                messagebox.showinfo("Thành công", "Đã thêm khách hàng mới.")
                # Call the refresh callback after adding a customer
                if self.refresh_room_management_callback:
                     self.refresh_room_management_callback()
                add_window.destroy()

            except Exception as e:
                messagebox.showerror("Lỗi Database", f"Không thể thêm khách hàng vào database:\n{e}")
                # Optional: remove the added customer from list/treeview if DB fails?
                # self.customer_list.pop()
                # self.populate_treeview()


        button_frame_bottom = tk.Frame(padding_frame, bg=COLOR_BACKGROUND_LIGHT)
        button_frame_bottom.grid(row=len(add_fields_and_titles) + 1, column=0, columnspan=3, pady=(5, 0)) # Placed below capture button frame
        button_frame_bottom.columnconfigure(0, weight=1)

        submit_btn = tk.Button(button_frame_bottom, text="LƯU KHÁCH HÀNG", command=submit,
                               font=("Arial", 10, "bold"), bg=COLOR_ACCENT_GREEN, fg="white",
                               activebackground="#1e7e34", activeforeground="white",
                               relief=tk.RAISED, padx=10, pady=5, cursor="hand2")
        submit_btn.pack(expand=True)


    # --- change_customer_information method (UPDATED for Room Number Dropdown and Callback) ---
    def change_customer_information(self):
        selected_item_id = self.tree.selection()
        if not selected_item_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn khách hàng để chỉnh sửa")
            return

        customer_id_to_edit = selected_item_id[0]
        selected_customer = None
        for customer in self.customer_list:
             # Compare string IDs
             if str(getattr(customer, 'id', None)) == customer_id_to_edit:
                 selected_customer = customer
                 break

        if not selected_customer:
             messagebox.showerror("Lỗi dữ liệu", f"Không tìm thấy dữ liệu khách hàng với ID {customer_id_to_edit} trong danh sách.")
             return

        edit_window = tk.Toplevel(self, bg=COLOR_BACKGROUND_LIGHT)
        edit_window.title(f"Chỉnh sửa thông tin: {getattr(selected_customer, 'name', '...')}")
        # Adjusted geometry
        edit_window.geometry("450x500")
        edit_window.transient(self.winfo_toplevel())
        edit_window.grab_set()

        padding_frame = tk.Frame(edit_window, bg=COLOR_BACKGROUND_LIGHT, padx=20, pady=20)
        padding_frame.pack(fill="both", expand=True)

        entries = {} # Use a dict to store Entry/Combobox/Label widgets

        edit_fields_and_titles = self.customer_fields
        field_title_map = {field: title for title, field in self.customer_fields}


        for i, (title, field) in enumerate(edit_fields_and_titles):
            tk.Label(padding_frame, text=title + ":", font=("Arial", 10), bg=COLOR_BACKGROUND_LIGHT, fg=COLOR_TEXT_DARK).grid(
                row=i, column=0, padx=5, pady=5, sticky="w"
            )

            # Get the current value from the selected customer object
            # Ensure dates are already YYYY-MM-DD strings from CustomerInfo
            current_value = getattr(selected_customer, field, None)
            current_value_str = str(current_value) if current_value is not None else "" # Ensure it's a string


            if field == "id":
                 # ID is read-only label
                 label_id_value = tk.Label(padding_frame, text=current_value_str, font=("Arial", 10, "bold"), bg=COLOR_BACKGROUND_LIGHT, fg=COLOR_TEXT_DARK)
                 label_id_value.grid(row=i, column=1, padx=5, pady=5, sticky="w")
                 entries[field] = label_id_value # Store label reference
            elif field == "sex":
                 combobox_items = ["Nam", "Nữ", "Khác"]
                 widget = ttk.Combobox(padding_frame, values=combobox_items, state="readonly", font=("Arial", 10))
                 widget.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
                 try:
                      # Set current value if it exists in the list
                      if current_value_str in combobox_items:
                          widget.set(current_value_str) # Use set() for Combobox
                      else:
                          widget.current(0) # Default to first if current value is invalid
                 except Exception:
                      widget.current(0) # Default on error
                 entries[field] = widget
            elif field == "room_type":
                 combobox_items = ["Thường", "VIP"]
                 widget = ttk.Combobox(padding_frame, values=combobox_items, state="readonly", font=("Arial", 10))
                 widget.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
                 try:
                      # Set current value if it exists in the list
                      if current_value_str in combobox_items:
                          widget.set(current_value_str) # Use set() for Combobox
                      else:
                          widget.current(0) # Default to first if current value is invalid
                 except Exception:
                      widget.current(0) # Default on error
                 entries[field] = widget
            elif field == "room_number":
                 # --- Room Number Combobox for Editing ---
                 # Get available rooms, and add the current room number to the list
                 available_rooms = self._get_available_room_numbers()
                 current_room = current_value_str # The customer's current room
                 # Add the current room to the available list if it's not already there
                 if current_room and current_room not in available_rooms:
                      room_options = sorted(available_rooms + [current_room], key=int)
                 else:
                      room_options = available_rooms # If current room is already available or empty

                 widget = ttk.Combobox(padding_frame, values=room_options, state="readonly", font=("Arial", 10))
                 widget.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
                 # Set the current room number as the default selection
                 if current_room in room_options:
                      widget.set(current_room) # Use set() for Combobox
                 elif room_options: # If current room is not an option, set to first available
                      widget.current(0)
                 entries[field] = widget # Store the Combobox widget
                 # --- End Room Number Combobox ---
            elif field in ["birthday", "checkin_date"]:
                 # Use an Entry (readonly) and a button for dates (Calendar outputs YYYY-MM-DD)
                 entry = tk.Entry(padding_frame, font=("Arial", 10), state="normal") # Can set state to normal to insert
                 entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
                 entry.insert(0, current_value_str) # Insert current YYYY-MM-DD string
                 entry.config(state="readonly") # Set back to readonly

                 entries[field] = entry # Store entry reference
                 date_button_command = self.create_calendar_command(padding_frame, entry, field)
                 date_button = tk.Button(padding_frame, text="Chọn ngày", command=date_button_command, font=("Arial", 8, "bold"),
                                         bg=COLOR_ACCENT_TEAL, fg="white", activebackground="#117a8b", activeforeground="white",
                                         relief=tk.RAISED, padx=5, pady=2, cursor="hand2")
                 date_button.grid(row=i, column=2, padx=(0, 5), pady=5, sticky="w")
                 # No need to store date_button in entries dict
            else:
                 # Standard Entry for other fields (name, nationality, country)
                 entry = tk.Entry(padding_frame, font=("Arial", 10))
                 entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
                 entry.insert(0, current_value_str) # Insert current value string
                 entries[field] = entry # Store the Entry widget

        padding_frame.columnconfigure(1, weight=1)


        def save_changes():
            updated_values = {}
            for field, widget in entries.items():
                 if isinstance(widget, (tk.Entry, ttk.Combobox)):
                      updated_values[field] = widget.get().strip() # Get value from Entry or Combobox
                 elif isinstance(widget, tk.Label) and field == 'id':
                      updated_values[field] = widget.cget("text").strip() # Get ID from label


            # Validation (similar to add customer)
            # room_number is now validated by the Combobox selection, but check if it's empty
            required_fields = ['id', 'name', 'checkin_date', 'room_type', 'room_number']
            for field in required_fields:
                 if not updated_values.get(field):
                      messagebox.showerror("Lỗi", f"Trường '{field_title_map.get(field, field)}' không được để trống.")
                      return

            # Validate dates are in YYYY-MM-DD format if not empty
            for field in ['birthday', 'checkin_date']:
                 date_str = updated_values.get(field)
                 if date_str: # Only validate if not empty
                      try:
                           datetime.strptime(date_str, "%Y-%m-%d")
                      except ValueError:
                           messagebox.showerror("Lỗi định dạng ngày", f"Trường '{field_title_map.get(field, field)}' có định dạng không hợp lệ. Vui lòng dùng YYYY-MM-DD.")
                           return

            # Check if the chosen room number is now occupied by a *different* customer
            chosen_room = updated_values.get('room_number')
            original_customer_id = updated_values.get('id')
            occupied_rooms_by_others = set()
            for customer in self.customer_list:
                 # Exclude the customer being edited
                 if str(getattr(customer, 'id', None)) != original_customer_id:
                      room_num = getattr(customer, 'room_number', None)
                      if room_num is not None and room_num != "":
                           occupied_rooms_by_others.add(str(room_num)) # Ensure string

            if chosen_room in occupied_rooms_by_others:
                 messagebox.showerror("Lỗi", f"Số phòng {chosen_room} đã có khách khác thuê.")
                 return


            # Find the index of the customer in the list
            original_customer_index = -1
            for i, customer in enumerate(self.customer_list):
                 # Compare string IDs
                 if str(getattr(customer, 'id', None)) == updated_values.get('id'):
                      original_customer_index = i
                      break

            if original_customer_index == -1:
                 messagebox.showerror("Lỗi dữ liệu", "Không tìm thấy khách hàng gốc trong danh sách.")
                 return

            # Create an updated CustomerInfo object (passing YYYY-MM-DD strings or empty strings)
            updated_customer_info = CustomerInfo(
                 id=updated_values.get('id'),
                 name=updated_values.get('name'),
                 sex=updated_values.get('sex'),
                 birthday=updated_values.get('birthday'), # Store as YYYY-MM-DD string
                 national=updated_values.get('national'), # Use nationality
                 country=updated_values.get('country'),
                 checkin_date=updated_values.get('checkin_date'), # Store as YYYY-MM-DD string
                 room_type=updated_values.get('room_type'),
                 room_number=updated_values.get('room_number') # Store the selected room number string
            )


            # Update the customer object in the list
            self.customer_list[original_customer_index] = updated_customer_info

            # Update Treeview
            self.populate_treeview() # Repopulate to ensure data is fresh


            # Update database
            try:
                self.db_conn.updateCustomerInDatabase(updated_customer_info) # Expects CustomerInfo with YYYY-MM-DD strings
                messagebox.showinfo("Thành công", f"Đã cập nhật thông tin khách hàng {updated_customer_info.id}.")
                edit_window.destroy()

                # Call the refresh callback after updating a customer
                if self.refresh_room_management_callback:
                     self.refresh_room_management_callback()

            except Exception as e:
                messagebox.showerror("Lỗi Database", f"Không thể cập nhật khách hàng trong database:\n{e}")
                # Optional: revert change in self.customer_list/treeview if DB fails?


        button_frame_bottom = tk.Frame(padding_frame, bg=COLOR_BACKGROUND_LIGHT)
        button_frame_bottom.grid(row=len(edit_fields_and_titles), column=0, columnspan=3, pady=10)
        button_frame_bottom.columnconfigure(0, weight=1)

        save_btn = tk.Button(button_frame_bottom, text="LƯU THAY ĐỔI", command=save_changes,
                             font=("Arial", 10, "bold"), bg=COLOR_ACCENT_GREEN, fg="white",
                             activebackground="#1e7e34", activeforeground="white",
                             relief=tk.RAISED, padx=10, pady=5, cursor="hand2")
        save_btn.pack(expand=True)


    # --- remove_customer method (Keep as is, uses ID string, added Callback) ---
    def remove_customer(self):
        selected_item_ids = self.tree.selection()
        if not selected_item_ids:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn khách hàng để xóa")
            return

        customer_ids_to_remove = selected_item_ids # iids are customer ID strings

        if messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc chắn muốn xóa {len(customer_ids_to_remove)} khách hàng đã chọn?"):
             removed_count = 0
             db_error_count = 0
             for customer_id in customer_ids_to_remove:
                 # Remove from local list
                 initial_list_length = len(self.customer_list)
                 # Compare string IDs
                 self.customer_list = [c for c in self.customer_list if str(getattr(c, 'id', None)) != customer_id]

                 if len(self.customer_list) < initial_list_length:
                      removed_count += 1
                      self.tree.delete(customer_id) # Remove from Treeview (using iid)

                      # Remove from database
                      try:
                         self.db_conn.removeCustomerFromDatabase(customer_id) # Expects string ID
                      except Exception as e:
                         print(f"Error removing customer {customer_id} from database: {e}")
                         db_error_count += 1

             if removed_count > 0:
                  messagebox.showinfo("Thành công", f"Đã xóa {removed_count} khách hàng.")
                  if db_error_count > 0:
                       messagebox.showwarning("Cảnh báo Database", f"Không thể xóa {db_error_count} khách hàng khỏi database.")

                  # Call the refresh callback after removing a customer
                  if self.refresh_room_management_callback:
                       self.refresh_room_management_callback()

             else:
                  messagebox.showwarning("Thông tin", "Không tìm thấy khách hàng phù hợp trong danh sách để xóa.")


    # --- sent_data_to_checkout method (UPDATED to pass CustomerInfo object) ---
    def sent_data_to_checkout(self):
        selected_item_id = self.tree.selection()

        if selected_item_id:
             # Find the customer object in the list using the selected iid (Customer ID string)
             customer_id_to_checkout = selected_item_id[0]
             customer_to_checkout = None
             for customer in self.customer_list:
                  # Compare string IDs
                  if str(getattr(customer, 'id', None)) == customer_id_to_checkout:
                      customer_to_checkout = customer
                      break

             if customer_to_checkout:
                  # Pass the CustomerInfo object directly to the controller
                  # The controller (App instance) should have an attribute to receive this object
                  # Assuming self.controller is the App instance and has a customer_information_temp attribute
                  try:
                      # Update the customer_information_temp object in the App
                      # Copy attributes from the selected customer object
                      self.controller.customer_information_temp.id = getattr(customer_to_checkout, 'id', None)
                      self.controller.customer_information_temp.name = getattr(customer_to_checkout, 'name', None)
                      self.controller.customer_information_temp.sex = getattr(customer_to_checkout, 'sex', None)
                      self.controller.customer_information_temp.birthday = getattr(customer_to_checkout, 'birthday', None) # Should be YYYY-MM-DD string or None
                      self.controller.customer_information_temp.national = getattr(customer_to_checkout, 'national', None) # Use nationality
                      self.controller.customer_information_temp.country = getattr(customer_to_checkout, 'country', None)
                      self.controller.customer_information_temp.checkin_date = getattr(customer_to_checkout, 'checkin_date', None) # Should be YYYY-MM-DD string or None
                      self.controller.customer_information_temp.room_type = getattr(customer_to_checkout, 'room_type', None)
                      self.controller.customer_information_temp.room_number = getattr(customer_to_checkout, 'room_number', None)

                      # print("Data sent to controller:", self.controller.customer_information_temp.__dict__) # Debugging

                      # Switch to the Checkout tab
                      self.show_tab("Thanh Toán")

                  except AttributeError as e:
                       messagebox.showerror("Lỗi dữ liệu", f"Đối tượng xử lý thanh toán không có thuộc tính cần thiết:\n{e}\nĐảm bảo controller (App) có thuộc tính customer_information_temp với các thuộc tính con.")
                  except Exception as e:
                       messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi chuẩn bị dữ liệu thanh toán: {e}")


             else:
                  messagebox.showwarning("Lỗi dữ liệu", f"Không tìm thấy dữ liệu khách hàng với ID {customer_id_to_checkout} trong danh sách.")

        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn khách hàng để thanh toán.")
