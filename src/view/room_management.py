import tkinter as tk
from tkinter import messagebox, ttk
import platform
from datetime import datetime, date # Import date (if needed for customer info display)

from view.models import CustomerInfo # Assume CustomerInfo is correctly imported
# from database import DB_Connector # Assume DB_Connector is correctly imported if needed here

# --- Define colors --- (Keep consistent)
COLOR_PRIMARY_BLUE = "#3B82F6"
COLOR_ACCENT_GREEN = "#28a745"
COLOR_ACCENT_RED = "#dc3545"
COLOR_ACCENT_TEAL = "#17a2b8"
COLOR_BACKGROUND_LIGHT = "#eef2f7"
COLOR_FRAME_BACKGROUND = "#f8f9fa"
COLOR_MAIN_PANEL_BG = "#ffffff"
COLOR_TEXT_DARK = "#333333"
COLOR_TEXT_MEDIUM = "#555555"
COLOR_BORDER_GRAY = "#cccccc"

# --- Define all possible room numbers ---
# Pattern: 101-105, 201-205, ..., 901-905
# Ensure this matches the room numbers used elsewhere (e.g., in Customer tab)
ALL_ROOM_NUMBERS = [f"{floor * 100 + room}" for floor in range(1, 10) for room in range(1, 6)]


