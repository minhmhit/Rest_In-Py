import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, date # Import date
# Assume CustomerInfo and DB_Connector are correctly imported
from customer_information import CustomerInfo
# from database import DB_Connector
from tkcalendar import Calendar
from database import DB_Connector

# Mock DB_Connector for testing if needed (copy from above)
# try:
# except ImportError:
#     print("Warning: database.py not found. Using mock DB_Connector.")
#     import mysql.connector # Need this import for the mock
#     class DB_Connector:
#         def __init__(self):
#             print("Mock DB_Connector initialized. No real connection.")
#             self.conn = None # Simulate no connection
#
#         def getCustomersFromDatabase(self):
#             print("Mock DB: getCustomersFromDatabase")
#             # Return mock data as CustomerInfo objects with YYYY-MM-DD strings
#             return [
#                  CustomerInfo("101", "Nguyen Van A", "Nam", "2000-01-15", "Viet Nam", "Ha Noi", "2024-04-20", "VIP", "301"),
#                  CustomerInfo("102", "Tran Thi B", "Nu", "1995-05-20", "Viet Nam", "HCM City", "2024-04-22", "Normal", "205"),
#                  CustomerInfo("103", "Le Van C", "Nam", "1998-11-11", "USA", "New York", "2024-04-25", "Normal", "201")
#             ]
#         # Add other mock methods (set, update, remove) that print actions
#         def setCustomerToDatabase(self, customer): print(f"Mock DB: Adding customer {customer.id}"); return True
#         def updateCustomerInDatabase(self, customer): print(f"Mock DB: Updating customer {customer.id}"); return True
#         def removeCustomerFromDatabase(self, customer_id): print(f"Mock DB: Removing customer {customer_id}"); return True
#         def closeBuffer(self): print("Mock DB: closeBuffer")
#         def is_connected(self): return False # Simulate not connected


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


