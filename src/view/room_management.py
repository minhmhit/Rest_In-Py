import tkinter as tk
from tkinter import messagebox

class RoomManagement(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#F5F5F5")

        self.rooms = [
            ('101', 'Normal'), ('102', 'VIP'), ('103', 'VIP'), ('104', 'Normal'), ('105', 'Normal'),
            ('106', 'Normal'), ('107', 'Normal'), ('108', 'Normal'), ('109', 'Normal'), ('201', 'Normal'),
            ('202', 'Normal'), ('203', 'Normal'), ('204', 'Normal'), ('205', 'VIP'), ('206', 'Normal'),
            ('207', 'Normal'), ('208', 'Normal'), ('209', 'Normal'), ('301', 'Normal'), ('302', 'Normal'),
            ('303', 'Normal'), ('304', 'Normal'), ('305', 'Normal'), ('306', 'Normal'), ('307', 'Normal'),
            ('308', 'Normal'), ('309', 'Normal'), ('401', 'Normal'), ('402', 'Normal'), ('403', 'Normal'),
            ('404', 'Normal'), ('405', 'Normal'), ('406', 'Normal'), ('407', 'Normal'), ('408', 'Normal'),
            ('409', 'Normal'), ('501', 'Normal'), ('502', 'Normal'), ('503', 'Normal'), ('504', 'Normal'),
            ('505', 'Normal'), ('506', 'Normal'), ('507', 'Normal'), ('508', 'Normal'), ('509', 'Normal'),
            ('601', 'Normal'), ('602', 'Normal'), ('603', 'Normal'), ('604', 'Normal'), ('605', 'Normal'),
            ('606', 'Normal'), ('607', 'Normal'), ('608', 'Normal'), ('609', 'Normal'), ('701', 'Normal'),
            ('702', 'Normal'), ('703', 'Normal'), ('704', 'Normal'), ('705', 'Normal'), ('706', 'Normal'),
            ('707', 'Normal'), ('708', 'Normal'), ('709', 'Normal'), ('801', 'Normal'), ('802', 'Normal'),
            ('803', 'Normal'), ('804', 'Normal'), ('805', 'Normal'), ('806', 'Normal'), ('807', 'Normal'),
            ('808', 'Normal'), ('809', 'Normal'), ('901', 'Normal'), ('902', 'Normal'), ('903', 'Normal'),
            ('904', 'Normal'), ('905', 'Normal'), ('906', 'Normal'), ('907', 'Normal'), ('908', 'Normal'),
            ('909', 'Normal'),
        ]

        self.customer_list = [
            (1, "Nguyễn Văn An", "Nam", "1990-05-20", "Việt Nam", "Long An", "2005-08-16", "Thường", '301'),
            (2, "Trần Thị Hoa", "Nữ", "1985-12-15", "Việt Nam", "Tra Vinh", "2015-02-20", "VIP", '102'),
            (3, "Lê Minh Tú", "Nam", "1992-07-30", "Việt Nam", "Ho Chi Minh", "2010-02-10", "VIP", '103'),
            (4, "Phạm Thùy Dung", "Nữ", "1998-09-05", "Việt Nam", "Ha Noi", "2018-11-15", "Thường", '104'),
            (5, "Hoàng Quốc Bảo", "Nam", "1987-11-22", "Việt Nam", "Bac Lieu", "2020-01-01", "Thường", '105'),
            (6, "Đặng Thu Hằng", "Nữ", "1995-04-18", "Việt Nam", "Hai Phong", "2015-02-20", "VIP", '205'),
            (7, "Bùi Quang Huy", "Nam", "1989-08-12", "Việt Nam", "Việt Nam", "2015-02-23", "Thường", '201')
        ]

        self.title_label = tk.Label(self, text="Room Status", font=("Arial", 16, "bold"), bg="#F5F5F5", pady=10)
        self.title_label.pack()

        self.content_frame = tk.Frame(self, bg="#F5F5F5")
        self.content_frame.pack(fill="both", expand=True, padx=10)

        self.room_tiles = {}

        self._create_room_tiles()

    def _get_customer_by_room(self, room_id):
        for customer in self.customer_list:
            if str(customer[8]) == room_id:
                return customer
        return None

    def _show_customer_info(self, event, room_id):
        customer = self._get_customer_by_room(room_id)
        if customer:
            customer_info = f"ID: {customer[0]}\nName: {customer[1]}\nGender: {customer[2]}\nBirth Date: {customer[3]}\nNationality: {customer[4]}\nAddress: {customer[5]}\nCheck-in Date: {customer[6]}\nType: {customer[7]}"
            messagebox.showinfo(f"Customer Info - Room {room_id}", customer_info)

    def _create_room_tiles(self):
        occupied_rooms = {str(customer[8]) for customer in self.customer_list}

        for room_id, room_type in self.rooms:
            is_occupied = room_id in occupied_rooms
            color = "#FFC0CB" if is_occupied else "#b6f7b0"
            tile = tk.Frame(self.content_frame, bg=color, bd=2, relief="groove", padx=10, pady=5)
            tile.pack(fill="x", pady=5)
            self.room_tiles[room_id] = tile

            tile.bind("<Button-1>", lambda event, r_id=room_id: self._show_customer_info(event, r_id))
            tile.config(cursor="hand2")

            room_id_label = tk.Label(tile, text=room_id, font=("Arial", 12), bg=color)
            room_id_label.pack(side="left")

            availability_text = "Occupied" if is_occupied else "Available"
            available_label = tk.Label(tile, text=availability_text, font=("Arial", 12), bg=color)
            available_label.pack(side="left", padx=5)

            type_label = tk.Label(tile, text=room_type, font=("Arial", 12), bg=color)
            type_label.pack(side="right")

