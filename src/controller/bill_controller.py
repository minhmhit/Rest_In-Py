from database import Session
from model import Bill, Tenant, Room, Service, BillService
import datetime

def create_bill(room_id, services_list):
   
    session = Session()
    room = session.query(Room).filter_by(id=room_id).first()
    if room:
        tenants = room.tenants
        if not tenants:
            raise ValueError("Phòng không có khách thuê")
        
        total_amount = room.price
        for service_id in services_list:
            service = session.query(Service).filter_by(id=service_id).first()
            if service:
                total_amount += service.price
                
        amount_per_tenant = total_amount / len(tenants)
        for tenant in tenants:
            new_bill = Bill(
                tenant_id=tenant.id, 
                room_id=room.id, 
                total_amount=amount_per_tenant,  
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