from sqlalchemy.orm import Session
from app.models.tokens_model import Token

def create(token_data: Token, db: Session):
    db.add(token_data)
    db.commit()
    db.refresh(token_data)
    
    return {
        "access_token": token_data.access_token,
        "refresh_token": token_data.refresh_token,
        "token_type": "bearer"
    }
    
def mark_revoked(db_token: Token, db: Session):
    db_token.revoked = True
    db.commit()
    db.refresh(db_token)