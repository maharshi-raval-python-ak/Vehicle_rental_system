import secrets
import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.clients_model import Client
from app.schemas.clients_schema import ClientCreate

def get_by_id(client_id: str, db: Session):
    client_id_uuid = uuid.UUID(client_id)
    if client_id_uuid is None:
        raise HTTPException(status_code=404, detail="client_id is needed.")
    return db.query(Client).filter(Client.client_id == client_id_uuid).first()

def create(db: Session, client_in: ClientCreate):
    existing = db.query(Client).filter(Client.client_name == client_in.client_name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Client name already registered")
    
    raw_secret = secrets.token_urlsafe(32)
    
    db_client = Client(client_name = client_in.client_name,
                       redirect_url = client_in.redirect_url,
                       client_secret = raw_secret)
    
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client