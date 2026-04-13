from datetime import datetime
from fastapi import HTTPException
from app.crud.trip_crud import trip_crud
from app.crud.booking_crud import booking_crud
from app.schemas.trip_schemas import TripCreate, TripUpdate
from app.schemas.booking_schemas import BookingUpdate
from app.schemas.vehicle_schemas import VehicleUpdate
from app.crud.vehicle_crud import vehicle_crud
from app.crud.location_crud import location_crud


class TripService:
    def start_trip(self, db, booking_id, otp, user_id):
        booking = booking_crud.get_by_id(booking_id, db)

        if booking.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not your booking")

        if booking.otp != otp:
            raise HTTPException(status_code=400, detail="Invalid OTP")

        if booking.trip:
            raise HTTPException(status_code=400, detail="Trip already started")

        trip_in = TripCreate(booking_id=booking_id, status="on-trip")
        new_trip = trip_crud.create(trip_in, db)

        trip_update = TripUpdate(start_time_actual=datetime.now(), otp_verified=True)
        trip_crud.update(new_trip.trip_id, trip_update, db)

        booking_update = BookingUpdate(status="on-trip")
        booking_crud.update(booking_id, booking_update, db)
        
        vehicle_update = VehicleUpdate(
            status="on-trip"
        )
        vehicle_crud.update(booking.vehicle_id, vehicle_update, db)

        return new_trip

    def end_trip(self, db, trip_id, user_id, area):
        trip = trip_crud.get_by_id(trip_id, db)

        if trip.booking.user_id != user_id:
            raise HTTPException(status_code=403, detail="Unauthorized")

        trip_update = TripUpdate(end_time_actual=datetime.now(), status="completed")
        updated_trip = trip_crud.update(trip_id, trip_update, db)

        booking_update = BookingUpdate(status="completed")
        booking_crud.update(trip.booking_id, booking_update, db)

        location = location_crud.get_by_area(db, area=area)
        if not location:
            raise HTTPException(
                status_code=404, detail=f"Area '{area}' is not a valid parking zone."
            )

        vehicle_update = VehicleUpdate(
            location_id=location.location_id, 
            status="available"
        )
        vehicle_crud.update(trip.booking.vehicle_id, vehicle_update, db)

        return updated_trip


trip_service = TripService()
