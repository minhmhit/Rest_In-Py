import tkinter as tk
from tkinter import LabelFrame, messagebox
from tkinter import font, ttk # Import ttk
from datetime import datetime # Often needed even in login for consistency or logging

from view.models import StaffInfo

# --- Define colors --- (Keep consistent with other files)
COLOR_PRIMARY_BLUE = "#3B82F6"
COLOR_ACCENT_GREEN = "#28a745"
COLOR_ACCENT_RED = "#dc3545"
COLOR_ACCENT_TEAL = "#17a2b8"
COLOR_BACKGROUND_LIGHT = "#eef2f7" # Light background for main frame
COLOR_FRAME_BACKGROUND = "#f8f9fa" # Background for panels/frames
COLOR_MAIN_PANEL_BG = "#ffffff" # White background for main content areas
COLOR_TEXT_DARK = "#333333"    # Dark gray for text
COLOR_TEXT_MEDIUM = "#555555" # Medium gray for secondary text/labels
COLOR_BORDER_GRAY = "#cccccc" # Light gray border

# Mock StaffInfo if not available for testing standalone
# try:
# except ImportError:
#     print("Warning: staff_information.py not found. Using mock StaffInfo.")
#     class StaffInfo:
#          def __init__(self, id=None, name=None, sex=None, birthday=None, role=None, username=None, password=None, permissions=None):
#              self.id = id
#              self.name = name
#              self.sex = sex
#              self.birthday = birthday
#              self.role = role
#              self.username = username if username is not None else ""
#              self.password = password if password is not None else ""
#              self.permissions = permissions
#          def haveNone(self): # Example check
#              return any(getattr(self, field) is None or getattr(self, field) == "" for field in ['username', 'password'])
#          def __str__(self):
#              return f"StaffInfo(ID: {self.id}, Username: {self.username}, Role: {self.role})"


