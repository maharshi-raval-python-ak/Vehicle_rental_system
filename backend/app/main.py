from fastapi import FastAPI
from app.api.v1 import routes, user_routes, vendor_routes, admin_routes

app = FastAPI(title="Vehicle-rental-system-platform-BACKEND")
app.include_router(routes.router)
app.include_router(user_routes.router)
app.include_router(vendor_routes.router)
app.include_router(admin_routes.router)
