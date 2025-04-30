import tkinter as tk
from tkinter import messagebox
import mysql.connector # Assuming you use mysql.connector

# Import your tab classes
from view.camera import Camera # Assuming Camera is in view/camera.py
from view.checkout import Checkout # Assuming Checkout is in view/checkout.py
from view.customer import Customer # Assuming Customer is in view/customer.py
from view.revenue import Revenue # Assuming Revenue is in view/revenue.py
from view.room_management import RoomManagement # Assuming RoomManagement is in view/room_management.py
from view.staff_management import StaffManagement # Assuming StaffManagement is in view/staff_management.py
from view.revenue_chart import RevenueChart # Assuming RevenueChart is in view/revenue_chart.py
from view.login_page import LoginPage # Import the LoginPage

# Import your models
from view.models import CustomerInfo, RevenueData # Assuming models are in view/models.py

# Import your database connector
from view.db.database import DB_Connector # Assuming DB_Connector is in view/db/database.py

import cv2 # Import cv2 for camera cleanup
import time # Import time for delay in cleanup
import os # Import os for forced exit (if needed)
from typing import Callable # Import Callable for type hinting


# Flag to control forced exit (Use with caution, only if clean exit fails)
FORCE_EXIT_ON_CLOSE = False # Keep False by default


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.is_fullscreen = False
        self.title("Quản Lí Nhà Trọ")
        self.geometry("1280x720")
        self.configure(bg="#3B82F6")
        self.bind("<F11>", self.toggle_fullscreen)

        # --- Database Connection ---
        self.db_conn = None
        try:
            self.db_conn = DB_Connector()
            print("[*] Database connection established.")
        except mysql.connector.Error as e:
            print(f"[!] Database connection error: {e}")
            messagebox.showerror("Database Error", "Không thể kết nối tới MySQL. Vui lòng kiểm tra kết nối và thử lại.")
            # Decide how to handle DB connection failure: exit, or run with limited functionality
            # For now, we'll allow the app to start but DB operations will fail.
            self.db_conn = None # Ensure db_conn is None if connection failed
        except Exception as e:
            print(f"[!] An unexpected error occurred during DB connection: {e}")
            messagebox.showerror("Application Error", f"Đã xảy ra lỗi không mong muốn khi kết nối DB: {e}")
            self.db_conn = None


        # --- Central Data Lists (Loaded from DB or initialized empty) ---
        self.customer_list = []
        self.staff_list = []
        self.revenue_list = [] # This is the main list holding RevenueData objects

        # Load initial data if DB connection was successful
        if self.db_conn:
            try:
                self.customer_list = self.db_conn.getCustomersFromDatabase() # Assuming this method exists
                self.staff_list = self.db_conn.getStaffsFromDatabase()     # Assuming this method exists
                self.revenue_list = self.db_conn.getRevenueFromDatabase()   # Assuming this method exists
                print(f"[*] Loaded {len(self.customer_list)} customers, {len(self.staff_list)} staffs, {len(self.revenue_list)} revenue records from DB.")
            except Exception as e:
                print(f"[!] Error loading initial data from DB: {e}")
                messagebox.showwarning("Database Load Error", f"Không thể tải dữ liệu ban đầu từ DB: {e}")
                # Data lists will remain empty


        # --- App bar (initially hidden, shown after login) ---
        self.appbar = tk.Frame(self, bg="#3B82F6", height=50)
        self.title_label = tk.Label(
            self.appbar,
            text="Quản Lí Nhà Trọ",
            bg="#3B82F6",
            fg="white",
            font=("Arial", 16, "bold"),
        )
        self.title_label.pack(side="left", padx=10)
        # self.appbar.pack(fill="x") # Don't pack initially


        # --- Button frame for tabs (initially hidden, shown after login) ---
        self.button_frame = tk.Frame(self.appbar, bg="#3B82F6")
        self.buttons = [] # To store tab buttons
        self.button_frame.pack(side="right")
        # self.button_frame.pack(side="right") # Don't pack initially


        # --- Tab Instances (initialized but not packed until show_main) ---
        self.tabs = {} # Dictionary to hold tab instances

        # CustomerInfo object to pass data to Checkout (assuming Customer tab updates this)
        self.customer_information_temp = CustomerInfo() # This will hold data of the customer selected for checkout

        # Initialize tab instances. Pass necessary data and callbacks.
        # Camera tab needs parent (self)
        self.camera_tab = Camera(self) # Assuming Camera.__init__ takes parent

        # Checkout tab needs parent (self), the customer_information_temp object,
        # the callback method to receive finalized revenue data, and db_conn
        self.checkout_tab = Checkout(self, self.customer_information_temp, self.add_revenue_record_callback, self.db_conn)

        # Revenue tab needs parent (self), the central revenue_list, and the db_conn
        self.revenue_tab = Revenue(self, self.revenue_list, self.db_conn)

        # Other tabs (assuming they need parent, data lists, db_conn, show_tab callback)
        # Pass the show_tab method to Customer tab so it can switch tabs
        # Pass the new refresh_room_management_callback to the Customer tab
        # CORRECTED LINE: Added self.refresh_room_management_callback as the last argument
        self.customer_tab = Customer(self, self.show_tab, self.customer_information_temp, self.customer_list, self.db_conn, self.refresh_room_management_callback)

        # Room Management tab needs parent and the customer_list
        self.room_management_tab = RoomManagement(self, self.customer_list) # Assuming it needs customer_list

        self.staff_management_tab = StaffManagement(self, self.staff_list, self.db_conn) # Assuming it needs staff_list and db_conn
        self.revenue_chart_tab = RevenueChart(self, self.customer_list) # Assuming it needs customer_list


        # --- Login Page ---
        # Initialize Login page, passing the show_main method as the success callback
        self.login_frame = LoginPage(self, self.show_main, self.staff_list)
        # Pack the login frame first so it's the initial view
        self.login_frame.pack(expand=True, fill="both")


        # --- Set window close protocol ---
        # This ensures on_closing is called when the window is closed (e.g., by clicking the 'X' button)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # --- DO NOT show initial tab here. show_main will handle this after login. ---
        # self.show_tab("Camera") # Remove this line


    def toggle_fullscreen(self,event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.attributes("-fullscreen", self.is_fullscreen)

    def show_main(self):
        """Called after successful login to set up and display the main application UI."""
        print("[*] Login successful. Setting up main application UI.")
        # Hide the login page
        self.login_frame.pack_forget()

        # Pack the app bar and button frame
        self.appbar.pack(fill="x")

        # Populate the tabs dictionary now that login is complete
        self.tabs = {
            "Camera": self.camera_tab,
            "Thanh Toán": self.checkout_tab,
            "Doanh thu": self.revenue_tab,
            "Danh Sách Thuê": self.customer_tab,
            "Quản Lý Phòng": self.room_management_tab,
            "Quản Lý Nhân Viên": self.staff_management_tab,
            "Biểu Đồ Doanh Thu": self.revenue_chart_tab,
        }

        # Create buttons to switch tabs
        # Clear existing buttons first if show_main could be called multiple times (unlikely here)
        for btn in self.buttons:
            btn.destroy()
        self.buttons = [] # Reset the list

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

        # Show the first tab after login (e.g., Camera)
        self.show_tab("Camera")
        print("[✓] Main application UI setup complete.")


    def show_tab(self, tab_name):
        """Switches the currently displayed tab."""
        print(f"[*] Switching to tab: {tab_name}")
        # Hide all tabs
        for name, tab in self.tabs.items():
            if tab and hasattr(tab, 'pack_forget'):
                tab.pack_forget()

        # Show the requested tab
        if tab_name in self.tabs and self.tabs[tab_name]:
            self.tabs[tab_name].pack(expand=True, fill="both")

            # --- Trigger refresh for specific tabs when shown ---
            # If switching to Checkout, load the current customer data
            if tab_name == "Thanh Toán" and hasattr(self.checkout_tab, 'refresh_display'):
                 print("[*] Showing Checkout tab, refreshing display.")
                 self.checkout_tab.refresh_display() # Call refresh on Checkout

            # If switching to Revenue, refresh its display from the central list
            elif tab_name == "Doanh thu" and hasattr(self.revenue_tab, 'refresh_display'):
                 print("[*] Showing Revenue tab, refreshing display.")
                 self.revenue_tab.refresh_display() # Call refresh on Revenue

            # If switching to Room Management, refresh its display
            elif tab_name == "Quản Lý Phòng" and hasattr(self.room_management_tab, 'refresh_display'):
                 print("[*] Showing Room Management tab, refreshing display.")
                 self.room_management_tab.refresh_display() # Call refresh on Room Management


            # Add similar logic for other tabs that need refresh when shown


    def add_revenue_record_callback(self, revenue_data: RevenueData) -> None:
        """
        Callback method provided to the Checkout tab to add a new revenue record.
        This method is called by the Checkout tab when a checkout is finalized.
        """
        print(f"[*] App received new revenue record from Checkout: {revenue_data}")
        # Add the new record to the central revenue list managed by the App
        if isinstance(revenue_data, RevenueData):
            self.revenue_list.append(revenue_data)
            print("[✓] Added record to central revenue_list in App.")

            # --- Optional: Save to Database ---
            # You would typically save the new record to the database here
            if self.db_conn:
                try:
                    # Assuming DB_Connector has a method to save revenue data
                    # Replace with your actual method name and parameters
                    # self.db_conn.save_revenue(revenue_data)
                    print("[*] Database save logic for new revenue record would go here.")
                except Exception as e:
                    print(f"[!] Error saving new revenue record to database: {e}")
                    messagebox.showerror("Database Save Error", f"Could not save revenue record: {e}")


            # Tell the Revenue tab to refresh its display to include the new record
            if hasattr(self.revenue_tab, 'refresh_display'):
                 print("[*] Signaling Revenue tab to refresh display.")
                 self.revenue_tab.refresh_display()
            else:
                 print("[!] Revenue tab instance or refresh_display method not found.")

        else:
            print("[!] Received non-RevenueData object in add_revenue_record_callback.")


    # --- New Callback for refreshing Room Management tab ---
    def refresh_room_management_callback(self) -> None:
        """
        Callback method called by the Customer tab when customer data that affects
        room occupancy is changed (added, edited, removed).
        This method signals the Room Management tab to refresh its display.
        """
        print("[*] App received signal to refresh Room Management tab.")
        if hasattr(self.room_management_tab, 'refresh_display'):
             print("[*] Signaling Room Management tab to refresh display.")
             self.room_management_tab.refresh_display()
        else:
             print("[!] Room Management tab instance or refresh_display method not found.")
    # --- End New Callback ---


    def on_closing(self):
        """Handles cleanup when the main window is closed."""
        print("[*] Closing main window...")

        # 1. Signal camera tab to stop its loop and release capture
        # This should also cancel Tkinter 'after' calls within the Camera tab
        if hasattr(self, 'camera_tab') and self.camera_tab and hasattr(self.camera_tab, 'stop_camera'):
            self.camera_tab.stop_camera()
            print("[*] Camera stop signal sent.")
        else:
            print("[!] Camera tab instance or stop_camera method not found during closing.")


        # 2. Explicitly destroy any OpenCV windows
        # This should happen after camera capture is released
        try:
            cv2.destroyAllWindows()
            print("[✓] Explicitly destroyed OpenCV windows.")
        except Exception as e:
             print(f"[!] Error destroying OpenCV windows: {e}")


        # 3. Add a small delay to allow resources to be released by the OS/libraries
        # Keeping the delay, might help with resource finalization
        time.sleep(0.5) # Sleep for 500 milliseconds

        # 4. Close database connection if it's open
        if hasattr(self, 'db_conn') and self.db_conn:
             try:
                 # Assuming this method closes the connection
                 self.db_conn.closeBuffer()
                 print("[✓] Database connection closed.")
             except Exception as e:
                 print(f"[!] Error closing database connection: {e}")

        # 5. Destroy the Tkinter window, which stops the mainloop
        try:
            self.destroy()
            print("[✓] Tkinter window destroyed.")
        except Exception as e:
             print(f"[!] Error destroying Tkinter window: {e}")


        # 6. Optional: Force exit if cleanup is still incomplete (Use with caution)
        if FORCE_EXIT_ON_CLOSE:
            print("[!] FORCE_EXIT_ON_CLOSE is True. Attempting os._exit(0).")
            os._exit(0) # This will terminate the process immediately

        print("[*] Application shutdown sequence finished.")
