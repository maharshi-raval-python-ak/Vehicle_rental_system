import uuid
from app.core.database import SessionLocal
from app.utils.auth_utils import get_password_hash
from app.models.users_model import User as AuthUser
from app.models.roles_model import Role
from app.models.users_role_model import UsersRole
from app.models.permissions_model import Permission
from app.models.role_permissions_model import RolePermission
from app.models.clients_model import Client
from sqlalchemy import text

ROLE_USER_ID = uuid.UUID("35f90649-8783-47c4-a5ce-87f1ced259ae")
ROLE_VENDOR_ID = uuid.UUID("a920c52f-0abf-4d50-92bf-b7f5b9ce907c")
ROLE_ADMIN_ID = uuid.UUID("1519dd38-ef74-4ca9-9b62-9cc57510d847")
CLIENT_ID = uuid.UUID("2827c517-c68d-4f44-94b7-9bf2faae3ff6")

MAHARSHI_ID = uuid.UUID("f47ac10b-58cc-4372-a567-0e02b2c3d471")
AJAY_ID = uuid.UUID("f47ac10b-58cc-4372-a567-0e02b2c3d472")
SWAYAM_ID = uuid.UUID("f47ac10b-58cc-4372-a567-0e02b2c3d473")
ROHAN_ID = uuid.UUID("f47ac10b-58cc-4372-a567-0e02b2c3d474")
VIVEK_ID = uuid.UUID("f47ac10b-58cc-4372-a567-0e02b2c3d475")

def seed_auth():
    db = SessionLocal()
    try:
        # Cleanup
        tables = ["auth.tokens", "auth.users_role", "auth.role_permissions", "auth.users", "auth.roles", "auth.permissions", "auth.clients"]
        for table in tables:
            db.execute(text(f'DELETE FROM {table}'))
        
        # Roles
        db.add_all([
            Role(roles_id=ROLE_USER_ID, name="user", description="Users can rent vehicles."),
            Role(roles_id=ROLE_VENDOR_ID, name="vendor", description="Vendor manages fleet."),
            Role(roles_id=ROLE_ADMIN_ID, name="admin", description="System administrator.")
        ])

        # Permissions
        perms_map = {
            "view_vehicles": "117726a4-c106-430a-9a6a-752f43e49ac0",
            "create_booking": "911f816a-fe36-4f6c-b734-bc29baac6848",
            "view_own_bookings": "98edaa53-922d-4c7f-92bb-1e4384d21e39",
            "cancel_own_booking": "97c4fb49-b574-479b-9071-4c0bd3f43237",
            "make_payment": "c4597f6d-aa63-4a34-8438-73b39ecd0519",
            "upload_trip_photos": "dc362866-0d46-4359-a12a-54d9a3853a6a",
            "create_review": "16d3e2c4-002b-472d-8a57-4c7feef36c1a",
            "add_vehicle": "4766c869-1015-45ca-948f-44df46fabfbd",
            "edit_own_vehicle": "6e0ceef6-e5d2-4318-8663-6605c449df99",
            "view_fleet_bookings": "3423a48c-c236-4321-ba2b-597c103dd95b",
            "verify_pickup": "b273b326-56d5-4a7a-be7b-74846b77a7bd",
            "inspect_return": "777c7b73-6dd8-4880-b7c9-9f1cd94d9341",
            "create_damage_report": "308a2aeb-deb1-4ce9-9585-673a76931a07",
            "view_revenue": "e8f6decb-d17a-45b1-a963-81f39e69754c",
            "manage_users": "82a2aa89-6591-470d-ab2b-8b950df4cefc",
            "approve_vendors": "c4ac803b-fd04-401e-ba95-e0794ded4b67",
            "view_all_transactions": "4adf9284-f61e-49fd-ab95-105eeb6ae358",
            "manage_disputes": "364f1f97-5895-450a-8a2e-95ee9e5b7dc5",
            "update_pricing_global": "249cd3f3-975c-46f2-b345-f529c61d654d",
            "system_maintenance": "d0dad7f2-a3f7-4dec-a5a8-b0d9f455cbae",
        }
        for name, p_id in perms_map.items():
            db.add(Permission(permissions_id=uuid.UUID(p_id), name=name))
            if name in ["view_vehicles", "create_booking"]: 
                db.add(RolePermission(role_id=ROLE_USER_ID, permission_id=uuid.UUID(p_id)))

        # Users
        users_data = [
            (MAHARSHI_ID, "maharshi.raval@armakuni.com", ROLE_ADMIN_ID),
            (AJAY_ID, "ajay.joshi@armakuni.com", ROLE_USER_ID),
            (SWAYAM_ID, "swayam.doshi@armakuni.com", ROLE_USER_ID),
            (ROHAN_ID, "rohan.roy@armakuni.com", ROLE_VENDOR_ID),
            (VIVEK_ID, "vivek.thumar@armakuni.com", ROLE_VENDOR_ID),
        ]
        for u_id, email, r_id in users_data:
            db.add(AuthUser(user_id=u_id, email=email, password_hash=get_password_hash("abc"), is_active=True))
            db.add(UsersRole(user_id=u_id, role_id=r_id))

        db.add(Client(client_id=CLIENT_ID, client_name="backend", client_secret="sCxYQLxT5VIpAlMF2VjvEyqv0t3X40D1fO4AA2oeqFw", redirect_url="http://backend:8001/", is_active=True))
        db.commit()
        print("Auth seeding complete.")
    except Exception as e:
        db.rollback()
        print(f"Auth seed failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_auth()
