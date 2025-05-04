from datetime import datetime, date
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar

# Assume DB_Connector and StaffInfo are imported
from view.db.database import DB_Connector
from view.models import StaffInfo

# --- Define colors --- (Keep consistent with other files)
COLOR_PRIMARY_BLUE = "#3B82F6"
COLOR_PRIMARY_BLUE_DARK = "#0056b3" # Darker blue for hover/active
COLOR_ACCENT_GREEN = "#28a745" # Green for success actions
COLOR_ACCENT_RED = "#dc3545" # Red for danger actions
COLOR_ACCENT_TEAL = "#17a2b8" # Teal for info/export actions
COLOR_BACKGROUND_LIGHT = "#eef2f7" # Light background for main frame
COLOR_FRAME_BACKGROUND = "#f8f9fa" # Slightly gray background for panels/frames
COLOR_MAIN_PANEL_BG = "#ffffff" # White background for main content areas
COLOR_TEXT_DARK = "#333333"    # Dark gray for primary text
COLOR_TEXT_MEDIUM = "#555555" # Medium gray for secondary text/frame titles
COLOR_BORDER_GRAY = "#cccccc" # Light gray border
COLOR_WHITE = "#ffffff" # White color
COLOR_TEXT_PLACEHOLDER = "gray" # Gray color for placeholder text

