import tkinter as tk
from tkinter import messagebox
import mysql.connector

from camera import Camera
from checkout import Checkout
from customer import Customer
from login_page import LoginPage
from revenue import Revenue
from customer_information import CustomerInfo
from room_management import RoomManagement
from staff_management import StaffManagement
from revenue_chart import RevenueChart
from database import DB_Connector

# get data from database - using XAMPP to connect
try:
    db_conn = DB_Connector()
    customer_list = db_conn.getCustomersFromDatabase()
    staff_list = db_conn.getStaffsFromDatabase()

    # main window
    root = tk.Tk()
    root.title("Quản Lí Nhà Trọ")
    # root.iconbitmap("/icon/hotel.ico")
    root.geometry("1280x720")
    root.configure(bg="#3B82F6")

    # app bar
    appbar = tk.Frame(root, bg="#3B82F6", height=50)
    title = tk.Label(
        appbar,
        text="Quản Lí Nhà Trọ",
        bg="#3B82F6",
        fg="white",
        font=("Arial", 16, "bold"),
    )

    # buttons for switching tabs
    button_frame = tk.Frame(appbar, bg="#3B82F6")
    buttons = []

    # dictionary to store tab frames
    tabs = {}

    # share customer information from customer.py -> checkout.py
    customer_information = CustomerInfo()

    # main function
    def show_main():
        login_frame.pack_forget()  # hide login page
        appbar.pack(fill="x")  # show the app bar
        title.pack(side="left", padx=10)
        button_frame.pack(side="right")

        # Create and show tabs
        global tabs
        tabs = {
            "Camera": Camera(root),
            "Thanh Toán": Checkout(root,customer_information),
            "Danh Sách Thuê": Customer(root,show_tab,customer_information,customer_list,db_conn),
            "Doanh thu": Revenue(root),
            "Quản Lý Phòng": RoomManagement(root),
            "Quản Lý Nhân  Viên": StaffManagement(root,staff_list,db_conn),
            "Biểu Đồ Doanh Thu": RevenueChart(root)
        }

        # create buttons to switch tabs
        for name in tabs.keys():
            btn = tk.Button(
                button_frame,
                width=16,
                text=name,
                bd=0,
                bg="#3B82F6",
                fg="white",
                command=lambda n=name: show_tab(n),
            )
            btn.pack(side="left", padx=5)
            buttons.append(btn)

        show_tab("Camera")  # show first tab by default


    def show_tab(tab_name):
        for tab in tabs.values():
            tab.pack_forget()
        tabs[tab_name].pack(expand=True, fill="both")


    # create the login page (only this is visible at start)
    login_frame = LoginPage(root, show_main)
    login_frame.pack(expand=True, fill="both")

    # start the app
    root.mainloop()

# handling error exception
except mysql.connector.Error as e:
    messagebox.showerror("Database Error", "Connect To MySQL Before Run App!")
