# lớp và hàm phòng
class Room:
    def __init__(self, room_id, room_number, price, area, status="available"):
        self.room_id = room_id
        self.room_number = room_number
        self.price = price
        self.area = area
        self.status = status  # available, occupied
        
    def to_dict(self):
        return {
            "room_id": self.room_id,
            "room_number": self.room_number,
            "price": self.price,
            "area": self.area,
            "status": self.status
        }
    
    def __str__(self):
        return f"Phòng {self.room_number}: {self.area}m², {self.price}đ, {self.status}"