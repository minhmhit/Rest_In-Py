from model.room import Room
class RoomController:
    def __init__(self, view):
        self.view = view
        self.rooms = []
        self.next_id = 1
        
        # Thêm một số phòng mẫu
        self.add_room("101", 2000000, 20)
        self.add_room("102", 1800000, 18)
        self.add_room("103", 2500000, 25)
    
    def list_rooms(self):
        self.view.show_rooms(self.rooms)
    
    def add_room(self, room_number, price, area):
        room = Room(self.next_id, room_number, price, area)
        self.rooms.append(room)
        self.next_id += 1
        return room
    
    def update_room(self, room_id, room_number, price, area, status):
        for room in self.rooms:
            if room.room_id == room_id:
                room.room_number = room_number
                room.price = price
                room.area = area
                room.status = status
                return True
        return False
    
    def delete_room(self, room_id):
        for i, room in enumerate(self.rooms):
            if room.room_id == room_id:
                del self.rooms[i]
                return True
        return False
    
    def get_room(self, room_id):
        for room in self.rooms:
            if room.room_id == room_id:
                return room
        return None
    
    def get_available_rooms(self):
        return [room for room in self.rooms if room.status == "available"]
    
    def set_room_status(self, room_id, status):
        room = self.get_room(room_id)
        if room:
            room.status = status
            return True
        return False