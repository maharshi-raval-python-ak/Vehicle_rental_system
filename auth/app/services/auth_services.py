from datetime import datetime, timedelta, timezone
from typing import Optional
import uuid
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.services.roles_services import assign_role_to_users_service
import jwt
from jwt.exceptions import InvalidTokenError
from app.schemas.users_schema import UserRegister
from sqlalchemy.orm import Session
from app.crud import users_crud, tokens_crud, clients_crud
from app.models.users_model import User
from app.models.tokens_model import Token
from app.utils.auth_utils import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password,
)
from app.core.config import settings
from app.core.database import get_db


def register_user(user_data: UserRegister, db: Session, role_name: str = "user"):
    if role_name not in ["user", "vendor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Public registration for this role is not allowed."
        )

    db_user = users_crud.get_by_email(db, user_data.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered.")

    try:
        new_user = users_crud.create(
            db, 
            email=user_data.email, 
            password_hash=get_password_hash(user_data.password)
        )
        
        db.flush() 

        assign_role_to_users_service(
            user_id=new_user.user_id, 
            role_name=role_name, 
            db=db
        )

        db.commit()
        db.refresh(new_user)
        
        return {"user_id": new_user.user_id, "email": new_user.email, "role": role_name}

    except Exception as e:
        db.rollback()
        
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")



def authenticate_user(email: str, password: str, db: Session):
    user = users_crud.get_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user


def login_service(
    db: Session,
    basic_creds: Optional[HTTPBasicCredentials],
    form_data: OAuth2PasswordRequestForm,
):
    client_id = (basic_creds.username if basic_creds else None) or form_data.client_id
    client_secret = (basic_creds.password if basic_creds else None) or form_data.client_secret
    
    if not client_id:
        raise HTTPException(status_code=400, detail="Client credentials missing")
    
    try:
        client_id_uuid = uuid.UUID(str(client_id))
    except (ValueError, AttributeError):
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid Client ID format. Expected UUID, got '{client_id}'"
        )
        
    client_record = clients_crud.get_by_id(str(client_id_uuid), db=db)
    if not client_record or client_record.client_secret != client_secret:
        raise HTTPException(status_code=401, detail="Invalid Client Credentials")

    user = authenticate_user(
        email=form_data.username, password=form_data.password, db=db
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User not registered or invalid password"
        )

    token_data = {
        "sub": str(user.user_id),
        "client_id": str(client_record.client_id),
        "email": user.email,
    }
    generated_access_token = create_access_token(token_data)
    generated_refresh_token = create_refresh_token(token_data)

    new_token_record = Token(
        user_id=user.user_id,
        client_id=client_record.client_id,
        access_token=generated_access_token,
        refresh_token=generated_refresh_token,
        expires_at=datetime.now(timezone.utc)
        + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )

    return tokens_crud.create(db=db, token_data=new_token_record)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not valiate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        db_token = db.query(Token).filter(Token.access_token == token).first()
        if not db_token:
            raise HTTPException(status_code=404, detail="Session not found")
        if db_token.revoked:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Tokens are revoked, Please login again.")
        payload = jwt.decode(
            token, settings.ACCESS_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        # print(f"Decoded Payload: {payload}")
        type = payload.get("type")
        user_id = payload.get("sub")
        if user_id is None or type != "access":
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = users_crud.get_by_id(db, uuid.UUID(user_id))
    if user is None:
        raise credentials_exception
    return user


def new_tokens_service(refresh_token: str, db: Session):
    db_token = db.query(Token).filter(Token.refresh_token == refresh_token).first()
    if not db_token or db_token.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    if db_token.revoked:
        db.query(Token).filter(Token.user_id==db_token.user_id).update({"revoked": True})
        db.commit()
        raise HTTPException(status_code=401, detail="Token reuse detected. All sessions revoked.")

    db_token.revoked = True 
    
    user = users_crud.get_by_id(db, db_token.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    
    token_data = {
        "sub": str(db_token.user_id),
        "client_id": str(db_token.client_id),
        "email": user.email,
    }
    generated_access_token = create_access_token(token_data)
    generated_refresh_token = create_refresh_token(token_data)
    
    new_token_record = Token(
        user_id=user.user_id,
        client_id=db_token.client_id,
        access_token=generated_access_token,
        refresh_token=generated_refresh_token,
        expires_at=datetime.now(timezone.utc)
        + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )

    return tokens_crud.create(db=db, token_data=new_token_record)

def logout_service(refresh_token: str, current_user: User, db: Session):
    db_token = db.query(Token).filter(Token.refresh_token == refresh_token, Token.user_id == current_user.user_id).first()
    
    if not db_token:
        raise HTTPException(status_code=404, detail="Session not found")
    
    tokens_crud.mark_revoked(db_token, db)
    
    return {"message": "Logged out successfully."}

def validate_service(access_token: str, db: Session):
    db_token = db.query(Token).filter(Token.access_token == access_token).first()
    if not db_token:
        raise HTTPException(status_code=404, detail="Session not found")
    user = users_crud.get_by_id(db, db_token.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    try:
        payload = jwt.decode(access_token, settings.ACCESS_SECRET_KEY, algorithms=[settings.ALGORITHM])
    except Exception as e:
        raise HTTPException(status_code=401, detail="User is unauthorized. Access token expired.")
    
    roles = [link.role.name for link in user.role_links]

    permissions = {
        perm_link.permission.name 
        for role_link in user.role_links 
        for perm_link in role_link.role.permission_links
    }

    
    return {"user_id": user.user_id,
            "email": user.email,
            "client_id": db_token.client_id,
            "roles": roles,
            "permissions": permissions,
            "is_valid": "Yes"}