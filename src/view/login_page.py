import tkinter as tk
from tkinter import messagebox
from tkinter import font

class LoginPage(tk.Frame):
    def __init__(self, parent, show_main):
        super().__init__(parent)
        self.parent = parent
        self.show_main = show_main  # function to show main UI
        
        self.label = tk.Label(self, text="ĐĂNG NHẬP TÀI KHOẢN",font=font.Font(family="Arial", size=20, weight="bold"), anchor='center', justify='center')
        self.label.pack()
        
        self.label_username = tk.Label(self, text="Username:")
        self.label_username.pack(pady=5)
        
        self.entry_username = tk.Entry(self)
        self.entry_username.pack(pady=5)
        
        self.label_password = tk.Label(self, text="Password:")
        self.label_password.pack(pady=5)
        
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack(pady=5)
        
        self.button_login = tk.Button(self, text="Login", command=self.login)
        self.button_login.pack(pady=10)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        if username == "1" and password == "1":
            messagebox.showinfo("Login Successful", "Welcome!")
            self.show_main()  # Switch to the main application
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)

