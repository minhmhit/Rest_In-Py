from view.db.database import DB_Connector
from tkinter import messagebox
import mysql.connector

from view.root_window import App

def main():
    try:
        db_conn = DB_Connector()
        customer_list = db_conn.getCustomersFromDatabase()
        staff_list = db_conn.getStaffsFromDatabase()
        revenue_list = db_conn.getRevenueFromDatabase()

        app = App(customer_list, staff_list, revenue_list)
        app.mainloop()

        # close Database
        db_conn.closeBuffer()

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", "Connect To MySQL Before Run App!")

if __name__ == "__main__":
    main()
