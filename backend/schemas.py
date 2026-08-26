from pydantic import BaseModel

class UserCreate(BaseModel):
    id_number: str
    phone: str
    name: str

class ApplicationCreate(BaseModel):
    user_id: int
    service_id: int
    account_ref: str | None = None #plot_number KBU/123, Meter METER-8876
    amount_billed: float | None = None # for land/water you enter bill amount

class PaymentCreate(BaseModel):
    application_id: int
    mpesa_code: str
    amount: float