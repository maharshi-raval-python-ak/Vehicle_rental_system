from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import SecretStr

conf = ConnectionConfig(
    MAIL_USERNAME = "maharshi.raval@armakuni.com",
    MAIL_PASSWORD = SecretStr("zdam ndjd vhmi gzpu"), 
    MAIL_FROM = "maharshi.raval@armakuni.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
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
