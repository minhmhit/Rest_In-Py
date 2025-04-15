import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from customer_information import CustomerInfo

from tkcalendar import Calendar

from database import DB_Connector

color1 = "#3B82F6"

class Customer(tk.Frame):
    def __init__(self, parent,show_tab,controller,customer_list,db_conn: DB_Connector):
        super().__init__(parent, bg="#F5F5F5")
        self.show_tab = show_tab
        self.controller = controller
        self.customer_list = customer_list
        self.db_conn = db_conn

        # Create panels
        self.mainPanel = tk.LabelFrame(
            self, text="Danh sách khách hàng", bg="white", font=("Arial", 12, "bold")
        )
        self.functionPanel = tk.LabelFrame(self, bg="lightgray")

        self.mainPanel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.functionPanel.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Customer list (Treeview)
        columns = (
            "ID",
            "Họ Tên",
            "Giới Tính",
            "Ngày Sinh",
            "Quốc Tịch",
            "Quê Quán",
            "Ngày Thuê Phòng",
            "Loại Phòng",
            "Số Phòng",
        )
        self.tree = ttk.Treeview(
            self.mainPanel, columns=columns, show="headings"
        )

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")

        # add data to tree
        for customer in self.customer_list:
            self.tree.insert("", "end", iid=customer.id, values=(
                customer.id,
                customer.name,
                customer.sex,
                customer.birthday,
                customer.national,
                customer.country,
                customer.checkin_date,
                customer.room_type,
                customer.room_number,
            ))

        scrollbar = ttk.Scrollbar(
            self.mainPanel, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.mainPanel.rowconfigure(0, weight=1)
        self.mainPanel.columnconfigure(0, weight=1)

        # buttons
        self.addCustomer = tk.Button(
            self.functionPanel,
            text="Thêm khách hàng",
            bg=color1,
            fg="white",
            command=self.open_add_customer,
        )
        self.removeCustomer = tk.Button(
            self.functionPanel,
            text="Xóa khách hàng",
            bg=color1,
            fg="white",
            command=self.remove_customer,
        )
        self.changeInformation = tk.Button(
            self.functionPanel,
            text="Chỉnh sửa thông tin khách hàng",
            bg=color1,
            fg="white",
            command=self.change_customer_information,
        )
        self.customerPayment = tk.Button(
            self.functionPanel,
            text="Thanh toán tiền phòng",
            bg=color1,
            fg="white",
            command=self.sent_data_to_checkout,
        )

        self.addCustomer.pack(side="left", expand=True, padx=10, pady=5)
        self.removeCustomer.pack(side="left", expand=True, padx=10, pady=5)
        self.changeInformation.pack(side="right",expand=True,padx=10,pady=5)
        self.customerPayment.pack(side="right",expand=True,padx=10,pady=5)

    def open_add_customer(self):
        add_window = tk.Toplevel(self)
        add_window.title("Thêm khách hàng")
        add_window.geometry("300x400")

        fields = [
            "ID",
            "Họ Tên",
            "Giới Tính",
            "Ngày Sinh",
            "Quốc Tịch",
            "Quê Quán",
            "Ngày Thuê Phòng", 
            "Loại Phòng",
            "Số Phòng"
        ]
        entries = {}

        for i, field in enumerate(fields):
            tk.Label(add_window, text=field).grid(
                row=i, column=0, padx=5, pady=5
            )
            entry = tk.Entry(add_window)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[field] = entry

        def prevent_keyboard_input(event):
            return "break"  # Prevents the default key press action

        # bind readonly event Entry
        entries["Ngày Sinh"].bind("<Key>", prevent_keyboard_input) # bind event
        entries["Ngày Sinh"].config(state="readonly")
        entries["Ngày Thuê Phòng"].bind("<Key>", prevent_keyboard_input) # bind event
        entries["Ngày Thuê Phòng"].config(state="readonly")

        def open_rent_date_calendar():
            def select_date():
                selected_date_str = cal.get_date()

                # No need to parse and reformat if get_date() returns the correct string format
                entries["Ngày Thuê Phòng"].config(state="normal") # Allow insertion
                entries["Ngày Thuê Phòng"].delete(0, tk.END)
                entries["Ngày Thuê Phòng"].insert(0, selected_date_str) # Insert the YYYY-MM-DD string
                entries["Ngày Thuê Phòng"].config(state="readonly") # Set back to readonly
                top.destroy()

            top = tk.Toplevel(add_window) # Make it child of add_window
            top.title("Chọn Ngày")

            # Calendar widget - CHANGED date_pattern
            cal = Calendar(top, date_pattern="yyyy-mm-dd", selectmode='day')
            cal.pack(pady=10)

            # Confirm button
            btn_select = tk.Button(top, text="Confirm", command=select_date)
            btn_select.pack(pady=5)

        def open_birthday_calendar():
            def select_date():
                selected_date_str = cal.get_date()
                entries["Ngày Sinh"].config(state="normal") # Allow insertion
                entries["Ngày Sinh"].delete(0, tk.END)
                entries["Ngày Sinh"].insert(0, selected_date_str) # Insert the YYYY-MM-DD string
                entries["Ngày Sinh"].config(state="readonly") # Set back to readonly
                top.destroy()

            top = tk.Toplevel(add_window) # Make it child of add_window
            top.title("Chọn Ngày")

            # Calendar widget - CHANGED date_pattern
            cal = Calendar(top, date_pattern="yyyy-mm-dd", selectmode='day')
            cal.pack(pady=10)

            # Confirm button
            btn_select = tk.Button(top, text="Xác Nhận", command=select_date)
            btn_select.pack(pady=5)

        # choose date button for "Ngày Sinh"
        choose_birthday = tk.Button(add_window, text="...", command=open_birthday_calendar)
        choose_birthday.grid(row=3 ,column=2, padx=(0, 5), pady=5, sticky="w")

        # Choose date button for "Ngày Thuê Phòng"
        choose_rent_date = tk.Button(add_window, text="...", command=open_rent_date_calendar) 
        choose_rent_date.grid(row=6, column=2, padx=(0, 5), pady=5, sticky="w") # align right of entry

        # Room type combobox
        combobox_items = ["Thường", "VIP"]
        combobox = ttk.Combobox(add_window, values=combobox_items, state="readonly") # Readonly is better
        combobox.current(0) # default data

        # Replace the placeholder Entry for "Loại Phòng"
        entries["Loại Phòng"].grid_forget() # Remove the temporary entry
        combobox.grid(row=7, column=1, padx=5, pady=5, sticky="ew")
        entries["Loại Phòng"] = combobox # Store combobox in entries dict

        def submit():
            new_customer_values = []
            for field in fields:
                widget = entries[field]
                value = widget.get()
                # Basic validation (optional but recommended)
                if field == "ID" and not value.isdigit():
                     messagebox.showerror("Lỗi", "ID phải là số.")
                     return
                if not value and field not in ["Giới Tính","Ngày Sinh","Quốc Tịch","Quê Quán"]: # Example required fields
                     messagebox.showerror("Lỗi", f"Trường '{field}' không được để trống.")
                     return
                new_customer_values.append(value)

            try:
                # convert birthday and check-in date to datetime objects
                birthday_dt_fm = datetime.strptime(new_customer_values[3], "%Y-%m-%d")
                checkin_dt_fm = datetime.strptime(new_customer_values[6], "%Y-%m-%d")
            except ValueError as e:
                messagebox.showerror("Lỗi định dạng ngày", f"Vui lòng nhập ngày theo định dạng yyyy-mm-dd.\nChi tiết: {e}")
                return

            new_customer_info = CustomerInfo(
                id=new_customer_values[0],
                name=new_customer_values[1],
                sex=new_customer_values[2],
                birthday=birthday_dt_fm,
                national=new_customer_values[4],
                country=new_customer_values[5],
                checkin_date=checkin_dt_fm,
                room_type=new_customer_values[7],
                room_number=new_customer_values[8]
            )

            # Add the CustomerInfo object to customer_list
            self.customer_list.append(new_customer_info)

            # Add to Treeview (using attributes of the object)
            last_insert_customer = self.tree.insert("", "end", iid=new_customer_info.id, values=(
                new_customer_info.id,
                new_customer_info.name,
                new_customer_info.sex,
                new_customer_info.birthday.strftime("%Y-%m-%d"),
                new_customer_info.national,
                new_customer_info.country,
                new_customer_info.checkin_date.strftime("%Y-%m-%d"),
                new_customer_info.room_type,
                new_customer_info.room_number,
            ))
            self.tree.move(last_insert_customer, "", 0)

            add_window.destroy()

            # add new customer to database 
            self.db_conn.setCustomerToDatabase(new_customer_info)

        submit_btn = tk.Button(add_window, text="Lưu", command=submit, bg=color1, fg="white")
        submit_btn.grid(row=len(fields), column=0, columnspan=3, pady=10)

    def change_customer_information(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn khách hàng để chỉnh sửa")
            return

        item_values = self.tree.item(selected_item[0])['values']
        edit_window = tk.Toplevel(self)
        edit_window.title("Chỉnh sửa thông tin khách hàng")
        edit_window.geometry("350x400")

        fields = [
            "ID",
            "Họ Tên",
            "Giới Tính",
            "Ngày Sinh",
            "Quốc Tịch",
            "Quê Quán",
            "Ngày Thuê Phòng",
            "Loại Phòng",
            "Số Phòng"
        ]
        entries = {}

        for i, (field, value) in enumerate(zip(fields, item_values)):
            tk.Label(edit_window, text=field).grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(edit_window)
            entry.insert(0, value)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[field] = entry

        def prevent_keyboard_input(event):
            return "break"  # Prevents the default key press action

        # bind readonly event Entry
        entries["ID"].bind("<Key>", prevent_keyboard_input) # bind event
        entries["ID"].config(state="readonly")
        entries["Ngày Sinh"].bind("<Key>", prevent_keyboard_input) # bind event
        entries["Ngày Sinh"].config(state="readonly")
        entries["Ngày Thuê Phòng"].bind("<Key>", prevent_keyboard_input) # bind event
        entries["Ngày Thuê Phòng"].config(state="readonly")

        def open_rent_date_calendar():
            def select_date():
                selected_date_str = cal.get_date()

                # No need to parse and reformat if get_date() returns the correct string format
                entries["Ngày Thuê Phòng"].config(state="normal") # Allow insertion
                entries["Ngày Thuê Phòng"].delete(0, tk.END)
                entries["Ngày Thuê Phòng"].insert(0, selected_date_str) # Insert the YYYY-MM-DD string
                entries["Ngày Thuê Phòng"].config(state="readonly") # Set back to readonly
                top.destroy()

            top = tk.Toplevel(edit_window) # Make it child of add_window
            top.title("Chọn Ngày")

            # Calendar widget - CHANGED date_pattern
            cal = Calendar(top, date_pattern="yyyy-mm-dd", selectmode='day')
            cal.pack(pady=10)

            # Confirm button
            btn_select = tk.Button(top, text="Confirm", command=select_date)
            btn_select.pack(pady=5)

        def open_birthday_calendar():
            def select_date():
                selected_date_str = cal.get_date()
                entries["Ngày Sinh"].config(state="normal") # Allow insertion
                entries["Ngày Sinh"].delete(0, tk.END)
                entries["Ngày Sinh"].insert(0, selected_date_str) # Insert the YYYY-MM-DD string
                entries["Ngày Sinh"].config(state="readonly") # Set back to readonly
                top.destroy()

            top = tk.Toplevel(edit_window) # Make it child of add_window
            top.title("Chọn Ngày")

            # Calendar widget - CHANGED date_pattern
            cal = Calendar(top, date_pattern="yyyy-mm-dd", selectmode='day')
            cal.pack(pady=10)

            # Confirm button
            btn_select = tk.Button(top, text="Xác Nhận", command=select_date)
            btn_select.pack(pady=5)

        def get_current_combobox(room_type_str):
            return 0 if room_type_str == "Thường" else 1

        # Choose date button - positioned next to the entry
        choose_birthday = tk.Button(edit_window, text="...", command=open_birthday_calendar)
        choose_birthday.grid(row=3 ,column=2, padx=(0, 5), pady=5, sticky="w")

        # Choose date button for "Ngày Thuê Phòng"
        choose_rent_date = tk.Button(edit_window, text="...", command=open_rent_date_calendar) 
        choose_rent_date.grid(row=6, column=2, padx=(0, 5), pady=5, sticky="w") 

        # Room type combobox
        combobox_items = ["Thường", "VIP"]
        combobox = ttk.Combobox(edit_window, values=combobox_items, state="readonly")
        # Get current value *before* replacing the widget
        current_room_type = entries["Loại Phòng"].get()
        # Replace placeholder Entry
        entries["Loại Phòng"].grid_forget()
        combobox.grid(row=7, column=1, padx=5, pady=5, sticky="ew")
        combobox.current(get_current_combobox(current_room_type)) # Set current data
        entries["Loại Phòng"] = combobox # Update entries dict

        def save_changes():
            new_customer_values = []
            for field in fields:
                widget = entries[field]
                value = widget.get()
                # Basic validation (optional but recommended)
                if field == "ID" and not value.isdigit():
                     messagebox.showerror("Lỗi", "ID phải là số.")
                     return
                if not value and field not in ["Giới Tính","Ngày Sinh","Quốc Tịch","Quê Quán"]: # Example required fields
                     messagebox.showerror("Lỗi", f"Trường '{field}' không được để trống.")
                     return
                new_customer_values.append(value)

            try:
                # convert birthday and check-in date to datetime objects
                birthday_dt_fm = datetime.strptime(new_customer_values[3], "%Y-%m-%d")
                checkin_dt_fm = datetime.strptime(new_customer_values[6], "%Y-%m-%d")
            except ValueError as e:
                messagebox.showerror("Lỗi định dạng ngày", f"Vui lòng nhập ngày theo định dạng yyyy-mm-dd.\nChi tiết: {e}")
                return

            new_customer_info = CustomerInfo(
                id=new_customer_values[0],
                name=new_customer_values[1],
                sex=new_customer_values[2],
                birthday=birthday_dt_fm,
                national=new_customer_values[4],
                country=new_customer_values[5],
                checkin_date=checkin_dt_fm,
                room_type=new_customer_values[7],
                room_number=new_customer_values[8]
            )

            # remove old customer data in local list(Treeview)
            self.tree.delete(new_customer_values[0])

            # Add the CustomerInfo object to customer_list
            self.customer_list.append(new_customer_info)

            # Add to Treeview (using attributes of the object)
            last_insert_customer = self.tree.insert("", "end", iid=new_customer_info.id,values=(
                new_customer_info.id,
                new_customer_info.name,
                new_customer_info.sex,
                new_customer_info.birthday.strftime("%Y-%m-%d"),
                new_customer_info.national,
                new_customer_info.country,
                new_customer_info.checkin_date.strftime("%Y-%m-%d"),
                new_customer_info.room_type,
                new_customer_info.room_number,
            ))
            self.tree.move(last_insert_customer, "", 0)

            edit_window.destroy()

            # change customer information in database 
            self.db_conn.updateCustomerInDatabase(new_customer_info)

        save_btn = tk.Button(edit_window, text="Lưu", command=save_changes, bg=color1, fg="white")
        save_btn.grid(row=len(fields), column=0, columnspan=3, pady=10)

    def remove_customer(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning(
                "Cảnh báo", "Vui lòng chọn khách hàng để xóa"
            )
            return

        item_values = self.tree.item(selected_item)["values"]
        customer_id = item_values[0]

        self.customer_list = [
            c for c in self.customer_list if c.id != customer_id
        ]
        self.tree.delete(selected_item)

        # remove customer from database
        self.db_conn.removeCustomerFromDatabase(customer_id)
        
    def sent_data_to_checkout(self):
        selected_item = self.tree.selection()

        if selected_item:  # Ensure something is selected
            item_values = self.tree.item(selected_item[0])["values"]  # Use selected_item[0]
            try:
                self.controller.id = item_values[0]
                self.controller.name = item_values[1]
                self.controller.sex = item_values[2]
                self.controller.birthday = item_values[3]
                self.controller.national = item_values[4]
                self.controller.country = item_values[5]
                self.controller.checkin_date = item_values[6]
                self.controller.room_type = item_values[7]
                self.show_tab("Thanh Toán")
        
            except ValueError:
                print("Invalid datetime format in Treeview.")
        else:
            print("No item selected.")
