import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.crud.vendor_crud import vendor_crud
from app.models.vendor_models import Vendor
from app.schemas.vendor_schemas import VendorCreate
from app.schemas.auth_schemas import AuthData
from app.crud import vehicle_crud
from app.crud import location_crud
from app.schemas.vehicle_schemas import VehicleCreate, VehicleCreateOuter, VehicleUpdate

class VendorService:
    def create_vendor_profile(self, db: Session, vendor_in: VendorCreate, auth_info: AuthData):
        try:
            vendor_crud.get_by_id(id=auth_info.user_id, db=db)
            raise HTTPException(status_code=400, detail="Vendor profile already exists")
        except HTTPException as e:
            if e.status_code != 404:
                raise e

        vendor_data = vendor_in.model_dump()
        vendor_data["vendor_id"] = auth_info.user_id 
        vendor_data["email"] = auth_info.email

        db_obj = Vendor(**vendor_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_vendor_profile(self, db: Session, auth_info: AuthData):
        return vendor_crud.get_by_id(id=auth_info.user_id, db=db)
    
    
    def create_vehicle_for_vendor(self, db: Session, vehicle_in: VehicleCreateOuter, vendor_id: uuid.UUID):
        location = location_crud.get_by_area(db, area=vehicle_in.area)
        vendor_crud.get_by_id(id=vendor_id, db=db)
            # raise HTTPException(
            #     status_code=status.HTTP_404_NOT_FOUND, 
            #     detail=f"Vendor haven't created his/her profile."
            # )
        
        if not location:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Area '{vehicle_in.area}' not found."
            )

        vehicle_data = vehicle_in.model_dump(exclude={"area"})
        vehicle_data.update({
            "location_id": location.location_id,
            "vendor_id": vendor_id
        })
        
        obj_in_data = VehicleCreate(**vehicle_data) 
        return vehicle_crud.create(obj_in=obj_in_data, db=db)
    
    def get_my_vehicles(self, db, auth_info):
        vendor = self.get_vendor_profile(db, auth_info)
        if not vendor.is_verified:
            raise HTTPException(status_code=403, detail="Vendor account is not verified.")
        return vehicle_crud.get_multi_by_vendor(db, vendor_id=auth_info.user_id)

    def update_vendor_vehicle(self, db, vehicle_id, vehicle_update, auth_info):
        vendor = self.get_vendor_profile(db, auth_info)
        if not vendor.is_verified:
            raise HTTPException(status_code=403, detail="Vendor account is not verified.")
        
        vehicle = vehicle_crud.get_by_id(vehicle_id, db)
        if vehicle.vendor_id != auth_info.user_id:
            raise HTTPException(status_code=403, detail="Permission denied.")

        update_data = vehicle_update.model_dump(exclude_unset=True)

        if "area" in update_data:
            area_name = update_data.pop("area")
            location = location_crud.get_by_area(db, area=area_name)
            if not location:
                raise HTTPException(
                    status_code=404, 
                    detail=f"Area '{area_name}' not found."
                )
            update_data["location_id"] = location.location_id

        update_object = VehicleUpdate(**update_data)
        return vehicle_crud.update(vehicle_id, update_object, db)

    def delete_vendor_vehicle(self, db, vehicle_id, auth_info):
        vendor = self.get_vendor_profile(db, auth_info)
        if not vendor.is_verified:
            raise HTTPException(status_code=403, detail="Vendor account is not verified.")

        vehicle = vehicle_crud.get_by_id(vehicle_id, db)
        if vehicle.vendor_id != auth_info.user_id:
            raise HTTPException(status_code=403, detail="Permission denied.")

        return vehicle_crud.delete(vehicle_id, db)
    
vendor_service = VendorService()
