import uuid
from datetime import datetime, timedelta, timezone
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.user_models import User
from app.models.vendor_models import Vendor
from app.models.location_model import Location
from app.models.vehicle_model import Vehicle
from app.models.booking_model import Booking
from app.models.trip_model import Trip
from app.models.payments_model import Payment
from app.models.damage_reports_model import DamageReport
from app.models.reviews_model import Review


def seed_backend():
    db: Session = SessionLocal()

    try:
        # Cleanup
        tables = [
            "backend.vehicle_checks",
            "backend.reviews",
            "backend.payments", 
            "backend.damage_reports", 
            "backend.trips", 
            "backend.bookings", 
            "backend.vehicles", 
            "backend.locations", 
            "backend.vendors", 
            "backend.users"
        ]
        for table in tables:
            db.execute(text(f'DELETE FROM {table}'))
            
        # SAME IDs (must match auth)
        AJAY_ID = uuid.UUID("f47ac10b-58cc-4372-a567-0e02b2c3d472")
        SWAYAM_ID = uuid.UUID("f47ac10b-58cc-4372-a567-0e02b2c3d473")
        ROHAN_ID = uuid.UUID("f47ac10b-58cc-4372-a567-0e02b2c3d474")
        VIVEK_ID = uuid.UUID("f47ac10b-58cc-4372-a567-0e02b2c3d475")

        # ---------------- USERS ----------------
        db.add_all([
            User(
                user_id=AJAY_ID,
                name="Ajay Joshi",
                email="ajay.joshi@armakuni.com",
                phone="9999999991",
                license_number="DL123456",
            ),
            User(
                user_id=SWAYAM_ID,
                name="Swayam Doshi",
                email="swayam.doshi@armakuni.com",
                phone="9999999992",
                license_number="GJ654321",
            ),
        ])

        # ---------------- VENDORS ----------------
        vendor1 = Vendor(
            vendor_id=ROHAN_ID,
            name="Rohan Roy",
            email="rohan.roy@armakuni.com",
            phone="8888888888",
            is_verified=True,
        )

        vendor2 = Vendor(
            vendor_id=VIVEK_ID,
            name="Vivek Thumar",
            email="vivek.thumar@armakuni.com",
            phone="6666666666",
            is_verified=True,
        )

        db.add_all([vendor1, vendor2])

        # ---------------- LOCATIONS ----------------
        loc1 = Location(location_id=uuid.uuid4(), city="Ahmedabad", area="Satellite", latitude=23.0305, longitude=72.5296)
        loc2 = Location(location_id=uuid.uuid4(), city="Ahmedabad", area="Bopal", latitude=23.035, longitude=72.4619)
        loc3 = Location(location_id=uuid.uuid4(), city="Ahmedabad", area="Navrangpura", latitude=23.0338, longitude=72.5633)
        loc4 = Location(location_id=uuid.uuid4(), city="Ahmedabad", area="Prahlad Nagar", latitude=23.012, longitude=72.5108)
        loc5 = Location(location_id=uuid.uuid4(), city="Ahmedabad", area="Sabarmati", latitude=23.0827, longitude=72.576)
        db.add_all([loc1, loc2, loc3, loc4, loc5])
        db.flush()

        # ---------------- VEHICLES ----------------
        vehicles = [
            Vehicle(vehicle_id=uuid.uuid4(), vendor_id=vendor1.vendor_id, location_id=loc1.location_id, type="Car", brand="Hyundai", model_name="i20", fuel_type="Petrol", seating_capacity=5, price_per_hour=150, deposit_amount=2000, status="available"),
            Vehicle(vehicle_id=uuid.uuid4(), vendor_id=vendor2.vendor_id, location_id=loc2.location_id, type="SUV", brand="Tata", model_name="Nexon EV", fuel_type="Electric", seating_capacity=5, price_per_hour=300, deposit_amount=5000, status="available"),
            Vehicle(vehicle_id=uuid.uuid4(), vendor_id=vendor2.vendor_id, location_id=loc3.location_id, type="Sedan", brand="Honda", model_name="City", fuel_type="Petrol", seating_capacity=5, price_per_hour=200, deposit_amount=3000, status="available"),
            Vehicle(vehicle_id=uuid.uuid4(), vendor_id=vendor2.vendor_id, location_id=loc4.location_id, type="Luxury", brand="BMW", model_name="3 Series", fuel_type="Diesel", seating_capacity=5, price_per_hour=850, deposit_amount=15000, status="available"),
            Vehicle(vehicle_id=uuid.uuid4(), vendor_id=vendor1.vendor_id, location_id=loc5.location_id, type="Bike", brand="Royal Enfield", model_name="Guerrilla 450", fuel_type="Petrol", seating_capacity=2, price_per_hour=120, deposit_amount=1500, status="available"),
            Vehicle(vehicle_id=uuid.uuid4(), vendor_id=vendor1.vendor_id, location_id=loc3.location_id, type="MUV", brand="Toyota", model_name="Innova Hycross", fuel_type="Hybrid", seating_capacity=7, price_per_hour=450, deposit_amount=7000, status="available"),
        ]
        db.add_all(vehicles)
        db.flush()

        # ---------------- BOOKING ----------------
        booking = Booking(
            booking_id=uuid.uuid4(),
            user_id=AJAY_ID,
            vehicle_id=vehicles[0].vehicle_id,
            start_time=datetime.now(timezone.utc),
            end_time=datetime.now(timezone.utc) + timedelta(hours=5),
            otp="1234",
            total_price=750,
            vendor_payout=600,
            security_deposit=2000,
            status="completed",
        )

        db.add(booking)
        db.flush()
        
        # ---------------- REVIEWS ----------------
        db.add(Review(
            review_id=uuid.uuid4(),
            user_id=AJAY_ID,
            vehicle_id=vehicles[0].vehicle_id,
            rating=5,
            comment="The i20 was in great condition. Smooth pickup at Satellite!"
        ))

        # ---------------- Payment ----------------    
        payment = Payment(
            payment_id=uuid.uuid4(),
            booking_id=booking.booking_id,
            amount=2750.0, # total_price + deposit
            payment_type="booking + deposit",
            method="UPI",
            status="captured",
            transaction_id=f"TXN_{uuid.uuid4().hex[:8].upper()}"
        )
        db.add(payment)
        
        # ---------------- TRIP ----------------
        trip = Trip(
            trip_id=uuid.uuid4(),
            booking_id=booking.booking_id,
            start_time_actual=datetime.now(timezone.utc),
            end_time_actual=datetime.now(timezone.utc) + timedelta(hours=5),
            status="completed",
        )

        db.add(trip)
        
        # ---------------- DAMAGE REPORT ----------------
        damage = DamageReport(
            report_id=uuid.uuid4(),
            trip_id=trip.trip_id,
            description="Minor scratch on left bumper",
            extra_charge=500.0
        )
        db.add(damage)

        db.commit()
        print("Backend seeded (full data)")

    except Exception as e:
        db.rollback()
        print("Backend seed failed:", e)

    finally:
        db.close()


if __name__ == "__main__":
    seed_backend()