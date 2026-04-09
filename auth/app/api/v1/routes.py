from typing import Optional
import uuid
from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.users_schema import UserRegister
from app.services.auth_services import (
    get_current_user,
    login_service,
    logout_service,
    new_tokens_service,
    register_user,
    validate_service,
)
from app.schemas.users_schema import UserResponse
from app.models.users_model import User
from app.models.clients_model import Client
from app.schemas.clients_schema import ClientCreate, ClientResponse
from app.services.clients_services import create_client_sevice, get_client_service
from app.crud import clients_crud
from app.services.roles_services import (
    add_permissions_to_role_service,
    assign_role_to_users_service,
    create_role_service,
)
from app.schemas.roles_schema import CreateRole, RoleResponse


router = APIRouter(prefix="/auth")

security_basic = HTTPBasic(auto_error=False)


@router.post("/register/user" , tags=["Register"])
def register_customer(user_in: UserRegister, db: Session = Depends(get_db)):
    return register_user(user_in, db, role_name="user")

@router.post("/register/vendor", tags=["Register"])
def register_vendor(user_in: UserRegister, db: Session = Depends(get_db)):
    return register_user(user_in, db, role_name="vendor")

@router.post("/token", tags=["Auth"])
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    basic_creds: Optional[HTTPBasicCredentials] = Depends(security_basic),
):
    return login_service(db, basic_creds, form_data)


@router.get("/testing", tags=["Auth"])
def check_login_token(current_user: User = Depends(get_current_user)):
    # print("In route")
    return current_user


@router.post("/refresh", tags=["Auth"])
def get_new_tokens(refresh_token: str, db: Session = Depends(get_db)):
    return new_tokens_service(refresh_token, db)


@router.post("/logout", tags=["Auth"])
def logout(
    refresh_token: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return logout_service(refresh_token, current_user, db)


@router.post("/validate", tags=["Tokens"])
def validate(access_token: str, db: Session = Depends(get_db)):
    return validate_service(access_token, db)


@router.post("/clients", tags=["Clients"])
def create_client(client_data: ClientCreate, db: Session = Depends(get_db)):
    return create_client_sevice(db, client_data)


@router.get("/clients/{client_id}", response_model=ClientResponse, tags=["Clients"])
def get_client(client_id: str, db: Session = Depends(get_db)):
    return get_client_service(db, client_id)


@router.post("/roles", response_model=RoleResponse, tags=["Roles"])
def create_role(role_data: CreateRole, db: Session = Depends(get_db)):
    return create_role_service(role_data, db)


@router.post("/users/{user_id}/roles", tags=["Roles"])
def assign_role_to_users(
    user_id: uuid.UUID, role_name: str, db: Session = Depends(get_db)
):
    return assign_role_to_users_service(user_id, role_name, db)


@router.post("/roles/{role_id}/permissions", tags=["Roles"])
def add_permissions_to_role(
    role_id: uuid.UUID, permission_name: str, db: Session = Depends(get_db)
):
    return add_permissions_to_role_service(role_id, permission_name, db)
