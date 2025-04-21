import customtkinter as ctk
from tkinter import font, messagebox

class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, show_main, staff_list):
        super().__init__(parent)
        self.parent = parent
        self.show_main = show_main  # Function to show main UI
        self.staff_list = staff_list

        # Configure grid layout for centering
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.login_frame = ctk.CTkFrame(self)
        self.login_frame.grid(row=0, column=0, padx=40, pady=40, sticky="nsew")
        self.login_frame.grid_columnconfigure(0, weight=1)

        self.title_font = ctk.CTkFont(family="Arial", size=24, weight="bold")
        self.label = ctk.CTkLabel(self.login_frame, text="ĐĂNG NHẬP TÀI KHOẢN", font=self.title_font)
        self.label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        self.username_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Tên đăng nhập")
        self.username_entry.grid(row=1, column=0, padx=20, pady=(10, 10), sticky="ew")

        self.password_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Mật khẩu", show="*")
        self.password_entry.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="ew")

        self.login_button = ctk.CTkButton(self.login_frame, text="Đăng nhập", command=self.login)
        self.login_button.grid(row=3, column=0, padx=20, pady=(20, 20), sticky="ew")

    def isUsernameExist(self, account_username) -> bool:
        for staff_member in self.staff_list:
            if staff_member.username == account_username:
                return True
        return False

    def isPasswordCorrect(self, account_password) -> bool:
        for staff_member in self.staff_list:
            if staff_member.password == account_password:
                return True
        return False

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.isUsernameExist(username):
            if self.isPasswordCorrect(password):
                messagebox.showinfo("Đăng nhập thành công", f"Xin chào {username}!")
                self.show_main()  # Switch to the main application
            else:
                messagebox.showwarning("Đăng nhập thất bại", f"Sai mật khẩu cho tài khoản: {username}!")
        else:
            messagebox.showerror("Đăng nhập thất bại", "Tài khoản hoặc mật khẩu không hợp lệ")
            self.username_entry.delete(0, ctk.END)
            self.password_entry.delete(0, ctk.END)
            self.username_entry.focus()
