from fastapi import APIRouter
from app.utils.helpers import authenticated

router = APIRouter()


# @router.get("/protected-resource")
# @authenticated
# async def get_data(
#     access_token: str
# ):
#     return {"status": "success", }
