from view.console_view import ConsoleView
from controller.room_controller import RoomController
from controller.tenant_controller import TenantController
from controller.payment_controller import PaymentController
from model.room import Room
from model.tenant import Tenant
from model.payment import Payment

class RentalApp:
    def __init__(self):
        self.view = ConsoleView()
        self.room_controller = RoomController(self.view)
        self.tenant_controller = TenantController(self.view, self.room_controller)
        self.payment_controller = PaymentController(self.view, self.room_controller)
    
    def run(self):
        while True:
            choice = self.view.show_menu()
            
            if choice == "1":
                self.handle_room_menu()
            elif choice == "2":
                self.handle_tenant_menu()
            elif choice == "3":
                self.handle_payment_menu()
            elif choice == "0":
                print("Cảm ơn bạn đã sử dụng ứng dụng. Tạm biệt!")
                break
            else:
                self.view.show_message("Lựa chọn không hợp lệ!")
    
    def handle_room_menu(self):
        while True:
            choice = self.view.show_room_menu()
            
            if choice == "1":
                self.room_controller.list_rooms()
            elif choice == "2":
                room_number, price, area = self.view.get_room_input()
                room = self.room_controller.add_room(room_number, price, area)
                self.view.show_message(f"Đã thêm phòng: {room}")
            elif choice == "3":
                self.room_controller.list_rooms()
                try:
                    room_id = self.view.get_id_input("Nhập ID phòng cần cập nhật: ")
                    room = self.room_controller.get_room(room_id)
                    if room:
                        room_number, price, area, status = self.view.get_room_input(is_update=True)
                        if self.room_controller.update_room(room_id, room_number, price, area, status):
                            self.view.show_message("Cập nhật thành công!")
                        else:
                            self.view.show_message("Cập nhật thất bại!")
                    else:
                        self.view.show_message("Không tìm thấy phòng!")
                except ValueError:
                    self.view.show_message("ID không hợp lệ!")
            elif choice == "4":
                self.room_controller.list_rooms()
                try:
                    room_id = self.view.get_id_input("Nhập ID phòng cần xóa: ")
                    if self.room_controller.delete_room(room_id):
                        self.view.show_message("Xóa phòng thành công!")
                    else:
                        self.view.show_message("Không tìm thấy phòng!")
                except ValueError:
                    self.view.show_message("ID không hợp lệ!")
            elif choice == "0":
                break
            else:
                self.view.show_message("Lựa chọn không hợp lệ!")
    
    def handle_tenant_menu(self):
        while True:
            choice = self.view.show_tenant_menu()
            
            if choice == "1":
                self.tenant_controller.list_tenants()
            elif choice == "2":
                name, phone, id_number = self.view.get_tenant_input()
                
                # Hiển thị phòng trống để chọn
                available_rooms = self.room_controller.get_available_rooms()
                if available_rooms:
                    self.view.show_message("Phòng khả dụng:")
                    self.view.show_rooms(available_rooms)
                    try:
                        room_id = int(input("Nhập ID phòng (0 nếu chưa thuê phòng): "))
                        if room_id != 0 and not self.room_controller.get_room(room_id):
                            self.view.show_message("Phòng không tồn tại!")
                            continue
                    except ValueError:
                        self.view.show_message("ID không hợp lệ!")
                        continue
                else:
                    self.view.show_message("Không có phòng trống!")
                    room_id = 0
                
                if room_id == 0:
                    room_id = None
                    
                tenant = self.tenant_controller.add_tenant(name, phone, id_number, room_id)
                self.view.show_message(f"Đã thêm người thuê: {tenant}")
            elif choice == "3":
                self.tenant_controller.list_tenants()
                try:
                    tenant_id = self.view.get_id_input("Nhập ID người thuê cần cập nhật: ")
                    tenant = self.tenant_controller.get_tenant(tenant_id)
                    if tenant:
                        name, phone, id_number = self.view.get_tenant_input()
                        if self.tenant_controller.update_tenant(tenant_id, name, phone, id_number):
                            self.view.show_message("Cập nhật thành công!")
                        else:
                            self.view.show_message("Cập nhật thất bại!")
                    else:
                        self.view.show_message("Không tìm thấy người thuê!")
                except ValueError:
                    self.view.show_message("ID không hợp lệ!")
            elif choice == "4":
                self.tenant_controller.list_tenants()
                try:
                    tenant_id = self.view.get_id_input("Nhập ID người thuê cần xóa: ")
                    if self.tenant_controller.delete_tenant(tenant_id):
                        self.view.show_message("Xóa người thuê thành công!")
                    else:
                        self.view.show_message("Không tìm thấy người thuê!")
                except ValueError:
                    self.view.show_message("ID không hợp lệ!")
            elif choice == "5":
                self.tenant_controller.list_tenants()
                try:
                    tenant_id = self.view.get_id_input("Nhập ID người thuê cần chuyển phòng: ")
                    tenant = self.tenant_controller.get_tenant(tenant_id)
                    if tenant:
                        available_rooms = self.room_controller.get_available_rooms()
                        if available_rooms:
                            self.view.show_message("Phòng khả dụng:")
                            self.view.show_rooms(available_rooms)
                            room_id = self.view.get_id_input("Nhập ID phòng mới: ")
                            if self.tenant_controller.assign_room(tenant_id, room_id):
                                self.view.show_message("Chuyển phòng thành công!")
                            else:
                                self.view.show_message("Phòng không tồn tại!")
                        else:
                            self.view.show_message("Không có phòng trống!")
                    else:
                        self.view.show_message("Không tìm thấy người thuê!")
                except ValueError:
                    self.view.show_message("ID không hợp lệ!")
            elif choice == "0":
                break
            else:
                self.view.show_message("Lựa chọn không hợp lệ!")
    
    def handle_payment_menu(self):
        while True:
            choice = self.view.show_payment_menu()
            
            if choice == "1":
                self.payment_controller.list_payments()
            elif choice == "2":
                try:
                    room_id, amount, description = self.view.get_payment_input(self.room_controller.rooms)
                    payment = self.payment_controller.add_payment(room_id, amount, description)
                    if payment:
                        self.view.show_message(f"Đã thêm thanh toán: {payment}")
                    else:
                        self.view.show_message("Phòng không tồn tại!")
                except ValueError:
                    self.view.show_message("Thông tin không hợp lệ!")
            elif choice == "3":
                self.payment_controller.list_payments()
                try:
                    payment_id = self.view.get_id_input("Nhập ID thanh toán cần xóa: ")
                    if self.payment_controller.delete_payment(payment_id):
                        self.view.show_message("Xóa thanh toán thành công!")
                    else:
                        self.view.show_message("Không tìm thấy thanh toán!")
                except ValueError:
                    self.view.show_message("ID không hợp lệ!")
            elif choice == "0":
                break
            else:
                self.view.show_message("Lựa chọn không hợp lệ!")

# Điểm khởi đầu khi chạy ứng dụng
if __name__ == "__main__":
    app = RentalApp()
    app.run()