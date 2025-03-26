from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    role = Column(String(10), nullable=False)

class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    room_number = Column(String(10), unique=True, nullable=False)
    price = Column(Float, nullable=False)
    status = Column(String(20), default='available')
    tenants = relationship('Tenant', backref='room', lazy=True)
    bills = relationship('Bill', backref='room', lazy=True)

class Tenant(Base):
    __tablename__ = 'tenants'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(15))
    identity_number = Column(String(20), unique=True)
    image_path = Column(String(200))
    move_in_date = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
    bills = relationship('Bill', backref='tenant', lazy=True)

class Service(Base):
    __tablename__ = 'services'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    bills = relationship('Bill', secondary='bill_services', backref='services')

class Bill(Base):
    __tablename__ = 'bills'
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False)
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
    total_amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC))

class BillService(Base):
    __tablename__ = 'bill_services'
    bill_id = Column(Integer, ForeignKey('bills.id'), primary_key=True)
    service_id = Column(Integer, ForeignKey('services.id'), primary_key=True)