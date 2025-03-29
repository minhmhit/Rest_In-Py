from database import Session
from model import Bill, Tenant, Room, Service, BillService
import datetime

def create_bill(tenant_id, services_list):
   
    session = Session()
    tenant = session.query(Tenant).filter_by(id=tenant_id).first()
    if tenant:
        room = tenant.room
        total_amount = room.price  
        for service_id in services_list: 
            service = session.query(Service).filter_by(id=service_id).first()
            if service:
                total_amount += service.price
        new_bill = Bill(
            tenant_id=tenant_id, 
            room_id=room.id, 
            total_amount=total_amount,
            created_at=datetime.datetime.now(datetime.UTC) 
        )
        session.add(new_bill)
        session.commit()
       
        for service_id in services_list:
            bill_service = BillService(bill_id=new_bill.id, service_id=service_id)
            session.add(bill_service)
        session.commit()
    else:
        raise ValueError("Không tìm thấy khách thuê")
    session.close()

def get_bill_by_id(bill_id):
    
    session = Session()
    bill = session.query(Bill).filter_by(id=bill_id).first()
    session.close()
    return bill

def get_bills_by_tenant(tenant_id):
    
    session = Session()
    bills = session.query(Bill).filter_by(tenant_id=tenant_id).all()
    session.close()
    return bills

def delete_bill(bill_id):
    
    session = Session()
    bill = session.query(Bill).filter_by(id=bill_id).first()
    if bill:
        session.delete(bill)  
        session.commit()
    else:
        raise ValueError("Không tìm thấy hóa đơn")
    session.close()