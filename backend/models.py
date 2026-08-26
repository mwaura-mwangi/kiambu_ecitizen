from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
import enum

class Status(str, enum.Enum):
    pending = "pending"
    paid = "paid"
    approved = "approved"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    id_number = Column(String, unique=True, index=True)
    phone = Column(String, unique=True)
    name = Column(String)

class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    price = Column(Float, nullable=True)
    requires_account = Column(String, nullable=True)

class Application(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    service_id = Column(Integer, ForeignKey("services.id"))
    status = Column(String, default=Status.pending)
    account_ref = Column(String, nullable=True)
    amount_billed = Column(Float, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User")
    service = relationship("Service")

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True)
    application_id = Column(Integer, ForeignKey("applications.id"))
    mpesa_code = Column(String, unique=True)
    amount = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)