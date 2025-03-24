import tkinter as tk
from tkinter import messagebox, ttk


class Customer(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#F5F5F5")

        self.customer_list = [
            (1, "Nguyễn Văn An", "Nam", "1990-05-20", "Việt Nam", "Long An"),
            (2, "Trần Thị Hoa", "Nữ", "1985-12-15", "Việt Nam", "Tra Vinh"),
            (3, "Lê Minh Tú", "Nam", "1992-07-30", "Việt Nam", "Ho Chi Minh"),
            (4, "Phạm Thùy Dung", "Nữ", "1998-09-05", "Việt Nam", "Ha Noi"),
            (5, "Hoàng Quốc Bảo", "Nam", "1987-11-22", "Việt Nam", "Bac Lieu"),
            (6, "Đặng Thu Hằng", "Nữ", "1995-04-18", "Việt Nam", "Hai Phong"),
            (7, "Bùi Quang Huy", "Nam", "1989-08-12", "Việt Nam", "Việt Nam"),
            (8, "Vũ Ngọc Linh", "Nữ", "1991-06-25", "Việt Nam", "Việt Nam"),
            (9, "Đoàn Văn Hải", "Nam", "1984-03-17", "Việt Nam", "Việt Nam"),
            (10, "Lý Thu Trang", "Nữ", "1993-09-29", "Việt Nam", "Việt Nam"),
            (11, "Phan Thanh Nam", "Nam", "1996-02-10", "Việt Nam", "Việt Nam"),
            (12, "Ngô Thị Mai", "Nữ", "1990-07-05", "Việt Nam", "Việt Nam"),
            (13, "Trịnh Quốc Đạt", "Nam", "1982-12-20", "Việt Nam", "Việt Nam"),
            (14, "Tạ Kim Oanh", "Nữ", "1999-01-14", "Việt Nam", "Việt Nam"),
            (15, "Dương Hữu Phúc", "Nam", "1994-05-23", "Việt Nam", "Việt Nam"),
            (16, "Hồ Minh Đức", "Nam", "1997-11-30", "Việt Nam", "Việt Nam"),
            (17, "Lâm Thị Lan", "Nữ", "1986-08-18", "Việt Nam", "Việt Nam"),
            (18, "Trần Gia Bảo", "Nam", "1995-09-08", "Việt Nam", "Việt Nam"),
            (
                19,
                "Nguyễn Hồng Nhung",
                "Nữ",
                "1998-04-21",
                "Việt Nam",
                "Việt Nam",
            ),
            (
                20,
                "Lương Quang Hải",
                "Nam",
                "1980-10-10",
                "Việt Nam",
                "Việt Nam",
            ),
            (21, "Mai Thị Hạnh", "Nữ", "1992-06-12", "Việt Nam", "Việt Nam"),
            (
                22,
                "Phùng Văn Thịnh",
                "Nam",
                "1983-03-04",
                "Việt Nam",
                "Việt Nam",
            ),
            (
                23,
                "Nguyễn Thanh Hương",
                "Nữ",
                "1997-07-27",
                "Việt Nam",
                "Việt Nam",
            ),
            (24, "Đỗ Trọng Khang", "Nam", "1991-09-15", "Việt Nam", "Việt Nam"),
            (25, "Hoàng Mỹ Linh", "Nữ", "1988-11-09", "Việt Nam", "Việt Nam"),
            (
                26,
                "Trịnh Minh Tuấn",
                "Nam",
                "1996-12-01",
                "Việt Nam",
                "Việt Nam",
            ),
            (27, "Bùi Hải Yến", "Nữ", "1994-05-07", "Việt Nam", "Việt Nam"),
            (28, "Lê Tấn Tài", "Nam", "1985-01-19", "Việt Nam", "Việt Nam"),
            (29, "Vương Phúc An", "Nam", "1999-10-22", "Việt Nam", "Việt Nam"),
            (30, "Đặng Quỳnh Hoa", "Nữ", "1993-07-13", "Việt Nam", "Việt Nam"),
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
            "Ngay Thue Phong",
            "Loai Phong",
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

        # Buttons
        self.addCustomer = tk.Button(
            self.functionPanel,
            text="Thêm khách hàng",
            bg="blue",
            fg="white",
            command=self.open_add_customer,
        )
        self.removeCustomer = tk.Button(
            self.functionPanel,
            text="Xóa khách hàng",
            bg="red",
            fg="white",
            command=self.remove_customer,
        )

        self.addCustomer.pack(side="left", expand=True, padx=10, pady=5)
        self.removeCustomer.pack(side="right", expand=True, padx=10, pady=5)

    def open_add_customer(self):
        add_window = tk.Toplevel(self)
        add_window.title("Thêm khách hàng")
        add_window.geometry("300x300")

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

        submit_btn = tk.Button(add_window, text="Submit", command=submit)
        submit_btn.grid(row=len(fields), columnspan=2, pady=10)

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
