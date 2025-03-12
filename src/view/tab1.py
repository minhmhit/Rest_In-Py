import tkinter as tk

class Tab1(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#F5F5F5")
        label = tk.Label(self, text="Welcome to Tab 1!", font=("Arial", 16), bg="#bd92c4", fg="white")
        label.pack(expand=True)
