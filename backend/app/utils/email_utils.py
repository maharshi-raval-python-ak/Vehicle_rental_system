from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import SecretStr
from app.core.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME = settings.MAIL_USERNAME,
    MAIL_PASSWORD = settings.MAIL_PASSWORD.get_secret_value(),  # type: ignore
    MAIL_FROM = settings.MAIL_FROM,
    MAIL_PORT = settings.MAIL_PORT,
    MAIL_SERVER = settings.MAIL_SERVER,
    MAIL_STARTTLS = settings.MAIL_STARTTLS,
    MAIL_SSL_TLS = settings.MAIL_SSL_TLS,
)

async def send_booking_emails(user_email, vendor_email, booking, otp, vehicle):
    fm = FastMail(conf)

    user_body = f"""
    Hello, your booking for {vehicle.brand} {vehicle.model_name} is initiated.
    Your OTP for verification is: {otp}
    Vendor Details: {vehicle.vendor.name} ({vehicle.vendor.phone})
    Time: {booking.start_time} to {booking.end_time}
    """
    user_message = MessageSchema(
        subject="Booking Confirmation & OTP",
        recipients=[user_email],
        body=user_body,
        subtype=MessageType.html 
    )

    vendor_body = f"""
    Hello, your vehicle {vehicle.brand} {vehicle.model_name} has been booked.
    Booking Period: {booking.start_time} to {booking.end_time}
    Total Payout: {booking.vendor_payout}
    """
    vendor_message = MessageSchema(
        subject="New Vehicle Booking Alert",
        recipients=[vendor_email],
        body=vendor_body,
        subtype=MessageType.html 
    )

    await fm.send_message(user_message)
    await fm.send_message(vendor_message)
