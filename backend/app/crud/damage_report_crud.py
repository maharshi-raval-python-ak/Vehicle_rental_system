import uuid
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.crud.crud_base import CRUDBase
from app.models.damage_reports_model import DamageReport
from app.schemas.damage_report_schemas import DamageReportCreate, DamageReportUpdate

class DamageReportCRUD(CRUDBase[DamageReport, DamageReportCreate, DamageReportUpdate]):
    def get_by_trip(self, db: Session, trip_id: uuid.UUID):
        return db.execute(select(DamageReport).where(DamageReport.trip_id == trip_id)).scalar_one_or_none()

damage_crud = DamageReportCRUD(DamageReport, "Damage Report")
