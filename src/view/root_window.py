import tkinter as tk

from camera import Camera
from checkout import Checkout
from customer import Customer
from login_page import LoginPage
from settings import Settings
from revenue import Revenue
from customer_information import CustomerInfo

# main window
root = tk.Tk()
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
customer_controller = CustomerInfo

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
        "Thanh Toán": Checkout(root,customer_controller),
        "Danh Sách Thuê": Customer(root,show_tab,customer_controller),
        "Doanh thu": Revenue(root),
        "Cài Đặt": Settings(root),
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
