import tkinter as tk
from tkinter import messagebox
import mysql.connector
from typing import List # Import Callable and List for type hinting

from view.app import App
from view.models import CustomerInfo, RevenueData, StaffInfo
from view.db.database import DB_Connector

def main():
    """Main function to initialize and run the application."""
    db_conn = None
    customer_list: List[CustomerInfo] = []
    staff_list: List[StaffInfo] = []
    revenue_list: List[RevenueData] = []

    try:
        db_conn = DB_Connector()
        print("[*] Database connection established in main.")
        # Load initial data
        customer_list = db_conn.getCustomersFromDatabase()
        staff_list = db_conn.getStaffsFromDatabase()
        revenue_list = db_conn.getRevenueFromDatabase()
        print(f"[*] Loaded {len(customer_list)} customers, {len(staff_list)} staffs, {len(revenue_list)} revenue records from DB in main.")


        # Pass the loaded data and the db_conn instance to the App
        app = App(customer_list, staff_list, revenue_list, db_conn)

        # Start the Tkinter main loop
        app.mainloop()

    except mysql.connector.Error as e:
        print(f"[!] Database connection error in main: {e}")
        # Check if a root window exists before showing messagebox
        if tk._default_root is not None:
             messagebox.showerror("Database Error", "Không thể kết nối tới MySQL. Vui lòng kiểm tra kết nối và thử lại.")
        else:
             print("Error: Could not connect to MySQL. Tkinter root not initialized.")

    except Exception as e:
        print(f"[!] An unexpected error occurred in main: {e}")
        # Check if a root window exists before showing messagebox
        if tk._default_root is not None:
             messagebox.showerror("Application Error", f"Đã xảy ra lỗi không mong muốn:\n{e}")
        else:
             print(f"Error: An unexpected error occurred: {e}. Tkinter root not initialized.")

    finally:
        # Ensure database connection is closed even if errors occur
        if db_conn:
            try:
                db_conn.closeBuffer()
                print("[✓] Database connection closed in main finally block.")
            except Exception as e:
                print(f"[!] Error closing database connection in main finally block: {e}")


if __name__ == "__main__":
    main()
