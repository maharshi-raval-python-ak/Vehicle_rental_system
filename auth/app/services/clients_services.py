from app.crud import clients_crud
from app.schemas.clients_schema import ClientCreate
from sqlalchemy.orm import Session

def create_client_sevice(db: Session, client_in: ClientCreate):
    return clients_crud.create(db, client_in)
    
def get_client_service(db: Session, client_id: str):
    client = clients_crud.get_by_id(client_id, db)
    return client