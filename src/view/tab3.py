import tkinter as tk

class Tab3(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#F5F5F5")
        label = tk.Label(self, text="Welcome to Tab 3!", font=("Arial", 16), bg="#bd92c4", fg="white")
        label.pack(expand=True)
