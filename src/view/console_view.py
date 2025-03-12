class ConsoleView:
    def show_menu(self):
        print("\n===== QUẢN LÝ NHÀ TRỌ =====")
        print("1. Quản lý phòng")
        print("2. Quản lý người thuê")
        print("3. Quản lý thanh toán")
        print("0. Thoát")
        return input("Chọn chức năng: ")
    
    def show_room_menu(self):
        print("\n----- QUẢN LÝ PHÒNG -----")
        print("1. Xem danh sách phòng")
        print("2. Thêm phòng mới")
        print("3. Cập nhật thông tin phòng")
        print("4. Xóa phòng")
        print("0. Quay lại")
        return input("Chọn chức năng: ")
    
    def show_tenant_menu(self):
        print("\n----- QUẢN LÝ NGƯỜI THUÊ -----")
        print("1. Xem danh sách người thuê")
        print("2. Thêm người thuê")
        print("3. Cập nhật thông tin người thuê")
        print("4. Xóa người thuê")
        print("5. Chuyển phòng")
        print("0. Quay lại")
        return input("Chọn chức năng: ")
    
    def show_payment_menu(self):
        print("\n----- QUẢN LÝ THANH TOÁN -----")
        print("1. Xem lịch sử thanh toán")
        print("2. Thêm thanh toán mới")
        print("3. Xóa thanh toán")
        print("0. Quay lại")
        return input("Chọn chức năng: ")
    
    def show_rooms(self, rooms):
        if not rooms:
            print("Không có phòng nào.")
            return
            
        print("\nDanh sách phòng:")
        for room in rooms:
            print(f"{room.room_id}. {room}")
    
    def show_tenants(self, tenants, rooms=None):
        if not tenants:
            print("Không có người thuê nào.")
            return
            
        room_map = {}
        if rooms:
            for room in rooms:
                room_map[room.room_id] = room.room_number
                
        print("\nDanh sách người thuê:")
        for tenant in tenants:
            room_info = f" - Phòng: {room_map.get(tenant.room_id, 'Chưa có')}" if tenant.room_id else ""
            print(f"{tenant.tenant_id}. {tenant}{room_info}")
    
    def show_payments(self, payments, rooms=None):
        if not payments:
            print("Không có lịch sử thanh toán.")
            return
            
        room_map = {}
        if rooms:
            for room in rooms:
                room_map[room.room_id] = room.room_number
                
        print("\nLịch sử thanh toán:")
        for payment in payments:
            room_info = f" - Phòng: {room_map.get(payment.room_id, 'N/A')}"
            print(f"{payment.payment_id}. {payment}{room_info}")
    
    def get_room_input(self, is_update=False):
        print("\nNhập thông tin phòng:")
        room_number = input("Số phòng: ")
        price = float(input("Giá phòng (VNĐ): "))
        area = float(input("Diện tích (m²): "))
        if is_update:
            status = input("Trạng thái (available/occupied): ")
            return room_number, price, area, status
        return room_number, price, area
    
    def get_tenant_input(self):
        print("\nNhập thông tin người thuê:")
        name = input("Họ tên: ")
        phone = input("Số điện thoại: ")
        id_number = input("Số CMND/CCCD: ")
        return name, phone, id_number
    
    def get_payment_input(self, rooms):
        print("\nNhập thông tin thanh toán:")
        self.show_rooms(rooms)
        room_id = int(input("ID phòng: "))
        amount = float(input("Số tiền (VNĐ): "))
        description = input("Mô tả (để trống nếu là tiền phòng): ") or "Tiền phòng"
        return room_id, amount, description
    
    def get_id_input(self, message):
        return int(input(message))
    
    def show_message(self, message):
        print(f"\n>>> {message}")