class Customer(tk.Frame):
    def __init__(self, parent,show_tab,controller,customer_list,db_conn: DB_Connector):
        super().__init__(parent, bg=COLOR_BACKGROUND_LIGHT)
        self.show_tab = show_tab
        self.controller = controller # Assumed to be the object receiving customer data for checkout
        self.customer_list = customer_list # The list holding CustomerInfo objects
        self.db_conn = db_conn

        # Define fields for consistency
        self.customer_fields = [
            ("ID", "id"), ("Họ Tên", "name"), ("Giới Tính", "sex"), ("Ngày Sinh", "birthday"),
            ("Quốc Tịch", "national"), ("Quê Quán", "country"), ("Ngày Thuê Phòng", "checkin_date"),
            ("Loại Phòng", "room_type"), ("Số Phòng", "room_number"),
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
                "Quê Quán": 120, "Ngày Thuê Phòng": 100, "Loại Phòng": 80, "Số Phòng": 80
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
                        str(getattr(customer, 'national', '') if getattr(customer, 'national', None) is not None else ""),
                        str(getattr(customer, 'country', '') if getattr(customer, 'country', None) is not None else ""),
                        getattr(customer, 'checkin_date', ''), # May be datetime or string
                        str(getattr(customer, 'room_type', '') if getattr(customer, 'room_type', None) is not None else ""),
                        str(getattr(customer, 'room_number', '') if getattr(customer, 'room_number', None) is not None else ""),
                     )

                     # Ensure dates are YYYY-MM-DD strings for the Treeview
                     values_formatted = list(values)
                     for i in [3, 6]: # Index of birthday and checkin_date
                          if isinstance(values_formatted[i], (datetime, date)):
                               values_formatted[i] = values_formatted[i].strftime("%Y-%m-%d")
                          elif values_formatted[i] is None:
                               values_formatted[i] = "" # Ensure None becomes empty string

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
                   entry_widget.config(state="normal")
                   entry_widget.delete(0, tk.END)
                   entry_widget.insert(0, selected_date_str) # Insert YYYY-MM-DD string
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


    # --- open_add_customer method (UPDATED for YYYY-MM-DD handling) ---
    def open_add_customer(self):
        add_window = tk.Toplevel(self, bg=COLOR_BACKGROUND_LIGHT)
        add_window.title("Thêm khách hàng mới")
        add_window.geometry("400x450")
        add_window.transient(self.winfo_toplevel())
        add_window.grab_set()

        padding_frame = tk.Frame(add_window, bg=COLOR_BACKGROUND_LIGHT, padx=20, pady=20)
        padding_frame.pack(fill="both", expand=True)

        entries = {}

        # Use the fields defined in __init__ for consistency
        # Include ID field for 'Add' as it's manually entered here
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
            elif field == "room_type":
                 combobox_items = ["Thường", "VIP"]
                 widget = ttk.Combobox(padding_frame, values=combobox_items, state="readonly", font=("Arial", 10))
                 widget.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
                 widget.current(0)
            elif field in ["birthday", "checkin_date"]:
                 # Use an Entry (readonly) and a button for dates (Calendar outputs YYYY-MM-DD)
                 entry = tk.Entry(padding_frame, font=("Arial", 10), state="readonly")
                 entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
                 entries[field] = entry
                 date_button_command = self.create_calendar_command(padding_frame, entry, field)
                 date_button = tk.Button(padding_frame, text="Chọn ngày", command=date_button_command, font=("Arial", 8), padx=2, pady=2)
                 date_button.grid(row=i, column=2, padx=(0, 5), pady=5, sticky="w")
                 widget = entry # Store entry reference
            else:
                # Standard Entry for other fields (id, name, national, country, room_number)
                entry = tk.Entry(padding_frame, font=("Arial", 10))
                entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
                widget = entry

            entries[field] = widget # Store the widget (Entry or Combobox)


        padding_frame.columnconfigure(1, weight=1) # Entry/Combobox column expands


        def submit():
            new_customer_values = {}
            for field, widget in entries.items():
                new_customer_values[field] = widget.get().strip() # Get value and strip whitespace

            # Validation
            required_fields = ['id', 'name', 'checkin_date', 'room_type', 'room_number']
            for field in required_fields:
                 if not new_customer_values.get(field):
                     messagebox.showerror("Lỗi", f"Trường '{field_title_map.get(field, field)}' không được để trống.")
                     return

            # Validate ID is numeric
            if not new_customer_values['id'].isdigit():
                messagebox.showerror("Lỗi", "ID phải là số.")
                return

            # Validate dates are in YYYY-MM-DD format if not empty
            for field in ['birthday', 'checkin_date']:
                 date_str = new_customer_values.get(field)
                 if date_str: # Only validate if not empty
                      try:
                           datetime.strptime(date_str, "%Y-%m-%d")
                      except ValueError:
                           messagebox.showerror("Lỗi định dạng ngày", f"Trường '{field_title_map.get(field, field)}' có định dạng không hợp lệ. Vui lòng dùng YYYY-MM-DD.")
                           return

            # Create CustomerInfo object (passing YYYY-MM-DD strings or empty strings)
            new_customer_info = CustomerInfo(
                id=new_customer_values.get('id'),
                name=new_customer_values.get('name'),
                sex=new_customer_values.get('sex'),
                birthday=new_customer_values.get('birthday'), # Store as YYYY-MM-DD string
                national=new_customer_values.get('national'),
                country=new_customer_values.get('country'),
                checkin_date=new_customer_values.get('checkin_date'), # Store as YYYY-MM-DD string
                room_type=new_customer_values.get('room_type'),
                room_number=new_customer_values.get('room_number')
            )

            # Add to customer_list and Treeview
            self.customer_list.append(new_customer_info)
            self.populate_treeview() # Repopulate to ensure data is fresh and sorted/ordered

            # Add to database
            try:
                 self.db_conn.setCustomerToDatabase(new_customer_info) # Expects CustomerInfo with YYYY-MM-DD strings
                 messagebox.showinfo("Thành công", "Đã thêm khách hàng mới.")
                 add_window.destroy()
            except Exception as e:
                 messagebox.showerror("Lỗi Database", f"Không thể thêm khách hàng vào database:\n{e}")
                 # Optional: remove the added customer from list/treeview if DB fails?
                 # self.customer_list.pop()
                 # self.populate_treeview()


        button_frame_bottom = tk.Frame(padding_frame, bg=COLOR_BACKGROUND_LIGHT)
        button_frame_bottom.grid(row=len(add_fields_and_titles), column=0, columnspan=3, pady=10)
        button_frame_bottom.columnconfigure(0, weight=1)

        submit_btn = tk.Button(button_frame_bottom, text="LƯU KHÁCH HÀNG", command=submit,
                               font=("Arial", 10, "bold"), bg=COLOR_ACCENT_GREEN, fg="white",
                               activebackground="#1e7e34", activeforeground="white",
                               relief=tk.RAISED, padx=10, pady=5, cursor="hand2")
        submit_btn.pack(expand=True)


    # --- change_customer_information method (UPDATED for YYYY-MM-DD handling) ---
    def change_customer_information(self):
        selected_item_id = self.tree.selection()
        if not selected_item_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn khách hàng để chỉnh sửa")
            return

        customer_id_to_edit = selected_item_id[0]
        selected_customer = None
        for customer in self.customer_list:
             if str(customer.id) == customer_id_to_edit:
                 selected_customer = customer
                 break

        if not selected_customer:
             messagebox.showerror("Lỗi dữ liệu", f"Không tìm thấy dữ liệu khách hàng với ID {customer_id_to_edit} trong danh sách.")
             return

        edit_window = tk.Toplevel(self, bg=COLOR_BACKGROUND_LIGHT)
        edit_window.title(f"Chỉnh sửa thông tin: {selected_customer.name}")
        edit_window.geometry("400x450")
        edit_window.transient(self.winfo_toplevel())
        edit_window.grab_set()

        padding_frame = tk.Frame(edit_window, bg=COLOR_BACKGROUND_LIGHT, padx=20, pady=20)
        padding_frame.pack(fill="both", expand=True)

        entries = {} # Use a dict to store Entry/Combobox widgets

        edit_fields_and_titles = self.customer_fields
        field_title_map = {field: title for title, field in self.customer_fields}


        for i, (title, field) in enumerate(edit_fields_and_titles):
            tk.Label(padding_frame, text=title + ":", font=("Arial", 10), bg=COLOR_BACKGROUND_LIGHT, fg=COLOR_TEXT_DARK).grid(
                row=i, column=0, padx=5, pady=5, sticky="w"
            )

            # Get the current value from the selected customer object
            # Ensure dates are already YYYY-MM-DD strings from CustomerInfo
            current_value = getattr(selected_customer, field, "")
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
                     current_index = combobox_items.index(current_value_str)
                     widget.current(current_index)
                 except ValueError:
                     widget.current(0)
                 entries[field] = widget
            elif field == "room_type":
                 combobox_items = ["Thường", "VIP"]
                 widget = ttk.Combobox(padding_frame, values=combobox_items, state="readonly", font=("Arial", 10))
                 widget.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
                 try:
                     current_index = combobox_items.index(current_value_str)
                     widget.current(current_index)
                 except ValueError:
                     widget.current(0)
                 entries[field] = widget
            elif field in ["birthday", "checkin_date"]:
                 # Use an Entry (readonly) and a button for dates (Calendar outputs YYYY-MM-DD)
                 entry = tk.Entry(padding_frame, font=("Arial", 10), state="readonly")
                 entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
                 entry.insert(0, current_value_str) # Insert current YYYY-MM-DD string
                 entries[field] = entry
                 date_button_command = self.create_calendar_command(padding_frame, entry, field)
                 date_button = tk.Button(padding_frame, text="Chọn ngày", command=date_button_command, font=("Arial", 8), padx=2, pady=2)
                 date_button.grid(row=i, column=2, padx=(0, 5), pady=5, sticky="w")
            else:
                # Standard Entry for other fields (name, national, country, room_number)
                entry = tk.Entry(padding_frame, font=("Arial", 10))
                entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
                entry.insert(0, current_value_str) # Insert current value string
                entries[field] = entry

        padding_frame.columnconfigure(1, weight=1)


        def save_changes():
            updated_values = {}
            for field, widget in entries.items():
                if isinstance(widget, (tk.Entry, ttk.Combobox)):
                    updated_values[field] = widget.get().strip() # Get value
                elif isinstance(widget, tk.Label) and field == 'id':
                     updated_values[field] = widget.cget("text") # Get ID from label

            # Validation (similar to add customer)
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


            # Find the index of the customer in the list
            original_customer_index = -1
            for i, customer in enumerate(self.customer_list):
                 if str(customer.id) == updated_values.get('id'):
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
                 national=updated_values.get('national'),
                 country=updated_values.get('country'),
                 checkin_date=updated_values.get('checkin_date'), # Store as YYYY-MM-DD string
                 room_type=updated_values.get('room_type'),
                 room_number=updated_values.get('room_number')
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


    # --- remove_customer method (Keep as is, uses ID string) ---
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
                 self.customer_list = [c for c in self.customer_list if str(c.id) != customer_id]

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
                 if str(customer.id) == customer_id_to_checkout:
                     customer_to_checkout = customer
                     break

             if customer_to_checkout:
                 # Pass the CustomerInfo object directly to the controller
                 # The controller should have an attribute to receive this object
                 # Assuming self.controller is designed to receive a CustomerInfo object
                 # E.g., self.controller.current_customer = customer_to_checkout
                 # Or copy attributes as before, ensuring dates are YYYY-MM-DD strings
                 try:
                      # Copy attributes (assuming controller has them)
                      # Pass YYYY-MM-DD strings as stored in CustomerInfo
                      self.controller.id = customer_to_checkout.id
                      self.controller.name = customer_to_checkout.name
                      self.controller.sex = customer_to_checkout.sex
                      self.controller.birthday = customer_to_checkout.birthday
                      self.controller.national = customer_to_checkout.national
                      self.controller.country = customer_to_checkout.country
                      self.controller.checkin_date = customer_to_checkout.checkin_date # YYYY-MM-DD string
                      self.controller.room_type = customer_to_checkout.room_type
                      self.controller.room_number = customer_to_checkout.room_number

                      # print("Data sent to controller:", self.controller.__dict__) # Debugging

                      self.show_tab("Thanh Toán") # Switch to checkout tab

                 except AttributeError as e:
                      messagebox.showerror("Lỗi dữ liệu", f"Đối tượng xử lý thanh toán không có thuộc tính cần thiết:\n{e}\nĐảm bảo controller có các thuộc tính id, name, sex, birthday, national, country, checkin_date, room_type, room_number.")
                 except Exception as e:
                      messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi chuẩn bị dữ liệu thanh toán: {e}")


             else:
                 messagebox.showwarning("Lỗi dữ liệu", f"Không tìm thấy dữ liệu khách hàng với ID {customer_id_to_checkout} trong danh sách.")

        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn khách hàng để thanh toán.")
