from app.crud.vehicle_crud import VehicleCRUD
from app.models.location_model import Location
from sqlalchemy import and_, select
from app.models.vehicle_model import Vehicle

class VehicleDAO(VehicleCRUD):
    def search_vehicles(self, db, city, area, v_type, min_p, max_p, fuel, seats):
        query = select(Vehicle).join(Location)
        filters = [Vehicle.status == "available"] #[Vehicle.status == "available", Location.city.ilike(f"%{city}%"), Location.area.ilike(f"%{area}%")]

        if city: filters.append(Location.city.ilike(f"%{city}%"))
        if area: filters.append(Location.area.ilike(f"%{area}%"))
        if v_type: filters.append(Vehicle.type == v_type)
        if fuel: filters.append(Vehicle.fuel_type == fuel)
        if seats: filters.append(Vehicle.seating_capacity >= seats)
        if min_p: filters.append(Vehicle.price_per_hour >= min_p)
        if max_p: filters.append(Vehicle.price_per_hour <= max_p)
        
        # for i in range(len(filters)):
        #     print(str(filters[i]))

        return db.execute(query.where(and_(*filters))).scalars().all()

# Create the DAO instance
vehicle_dao = VehicleDAO(Vehicle, "Vehicle")
