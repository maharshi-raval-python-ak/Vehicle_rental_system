import uuid
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.crud.crud_base import CRUDBase
from app.models.payments_model import Payment
from app.schemas.payments_schemas import PaymentCreate, PaymentUpdate

class PaymentCRUD(CRUDBase[Payment, PaymentCreate, PaymentUpdate]):
    def get_by_transaction_id(self, db: Session, transaction_id: str):
        return db.execute(select(Payment).where(Payment.transaction_id == transaction_id)).scalar_one_or_none()

payment_crud = PaymentCRUD(Payment, "Payment")
