import tkinter as tk
from tkinter import LabelFrame, messagebox
from tkinter import font

class LoginPage(tk.Frame):
    def __init__(self, parent, show_main):
        super().__init__(parent)
        self.parent = parent
        self.show_main = show_main  # Function to show main UI

        # Centering login screen
        self.login_screen = LabelFrame(self, bg="#e3e3e3", padx=200, pady=200)
        self.login_screen.pack(expand=True,fill="both", anchor="center")
        
        self.label = tk.Label(self.login_screen, text="ĐĂNG NHẬP TÀI KHOẢN", 
                               font=font.Font(family="Arial", size=20, weight="bold"),
                               anchor='center', justify='center')
        self.label.pack()
        
        self.label_username = tk.Label(self.login_screen, text="Username:")
        self.label_username.pack(pady=5)
        
        self.entry_username = tk.Entry(self.login_screen, fg='gray')
        self.entry_username.insert(0, "Enter your username...")
        self.entry_username.pack(pady=5)
        
        self.label_password = tk.Label(self.login_screen, text="Password:")
        self.label_password.pack(pady=5)
        
        self.entry_password = tk.Entry(self.login_screen, show="*", fg='gray')
        self.entry_password.insert(0, "Enter your password...")
        self.entry_password.pack(pady=5)
        
        self.button_login = tk.Button(self.login_screen, text="Login", command=self.login)
        self.button_login.pack(pady=10)

        # Bind event for placeholders
        self.entry_username.bind("<FocusIn>", lambda event: self.clear_placeholder(self.entry_username, "Enter your username..."))
        self.entry_username.bind("<FocusOut>", lambda event: self.restore_placeholder(self.entry_username, "Enter your username..."))

        self.entry_password.bind("<FocusIn>", lambda event: self.clear_placeholder(self.entry_password, "Enter your password...", hide=True))
        self.entry_password.bind("<FocusOut>", lambda event: self.restore_placeholder(self.entry_password, "Enter your password...", hide=True))
    
    def clear_placeholder(self, entry, placeholder, hide=False):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="black")
            if hide:
                entry.config(show="*")
    
    def restore_placeholder(self, entry, placeholder, hide=False):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg="gray")
            if hide:
                entry.config(show="")

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        if username == "1" and password == "1":
            messagebox.showinfo("Dang Nhap Thanh Cong", f"Xin Chao {username}!")
            self.show_main()  # Switch to the main application
        else:
            messagebox.showerror("Dang Nhap That Bai", "Tai Khoan Hay Mat Khau Khong Hop Le")
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
            self.restore_placeholder(self.entry_username, "Enter your username...")
            self.restore_placeholder(self.entry_password, "Enter your password...", hide=True)
