# Lớp và hàm khách thuê
class Tenant:
    def __init__(self, tenant_id, name, phone, id_number, room_id=None):
        self.tenant_id = tenant_id
        self.name = name
        self.phone = phone
        self.id_number = id_number
        self.room_id = room_id
        
    def to_dict(self):
        return {
            "tenant_id": self.tenant_id,
            "name": self.name,
            "phone": self.phone,
            "id_number": self.id_number,
            "room_id": self.room_id
        }
    
    def __str__(self):
        return f"{self.name} - SĐT: {self.phone} - CMND/CCCD: {self.id_number}"

