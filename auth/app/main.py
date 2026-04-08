from fastapi import FastAPI
from app.api.v1 import routes

app = FastAPI(title="Vehicle-rental-service-platform-AUTHENTICATION")
app.include_router(routes.router)
