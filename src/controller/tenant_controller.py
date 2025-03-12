# xử lý logic kết nối giữa view và controller
from model.tenant import Tenant

class TenantController:
    def __init__(self, view, room_controller):
        self.view = view
        self.room_controller = room_controller
        self.tenants = []
        self.next_id = 1
    
    def list_tenants(self):
        self.view.show_tenants(self.tenants, self.room_controller.rooms)
    
    def add_tenant(self, name, phone, id_number, room_id=None):
        tenant = Tenant(self.next_id, name, phone, id_number, room_id)
        self.tenants.append(tenant)
        
        if room_id:
            self.room_controller.set_room_status(room_id, "occupied")
            
        self.next_id += 1
        return tenant
    
    def update_tenant(self, tenant_id, name, phone, id_number):
        for tenant in self.tenants:
            if tenant.tenant_id == tenant_id:
                tenant.name = name
                tenant.phone = phone
                tenant.id_number = id_number
                return True
        return False
    
    def delete_tenant(self, tenant_id):
        for i, tenant in enumerate(self.tenants):
            if tenant.tenant_id == tenant_id:
                # Nếu người thuê đang thuê phòng, đặt trạng thái phòng thành "available"
                if tenant.room_id:
                    self.room_controller.set_room_status(tenant.room_id, "available")
                del self.tenants[i]
                return True
        return False
    
    def get_tenant(self, tenant_id):
        for tenant in self.tenants:
            if tenant.tenant_id == tenant_id:
                return tenant
        return None
    
    def assign_room(self, tenant_id, room_id):
        tenant = self.get_tenant(tenant_id)
        room = self.room_controller.get_room(room_id)
        
        if not tenant or not room:
            return False
            
        # Nếu người thuê đã có phòng, đặt trạng thái phòng cũ thành "available"
        if tenant.room_id:
            self.room_controller.set_room_status(tenant.room_id, "available")
            
        # Cập nhật phòng mới
        tenant.room_id = room_id
        room.status = "occupied"
        return True
    
    def get_tenants_by_room(self, room_id):
        return [tenant for tenant in self.tenants if tenant.room_id == room_id]