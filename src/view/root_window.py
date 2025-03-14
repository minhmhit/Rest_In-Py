import tkinter as tk
from login_page import LoginPage
from tab2 import Tab2
from tab3 import Tab3
from tab4 import Tab4
from tab5 import Tab5
from camera import Camera

# main window
root = tk.Tk()
root.geometry("1280x720")
root.configure(bg="#3B82F6")

# app bar 
appbar = tk.Frame(root, bg="#3B82F6", height=50)
title = tk.Label(appbar, text="Màn Hình Chính", bg="#3B82F6", fg="white", font=("Arial", 16, "bold"))

# buttons for switching tabs 
button_frame = tk.Frame(appbar, bg="#3B82F6")
buttons = []

# dictionary to store tab frames 
tabs = {}

def show_main():
    login_frame.pack_forget()  # Hide login page
    appbar.pack(fill="x")  # Show the app bar
    title.pack(side="left", padx=10)
    button_frame.pack(side="right")

    # Create and show tabs
    global tabs
    tabs = {
        "Camera": Camera(root),
        "Tab 2": Tab2(root),
        "Tab 3": Tab3(root),
        "Tab 4": Tab4(root),
        "Tab 5": Tab5(root),
    }

    # create buttons to switch tabs
    for name in tabs.keys():
        btn = tk.Button(button_frame, width=16, text=name, bd=0, bg="#3B82F6", fg="white",
                        command=lambda n=name: show_tab(n))
        btn.pack(side="left", padx=5)
        buttons.append(btn)

    show_tab("Camera")  # show first tab by default

def show_tab(tab_name):
    for tab in tabs.values():
        tab.pack_forget()
    tabs[tab_name].pack(expand=True, fill="both")

# create the login page (only this is visible at start)
login_frame = LoginPage(root, show_main)
login_frame.pack(expand=True, fill="both")

# start the app
root.mainloop()
