from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import Base, engine, get_db
import models, schemas
from database import SessionLocal
import random

# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Kiambu eCitizen Lite")

# Seed services on startup
@app.on_event("startup")
def seed():
    """ Seed the database with initial services if empty. """
    db = SessionLocal()
    if db.query(models.Service).count() == 0:
        db.add_all([
            models.Service(name="Business Permit", amount=5000),
            models.Service(name="Market Stall Fee", amount=200),
            models.Service(name="Parking Daily", amount=100),
            models.Service(name="Land Rates", amount=None),
            models.Service(name="Water Bill", amount=None, requires_account="meter_number"),
            models.Service(name="County Cess - Produce", amount=500, requires_account="vehicle_number"),
        ])
        db.commit()
        print("seeded services")
    db.close()

# create a new user
@app.post("/users")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """ Create a new user in the database. """
    # Check if user with phone exists
    existing = db.query(models.User).filter(models.User.phone == user.phone).first()
    if existing:
        return existing
    
    # If not, create new user
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# List all services
@app.get("/services")
def list_services(db: Session = Depends(get_db)):
    """ Return a list of all available services. """
    return db.query(models.Service).all()

# Apply for a service
@app.post("/applications")
def apply(data: schemas.ApplicationCreate, db: Session = Depends(get_db)):
    """ Create a new application for a service. """
    app_obj = models.Application(
        user_id=data.user_id,
        service_id=data.service_id,
        status="pending",
        account_ref = data.account_ref,
        amount_billed = data.amount_billed or 0
    )
    db.add(app_obj); db.commit(); db.refresh(app_obj)
    return app_obj

# Process payment
@app.post("/payments")
def pay(data: schemas.PaymentCreate, db: Session = Depends(get_db)):
    """ Record a payment and update application status. """
    # Mock M-Pesa validation
    payment = models.Payment(**data.dict())
    db.add(payment)
    # update application to paid
    app_obj = db.query(models.Application).filter(models.Application.id == data.application_id).first()
    if app_obj:
        app_obj.status = models.Status.paid # type:ignore
    db.commit(); db.refresh(payment)
    return {"message": "Payment received", "receipt": payment.mpesa_code, "status": "paid"}

# Get applications for a user
@app.get("/applications/{user_id}")
def my_applications(
    user_id: int, 
    db: Session = Depends(get_db)
):
    """ Return all applications for a given user ID. """
    return db.query(models.Application).filter(models.Application.user_id == user_id).all()

# Send STK push
@app.post("/payments/stk")
def stk_push(data: dict):
    print(f"[MOCK M-PESA] STK Push to {data['phone']} for Ksh {data['amount']}")
    """ Call Daraja API to send STK push (TODO: implement after Daraja registration). """
    # Call Daraja API (we'll implement this after Daraja reg)
    return {
        "status": "success",
        "message": "STK push sent",
        "transaction_id": "mock-transaction-id",
        "phone": data["phone"],
        "amount": data["amount"]
    }