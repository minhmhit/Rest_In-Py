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
import cv2  # Import cv2 at the top level

class App(tk.Tk):
    def __init__(self, customer_list, staff_list):
        super().__init__()
        self.title("Quản Lí Nhà Trọ")
        self.geometry("1280x720")
        self.configure(bg="#3B82F6")

        self.customer_list = customer_list
        self.staff_list = staff_list
        self.db_conn = DB_Connector()  # Initialize the database connector here

        # App bar
        self.appbar = tk.Frame(self, bg="#3B82F6", height=50)
        self.title_label = tk.Label(
            self.appbar,
            text="Quản Lí Nhà Trọ",
            bg="#3B82F6",
            fg="white",
            font=("Arial", 16, "bold"),
        )
        self.title_label.pack(side="left", padx=10)
        self.appbar.pack(fill="x")

        # Button frame
        self.button_frame = tk.Frame(self.appbar, bg="#3B82F6")
        self.buttons = []
        self.button_frame.pack(side="right")

        # Tab dictionary
        self.tabs = {}
        self.customer_information = CustomerInfo()
        self.camera_tab = Camera(self)
        self.login_frame = LoginPage(self, self.show_main, self.staff_list)
        self.login_frame.pack(expand=True, fill="both")

        # close all buffer after delete window
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def show_main(self):
        self.login_frame.pack_forget()  # hide login page

        # Create tabs
        self.tabs = {
            "Camera": self.camera_tab,
            "Thanh Toán": Checkout(self, self.customer_information),
            "Danh Sách Thuê": Customer(self, self.show_tab, self.customer_information, self.customer_list, self.db_conn),
            "Doanh thu": Revenue(self),
            "Quản Lý Phòng": RoomManagement(self,self.customer_list),
            "Quản Lý Nhân  Viên": StaffManagement(self, self.staff_list, self.db_conn),
            "Biểu Đồ Doanh Thu": RevenueChart(self)
        }

        # Create buttons to switch tabs
        for name in self.tabs.keys():
            btn = tk.Button(
                self.button_frame,
                width=16,
                text=name,
                bd=0,
                bg="#3B82F6",
                fg="white",
                command=lambda n=name: self.show_tab(n),
            )
            btn.pack(side="left", padx=5)
            self.buttons.append(btn)

        self.show_tab("Camera")  # show first tab by default

    def show_tab(self, tab_name):
        for name, tab in self.tabs.items():
            if tab:
                tab.pack_forget()
        if tab_name in self.tabs and self.tabs[tab_name]:
            self.tabs[tab_name].pack(expand=True, fill="both")

    def on_closing(self):
        self.stop_camera()
        self.destroy()
        self.quit()

    def stop_camera(self):
        if hasattr(self, 'camera_tab'):
            self.camera_tab.running = False  # Stop the update_frame loop
            if self.camera_tab.after_id is not None:
                self.camera_tab.show_camera.after_cancel(self.camera_tab.after_id)
                self.camera_tab.after_id = None

            if hasattr(self.camera_tab, 'cap') and self.camera_tab.cap.isOpened():
                self.camera_tab.cap.release()
                print("Camera released.")  # For debugging

        cv2.destroyAllWindows()
        print("OpenCV windows destroyed.") # For debugging

def main():
    try:
        db_conn = DB_Connector()
        customer_list = db_conn.getCustomersFromDatabase()
        staff_list = db_conn.getStaffsFromDatabase()

        app = App(customer_list, staff_list)
        app.mainloop()

        # close Database
        db_conn.closeBuffer()

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", "Connect To MySQL Before Run App!")

if __name__ == "__main__":
    main()
