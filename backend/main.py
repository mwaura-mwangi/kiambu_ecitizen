from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import Base, engine, get_db
import models, schemas
import random

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Kiambu eCitizen Lite")

# Seed 3 services on startup
@app.on_event("startup")
def seed():
    db = next(get_db())
    if db.query(models.Service).count() == 0:
        db.add_all([
            models.Service(name="Business Permit", price=5000),
            models.Service(name="Market Stall Fee", price=200),
            models.Service(name="Parking Daily", price=100),
            models.Service(name="Land Rates", price=None, requires_account="plot_number"),
            models.Service(name="Water Bill", price=None, requires_account="meter_number"),
            models.Service(name="County Cess - Produce", price=500, requires_account="vehicle_number"),
        ])
        db.commit()

@app.post("/users")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(**user.dict())
    db.add(db_user); db.commit(); db.refresh(db_user)
    return db_user

@app.get("/services")
def list_services(db: Session = Depends(get_db)):
    return db.query(models.Service).all()

@app.post("/applications")
def apply(data: schemas.ApplicationCreate, db: Session = Depends(get_db)):
    app_obj = models.Application(
        user_id=data.user_id,
        service_id=data.service_id,
        status="pending",
        account_ref = data.account_ref,
        ammount_billed = data.amount_billed or 0
        )
    db.add(app_obj); db.commit(); db.refresh(app_obj)
    return app_obj

@app.post("/payments")
def pay(data: schemas.PaymentCreate, db: Session = Depends(get_db)):
    # Mock M-Pesa validation
    payment = models.Payment(**data.dict())
    db.add(payment)
    # update application to paid
    app_obj = db.query(models.Application).filter(models.Application.id == data.application_id).first()
    if app_obj: app_obj.status = models.Status.paid # type:ignore
    db.commit(); db.refresh(payment)
    return {"message": "Payment received", "receipt": payment.mpesa_code, "status": "paid"}

@app.get("/applications/{user_id}")
def my_applications(
    user_id: int, 
    db: Session = Depends(get_db)):
    return db.query(models.Application).filter(models.Application.user_id == user_id).all()