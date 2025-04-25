import tkinter as tk
from tkinter import messagebox
import platform

class RoomManagement(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#F5F5F5")

        # --- Data with Integer Room Numbers ---
        self.rooms = [
            (101, 'Normal'), (102, 'VIP'), (103, 'VIP'), (104, 'Normal'), (105, 'Normal'),
            (106, 'Normal'), (107, 'Normal'), (108, 'Normal'), (109, 'Normal'), (201, 'Normal'),
            (202, 'Normal'), (203, 'Normal'), (204, 'Normal'), (205, 'VIP'), (206, 'Normal'),
            (207, 'Normal'), (208, 'Normal'), (209, 'Normal'), (301, 'Normal'), (302, 'Normal'),
            (303, 'Normal'), (304, 'Normal'), (305, 'Normal'), (306, 'Normal'), (307, 'Normal'),
            (308, 'Normal'), (309, 'Normal'), (401, 'Normal'), (402, 'Normal'), (403, 'Normal'),
            (404, 'Normal'), (405, 'Normal'), (406, 'Normal'), (407, 'Normal'), (408, 'Normal'),
            (409, 'Normal'), (501, 'Normal'), (502, 'Normal'), (503, 'Normal'), (504, 'Normal'),
            (505, 'Normal'), (506, 'Normal'), (507, 'Normal'), (508, 'Normal'), (509, 'Normal'),
            (601, 'Normal'), (602, 'Normal'), (603, 'Normal'), (604, 'Normal'), (605, 'Normal'),
            (606, 'Normal'), (607, 'Normal'), (608, 'Normal'), (609, 'Normal'), (701, 'Normal'),
            (702, 'Normal'), (703, 'Normal'), (704, 'Normal'), (705, 'Normal'), (706, 'Normal'),
            (707, 'Normal'), (708, 'Normal'), (709, 'Normal'), (801, 'Normal'), (802, 'Normal'),
            (803, 'Normal'), (804, 'Normal'), (805, 'Normal'), (806, 'Normal'), (807, 'Normal'),
            (808, 'Normal'), (809, 'Normal'), (901, 'Normal'), (902, 'Normal'), (903, 'Normal'),
            (904, 'Normal'), (905, 'Normal'), (906, 'Normal'), (907, 'Normal'), (908, 'Normal'),
            (909, 'Normal'),
        ]

        self.customer_list = [
            # Note the last element is now an integer
            (1, "Nguyễn Văn An", "Nam", "1990-05-20", "Việt Nam", "Long An", "2005-08-16", "Thường", 301),
            (2, "Trần Thị Hoa", "Nữ", "1985-12-15", "Việt Nam", "Tra Vinh", "2015-02-20", "VIP", 102),
            (3, "Lê Minh Tú", "Nam", "1992-07-30", "Việt Nam", "Ho Chi Minh", "2010-02-10", "VIP", 103),
            (4, "Phạm Thùy Dung", "Nữ", "1998-09-05", "Việt Nam", "Ha Noi", "2018-11-15", "Thường", 104),
            (5, "Hoàng Quốc Bảo", "Nam", "1987-11-22", "Việt Nam", "Bac Lieu", "2020-01-01", "Thường", 105),
            (6, "Đặng Thu Hằng", "Nữ", "1995-04-18", "Việt Nam", "Hai Phong", "2015-02-20", "VIP", 205),
            (7, "Bùi Quang Huy", "Nam", "1989-08-12", "Việt Nam", "Vĩnh Long", "2015-02-23", "Thường", 201) # Corrected address typo
        ]
        # --- End Data ---

        self.title_label = tk.Label(self, text="Danh Sách Phòng Hiện Có", font=("Arial", 16, "bold"), bg="#F5F5F5", pady=10)
        self.title_label.pack(fill="x")

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
        self._create_room_tiles()

    def _on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event=None):
        canvas_width = self.canvas.winfo_width()
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)

    def _bind_mouse_wheel(self, widget):
        if platform.system() == "Windows":
            widget.bind_all("<MouseWheel>", self._on_mousewheel, add='+')
        elif platform.system() == "Darwin":
             widget.bind_all("<MouseWheel>", self._on_mousewheel, add='+')
             widget.bind_all("<Button-4>", self._on_mousewheel, add='+')
             widget.bind_all("<Button-5>", self._on_mousewheel, add='+')
        else: # Linux/other Unix
            widget.bind_all("<Button-4>", self._on_mousewheel, add='+')
            widget.bind_all("<Button-5>", self._on_mousewheel, add='+')

    def _unbind_mouse_wheel(self, widget):
        # Optional cleanup
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
             scroll_units = -1 * (event.delta // 120)
        elif platform.system() == "Darwin":
            scroll_units = -1 * event.delta
            if event.num == 4: scroll_units = -1
            if event.num == 5: scroll_units = 1
        if scroll_units != 0: self.canvas.yview_scroll(scroll_units, "units")


    def _get_customer_by_room(self, room_id):
        """Finds customer data based on integer room_id."""
        # Ensure room_id is treated as integer for comparison
        try:
            target_room_id = int(room_id)
        except (ValueError, TypeError):
            # Handle cases where room_id might not be convertible (optional)
            print(f"Warning: Invalid room_id format received: {room_id}")
            return None

        for customer in self.customer_list:
            # *** CORRECTED: Direct integer comparison ***
            if customer[8] == target_room_id:
                return customer
        return None

    def _show_customer_info(self, event, room_id):
        """Displays customer info in a messagebox."""
        # room_id received from lambda should already be an integer
        customer = self._get_customer_by_room(room_id)
        if customer:
            # Format customer info for display
            customer_info = (f"ID: {customer[0]}\nTên: {customer[1]}\nGiới Tính: {customer[2]}\n"
                             f"Ngày Sinh: {customer[3]}\nQuốc Tịch: {customer[4]}\nĐịa Chỉ: {customer[5]}\n"
                             f"Ngày Nhận Phòng: {customer[6]}\nLoại Khách: {customer[7]}")
            messagebox.showinfo(f"Thông Tin Khách Hàng - Phòng {room_id}", customer_info)
        else:
            # Optionally show a message if the room is clicked but no customer is assigned
             messagebox.showinfo(f"Thông Tin Phòng {room_id}", "Phòng này hiện đang trống.")


    def _create_room_tiles(self):
        """Creates the visual tiles for each room."""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.room_tiles.clear()

        # *** CORRECTED: Use integers directly for occupied rooms ***
        occupied_rooms = {customer[8] for customer in self.customer_list} # Get occupied room numbers (integers)

        for room_id, room_type in self.rooms: # room_id is now an integer
            is_occupied = room_id in occupied_rooms # Direct integer check
            color = "#FFC0CB" if is_occupied else "#b6f7b0"

            tile = tk.Frame(self.scrollable_frame, bg=color, bd=1, relief="solid", padx=10, pady=5)
            tile.pack(fill="x", pady=(5, 0), padx=5)
            self.room_tiles[room_id] = tile # Store with integer key

            # --- Bind click events ---
            # The lambda captures the integer room_id correctly
            tile.bind("<Button-1>", lambda event, r_id=room_id: self._show_customer_info(event, r_id))
            tile.config(cursor="hand2")

            # --- Labels ---
            # Displaying the integer room_id works fine
            room_id_label = tk.Label(tile, text=f"Phòng: {room_id}", font=("Arial", 11), bg=color)
            room_id_label.pack(side="left")
            room_id_label.bind("<Button-1>", lambda event, r_id=room_id: self._show_customer_info(event, r_id))

            availability_text = "Đang có khách" if is_occupied else "Còn trống"
            availability_color = "red" if is_occupied else "dark green"
            available_label = tk.Label(tile, text=availability_text, font=("Arial", 11, "italic"), fg=availability_color, bg=color)
            available_label.pack(side="left", padx=15)
            available_label.bind("<Button-1>", lambda event, r_id=room_id: self._show_customer_info(event, r_id))

            type_label = tk.Label(tile, text=f"Loại: {room_type}", font=("Arial", 11), bg=color)
            type_label.pack(side="right")
            type_label.bind("<Button-1>", lambda event, r_id=room_id: self._show_customer_info(event, r_id))
