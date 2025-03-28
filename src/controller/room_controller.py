from database import Session
from model import Room

def create_room(room_number, price, status='available'):
   
    session = Session()
    new_room = Room(room_number=room_number, price=price, status=status)
    session.add(new_room)
    session.commit()
    session.close()

def get_room_by_id(room_id):
    
    session = Session()
    room = session.query(Room).filter_by(id=room_id).first()
    session.close()
    return room

def get_all_rooms():
    
    session = Session()
    rooms = session.query(Room).all()
    session.close()
    return rooms

def update_room(room_id, **kwargs):
   
    session = Session()
    room = session.query(Room).filter_by(id=room_id).first()
    if room:
        for key, value in kwargs.items():
            setattr(room, key, value)
        session.commit()
    else:
        raise ValueError("Không tìm thấy phòng")
    session.close()

def delete_room(room_id):
    
    session = Session()
    room = session.query(Room).filter_by(id=room_id).first()
    if room:
        if room.tenants:  
            raise ValueError("Không thể xóa phòng đang có khách thuê")
        session.delete(room)
        session.commit()
    else:
        raise ValueError("Không tìm thấy phòng")
    session.close()