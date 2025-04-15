import tkinter as tk
from tkinter import ttk

class Revenue(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#F5F5F5")

        # id - name - sex - birthday - national - country - checkin_date - room_type - room total price - room number
        self.customer_list = [
            (1, "Nguyễn Văn An", "Nam", "1990-05-20", "Việt Nam", "Long An", "2008-12-05", "VIP", 150.00 ,103),
            (2, "Trần Thị Hoa", "Nữ", "1985-12-15", "Việt Nam", "Trà Vinh", "2011-05-03", "Thường", 80.00,101),
            (3, "Lê Minh Tú", "Nam", "1992-07-30", "Việt Nam", "Hồ Chí Minh", "2011-09-16", "VIP", 150.00,204),
            (4, "Phạm Thùy Dung", "Nữ", "1998-09-05", "Việt Nam", "Hà Nội", "2009-12-31", "Thường", 80.00,202),
            (5, "Hoàng Quốc Bảo", "Nam", "1987-11-22", "Việt Nam", "Bạc Liêu", "2013-10-16", "Thường", 80.00,301),
            (6, "Đặng Thu Hằng", "Nữ", "1995-04-18", "Việt Nam", "Hải Phòng", "2017-02-10", "Thường", 80.00,305),
            (7, "Bùi Quang Huy", "Nam", "1989-08-12", "Việt Nam", "Việt Nam", "2018-01-30", "VIP", 150.00,901),
            (8, "Vũ Ngọc Linh", "Nữ", "1991-06-25", "Việt Nam", "Việt Nam", "2000-04-22", "Thường", 80.00,902),
            (9, "Đoàn Văn Hải", "Nam", "1984-03-17", "Việt Nam", "Việt Nam", "2018-10-04", "Thường", 80.00,604),
            (10, "Lý Thu Trang", "Nữ", "1993-09-29", "Việt Nam", "Việt Nam", "2018-12-19", "Thường", 80.00,502),
            (11, "Nguyễn Văn Bình", "Nam", "1982-07-21", "Việt Nam", "Đà Nẵng", "2020-05-28", "VIP", 150.00,405),
            (12, "Phạm Thanh Mai", "Nữ", "1994-03-12", "Việt Nam", "Cần Thơ", "2020-06-17", "Thường", 80.00,204),
            # (13, "Trần Đình Nam", "Nam", "1990-10-01", "Việt Nam", "Nghệ An", "2020-06-24", "VIP", 150.00),
            # (14, "Hoàng Thu Hà", "Nữ", "1997-08-15", "Việt Nam", "Quảng Ninh", "2021-11-12", "Thường", 80.00),
            # (15, "Lê Hoàng Sơn", "Nam", "1995-11-09", "Việt Nam", "Bình Dương", "2022-02-08", "VIP", 150.00),
            # (16, "Đặng Ngọc Phúc", "Nam", "1988-12-30", "Việt Nam", "Huế", "2023-02-08", "Thường", 80.00),
            # (17, "Ngô Minh Tuấn", "Nam", "1999-05-07", "Việt Nam", "Hà Nam", "2023-09-27", "Thường", 80.00),
            # (18, "Lý Ngọc Hân", "Nữ", "1991-01-14", "Việt Nam", "Phú Thọ", "2024-01-03", "VIP", 150.00),
            # (19, "Phan Thị Lan", "Nữ", "1986-06-17", "Việt Nam", "Bình Thuận", "2024-01-05", "Thường", 80.00),
            # (20, "Nguyễn Đăng Khoa", "Nam", "1994-09-23", "Việt Nam", "Vũng Tàu", "2025-04-08", "VIP", 150.00),
            # (21, "Võ Hồng Quân", "Nam", "1987-04-08", "Việt Nam", "Tây Ninh", "2014-09-15", "VIP", 150.00),
            # (22, "Dương Thị Nhung", "Nữ", "1995-05-19", "Việt Nam", "Gia Lai", "2023-03-30", "Thường", 80.00),
            # (23, "Lê Văn Huy", "Nam", "1983-02-14", "Việt Nam", "Hà Giang", "2012-09-09", "VIP", 150.00),
            # (24, "Nguyễn Thị Thanh", "Nữ", "1998-10-27", "Việt Nam", "Đắk Lắk", "2020-02-20", "Thường", 80.00),
            # (25, "Trần Hữu Phước", "Nam", "1990-08-09", "Việt Nam", "Cà Mau", "2013-03-12", "VIP", 150.00),
            # (26, "Đào Thị Phượng", "Nữ", "1996-02-22", "Việt Nam", "Bắc Giang", "2016-02-20", "Thường", 80.00),
            # (27, "Nguyễn Nhật Linh", "Nam", "1989-07-05", "Việt Nam", "Thanh Hóa", "2017-09-12", "VIP", 150.00),
            # (28, "Trương Ngọc Anh", "Nữ", "1992-12-31", "Việt Nam", "Bình Phước", "2021-11-12", "Thường", 80.00),
            # (29, "Lâm Hoàng Dũng", "Nam", "1997-11-17", "Việt Nam", "Sóc Trăng", "2022-12-21", "VIP", 150.00),
            # (30, "Võ Thị Hạnh", "Nữ", "1993-06-09", "Việt Nam", "An Giang", "1975-04-30", "Thường", 80.00),
        ]
        
        # LabelFrame for the Table
        table_frame = tk.LabelFrame(self, text="Motel Revenue", bg="#F5F5F5", font=("Arial", 12, "bold"))
        table_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Columns Definition
        columns = ("ID", "Name", "Sex", "Birthday", "Nationality", "Country", "Check-in Date", "Room Type", "Total Cost")

        # Treeview Widget
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=100)
        
        self.tree.pack(padx=10, pady=5, fill="both", expand=True)

        # insert data
        for customer in self.customer_list:
            self.tree.insert("", "end", values=customer)

        # LabelFrame for Total Revenue
        revenue_frame = tk.LabelFrame(self, text="Total Revenue", bg="#F5F5F5", font=("Arial", 12, "bold"))
        revenue_frame.pack(padx=10, pady=10, fill="x")

        self.total_revenue_label = tk.Label(revenue_frame, text="Total Revenue: $0.00", font=("Arial", 12, "bold"), bg="#F5F5F5")
        self.total_revenue_label.pack(padx=10, pady=5)

        # update total revenue
        self.update_total_revenue()

    def update_total_revenue(self):
        total = sum(float(self.tree.item(item, "values")[-1]) for item in self.tree.get_children())
        self.total_revenue_label.config(text=f"Total Revenue: ${total:.2f}")

    def add_record(self, customer):
        self.tree.insert("", "end", values=customer)

        # move new customer to the top of table
        last_insert_customer = self.tree.insert("", "end", values=customer)
        self.tree.move(last_insert_customer, "", 0)

        # update total revenue
        self.update_total_revenue()