class LoginPage(tk.Frame):
    def __init__(self, parent, show_main, staff_list):
        super().__init__(parent, bg=COLOR_BACKGROUND_LIGHT) # Set main frame background
        self.parent = parent
        self.show_main = show_main  # Function to show main UI
        self.staff_list = staff_list # List of StaffInfo objects

        # --- Login Screen Container (LabelFrame) ---
        self.login_screen = LabelFrame(
            self, text="ĐĂNG NHẬP", # LabelFrame title
            bg=COLOR_MAIN_PANEL_BG, # White background
            fg=COLOR_TEXT_MEDIUM, # Title text color
            font=("Arial", 14, "bold"), # Title font
            padx=20, pady=20, # Reduced padding inside LabelFrame
            bd=1, relief=tk.GROOVE # Border style
        )
        # Pack the LabelFrame to center and expand
        self.login_screen.pack(expand=True, fill="both", padx=50, pady=50) # Padding around the login box


        # --- Inner Frame for Centering Content ---
        # Use a simple Frame to put content inside the LabelFrame for grid layout
        self.login_content_frame = tk.Frame(self.login_screen, bg=COLOR_MAIN_PANEL_BG)
        # Pack this inner frame to center its contents within the LabelFrame
        self.login_content_frame.pack(expand=True)

        # Center the grid inside this frame
        self.login_content_frame.columnconfigure(0, weight=1)
        self.login_content_frame.columnconfigure(1, weight=1)
        self.login_content_frame.rowconfigure("all", weight=1) # Not strictly necessary for this layout but good practice

        # --- Widgets inside login_content_frame ---

        # Title Label
        self.title_label = tk.Label(
            self.login_content_frame, text="ĐĂNG NHẬP HỆ THỐNG",
            font=("Arial", 20, "bold"), fg=COLOR_TEXT_DARK, bg=COLOR_MAIN_PANEL_BG
        )
        # Span across columns, pady below title
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="nsew")

        # Username Label and Entry
        self.label_username = tk.Label(
            self.login_content_frame, text="Tên đăng nhập:", font=("Arial", 10, "bold"),
            bg=COLOR_MAIN_PANEL_BG, fg=COLOR_TEXT_DARK
        )
        self.label_username.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.entry_username = tk.Entry(
            self.login_content_frame, font=("Arial", 10), width=30, # Fixed width or use sticky="ew"
            bd=1, relief=tk.SOLID # Add border
        )
        self.entry_username.grid(row=1, column=1, padx=5, pady=5, sticky="ew") # Expand entry horizontally
        self.entry_username.insert(0, "Nhập tên đăng nhập...") # Placeholder text
        self.entry_username.config(fg="gray")

        # Password Label and Entry
        self.label_password = tk.Label(
            self.login_content_frame, text="Mật khẩu:", font=("Arial", 10, "bold"),
            bg=COLOR_MAIN_PANEL_BG, fg=COLOR_TEXT_DARK
        )
        self.label_password.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.entry_password = tk.Entry(
            self.login_content_frame, show="", font=("Arial", 10), width=30, # show="" initially for placeholder
            bd=1, relief=tk.SOLID # Add border
        )
        self.entry_password.grid(row=2, column=1, padx=5, pady=5, sticky="ew") # Expand entry horizontally
        self.entry_password.insert(0, "Nhập mật khẩu...") # Placeholder text
        self.entry_password.config(fg="gray")


        # Login Button
        button_font = ("Arial", 10, "bold")
        button_pady = 8
        button_padx = 20

        self.button_login = tk.Button(
            self.login_content_frame, text="ĐĂNG NHẬP", font=button_font,
            bg=COLOR_PRIMARY_BLUE, fg="white",
            activebackground="#0056b3", activeforeground="white",
            relief=tk.RAISED, padx=button_padx, pady=button_pady, cursor="hand2",
            command=self.login # Call the login method
        )
        # Place button below entries, span columns, add vertical padding
        self.button_login.grid(row=3, column=0, columnspan=2, pady=20, sticky="nsew") # Make button fill width


        # --- Bind events for placeholders ---
        self.entry_username.bind("<FocusIn>", lambda event: self.clear_placeholder(self.entry_username, "Nhập tên đăng nhập..."))
        self.entry_username.bind("<FocusOut>", lambda event: self.restore_placeholder(self.entry_username, "Nhập tên đăng nhập..."))

        self.entry_password.bind("<FocusIn>", lambda event: self.clear_placeholder(self.entry_password, "Nhập mật khẩu...", hide=True))
        self.entry_password.bind("<FocusOut>", lambda event: self.restore_placeholder(self.entry_password, "Nhập mật khẩu...", hide=True))

        # Bind <Return> key to the login button
        self.entry_username.bind("<Return>", lambda event=None: self.button_login.invoke())
        self.entry_password.bind("<Return>", lambda event=None: self.button_login.invoke())
        self.button_login.bind("<Return>", lambda event=None: self.button_login.invoke()) # Also bind return key on the button itself


    # --- Placeholder methods ---
    def clear_placeholder(self, entry, placeholder, hide=False):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg=COLOR_TEXT_DARK) # Change text color to dark
            if hide:
                entry.config(show="*") # Hide text for password

    def restore_placeholder(self, entry, placeholder, hide=False):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg="gray") # Restore placeholder color
            if hide:
                entry.config(show="") # Show placeholder text

    # --- Login Logic (FIXED security flaw) ---
    def login(self):
        username = self.entry_username.get().strip() # Get and strip whitespace
        password = self.entry_password.get().strip() # Get and strip whitespace

        # Avoid trying to log in with placeholder text
        if username == "Nhập tên đăng nhập..." or password == "Nhập mật khẩu...":
             messagebox.showwarning("Cảnh báo", "Vui lòng nhập tên đăng nhập và mật khẩu.")
             return

        authenticated_staff = None
        # Iterate through the staff list to find the matching user AND check their password
        for staff_member in self.staff_list:
            # Assuming StaffInfo object has 'username' and 'password' attributes (strings)
            if staff_member.username == username:
                # Found the user, now check THIS user's password
                if staff_member.password == password:
                    authenticated_staff = staff_member # Authentication successful
                    break # Found and authenticated, exit loop

                else:
                    # Found user, but password incorrect for this specific user
                    messagebox.showwarning("Đăng Nhập Thất Bại", f"Sai mật khẩu cho tài khoản: {username}!")
                    self.reset_login_fields() # Clear fields and restore placeholders
                    return # Stop the login attempt immediately

        # After the loop, check if authentication was successful
        if authenticated_staff:
            # Login successful
            # You might want to store the authenticated_staff object somewhere accessible
            # self.authenticated_user = authenticated_staff # Example
            messagebox.showinfo("Đăng Nhập Thành Công", f"Xin Chào {authenticated_staff.name}!") # Use staff name in welcome
            self.show_main() # Call the function to switch to the main application UI
        else:
            # Loop finished, user was not found
            messagebox.showerror("Đăng Nhập Thất Bại", "Tên đăng nhập hoặc mật khẩu không hợp lệ.")
            self.reset_login_fields()


    def reset_login_fields(self):
        """Helper to clear login entries and restore placeholders."""
        self.entry_username.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        # Restore placeholders manually after clearing
        self.restore_placeholder(self.entry_username, "Nhập tên đăng nhập...")
        self.restore_placeholder(self.entry_password, "Nhập mật khẩu...", hide=True)
