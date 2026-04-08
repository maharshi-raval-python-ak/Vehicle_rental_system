from fastapi import FastAPI
from app.api.v1 import routes

app = FastAPI(title="Vehicle-rental-system-platform-BACKEND")
app.include_router(routes.router)
