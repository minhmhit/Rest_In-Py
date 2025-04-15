from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar

from database import DB_Connector
from staff_information import StaffInfo

color1 = "#3B82F6"

class StaffManagement(tk.Frame):
    def __init__(self, parent, staff_list, db_conn: DB_Connector):
        super().__init__(parent, bg="#F5F5F5")
        self.staff_list = staff_list
        self.db_conn = db_conn

        # Title
        title = tk.Label(self, text="Danh sách nhân viên", font=("Arial", 14, "bold"), anchor="w", bg="#F5F5F5")
        title.pack(fill="x", padx=10, pady=(10, 5))

        # Treeview Table
        columns = ("id", "name", "gender", "birthday", "role", "username", "password", "permissions")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        headings = {
            "id": "ID",
            "name": "Họ Tên",
            "gender": "Giới Tính",
            "birthday": "Ngày Sinh",
            "role": "Chức vụ",
            "username": "Tên đăng nhập",
            "password": "Mật Khẩu",
            "permissions": "Phân quyền"
        }

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        # add data to tree
        for staff in self.staff_list:
            self.tree.insert("", "end", iid=staff.id, values=( 
                staff.id,
                staff.name,
                staff.sex,
                staff.birthday,
                staff.role,
                staff.username,
                staff.password,
                staff.permissions,
            ))

        # Bottom Buttons
        button_frame = tk.Frame(self, bg="#F5F5F5")
        button_frame.pack(pady=10)

        btn_add = tk.Button(button_frame, text="Thêm nhân viên", width=20, bg="#007BFF", fg="white", command=self.open_add_staff)
        btn_delete = tk.Button(button_frame, text="Xóa nhân viên", width=20, bg="#007BFF", fg="white", command=self.remove_staff)
        btn_edit = tk.Button(button_frame, text="Chỉnh sửa thông tin", width=20, bg="#007BFF", fg="white", command=self.change_staff_information)

        btn_add.grid(row=0, column=0, padx=10)
        btn_delete.grid(row=0, column=1, padx=10)
        btn_edit.grid(row=0, column=2, padx=10)

    def open_add_staff(self):
        add_window = tk.Toplevel(self)
        add_window.title("Thêm nhân viên")
        add_window.geometry("300x400")

        fields = [
            "id",
            "name", 
            "gender", 
            "birthday", 
            "role", 
            "username", 
            "password", 
            "permissions",
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
            return "break";

        # bind readonly event entry
        entries["birthday"].bind("<Key>",prevent_keyboard_input)
        entries["birthday"].config(state="readonly")

        def open_birthday_calendar():
            def select_date():
                selected_date_str = cal.get_date()  # Get selected date
                entries["birthday"].config(state="normal")
                entries["birthday"].delete(0, tk.END)  # Clear previous value
                entries["birthday"].insert(0, selected_date_str)
                entries["birthday"].config(state="readonly")
                top.destroy()

            # Create a new top-level window for the calendar
            top = tk.Toplevel(self)
            top.title("Chọn Ngày")

            # Calendar widget
            cal = Calendar(top, date_pattern="yyyy-mm-dd", selectmode='day')
            cal.pack(pady=10)

            # Confirm button
            btn_select = tk.Button(top, text="Xác Nhận", command=select_date)
            btn_select.pack(pady=5)

        # choose date button
        choose_birthday = tk.Button(add_window,text="...",command=open_birthday_calendar)
        choose_birthday.grid(row=3,column=2,padx=(0, 5), pady=5, sticky="w")

        def submit():
            new_staff_values = []
            for field in fields:
                widget = entries[field]
                value = widget.get()
                # Basic validation (optional but recommended)
                if field == "ID" and not value.isdigit():
                     messagebox.showerror("Lỗi", "ID phải là số.")
                     return
                if not value and field not in ["username","password","permissions"]: # Example required fields
                     messagebox.showerror("Lỗi", f"Trường '{field}' không được để trống.")
                     return
                new_staff_values.append(value)

            try:
                # convert birthday and check-in date to datetime objects
                birthday_dt_fm = datetime.strptime(new_staff_values[3], "%Y-%m-%d")
            except ValueError as e:
                messagebox.showerror("Lỗi định dạng ngày", f"Vui lòng nhập ngày theo định dạng yyyy-mm-dd.\nChi tiết: {e}")
                return

            new_staff_info = StaffInfo(
                id=new_staff_values[0],
                name=new_staff_values[1],
                sex=new_staff_values[2],
                birthday=birthday_dt_fm,
                role=new_staff_values[4],
                username=new_staff_values[5],
                password=new_staff_values[6],
                permissions=new_staff_values[7]
            )

            # Add the CustomerInfo object to customer_list
            self.staff_list.append(new_staff_info)

            # Add to Treeview (using attributes of the object)
            last_insert_staff = self.tree.insert("", "end", iid=new_staff_info.id, values=(
                new_staff_info.id,
                new_staff_info.name,
                new_staff_info.sex,
                new_staff_info.birthday.strftime("%Y-%m-%d"),
                new_staff_info.role,
                new_staff_info.username,
                new_staff_info.password,
                new_staff_info.permissions
            ))
            self.tree.move(last_insert_staff, "", 0)

            add_window.destroy()

            # add new staff to database 
            self.db_conn.setStaffToDatabase(new_staff_info)

        submit_btn = tk.Button(add_window, text="Lưu", command=submit, bg=color1, fg="white")
        submit_btn.grid(row=len(fields), column=0, columnspan=3, pady=10)

    def change_staff_information(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn nhân viên để chỉnh sửa")
            return

        item_values = self.tree.item(selected_item[0])['values']
        edit_window = tk.Toplevel(self)
        edit_window.title("Chỉnh sửa thông tin nhân viên")
        edit_window.geometry("350x400")

        fields = [
            "id",
            "name", 
            "gender", 
            "birthday", 
            "role", 
            "username", 
            "password", 
            "permissions",
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
        entries["id"].bind("<Key>", prevent_keyboard_input) # bind event
        entries["id"].config(state="readonly")
        entries["birthday"].bind("<Key>", prevent_keyboard_input) # bind event
        entries["birthday"].config(state="readonly")

        def open_birthday_calendar():
            def select_date():
                selected_date_str = cal.get_date()
                entries["birthday"].config(state="normal") # Allow insertion
                entries["birthday"].delete(0, tk.END)
                entries["birthday"].insert(0, selected_date_str) # Insert the YYYY-MM-DD string
                entries["birthday"].config(state="readonly") # Set back to readonly
                top.destroy()

            top = tk.Toplevel(edit_window) # Make it child of add_window
            top.title("Chọn Ngày")

            # Calendar widget - CHANGED date_pattern
            cal = Calendar(top, date_pattern="yyyy-mm-dd", selectmode='day')
            cal.pack(pady=10)

            # Confirm button
            btn_select = tk.Button(top, text="Xác Nhận", command=select_date)
            btn_select.pack(pady=5)

        # Choose date button - positioned next to the entry
        choose_birthday = tk.Button(edit_window, text="...", command=open_birthday_calendar)
        choose_birthday.grid(row=3 ,column=2, padx=(0, 5), pady=5, sticky="w")

        def save_changes():
            new_staff_values = []
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
                new_staff_values.append(value)

            try:
                # convert birthday to datetime objects
                birthday_dt_fm = datetime.strptime(new_staff_values[3], "%Y-%m-%d")
            except ValueError as e:
                messagebox.showerror("Lỗi định dạng ngày", f"Vui lòng nhập ngày theo định dạng yyyy-mm-dd.\nChi tiết: {e}")
                return

            new_staff_info = StaffInfo(
                id=new_staff_values[0],
                name=new_staff_values[1],
                sex=new_staff_values[2],
                birthday=birthday_dt_fm,
                role=new_staff_values[4],
                username=new_staff_values[5],
                password=new_staff_values[6],
                permissions=new_staff_values[7]
            )

            # remove old staff data in local list(Treeview)
            self.tree.delete(new_staff_values[0])

            # Add the StaffInfo object to staff_list
            self.staff_list.append(new_staff_info)

            # Add to Treeview (using attributes of the object)
            last_insert_staff = self.tree.insert("", "end", iid=new_staff_info.id, values=(
                new_staff_info.id,
                new_staff_info.name,
                new_staff_info.sex,
                new_staff_info.birthday.strftime("%Y-%m-%d"),
                new_staff_info.role,
                new_staff_info.username,
                new_staff_info.password,
                new_staff_info.permissions
            ))
            self.tree.move(last_insert_staff, "", 0)

            edit_window.destroy()

            # change staff information in database 
            self.db_conn.updateStaffInDatabase(new_staff_info)

        save_btn = tk.Button(edit_window, text="Lưu", command=save_changes, bg=color1, fg="white")
        save_btn.grid(row=len(fields), column=0, columnspan=3, pady=10)

    def remove_staff(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning(
                "Cảnh báo", "Vui lòng chọn nhân viên để xóa"
            )
            return

        item_values = self.tree.item(selected_item)["values"]
        staff_id = item_values[0]

        self.staff_list = [
            c for c in self.staff_list if c.id != staff_id
        ]
        self.tree.delete(selected_item)

        # remove staff from database
        self.db_conn.removeStaffFromDatabase(staff_id)

    # def change_staff_information(self):
    #     selected_item = self.tree.selection()
    #     if not selected_item:
    #         messagebox.showwarning("Cảnh báo", "Vui lòng chọn nhân viên để chỉnh sửa")
    #         return
    #
    #     item_values = self.tree.item(selected_item[0])["values"]
    #     edit_window = tk.Toplevel(self)
    #     edit_window.title("Chỉnh sửa thông tin khách hàng")
    #     edit_window.geometry("350x400")
    #
    #     fields = [
    #         "id", 
    #         "name", 
    #         "gender",
    #         "birthday",
    #         "role",
    #         "username",
    #         "password",
    #         "permissions",
    #     ]
    #     entries = {}
    #
    #     for i, (field, value) in enumerate(zip(fields, item_values)):
    #         tk.Label(edit_window, text=field).grid(row=i, column=0, padx=5, pady=5)
    #         entry = tk.Entry(edit_window)
    #         entry.insert(0, value)
    #         entry.grid(row=i, column=1, padx=5, pady=5)
    #         entries[field] = entry
    #
    #     def prevent_keyboard_input(event):
    #         return "break"  # Prevents the default key press action
    #
    #     # bind readonly event Entry
    #     entries["birthday"].bind("<Key>", prevent_keyboard_input) # bind event
    #
    #     def open_calendar():
    #         def select_date():
    #             selected_date = cal.get_date()  # Get selected date
    #             entries["birthday"].delete(0, tk.END)  # Clear previous value
    #             entries["birthday"].insert(0, datetime.strptime(selected_date, "%d/%m/%Y").strftime("%d/%m/%Y"))
    #             top.destroy()  # Close the calendar window
    #
    #         # Create a new top-level window for the calendar
    #         top = tk.Toplevel(self)
    #         top.title("Choose a Date")
    #
    #         # Calendar widget
    #         cal = Calendar(top, date_pattern="dd/MM/yyyy")
    #         cal.pack(pady=10)
    #
    #         # Confirm button
    #         btn_select = tk.Button(top, text="Confirm", command=select_date)
    #         btn_select.pack(pady=5)
    #
    #     # choose date button
    #     choose_date = tk.Button(edit_window,text="birthday",command=open_calendar)
    #     choose_date.grid(row=3,column=2)
    #
    #     def save_changes():
    #         new_values = tuple(entry.get() for entry in entries.values())
    #         self.tree.item(selected_item[0], values=new_values)
    #         for index, customer in enumerate(self.staff_list):
    #             if customer[0] == item_values[0]:  # Update correct customer by ID
    #                 self.staff_list[index] = new_values
    #                 break
    #         edit_window.destroy()
    #
    #     save_btn = tk.Button(edit_window, text="Lưu", command=save_changes)
    #     save_btn.grid(row=len(fields), columnspan=2, pady=10)
