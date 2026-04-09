from pydantic import BaseModel
from typing import Optional
import uuid

class PaymentBase(BaseModel):
    booking_id: uuid.UUID
    amount: float
    payment_type: str # 'booking + deposit' or 'damage'
    method: str
    status: str
    transaction_id: str

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    status: Optional[str] = None
    transaction_id: Optional[str] = None
