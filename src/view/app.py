import tkinter as tk
from tkinter import messagebox
import mysql.connector
import time # Import time for delay in cleanup
import os # Import os for forced exit (if needed)
from typing import Callable, List # Import Callable and List for type hinting

# Import your tab classes
from view.camera import Camera
from view.checkout import Checkout
from view.customer import Customer
from view.login_page import LoginPage
from view.revenue import Revenue
from view.models import CustomerInfo, RevenueData, StaffInfo # Ensure necessary models are imported
from view.room_management import RoomManagement
from view.staff_management import StaffManagement
from view.revenue_chart import RevenueChart
from view.db.database import DB_Connector

import cv2 # Import cv2 at the top level

# Flag to control forced exit (Use with caution, only if clean exit fails)
FORCE_EXIT_ON_CLOSE = False # Keep False by default


class App(tk.Tk):
    # Initialize with data lists (loaded in main) and db_conn
    def __init__(self, customer_list: List[CustomerInfo], staff_list: List[StaffInfo], revenue_list: List[RevenueData], db_conn: DB_Connector):
        super().__init__()
        self.is_fullscreen = False
        self.title("Quản Lí Nhà Trọ")
        self.geometry("1280x720")
        self.configure(bg="#3B82F6")
        self.bind("<F11>", self.toggle_fullscreen)

        # --- Database Connection ---
        # Store the DB_Connector instance passed from main
        self.db_conn = db_conn
        if self.db_conn:
             print("[*] App initialized with database connection.")
        else:
             print("[!] App initialized without a valid database connection.")


        # --- Central Data Lists (Passed from main) ---
        self.customer_list = customer_list
        self.staff_list = staff_list
        self.revenue_list = revenue_list # This is the main list holding RevenueData objects
        print(f"[*] App received {len(self.customer_list)} customers, {len(self.staff_list)} staffs, {len(self.revenue_list)} revenue records.")


        # --- Data for Checkout Tab ---
        # This attribute will hold the CustomerInfo object selected by the user for checkout
        self.current_customer_for_checkout: CustomerInfo | None = None


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
        # self.button_frame.pack(side="right") # Don't pack initially


        # --- Tab Instances (initialized but not packed until show_main) ---
        self.tabs = {} # Dictionary to hold tab instances

        # Initialize tab instances. Pass necessary data and callbacks.
        # Camera tab needs parent (self)
        self.camera_tab: Camera | None = None # Initialize as None, created in show_main

        # Login Page - Initialize first and pack
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

    # --- Method to set the current customer for checkout (Called by Customer tab) ---
    def set_current_customer_for_checkout(self, customer: CustomerInfo):
        """Stores the selected customer data for the Checkout tab."""
        self.current_customer_for_checkout = customer
        print(f"[*] App received customer ID {getattr(customer, 'id', 'N/A')} for checkout.")


    # --- Callback method to add a revenue record (Called by Checkout tab) ---
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
                    # Check if the main window still exists before showing messagebox
                    if self.winfo_exists():
                         messagebox.showerror("Database Save Error", f"Could not save revenue record: {e}")


            # Tell the Revenue tab to refresh its display to include the new record
            # Check if the tab instance exists before calling the method
            if hasattr(self, 'revenue_tab') and self.revenue_tab and hasattr(self.revenue_tab, 'refresh_display'):
                 print("[*] Signaling Revenue tab to refresh display.")
                 self.revenue_tab.refresh_display()
            else:
                 print("[!] Revenue tab instance or refresh_display method not found.")

            # --- Clear the current customer data after successful checkout ---
            self.current_customer_for_checkout = None
            print("[*] Cleared current customer data in App after checkout.")

        else:
            print("[!] Received non-RevenueData object in add_revenue_record_callback.")
            # Check if the main window still exists before showing messagebox
            if self.winfo_exists():
                 messagebox.showwarning("Lỗi dữ liệu", "Đã nhận dữ liệu doanh thu không hợp lệ.")


    # --- New Callback for refreshing Room Management tab ---
    def refresh_room_management_callback(self) -> None:
        """
        Callback method called by the Customer tab when customer data that affects
        room occupancy is changed (added, edited, removed).
        This method signals the Room Management tab to refresh its display.
        """
        print("[*] App received signal to refresh Room Management tab.")
        # Check if the tab instance exists before calling the method
        if hasattr(self, 'room_management_tab') and self.room_management_tab and hasattr(self.room_management_tab, 'refresh_display'):
             print("[*] Signaling Room Management tab to refresh display.")
             self.room_management_tab.refresh_display()
        else:
             print("[!] Room Management tab instance or refresh_display method not found.")
    # --- End New Callback ---


    def show_main(self):
        """Called after successful login to set up and display the main application UI."""
        print("[*] Login successful. Setting up main application UI.")
        # Hide the login page
        self.login_frame.pack_forget()

        # Pack the app bar and button frame
        self.appbar.pack(fill="x")
        self.button_frame.pack(side="right") # Pack the button frame here

        # Initialize other tabs now that login is complete and DB is connected (handled in main)
        # Pass 'self' as the controller to tabs that need to interact with App data/methods
        # Pass callbacks where needed

        # Initialize Camera tab (needs parent)
        self.camera_tab = Camera(self) # Now initialized here after login

        # Initialize Checkout tab (needs parent, controller=self, and revenue_callback)
        self.checkout_tab = Checkout(self, self, self.add_revenue_record_callback,self.db_conn)

        # Initialize Customer tab (needs parent, show_tab, controller=self, customer_list, db_conn, refresh_room_management_callback)
        self.customer_tab = Customer(self, self.show_tab, self, self.customer_list, self.db_conn, self.refresh_room_management_callback)

        # Initialize Revenue tab (needs parent, revenue_list, db_conn)
        self.revenue_tab = Revenue(self, self.revenue_list, self.db_conn)

        # Initialize Room Management tab (needs parent, customer_list)
        self.room_management_tab = RoomManagement(self, self.customer_list)

        # Initialize Staff Management tab (needs parent, staff_list, db_conn)
        self.staff_management_tab = StaffManagement(self, self.staff_list, self.db_conn)

        # Initialize Revenue Chart tab (needs parent, customer_list - assuming)
        self.revenue_chart_tab = RevenueChart(self, self.customer_list)


        # Populate the tabs dictionary now that login is complete
        self.tabs = {
            "Camera": self.camera_tab,
            "Thanh Toán": self.checkout_tab,
            "Danh Sách Thuê": self.customer_tab,
            "Doanh thu": self.revenue_tab,
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

        self.show_tab("Camera") # show first tab by default
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
            # Check if the tab instance exists before calling the method
            if tab_name == "Thanh Toán" and hasattr(self, 'checkout_tab') and self.checkout_tab and hasattr(self.checkout_tab, 'refresh_display'):
                 print("[*] Showing Checkout tab, refreshing display.")
                 self.checkout_tab.refresh_display() # Call refresh on Checkout

            # If switching to Revenue, refresh its display from the central list
            # Check if the tab instance exists before calling the method
            elif tab_name == "Doanh thu" and hasattr(self, 'revenue_tab') and self.revenue_tab and hasattr(self.revenue_tab, 'refresh_display'):
                 print("[*] Showing Revenue tab, refreshing display.")
                 self.revenue_tab.refresh_display() # Call refresh on Revenue

            # If switching to Room Management, refresh its display
            # Check if the tab instance exists before calling the method
            elif tab_name == "Quản Lý Phòng" and hasattr(self, 'room_management_tab') and self.room_management_tab and hasattr(self.room_management_tab, 'refresh_display'):
                 print("[*] Showing Room Management tab, refreshing display.")
                 self.room_management_tab.refresh_display() # Call refresh on Room Management

            # Add similar logic for other tabs that need refresh when shown


    def on_closing(self):
        """Handles cleanup when the main window is closed."""
        print("[*] Closing main window...")

        # 1. Signal camera tab to stop its loop and release capture
        # This should also cancel Tkinter 'after' calls within the Camera tab
        # Add checks to ensure the tab instance and stop_camera method exist
        if hasattr(self, 'camera_tab') and self.camera_tab and hasattr(self.camera_tab, 'stop_camera'):
            try:
                self.camera_tab.stop_camera()
                print("[*] Camera stop signal sent and processed.")
            except Exception as e:
                print(f"[!] Error calling camera_tab.stop_camera(): {e}")
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
        time.sleep(0.1) # Reduced delay slightly


        # 4. Close database connection if it's open
        # The DB_Connector is now closed in the main function's finally block
        # if hasattr(self, 'db_conn') and self.db_conn:
        #      try:
        #          # Assuming this method closes the connection
        #          self.db_conn.closeBuffer()
        #          print("[✓] Database connection closed.")
        #      except Exception as e:
        #          print(f"[!] Error closing database connection: {e}")
        print("[*] Database connection closure is handled in main function.")


        # 5. Destroy the Tkinter window, which stops the mainloop
        try:
            # Check if the window still exists before destroying
            if self.winfo_exists():
                 self.destroy()
                 print("[✓] Tkinter window destroyed.")
            else:
                 print("[*] Tkinter window already destroyed.")
        except Exception as e:
             print(f"[!] Error destroying Tkinter window: {e}")


        # 6. Optional: Force exit if cleanup is still incomplete (Use with caution)
        if FORCE_EXIT_ON_CLOSE:
            print("[!] FORCE_EXIT_ON_CLOSE is True. Attempting os._exit(0).")
            os._exit(0) # This will terminate the process immediately

        self.quit()
        print("[*] Application shutdown sequence finished.")
        # The process should exit naturally now if all resources are released.


