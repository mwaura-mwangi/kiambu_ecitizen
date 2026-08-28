from pydantic import BaseModel

# Schema for creating a new user
class UserCreate(BaseModel):
    """
    Represents user data required for creation.
    """
    id_number: str  # ID number of the user
    phone: str  # Phone number of the user
    name: str  # Name of the user

# Schema for creating a new application
class ApplicationCreate(BaseModel):
    """
    Represents application data required for creation.
    """
    user_id: int  # ID of the user applying
    service_id: int  # ID of the service applied for
    account_ref: str | None = None  # Account reference (e.g. plot number, meter number)
    amount_billed: float | None = None  # Amount billed (for services like land/water)

# Schema for creating a new payment
class PaymentCreate(BaseModel):
    """
    Represents payment data required for creation.
    """
    application_id: int  # ID of the application being paid for
    mpesa_code: str  # M-Pesa transaction code
    amount: float  # Amount paid