class RoomManagement(tk.Frame):
    def __init__(self, parent, customer_list):
        super().__init__(parent, bg="#F5F5F5")

        self.rooms = [
            ('101', 'thường'), ('102', 'VIP'), ('103', 'VIP'), ('104', 'thường'), ('105', 'thường'),
            ('106', 'thường'), ('107', 'thường'), ('108', 'thường'), ('109', 'thường'), ('201', 'thường'),
            ('202', 'thường'), ('203', 'thường'), ('204', 'thường'), ('205', 'VIP'), ('206', 'thường'),
            ('207', 'thường'), ('208', 'thường'), ('209', 'thường'), ('301', 'thường'), ('302', 'thường'),
            ('303', 'thường'), ('304', 'thường'), ('305', 'thường'), ('306', 'thường'), ('307', 'thường'),
            ('308', 'thường'), ('309', 'thường'), ('401', 'thường'), ('402', 'thường'), ('403', 'thường'),
            ('404', 'thường'), ('405', 'thường'), ('406', 'thường'), ('407', 'thường'), ('408', 'thường'),
            ('409', 'thường'), ('501', 'thường'), ('502', 'thường'), ('503', 'thường'), ('504', 'thường'),
            ('505', 'thường'), ('506', 'thường'), ('507', 'thường'), ('508', 'thường'), ('509', 'thường'),
            ('601', 'thường'), ('602', 'thường'), ('603', 'thường'), ('604', 'thường'), ('605', 'thường'),
            ('606', 'thường'), ('607', 'thường'), ('608', 'thường'), ('609', 'thường'), ('701', 'thường'),
            ('702', 'thường'), ('703', 'thường'), ('704', 'thường'), ('705', 'thường'), ('706', 'thường'),
            ('707', 'thường'), ('708', 'thường'), ('709', 'thường'), ('801', 'thường'), ('802', 'thường'),
            ('803', 'thường'), ('804', 'thường'), ('805', 'thường'), ('806', 'thường'), ('807', 'thường'),
            ('808', 'thường'), ('809', 'thường'), ('901', 'thường'), ('902', 'thường'), ('903', 'thường'),
            ('904', 'thường'), ('905', 'thường'), ('906', 'thường'), ('907', 'thường'), ('908', 'thường'),
            ('909', 'thường'),
        ]


        # Store the reference to the central customer list managed by the App
        self.customer_list = customer_list

        # --- Title and Refresh Button Frame ---
        self.title_frame = tk.Frame(self, bg="#F5F5F5")
        self.title_frame.pack(fill="x", pady=10, padx=10)

        self.title_label = tk.Label(self.title_frame, text="Danh Sách Phòng Hiện Có", font=("Arial", 16, "bold"), bg="#F5F5F5")
        self.title_label.pack(side="left", fill="x", expand=True) # Title takes left side and expands

        # Refresh Button
        self.refresh_button = tk.Button(
            self.title_frame,
            text="Tải lại", # Button text
            command=self.refresh_display, # Call the refresh method
            font=("Arial", 10),
            bg=COLOR_ACCENT_TEAL, # Use Teal color
            fg="white",
            activebackground="#117a8b",
            activeforeground="white",
            bd=0,
            padx=10,
            pady=5,
            relief=tk.FLAT,
            cursor="hand2"
        )
        self.refresh_button.pack(side="right") # Button takes right side

        # --- Scrolling Setup ---
        self.outer_content_frame = tk.Frame(self, bg="#F5F5F5")
        self.outer_content_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.canvas = tk.Canvas(self.outer_content_frame, bg="#F5F5F5", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.outer_content_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#F5F5F5")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        self._bind_mouse_wheel(self.canvas)
        self._bind_mouse_wheel(self.scrollable_frame)
        # --- End Scrolling Setup ---

        self.room_tiles = {}
        # Initial creation of room tiles
        self._create_room_tiles()

    def _on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event=None):
        canvas_width = self.canvas.winfo_width()
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)

    def _bind_mouse_wheel(self, widget):
        # Bind mouse wheel events for scrolling
        if platform.system() == "Windows":
            widget.bind_all("<MouseWheel>", self._on_mousewheel, add='+')
        elif platform.system() == "Darwin": # macOS
             widget.bind_all("<MouseWheel>", self._on_mousewheel, add='+')
             # macOS also uses Button-4/Button-5 for horizontal scrolling, but sometimes vertical
             widget.bind_all("<Button-4>", self._on_mousewheel, add='+')
             widget.bind_all("<Button-5>", self._on_mousewheel, add='+')
        else: # Linux/other Unix
            widget.bind_all("<Button-4>", self._on_mousewheel, add='+') # Scroll up
            widget.bind_all("<Button-5>", self._on_mousewheel, add='+') # Scroll down

    def _unbind_mouse_wheel(self, widget):
        # Optional cleanup for mouse wheel bindings
        if platform.system() == "Windows": widget.unbind_all("<MouseWheel>")
        elif platform.system() == "Darwin":
             widget.unbind_all("<MouseWheel>")
             widget.unbind_all("<Button-4>")
             widget.unbind_all("<Button-5>")
        else:
            widget.unbind_all("<Button-4>")
            widget.unbind_all("<Button-5>")

    def _on_mousewheel(self, event):
        scroll_units = 0
        if platform.system() == "Linux":
            if event.num == 4: scroll_units = -1
            elif event.num == 5: scroll_units = 1
        elif platform.system() == "Windows":
             # event.delta is typically 120 or -120
             scroll_units = -1 * (event.delta // 120)
        elif platform.system() == "Darwin": # macOS
             # event.delta seems to be more granular on macOS
             scroll_units = -1 * event.delta
             # Handle Button-4/Button-5 on macOS if they trigger vertical scroll
             if event.num == 4: scroll_units = -1
             if event.num == 5: scroll_units = 1

        if scroll_units != 0:
            self.canvas.yview_scroll(scroll_units, "units")


    def _get_customer_by_room(self, room_id_str):
        """Finds customer data based on string room_id."""
        # Ensure room_id is treated as string for comparison
        target_room_id_str = str(room_id_str)

        for customer in self.customer_list:
            # Get the room_number attribute safely and compare as strings
            customer_room_num = getattr(customer, 'room_number', None)
            if customer_room_num is not None and str(customer_room_num) == target_room_id_str:
                return customer
        return None

    def _show_customer_info(self, event, room_id_str):
        """Displays customer info in a messagebox for a given room_id string."""
        # room_id_str received from lambda should be the string room number
        customer = self._get_customer_by_room(room_id_str)
        if customer:
            # Format customer info for display
            # Safely get attributes, providing default empty strings if None
            customer_info = (
                f"ID: {getattr(customer, 'id', '')}\n"
                f"Tên: {getattr(customer, 'name', '')}\n"
                f"Giới Tính: {getattr(customer, 'sex', '')}\n"
                f"Ngày Sinh: {getattr(customer, 'birthday', '')}\n" # Assuming birthday is already formatted string
                f"Quốc Tịch: {getattr(customer, 'national', '')}\n" 
                f"Quê Quán: {getattr(customer, 'country', '')}\n"
                f"Ngày Nhận Phòng: {getattr(customer, 'checkin_date', '')}\n" # Assuming checkin_date is already formatted string
                f"Loại Phòng: {getattr(customer, 'room_type', '')}" # Use Loại Phòng
            )
            messagebox.showinfo(f"Thông Tin Khách Hàng - Phòng {room_id_str}", customer_info)
        else:
            messagebox.showinfo(f"Thông Tin Phòng {room_id_str}", "Phòng này hiện đang trống.")


    def _create_room_tiles(self):
        """Creates or updates the visual tiles for each room based on current customer list."""
        print("[*] Creating/Updating room tiles...")
        # Clear existing tiles
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.room_tiles.clear()

        # Get occupied room numbers as strings from the current customer list
        occupied_rooms = {str(getattr(customer, 'room_number', None)) for customer in self.customer_list if getattr(customer, 'room_number', None) is not None and getattr(customer, 'room_number', None) != ""}

        # Sort rooms numerically for consistent display order
        sorted_rooms = sorted(self.rooms, key=lambda item: int(item[0]))

        for room_id_str, room_type in sorted_rooms: # room_id_str is now a string
            is_occupied = room_id_str in occupied_rooms # Check if string room ID is in occupied set
            color = "#FFC0CB" if is_occupied else "#b6f7b0" # Pink for occupied, Light Green for available

            tile = tk.Frame(self.scrollable_frame, bg=color, bd=1, relief="solid", padx=10, pady=5)
            tile.pack(fill="x", pady=(5, 0), padx=5)
            self.room_tiles[room_id_str] = tile # Store with string key

            # --- Bind click events ---
            # The lambda captures the string room_id_str correctly
            tile.bind("<Button-1>", lambda event, r_id_str=room_id_str: self._show_customer_info(event, r_id_str))
            tile.config(cursor="hand2")

            # --- Labels ---
            # Displaying the string room_id_str
            room_id_label = tk.Label(tile, text=f"Phòng: {room_id_str}", font=("Arial", 11), bg=color)
            room_id_label.pack(side="left")
            room_id_label.bind("<Button-1>", lambda event, r_id_str=room_id_str: self._show_customer_info(event, r_id_str))

            availability_text = "Đang có khách" if is_occupied else "Còn trống"
            availability_color = "red" if is_occupied else "dark green"
            available_label = tk.Label(tile, text=availability_text, font=("Arial", 11, "italic"), fg=availability_color, bg=color)
            available_label.pack(side="left", padx=15)
            available_label.bind("<Button-1>", lambda event, r_id_str=room_id_str: self._show_customer_info(event, r_id_str))

            type_label = tk.Label(tile, text=f"Loại: {room_type}", font=("Arial", 11), bg=color)
            type_label.pack(side="right")
            type_label.bind("<Button-1>", lambda event, r_id_str=room_id_str: self._show_customer_info(event, r_id_str))

        print("[✓] Room tiles created/updated.")


    # --- Method to refresh the display ---
    # This method is called by the Refresh button and by the App when the tab is shown
    def refresh_display(self):
        """Refreshes the room tile display based on the current customer list."""
        print("[*] Room Management tab refreshing display...")
        self._create_room_tiles() # Recreate tiles to reflect current occupancy
        print("[✓] Room Management tab display refreshed.")

