from typing import Optional
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.utils.helpers import authenticated
from app.core.database import get_db
from app.schemas.auth_schemas import AuthData
from app.schemas.response_model import ResponseModel
from app.services.vendor_services import vendor_service
from app.schemas.vehicle_schemas import VehicleCreateOuter, VehicleResponse
from app.services.vehicle_services import vehicle_service


router = APIRouter(prefix="/vehicles", tags=["Vehicle"])

@router.post("/get_vehicles", response_model=ResponseModel[list[VehicleResponse]])
@authenticated(allowed_roles=["user"])
async def get_vehicles(
    access_token: str,
    db: Session = Depends(get_db),
    auth_info: AuthData = Depends(lambda: None), 
):
    vehicles = vehicle_service.get_all_vehicles(db)

    return {"data": vehicles, "message": "Vehicle added successfully"}      

@router.post("/get_vehicle/{vehicle_id}", response_model=ResponseModel[VehicleResponse])
@authenticated(allowed_roles=["user"])
async def get_vehicle_vehicleid(
    access_token: str,
    vehicle_id: uuid.UUID,
    db: Session = Depends(get_db),
    auth_info: AuthData = Depends(lambda: None), 
):
    vehicle = vehicle_service.get_vehicle_by_vehicle_id(db, vehicle_id)

    return {"data": vehicle, "message": "Vehicle added successfully"}      

# GET /vehicles?city=&area=&type=&min_price=&max_price=&fuel=&seats=

@router.get("/", response_model=ResponseModel[list[VehicleResponse]])
async def search_available_vehicles(
    db: Session = Depends(get_db),
    city: Optional[str] = Query(None),
    area: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    fuel: Optional[str] = Query(None),
    seats: Optional[int] = Query(None),
):
    results = vehicle_service.get_filtered_vehicles(
        db=db, 
        city=city, 
        area=area,
        v_type=type, 
        min_p=min_price, 
        max_p=max_price, 
        fuel=fuel, 
        seats=seats
    )
    
    return {"data": results, "message": "Search results retrieved successfully"}
