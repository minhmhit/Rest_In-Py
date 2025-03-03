# tạo module view
import tkinter 

# initialize
root = tkinter.Tk()
root.geometry("1280x720")
root.title("Window")

# frame
frame = tkinter.Frame(root)
frame.grid(sticky="nsew")

# app bar,interact screen 
root.grid_rowconfigure(0, weight=2)  # App bar (fixed height)
root.grid_rowconfigure(1, weight=20)  # Main content (expands)
root.grid_columnconfigure(0, weight=1)

# Create the app bar (10% height of the window)
app_bar = tkinter.LabelFrame(root, bg="black", text="App Bar", fg="white",bd=0,)
app_bar.grid(row=0, column=0, sticky="nsew")

# Create the main content area
main_content = tkinter.LabelFrame(root, bg="white", text="Main Content",bd=0)
main_content.grid(row=1, column=0, sticky="nsew")


# run app
root.mainloop()