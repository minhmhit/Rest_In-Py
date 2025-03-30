from database import Session
from model import Tenant, Room, User
import datetime

def create_tenant(name, phone, identity_number, image_path, room_id):
    
    session = Session()
    room = session.query(Room).filter_by(id=room_id).first()
    if room and room.status == 'available':
        
        new_user = User(
            username=identity_number,
            password='default_password',
            role='tenant'
        )
        
        session.add(new_user)
        session.commit()
        
        new_tenant = Tenant(
            name=name, 
            phone=phone, 
            identity_number=identity_number, 
            image_path=image_path, 
            room_id=room_id,
            move_in_date=datetime.datetime.now(datetime.UTC),
            user_id=new_user.id
        )
        
        session.add(new_tenant)
        room.status = 'occupied' 
        session.commit()
    else:
        raise ValueError("Phòng không trống hoặc không tồn tại")
    session.close()

def get_tenant_by_id(tenant_id):
   
    session = Session()
    tenant = session.query(Tenant).filter_by(id=tenant_id).first()
    session.close()
    return tenant

def update_tenant(tenant_id, **kwargs):
   
    session = Session()
    tenant = session.query(Tenant).filter_by(id=tenant_id).first()
    if tenant:
        for key, value in kwargs.items():
            setattr(tenant, key, value)
        session.commit()
    else:
        raise ValueError("Không tìm thấy khách thuê")
    session.close()

def delete_tenant(tenant_id):
   
    session = Session()
    tenant = session.query(Tenant).filter_by(id=tenant_id).first()
    if tenant:
        room = tenant.room 
        user = session.query(User).filter_by(id=tenant.user_id).first()
        if user:
            session.delete(user)
        session.delete(tenant)
        room.status = 'available'  
        session.commit()
    else:
        raise ValueError("Không tìm thấy khách thuê")
    session.close()