class StaffManagement(tk.Frame):
    def __init__(self, parent, staff_list, db_conn: DB_Connector):
        super().__init__(parent, bg=COLOR_BACKGROUND_LIGHT) # Use consistent background

        self.staff_list = staff_list # List of StaffInfo objects (in-memory)
        self.db_conn = db_conn

        # Define fields for consistency across Treeview and forms
        self.staff_fields = [
            ("ID", "id"), ("Họ Tên", "name"), ("Giới Tính", "sex"), ("Ngày Sinh", "birthday"),
            ("Chức vụ", "role"), ("Tên đăng nhập", "username"), ("Mật Khẩu", "password"), ("Phân quyền", "permissions")
        ]
        # Use the field titles as Treeview column headings
        self.treeview_columns = [title for title, field in self.staff_fields]
        # Create a mapping from field name to title for easier lookup in validation/messages
        self.field_name_to_title = {field: title for title, field in self.staff_fields}


        # --- Main Panel (LabelFrame for Treeview) ---
        self.mainPanel = tk.LabelFrame(
            self, text="DANH SÁCH NHÂN VIÊN", bg=COLOR_MAIN_PANEL_BG, fg=COLOR_TEXT_MEDIUM,
            font=("Arial", 14, "bold"), padx=15, pady=15, bd=1, relief=tk.GROOVE
        )
        self.mainPanel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10) # Use grid for main layout


        # --- Function Panel (Frame for Buttons) ---
        self.functionPanel = tk.Frame(self, bg=COLOR_FRAME_BACKGROUND, padx=10, pady=10) # Use consistent background
        self.functionPanel.grid(row=1, column=0, sticky="ew", padx=10, pady=10) # Use grid


        # Configure grid weights for the main frame
        self.rowconfigure(0, weight=1) # Main panel (treeview) takes most vertical space
        self.columnconfigure(0, weight=1) # Single column expands horizontally


        # --- Treeview Table ---
        style = ttk.Style()
        style.theme_use("default") # Use the default theme as a base
        # Configure Treeview heading style
        style.configure("StaffManagement.Treeview.Heading", font=("Arial", 10, "bold"), background=COLOR_PRIMARY_BLUE, foreground=COLOR_WHITE)
        # Configure Treeview row style
        style.configure("StaffManagement.Treeview", font=("Arial", 10), rowheight=25, fieldbackground=COLOR_MAIN_PANEL_BG, foreground=COLOR_TEXT_DARK)
        # Configure selected row style
        style.map("StaffManagement.Treeview", background=[("selected", COLOR_PRIMARY_BLUE)], foreground=[("selected", COLOR_WHITE)])


        self.tree = ttk.Treeview(
            self.mainPanel, columns=self.treeview_columns, show="headings", style="StaffManagement.Treeview" # Apply custom style
        )

        # Configure Treeview columns
        for col in self.treeview_columns:
            self.tree.heading(col, text=col, anchor="center") # Center header text
            # Set column widths (adjust as needed)
            width_map = {
                "ID": 60, "Họ Tên": 150, "Giới Tính": 80, "Ngày Sinh": 100,
                "Chức vụ": 100, "Tên đăng nhập": 120, "Mật Khẩu": 100, "Phân quyền": 100
            }
            self.tree.column(col, width=width_map.get(col, 100), anchor="center") # Center cell text


        # Scrollbar for Treeview
        scrollbar = ttk.Scrollbar(
            self.mainPanel, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Place Treeview and Scrollbar inside mainPanel using grid
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Configure grid weights for mainPanel (Treeview area)
        self.mainPanel.rowconfigure(0, weight=1) # Row containing treeview expands vertically
        self.mainPanel.columnconfigure(0, weight=1) # Column containing treeview expands horizontally


        # Populate Treeview initially
        self.populate_treeview()

        self.button_font = ("Arial", 10, "bold")
        self.button_pady = 8
        self.button_padx = 15
        # --- End FIX ---

        self.btn_add = tk.Button(
            self.functionPanel, text="Thêm nhân viên", font=self.button_font, # Use self.
            bg=COLOR_ACCENT_GREEN, fg=COLOR_WHITE, activebackground="#1e7e34", activeforeground=COLOR_WHITE,
            relief=tk.RAISED, padx=self.button_padx, pady=self.button_pady, cursor="hand2", # Use self.
            command=self.open_add_staff,
        )
        self.btn_delete = tk.Button(
            self.functionPanel, text="Xóa nhân viên", font=self.button_font, # Use self.
            bg=COLOR_ACCENT_RED, fg=COLOR_WHITE, activebackground="#c82333", activeforeground=COLOR_WHITE,
            relief=tk.RAISED, padx=self.button_padx, pady=self.button_pady, cursor="hand2", # Use self.
            command=self.remove_staff,
        )
        self.btn_edit = tk.Button(
            self.functionPanel, text="Chỉnh sửa thông tin", font=self.button_font, # Use self.
            bg=COLOR_ACCENT_TEAL, fg=COLOR_WHITE, activebackground="#117a8b", activeforeground=COLOR_WHITE,
            relief=tk.RAISED, padx=self.button_padx, pady=self.button_pady, cursor="hand2", # Use self.
            command=self.change_staff_information,
        )

        # Use pack for buttons within the functionPanel to distribute space
        self.btn_add.pack(side="left", expand=True, fill=tk.X, padx=5)
        self.btn_delete.pack(side="left", expand=True, fill=tk.X, padx=5)
        self.btn_edit.pack(side="left", expand=True, fill=tk.X, padx=5)


    # --- Helper to process raw date input (string or datetime) into datetime object ---
    def _process_date_input_to_datetime(self, raw_date_value):
         """Converts raw date input (string or datetime) to a datetime object or None."""
         if isinstance(raw_date_value, datetime):
              return raw_date_value # Already a datetime object
         elif isinstance(raw_date_value, date): # Handle date objects too
              return datetime.combine(raw_date_value, datetime.min.time()) # Convert date to datetime
         elif isinstance(raw_date_value, str) and raw_date_value.strip(): # Check for non-empty string after stripping whitespace
              try:
                   # Try parsing from YYYY-MM-DD string
                   return datetime.strptime(raw_date_value.strip(), "%Y-%m-%d") # Strip whitespace before parsing
              except ValueError:
                   print(f"Warning: Could not parse date string '{raw_date_value}'. Expected YYYY-MM-DD.")
                   return None
         else:
              return None # None, empty string, or other types are treated as no date


    # --- Helper to create calendar command closures (Outputs YYYY-MM-DD) ---
    def create_calendar_command(self, parent_window, entry_widget, field_title): # Renamed field_name to field_title for clarity with button text
         """Helper to create calendar command closures."""
         def open_calendar():
              def select_date():
                   # get_date() returns string in date_pattern format (yyyy-mm-dd)
                   selected_date_str = cal.get_date()
                   # Allow insertion programmatically
                   entry_widget.config(state="normal") # Temporarily set to normal to insert
                   entry_widget.delete(0, tk.END)
                   entry_widget.insert(0, selected_date_str) # Insert YYYY-MM-DD string
                   # No need to set back to readonly if using <Key> bind to prevent input
                   # entry_widget.config(state="readonly")
                   top.destroy()

              top = tk.Toplevel(parent_window)
              top.title(f"Chọn Ngày {field_title}") # Use the field title for the window title
              top.transient(parent_window.winfo_toplevel()) # Keep calendar on top of the pop-up window
              top.grab_set() # Block interaction with other windows

              # Calendar widget - Use YYYY-MM-DD date_pattern
              cal = Calendar(top, date_pattern="yyyy-mm-dd", selectmode='day', font=("Arial", 10))
              cal.pack(pady=10, padx=10)

              # Confirm button for calendar
              btn_select = tk.Button(top, text="Xác Nhận", command=select_date, font=("Arial", 10, "bold"),
                                    bg=COLOR_PRIMARY_BLUE, fg=COLOR_WHITE, activebackground=COLOR_PRIMARY_BLUE_DARK, activeforeground=COLOR_WHITE,
                                    relief=tk.RAISED, padx=10, pady=5, cursor="hand2")
              btn_select.pack(pady=5)

         return open_calendar


    # --- Helper to map field name to Vietnamese title (Optional but good) ---
    def get_field_title(self, field_name):
        return self.field_name_to_title.get(field_name, field_name)


    # --- populate_treeview method ---
    def populate_treeview(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Add data (expecting StaffInfo objects)
        for staff in self.staff_list:
            # Ideally, StaffInfo has get_values_for_treeview
            if hasattr(staff, 'get_values_for_treeview'):
                 values = staff.get_values_for_treeview()
                 # Ensure iid is a string and not empty
                 staff_id_str = str(getattr(staff, 'id', '')) if getattr(staff, 'id', None) is not None else f"temp_{id(staff)}" # Use id() for temp if no id
                 if staff_id_str.strip() == "": staff_id_str = f"temp_{id(staff)}" # Use temp iid if ID is empty string

                 # Ensure values are strings and format dates if needed (though get_values should handle this)
                 formatted_values = []
                 # Loop through defined fields to match order and format
                 for i, (title, field_name) in enumerate(self.staff_fields):
                      value = getattr(staff, field_name, "") # Get value by field name
                      if field_name == "birthday" and isinstance(value, (datetime, date)):
                           formatted_values.append(value.strftime("%Y-%m-%d"))
                      elif value is None:
                           formatted_values.append("") # Ensure None becomes empty string
                      else:
                           formatted_values.append(str(value) if value is not None else "") # Convert other values to string

                 self.tree.insert("", "end", iid=staff_id_str, values=formatted_values)

            else:
                 # Fallback logic if StaffInfo doesn't have the method (less ideal)
                 print(f"Warning: Staff object {staff} does not have get_values_for_treeview method. Using fallback.")
                 try:
                     # Attempt to get values directly based on common attributes
                     values = (
                        str(getattr(staff, 'id', '') if getattr(staff, 'id', None) is not None else ""),
                        str(getattr(staff, 'name', '') if getattr(staff, 'name', None) is not None else ""),
                        str(getattr(staff, 'sex', '') if getattr(staff, 'sex', None) is not None else ""),
                        getattr(staff, 'birthday', ''), # May be datetime, date, string, or None
                        str(getattr(staff, 'role', '') if getattr(staff, 'role', None) is not None else ""),
                        str(getattr(staff, 'username', '') if getattr(staff, 'username', None) is not None else ""),
                        str(getattr(staff, 'password', '') if getattr(staff, 'password', None) is not None else ""),
                        str(getattr(staff, 'permissions', '') if getattr(staff, 'permissions', None) is not None else ""),
                     )

                     # Ensure birthday is YYYY-MM-DD string for the Treeview
                     values_formatted = list(values)
                     birthday_index = 3 # Index of birthday field

                     raw_birthday_value = values_formatted[birthday_index]
                     birthday_display_str = ""
                     if raw_birthday_value is not None and raw_birthday_value != "":
                          if isinstance(raw_birthday_value, (datetime, date)):
                               birthday_display_str = raw_birthday_value.strftime("%Y-%m-%d")
                          elif isinstance(raw_birthday_value, str):
                               # Assume string is already YYYY-MM-DD or attempt parsing if necessary
                               try:
                                   datetime.strptime(raw_birthday_value, "%Y-%m-%d") # Validate format
                                   birthday_display_str = raw_birthday_value # Use the string if valid
                               except ValueError:
                                    birthday_display_str = "Invalid Date" # Indicate invalid string format

                     values_formatted[birthday_index] = birthday_display_str

                     # Ensure all values are strings for Treeview
                     final_tree_values = [str(v) if v is not None else "" for v in values_formatted]


                     staff_id_str = final_tree_values[0] if final_tree_values[0].strip() else f"temp_{id(staff)}" # Use ID or temp
                     self.tree.insert("", "end", iid=staff_id_str, values=final_tree_values)

                 except Exception as e:
                      print(f"Error inserting staff {staff} into treeview using fallback: {e}")


    # --- open_add_staff method (Refactored with consistent styling and logic) ---
    def open_add_staff(self):
        add_window = tk.Toplevel(self, bg=COLOR_BACKGROUND_LIGHT) # Consistent background
        add_window.title("Thêm nhân viên mới")
        add_window.geometry("400x500") # Adjust size as needed
        add_window.transient(self.winfo_toplevel()) # Keep window on top of parent
        add_window.grab_set() # Block interaction with parent

        padding_frame = tk.Frame(add_window, bg=COLOR_BACKGROUND_LIGHT, padx=20, pady=20) # Consistent padding frame
        padding_frame.pack(fill="both", expand=True)

        entries = {} # Use a dict to store Entry/Combobox widgets


        # Use self.staff_fields to create labels and entries
        for i, (title, field) in enumerate(self.staff_fields):
            tk.Label(padding_frame, text=title + ":", font=("Arial", 10), bg=COLOR_BACKGROUND_LIGHT, fg=COLOR_TEXT_DARK).grid(
                row=i, column=0, padx=5, pady=5, sticky="w"
            )

            if field == "sex": # Giới Tính
                 combobox_items = ["Nam", "Nữ", "Khác"]
                 widget = ttk.Combobox(padding_frame, values=combobox_items, state="readonly", font=("Arial", 10))
                 widget.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
                 widget.current(0) # Select first item by default
            elif field == "role": # Chức vụ
                 combobox_items = ["Quản Lí", "Nhân Viên", "Quản Trị Viên"] # Example roles
                 widget = ttk.Combobox(padding_frame, values=combobox_items, state="readonly", font=("Arial", 10))
                 widget.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
                 widget.current(0)
            elif field == "birthday": # Ngày Sinh
                 # Use an Entry (non-editable by keyboard) and a button for Calendar
                 entry = tk.Entry(padding_frame, font=("Arial", 10)) # No state="readonly" here
                 entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
                 # --- Bind <Key> event to prevent direct input ---
                 # This prevents user typing but allows programmatic insert
                 entry.bind("<Key>", lambda event: "break")
                 # --- End Bind ---
                 entries[field] = entry # Store entry reference
                 # Pass the field title for the calendar window title
                 date_button_command = self.create_calendar_command(padding_frame, entry, self.get_field_title(field))
                 date_button = tk.Button(padding_frame, text="Chọn ngày", command=date_button_command, font=("Arial", 8, "bold"), # Consistent button style
                                         bg=COLOR_ACCENT_TEAL, fg=COLOR_WHITE, activebackground="#117a8b", activeforeground=COLOR_WHITE,
                                         relief=tk.RAISED, padx=5, pady=2, cursor="hand2")
                 date_button.grid(row=i, column=2, padx=(0, 5), pady=5, sticky="w")
                 widget = entry # Ensure 'widget' variable is set for entries[field] assignment

            elif field == "password": # Mật khẩu - Use show="*"
                 entry = tk.Entry(padding_frame, font=("Arial", 10), show="*")
                 entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
                 widget = entry
            else:
                # Standard Entry for other fields (id, name, username, permissions)
                entry = tk.Entry(padding_frame, font=("Arial", 10))
                entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
                widget = entry

            entries[field] = widget # Store the widget (Entry or Combobox)


        # Configure column weights for grid
        padding_frame.columnconfigure(1, weight=1) # Entry/Combobox column expands
        # Column 0 (label) and Column 2 (button) take minimal space


        def submit():
            new_staff_values = {}
            for field, widget in entries.items():
                 # Get value from widget, handle Comboboxes vs Entries
                 if isinstance(widget, (tk.Entry, ttk.Combobox)):
                      new_staff_values[field] = widget.get().strip() # Get value and strip whitespace
                 elif isinstance(widget, tk.Label) and field == 'id': # Should not happen in add form, but safe check
                      new_staff_values[field] = widget.cget("text").strip()


            # Validation
            required_fields = ['id', 'name', 'username', 'password', 'role'] # Example required fields
            # Use the instance's field_name_to_title map
            for field in required_fields:
                 if not new_staff_values.get(field): # Check if value is empty string or None
                     messagebox.showerror("Lỗi", f"Trường '{self.get_field_title(field)}' không được để trống.")
                     return

            # Validate ID is numeric (assuming ID should be numeric)
            staff_id = new_staff_values.get('id', '')
            if not staff_id.isdigit():
                messagebox.showerror("Lỗi", "ID phải là số.")
                return

            # Validate birthday format if not empty
            birthday_str = new_staff_values.get('birthday')
            if birthday_str:
                 try:
                      datetime.strptime(birthday_str, "%Y-%m-%d") # Just validate format
                 except ValueError:
                      messagebox.showerror("Lỗi định dạng ngày", f"Ngày sinh có định dạng không hợp lệ. Vui lòng dùng YYYY-MM-DD.")
                      return

            # Check if ID already exists in the current list
            if any(str(staff.id) == staff_id for staff in self.staff_list):
                 messagebox.showerror("Lỗi ID", f"ID nhân viên '{staff_id}' đã tồn tại.")
                 return


            # Create StaffInfo object (assuming it takes YYYY-MM-DD string for birthday)
            # Ensure attributes passed match StaffInfo constructor
            new_staff_info = StaffInfo(
                id=new_staff_values.get('id'),
                name=new_staff_values.get('name'),
                sex=new_staff_values.get('sex'),
                birthday=new_staff_values.get('birthday'), # Pass YYYY-MM-DD string or ""
                role=new_staff_values.get('role'),
                username=new_staff_values.get('username'),
                password=new_staff_values.get('password'),
                permissions=new_staff_values.get('permissions')
            )

            # Add to staff_list (in-memory list)
            self.staff_list.append(new_staff_info)

            # Update Treeview
            # self.populate_treeview() # Repopulating is simpler than inserting individually
            # Or insert individually for efficiency and control over position
            # Let's populate_treeview for consistency with Customer
            self.populate_treeview()


            # Add to database
            try:
                 # Expects StaffInfo object with string IDs and YYYY-MM-DD birthday string
                 self.db_conn.setStaffToDatabase(new_staff_info)
                 messagebox.showinfo("Thành công", "Đã thêm nhân viên mới.")
                 add_window.destroy()
            except Exception as e:
                 messagebox.showerror("Lỗi Database", f"Không thể thêm nhân viên vào database:\n{e}")
                 # Optional: Remove the added staff from list/treeview if DB insertion fails
                 # Find and remove the staff by ID from the list
                 # self.staff_list = [s for s in self.staff_list if str(s.id) != staff_id]
                 # self.tree.delete(staff_id) # Remove from treeview


        # --- Submit Button ---
        button_font_submit = ("Arial", 10, "bold") # Define locally or use instance attribute
        button_pady_submit = 8
        button_padx_submit = 15

        button_frame_bottom = tk.Frame(padding_frame, bg=COLOR_BACKGROUND_LIGHT)
        button_frame_bottom.grid(row=len(self.staff_fields), column=0, columnspan=3, pady=10) # Place below fields
        button_frame_bottom.columnconfigure(0, weight=1)

        # --- FIX NameError: Use self.button_font, self.button_padx, self.button_pady ---
        submit_btn = tk.Button(button_frame_bottom, text="LƯU NHÂN VIÊN", command=submit,
                               font=self.button_font, bg=COLOR_ACCENT_GREEN, fg=COLOR_WHITE,
                               activebackground="#1e7e34", activeforeground=COLOR_WHITE,
                               relief=tk.RAISED, padx=self.button_padx, pady=self.button_pady, cursor="hand2")
        # --- End FIX ---
        submit_btn.pack(expand=True, fill=tk.X)


    # --- change_staff_information method (Refactored with consistent styling and logic) ---
    def change_staff_information(self):
        selected_item_ids = self.tree.selection() # Selection returns a tuple of iids
        if not selected_item_ids: # Check if any item is selected
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn nhân viên để chỉnh sửa")
            return
        # Assuming single selection, get the iid of the first selected item
        selected_item_id = selected_item_ids[0]


        # Find the StaffInfo object in the list using the selected iid (Staff ID string)
        staff_id_to_edit = selected_item_id
        selected_staff = None
        for staff in self.staff_list:
             if str(staff.id) == staff_id_to_edit:
                 selected_staff = staff
                 break

        if not selected_staff:
             messagebox.showerror("Lỗi dữ liệu", f"Không tìm thấy dữ liệu nhân viên với ID {staff_id_to_edit} trong danh sách.")
             return


        edit_window = tk.Toplevel(self, bg=COLOR_BACKGROUND_LIGHT) # Consistent background
        edit_window.title(f"Chỉnh sửa thông tin: {selected_staff.name}")
        edit_window.geometry("400x500") # Adjust size
        edit_window.transient(self.winfo_toplevel()) # Keep window on top
        edit_window.grab_set() # Block interaction with parent

        padding_frame = tk.Frame(edit_window, bg=COLOR_BACKGROUND_LIGHT, padx=20, pady=20) # Consistent padding frame
        padding_frame.pack(fill="both", expand=True)

        entries = {} # Use a dict to store Entry/Combobox widgets


        # Use self.staff_fields to create labels and entries/comboboxes
        for i, (title, field) in enumerate(self.staff_fields):
            tk.Label(padding_frame, text=title + ":", font=("Arial", 10), bg=COLOR_BACKGROUND_LIGHT, fg=COLOR_TEXT_DARK).grid(
                row=i, column=0, padx=5, pady=5, sticky="w"
            )

            # --- Get and format the current value from the selected staff object ---
            # Get the value from the found StaffInfo object, defaulting to None
            raw_value = getattr(selected_staff, field, None)

            current_value_str = "" # Default display string is empty

            if field == "birthday": # Handle birthday specifically
                 # For birthday, if the raw value exists (non-None, non-empty),
                 # format it into the YYYY-MM-DD string for display.
                 if raw_value is not None and str(raw_value).strip() != "": # Check after converting to string and stripping
                     if isinstance(raw_value, str):
                          # If it's already a string, assume YYYY-MM-DD and use it
                          current_value_str = raw_value.strip() # Strip whitespace just in case
                     elif isinstance(raw_value, (datetime, date)):
                          # If it's a datetime/date object, format it to YYYY-MM-DD string
                          current_value_str = raw_value.strftime("%Y-%m-%d")
                 # Else: raw_value is None or "", current_value_str remains ""

            else:
                 # For other fields (id, name, sex, role, username, password, permissions)
                 # Convert value to string, handling None
                 current_value_str = str(raw_value) if raw_value is not None else ""
                 # For ID, ensure it's treated as string and not empty for Treeview iid
                 if field == "id" and current_value_str.strip() == "":
                      current_value_str = f"temp_{id(selected_staff)}" # Use a temp ID for display if actual ID is missing


            # --- End Get and format ---


            if field == "id": # ID field (read-only label)
                 label_id_value = tk.Label(padding_frame, text=current_value_str, font=("Arial", 10, "bold"), bg=COLOR_MAIN_PANEL_BG, fg=COLOR_TEXT_DARK)
                 label_id_value.grid(row=i, column=1, padx=5, pady=5, sticky="w")
                 entries[field] = label_id_value # Store label reference
                 # ID label is not editable, no need to bind <Key>

            elif field == "sex": # Giới Tính
                 combobox_items = ["Nam", "Nữ", "Khác"]
                 widget = ttk.Combobox(padding_frame, values=combobox_items, state="readonly", font=("Arial", 10))
                 widget.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
                 try:
                     # Select current value in combobox
                     current_index = combobox_items.index(current_value_str)
                     widget.current(current_index)
                 except ValueError:
                     widget.current(0) # Default if current value not found
                 entries[field] = widget

            elif field == "role": # Chức vụ
                 combobox_items = ["Manager", "Staff", "Admin"] # Example roles (adjust as needed)
                 widget = ttk.Combobox(padding_frame, values=combobox_items, state="readonly", font=("Arial", 10))
                 widget.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
                 try:
                     # Select current value in combobox
                     current_index = combobox_items.index(current_value_str)
                     widget.current(current_index)
                 except ValueError:
                     widget.current(0) # Default if current value not found
                 entries[field] = widget

            elif field == "birthday": # Ngày Sinh
                 # Use an Entry (non-editable by keyboard) and a button for Calendar
                 entry = tk.Entry(padding_frame, font=("Arial", 10)) # No state="readonly" here
                 entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
                 # --- Bind <Key> event to prevent direct input ---
                 entry.bind("<Key>", lambda event: "break")
                 # --- End Bind ---

                 # --- Dòng CHÈN GIÁ TRỊ vào Entry ngày sinh ---
                 # Insert the current date string (YYYY-MM-DD or "")
                 entry.insert(0, current_value_str)
                 # --- End INSERT ---

                 entries[field] = entry # Store entry reference
                 # Pass the field title for the calendar window title
                 date_button_command = self.create_calendar_command(padding_frame, entry, self.get_field_title(field))
                 date_button = tk.Button(padding_frame, text="Chọn ngày", command=date_button_command, font=("Arial", 8, "bold"),
                                         bg=COLOR_ACCENT_TEAL, fg=COLOR_WHITE, activebackground="#117a8b", activeforeground=COLOR_WHITE,
                                         relief=tk.RAISED, padx=5, pady=2, cursor="hand2")
                 date_button.grid(row=i, column=2, padx=(0, 5), pady=5, sticky="w")

            elif field == "password": # Mật khẩu - Use show="*"
                 entry = tk.Entry(padding_frame, font=("Arial", 10), show="*")
                 entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
                 entry.insert(0, current_value_str) # Insert current value
                 entries[field] = entry

            else:
                # Standard Entry for other fields (name, username, permissions)
                entry = tk.Entry(padding_frame, font=("Arial", 10))
                entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
                entry.insert(0, current_value_str) # Insert current value
                entries[field] = entry


        # Configure column weights for grid
        padding_frame.columnconfigure(1, weight=1) # Entry/Combobox column expands
        # Column 0 (label) and Column 2 (button) take minimal space


        def save_changes():
            updated_values = {}
            for field, widget in entries.items():
                 # Get value from widget, handle Entry, Combobox, and Label (for ID)
                 if isinstance(widget, (tk.Entry, ttk.Combobox)):
                      updated_values[field] = widget.get().strip()
                 elif isinstance(widget, tk.Label) and field == 'id':
                      updated_values[field] = widget.cget("text").strip() # Get ID from label


            # Validation
            required_fields = ['id', 'name', 'username', 'password', 'role'] # Example required fields
            # Use the instance's field_name_to_title map
            for field in required_fields:
                 if not updated_values.get(field): # Check if value is empty string or None
                     messagebox.showerror("Lỗi", f"Trường '{self.get_field_title(field)}' không được để trống.")
                     return

            # Validate birthday format if not empty
            birthday_str = updated_values.get('birthday')
            if birthday_str:
                 try:
                      datetime.strptime(birthday_str, "%Y-%m-%d") # Just validate format
                 except ValueError:
                      messagebox.showerror("Lỗi định dạng ngày", f"Ngày sinh có định dạng không hợp lệ. Vui lòng dùng YYYY-MM-DD.")
                      return

            # Find the index of the staff object in the local list using the ID from the form
            original_staff_index = -1
            staff_id_from_form = updated_values.get('id') # Get ID from the form's value
            for i, staff in enumerate(self.staff_list):
                 if str(staff.id) == staff_id_from_form: # Compare as strings
                     original_staff_index = i
                     break

            if original_staff_index == -1:
                 messagebox.showerror("Lỗi dữ liệu", "Không tìm thấy nhân viên gốc trong danh sách.")
                 return

            # Create an updated StaffInfo object
            updated_staff_info = StaffInfo(
                 id=updated_values.get('id'),
                 name=updated_values.get('name'),
                 sex=updated_values.get('sex'),
                 birthday=updated_values.get('birthday'), # Pass YYYY-MM-DD string or ""
                 role=updated_values.get('role'),
                 username=updated_values.get('username'),
                 password=updated_values.get('password'),
                 permissions=updated_values.get('permissions')
            )


            # Update the staff object in the local list by replacing the old object
            self.staff_list[original_staff_index] = updated_staff_info

            # Update Treeview - Repopulate to ensure data is fresh and sorted/ordered if needed
            self.populate_treeview()


            # Update database
            try:
                 # Expects StaffInfo object with string ID and YYYY-MM-DD birthday string
                 self.db_conn.updateStaffInDatabase(updated_staff_info)
                 messagebox.showinfo("Thành công", f"Đã cập nhật thông tin nhân viên {updated_staff_info.id}.")
                 edit_window.destroy()
            except Exception as e:
                 messagebox.showerror("Lỗi Database", f"Không thể cập nhật nhân viên trong database:\n{e}")
                 # Optional: Revert change in self.staff_list/Treeview if DB fails?
                 # This would involve finding the updated_staff_info in the list (should be at original_staff_index)
                 # and replacing it back with the original_staff object found at the beginning of change_staff_information


        # --- Save Button ---
        button_frame_bottom = tk.Frame(padding_frame, bg=COLOR_BACKGROUND_LIGHT)
        button_frame_bottom.grid(row=len(self.staff_fields), column=0, columnspan=3, pady=10) # Place below fields
        button_frame_bottom.columnconfigure(0, weight=1)

        # --- FIX NameError: Use self.button_font, self.button_padx, self.button_pady ---
        save_btn = tk.Button(button_frame_bottom, text="LƯU THAY ĐỔI", command=save_changes,
                            font=self.button_font, bg=COLOR_ACCENT_GREEN, fg=COLOR_WHITE,
                            activebackground="#1e7e34", activeforeground=COLOR_WHITE,
                            relief=tk.RAISED, padx=self.button_padx, pady=self.button_pady, cursor="hand2")
        # --- End FIX ---
        save_btn.pack(expand=True, fill=tk.X)


    # --- remove_staff method (Refactored with consistent styling and data handling) ---
    def remove_staff(self):
        selected_item_ids = self.tree.selection() # Selection returns a tuple of iids
        if not selected_item_ids: # Check if any item is selected
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn nhân viên để xóa")
            return

        # Assuming iids are the staff IDs (strings)
        staff_ids_to_remove = selected_item_ids

        if messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc chắn muốn xóa {len(staff_ids_to_remove)} nhân viên đã chọn?"):
             removed_count = 0
             db_error_count = 0
             for staff_id in staff_ids_to_remove:
                 # Remove from local list by ID
                 initial_list_length = len(self.staff_list)
                 self.staff_list = [s for s in self.staff_list if str(s.id) != staff_id] # Compare as strings

                 if len(self.staff_list) < initial_list_length:
                      # Successfully removed from list
                      removed_count += 1
                      self.tree.delete(staff_id) # Remove from Treeview by iid (Staff ID string)

                      # Remove from database
                      try:
                          self.db_conn.removeStaffFromDatabase(staff_id) # Expects string ID
                      except Exception as e:
                          print(f"Error removing staff {staff_id} from database: {e}")
                          db_error_count += 1 # Count DB errors

             # Show feedback to the user
             if removed_count > 0:
                  messagebox.showinfo("Thành công", f"Đã xóa {removed_count} nhân viên.")
                  if db_error_count > 0:
                       messagebox.showwarning("Cảnh báo Database", f"Không thể xóa {db_error_count} nhân viên khỏi database.")
             else:
                 # This case happens if the selected ID wasn't found in the local list
                 messagebox.showwarning("Thông tin", "Không tìm thấy nhân viên phù hợp trong danh sách để xóa.")
