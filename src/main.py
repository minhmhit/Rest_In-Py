# from view.db.database import DB_Connector
# from tkinter import messagebox
# import mysql.connector

from view.app import App

# --- Main execution block ---
def main():
    """Main function to initialize and run the application."""
    app = App()
    app.mainloop()
    print("[*] App mainloop finished.")

if __name__ == "__main__":
    main()
