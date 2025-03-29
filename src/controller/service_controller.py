from database import Session
from model import Service

def create_service(name, price):

    session = Session()
    new_service = Service(name=name, price=price)
    session.add(new_service)
    session.commit()
    session.close()

def get_service_by_id(service_id):
    
    session = Session()
    service = session.query(Service).filter_by(id=service_id).first()
    session.close()
    return service

def get_all_services():
    
    session = Session()
    services = session.query(Service).all()
    session.close()
    return services

def update_service(service_id, **kwargs):
    
    session = Session()
    service = session.query(Service).filter_by(id=service_id).first()
    if service:
        for key, value in kwargs.items():
            setattr(service, key, value)
        session.commit()
    else:
        raise ValueError("Không tìm thấy dịch vụ")
    session.close()

def delete_service(service_id):
   
    session = Session()
    service = session.query(Service).filter_by(id=service_id).first()
    if service:
        session.delete(service)
        session.commit()
    else:
        raise ValueError("Không tìm thấy dịch vụ")
    session.close()