import tkinter as tk
from tkinter import ttk, Toplevel, Label
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

class RevenueChart(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#F5F5F5")
        self.pack(fill=tk.BOTH, expand=True)
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
        ]

        # tạo biểu đồ
        self.create_widgets()

    def create_widgets(self):
        # --- Xử lý Dữ liệu ---
        revenue_by_year = {} # Doanh thu theo năm
        customer_count_by_year = {} # Số lượng khách hàng theo năm
        province_revenue_by_year = {} # Doanh thu theo tỉnh theo năm

        for customer in self.customer_list:
            join_date_str = customer[6] # Ngày tham gia
            revenue = customer[7] == "VIP" and customer[8] or customer[8] # Doanh thu
            year = datetime.strptime(join_date_str, "%Y-%m-%d").year # Năm
            province = customer[5] # Tỉnh

            # Tổng Doanh thu theo Năm
            if year not in revenue_by_year:
                revenue_by_year[year] = 0
            revenue_by_year[year] += revenue

            # Số lượng Khách hàng theo Năm
            if year not in customer_count_by_year:
                customer_count_by_year[year] = 0
            customer_count_by_year[year] += 1

            # Doanh thu Tỉnh theo Năm
            if year not in province_revenue_by_year:
                province_revenue_by_year[year] = {}
            if province not in province_revenue_by_year[year]:
                province_revenue_by_year[year][province] = 0
            province_revenue_by_year[year][province] += revenue

        years = sorted(revenue_by_year.keys()) # Các năm

        # --- Notebook cho các Biểu đồ khác nhau ---
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- Style cho Frame ---
        style = ttk.Style()
        style.configure("MyFrame.TFrame", background="#F5F5F5")

        # --- Biểu đồ Tổng Doanh thu ---
        revenue_frame = ttk.Frame(notebook, style="MyFrame.TFrame")
        notebook.add(revenue_frame, text="Tổng Doanh Thu")
        self.create_revenue_chart(revenue_frame, years, [revenue_by_year.get(year, 0) for year in years])

        # --- Biểu đồ Tăng trưởng Khách hàng ---
        customer_frame = ttk.Frame(notebook, style="MyFrame.TFrame")
        notebook.add(customer_frame, text="Tăng Trưởng Khách Hàng")
        self.create_customer_chart(customer_frame, years, [customer_count_by_year.get(year, 0) for year in years])

        # --- Biểu đồ Doanh thu theo Tỉnh ---
        province_frame = ttk.Frame(notebook, style="MyFrame.TFrame")
        notebook.add(province_frame, text="Doanh Thu theo Tỉnh")
        self.province_revenue_data = province_revenue_by_year # Lưu trữ dữ liệu để dùng sau
        self.province_colors = {} # Lưu trữ mapping tỉnh và màu
        self.create_province_revenue_chart(province_frame, years, province_revenue_by_year)

        # Nút hiển thị màu sắc
        color_button = ttk.Button(province_frame, text="Hiển thị Màu sắc Tỉnh", command=self.show_province_colors)
        color_button.pack(pady=5)

    def create_revenue_chart(self, parent, years, revenue_data):
        fig, ax = plt.subplots(figsize=(8, 6), facecolor="#F5F5F5")
        ax.bar(years, revenue_data, color="#708090")
        ax.set_xlabel("Năm", fontsize=12, color="#333")
        ax.set_ylabel("Tổng Doanh Thu", fontsize=12, color="#333")
        ax.set_title("Tổng Doanh Thu qua các Năm", fontsize=14, color="#333")
        ax.tick_params(axis='x', colors='#555')
        ax.tick_params(axis='y', colors='#555')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_facecolor("#F0F8FF")
        fig.patch.set_facecolor("#F5F5F5")

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        canvas.draw()

    def create_customer_chart(self, parent, years, customer_data):
        fig, ax = plt.subplots(figsize=(8, 6), facecolor="#F5F5F5")
        ax.plot(years, customer_data, marker='o', linestyle='-', color="#4682B4")
        ax.set_xlabel("Năm", fontsize=12, color="#333")
        ax.set_ylabel("Số lượng Khách hàng", fontsize=12, color="#333")
        ax.set_title("Tăng trưởng Khách hàng qua các Năm", fontsize=14, color="#333")
        ax.tick_params(axis='x', colors='#555')
        ax.tick_params(axis='y', colors='#555')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.set_facecolor("#E0FFFF")
        fig.patch.set_facecolor("#F5F5F5")

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        canvas.draw()

    def create_province_revenue_chart(self, parent, years, province_revenue_data):
        fig, ax = plt.subplots(figsize=(10, 7), facecolor="#F5F5F5")
        num_provinces = len(set(p for year_data in province_revenue_data.values() for p in year_data.keys()))
        bar_width = 0.8 / num_provinces
        colors = plt.cm.get_cmap('viridis', num_provinces)
        province_labels = []
        province_positions = {}
        color_map = {}

        all_provinces = set()
        for year_data in province_revenue_data.values():
            all_provinces.update(year_data.keys())
        sorted_provinces = sorted(list(all_provinces))
        for i, province in enumerate(sorted_provinces):
            province_positions[province] = i
            color_map[province] = colors(i)
            self.province_colors[province] = color_map[province] # Lưu màu

        for i, year in enumerate(years):
            province_data = province_revenue_data.get(year, {})
            for province, revenue in province_data.items():
                position = province_positions[province]
                x_pos = i + (position - num_provinces // 2) * bar_width
                ax.bar(x_pos, revenue, width=bar_width, label=province if year == years[0] else "", color=color_map[province])

        ax.set_xlabel("Năm", fontsize=12, color="#333")
        ax.set_ylabel("Doanh Thu", fontsize=12, color="#333")
        ax.set_title("Doanh thu theo Tỉnh qua các Năm", fontsize=14, color="#333")
        ax.set_xticks(range(len(years)))
        ax.set_xticklabels(years, fontsize=10, color="#555")
        ax.tick_params(axis='y', colors='#555')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.legend(title="Tỉnh", fontsize=9)
        ax.set_facecolor("#FAF0E6")
        fig.patch.set_facecolor("#F5F5F5")
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        canvas.draw()

    def show_province_colors(self):
        top = Toplevel(self)
        top.title("Màu sắc theo Tỉnh")
        top.configure(bg="#F5F5F5")

        for province, color_tuple in self.province_colors.items():
            color_hex = '#%02x%02x%02x' % (int(color_tuple[0]*255), int(color_tuple[1]*255), int(color_tuple[2]*255))
            frame = ttk.Frame(top, padding=5)
            frame.pack(fill=tk.X)
            color_label = Label(frame, text="", bg=color_hex, width=5)
            color_label.pack(side=tk.LEFT, padx=5)
            province_label = Label(frame, text=f"{province}: {color_hex}", bg="#F5F5F5")
            province_label.pack(side=tk.LEFT)
