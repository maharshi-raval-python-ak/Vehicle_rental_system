import random
import uuid
from fastapi import HTTPException, status, BackgroundTasks
from app.dao.vehicle_dao import vehicle_dao
from app.schemas.booking_schemas import BookingCreate, BookingCreateOuter
from app.crud.booking_crud import booking_crud
from app.utils.email_utils import send_booking_emails


class BookingService:
    async def create_booking(
        self,
        db,
        booking_in: BookingCreateOuter,
        user_id: uuid.UUID,
        background_tasks: BackgroundTasks,
        user_email: str,
    ):
        vehicle = vehicle_dao.get_by_id(booking_in.vehicle_id, db)

        duration = (booking_in.end_time - booking_in.start_time).total_seconds() / 3600
        if duration <= 0:
            raise HTTPException(status_code=400, detail="Invalid time range")

        total_price = duration * vehicle.price_per_hour
        security_deposit = vehicle.deposit_amount
        vendor_payout = total_price * 0.90  # -> 10% platform fee

        generated_otp = str(random.randint(100000, 999999))

        obj_in = BookingCreate(
            vehicle_id=booking_in.vehicle_id,
            user_id=user_id,
            start_time=booking_in.start_time,
            end_time=booking_in.end_time,
            total_price=total_price,
            vendor_payout=vendor_payout,
            security_deposit=security_deposit,
            otp=generated_otp,
        )

        new_booking = booking_crud.create(obj_in, db)

        background_tasks.add_task(
            send_booking_emails,
            user_email=user_email,
            vendor_email=vehicle.vendor.email,
            booking=new_booking,
            otp=generated_otp,
            vehicle=vehicle,
        )

        return new_booking

    def get_my_bookings(self, db, user_id):
        return booking_crud.get_by_user(user_id, db)

    def get_vendor_booking_detail(self, db, booking_id, vendor_id):
        booking = booking_crud.get_by_id(booking_id, db)

        if booking.vehicle.vendor_id != vendor_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to view this booking",
            )
        return booking


booking_service = BookingService()
