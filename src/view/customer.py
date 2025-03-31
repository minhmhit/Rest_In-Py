import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

from customer_information import CustomerInfo

color1 = "#3B82F6"

class Customer(tk.Frame):
    def __init__(self, parent,show_tab,controller):
        super().__init__(parent, bg="#F5F5F5")
        self.show_tab = show_tab
        # self.customer_controller = controller
        self.controller = controller

        # id - name - sex - birthday - national - country - checkin_date - room_type
        self.customer_list = [
            (1, "Nguyễn Văn An", "Nam", "1990-05-20", "Việt Nam", "Long An","16/08/2005","VIP"),
            (2, "Trần Thị Hoa", "Nữ", "1985-12-15", "Việt Nam", "Tra Vinh","20/02/2015","Thường"),
            (3, "Lê Minh Tú", "Nam", "1992-07-30", "Việt Nam", "Ho Chi Minh","10/02/2010","VIP"),
            (4, "Phạm Thùy Dung", "Nữ", "1998-09-05", "Việt Nam", "Ha Noi","14/11/2018","Thường"),
            # (5, "Hoàng Quốc Bảo", "Nam", "1987-11-22", "Việt Nam", "Bac Lieu"),
            # (6, "Đặng Thu Hằng", "Nữ", "1995-04-18", "Việt Nam", "Hai Phong"),
            # (7, "Bùi Quang Huy", "Nam", "1989-08-12", "Việt Nam", "Việt Nam"),
            # (8, "Vũ Ngọc Linh", "Nữ", "1991-06-25", "Việt Nam", "Việt Nam"),
            # (9, "Đoàn Văn Hải", "Nam", "1984-03-17", "Việt Nam", "Việt Nam"),
            # (10, "Lý Thu Trang", "Nữ", "1993-09-29", "Việt Nam", "Việt Nam"),
            # (11, "Phan Thanh Nam", "Nam", "1996-02-10", "Việt Nam", "Việt Nam"),
            # (12, "Ngô Thị Mai", "Nữ", "1990-07-05", "Việt Nam", "Việt Nam"),
            # (13, "Trịnh Quốc Đạt", "Nam", "1982-12-20", "Việt Nam", "Việt Nam"),
            # (14, "Tạ Kim Oanh", "Nữ", "1999-01-14", "Việt Nam", "Việt Nam"),
            # (15, "Dương Hữu Phúc", "Nam", "1994-05-23", "Việt Nam", "Việt Nam"),
            # (16, "Hồ Minh Đức", "Nam", "1997-11-30", "Việt Nam", "Việt Nam"),
            # (17, "Lâm Thị Lan", "Nữ", "1986-08-18", "Việt Nam", "Việt Nam"),
            # (18, "Trần Gia Bảo", "Nam", "1995-09-08", "Việt Nam", "Việt Nam"),
            # (
            #     19,
            #     "Nguyễn Hồng Nhung",
            #     "Nữ",
            #     "1998-04-21",
            #     "Việt Nam",
            #     "Việt Nam",
            # ),
            # (
            #     20,
            #     "Lương Quang Hải",
            #     "Nam",
            #     "1980-10-10",
            #     "Việt Nam",
            #     "Việt Nam",
            # ),
            # (21, "Mai Thị Hạnh", "Nữ", "1992-06-12", "Việt Nam", "Việt Nam"),
            # (
            #     22,
            #     "Phùng Văn Thịnh",
            #     "Nam",
            #     "1983-03-04",
            #     "Việt Nam",
            #     "Việt Nam",
            # ),
            # (
            #     23,
            #     "Nguyễn Thanh Hương",
            #     "Nữ",
            #     "1997-07-27",
            #     "Việt Nam",
            #     "Việt Nam",
            # ),
            # (24, "Đỗ Trọng Khang", "Nam", "1991-09-15", "Việt Nam", "Việt Nam"),
            # (25, "Hoàng Mỹ Linh", "Nữ", "1988-11-09", "Việt Nam", "Việt Nam"),
            # (
            #     26,
            #     "Trịnh Minh Tuấn",
            #     "Nam",
            #     "1996-12-01",
            #     "Việt Nam",
            #     "Việt Nam",
            # ),
            # (27, "Bùi Hải Yến", "Nữ", "1994-05-07", "Việt Nam", "Việt Nam"),
            # (28, "Lê Tấn Tài", "Nam", "1985-01-19", "Việt Nam", "Việt Nam"),
            # (29, "Vương Phúc An", "Nam", "1999-10-22", "Việt Nam", "Việt Nam"),
            # (30, "Đặng Quỳnh Hoa", "Nữ", "1993-07-13", "Việt Nam", "Việt Nam"),
        ]

        # Create panels
        self.mainPanel = tk.LabelFrame(
            self, text="Danh sách khách hàng", bg="white"
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
        )
        self.tree = ttk.Treeview(
            self.mainPanel, columns=columns, show="headings"
        )

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")

        for customer in self.customer_list:
            self.tree.insert("", "end", values=customer)

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
        ]
        entries = {}

        for i, field in enumerate(fields):
            tk.Label(add_window, text=field).grid(
                row=i, column=0, padx=5, pady=5
            )
            entry = tk.Entry(add_window)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[field] = entry

        def submit():
            new_customer = tuple(entry.get() for entry in entries.values())
            self.customer_list.append(new_customer)
            self.tree.insert("", "end", values=new_customer)
            add_window.destroy()

        submit_btn = tk.Button(add_window, text="Lưu", command=submit)
        submit_btn.grid(row=len(fields), columnspan=2, pady=10)

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
            "ID", "Họ Tên", "Giới Tính", "Ngày Sinh", "Quốc Tịch", "Quê Quán", "Ngày Thuê Phòng", "Loại Phòng"
        ]
        entries = {}

        for i, (field, value) in enumerate(zip(fields, item_values)):
            tk.Label(edit_window, text=field).grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(edit_window)
            entry.insert(0, value)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[field] = entry

        def save_changes():
            new_values = tuple(entry.get() for entry in entries.values())
            self.tree.item(selected_item[0], values=new_values)
            for index, customer in enumerate(self.customer_list):
                if customer[0] == item_values[0]:  # Update correct customer by ID
                    self.customer_list[index] = new_values
                    break
            edit_window.destroy()

        save_btn = tk.Button(edit_window, text="Lưu", command=save_changes)
        save_btn.grid(row=len(fields), columnspan=2, pady=10)

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
            c for c in self.customer_list if c[0] != customer_id
        ]
        self.tree.delete(selected_item)
        
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
