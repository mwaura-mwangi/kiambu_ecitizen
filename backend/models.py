from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
import enum

# Define application status enum
class Status(str, enum.Enum):
    """
    Enum for application status.
    """
    pending = "pending"
    paid = "paid"
    approved = "approved"

# User model
class User(Base):
    """
    Represents a user in the system.
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    id_number = Column(String, unique=True, index=True)
    phone = Column(String, unique=True)
    name = Column(String) # Name of the user

# Service model
class Service(Base):
    """
    Represents a service offered by the county.
    """
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False) # Name of the service
    amount = Column(Float, nullable=True) # Amount payable for the service
    description = Column(String, nullable=True) # Description of the service
    requires_account = Column(String, nullable=True) # Account reference required (e.g. meter number)

# Application model
class Application(Base):
    """
    Represents an application for a service by a user.
    """
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True) 
    user_id = Column(Integer, ForeignKey("users.id")) # ID of the user applying
    service_id = Column(Integer, ForeignKey("services.id")) # ID of the service applied for
    status = Column(String, default=Status.pending) # Status of the application
    account_ref = Column(String, nullable=True) # Account reference (if required)
    amount_billed = Column(Float, default=0) # Amount billed for the service
    created_at = Column(DateTime, default=datetime.utcnow) # Timestamp of application creation
    created_at = Column(DateTime, default=datetime.utcnow) 
    user = relationship("User") # Relationship with User model
    service = relationship("Service") # Relationship with Service model

# Payment model
class Payment(Base):
    """
    Represents a payment made for an application.
    """
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True)
    application_id = Column(Integer, ForeignKey("applications.id")) # ID of the application paid for
    mpesa_code = Column(String, unique=True) # M-Pesa transaction code
    amount = Column(Float) # Amount paid
    timestamp = Column(DateTime, default=datetime.utcnow) # Timestamp of payment