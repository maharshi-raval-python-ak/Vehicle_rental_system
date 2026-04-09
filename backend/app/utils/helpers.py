import httpx
from fastapi import HTTPException
from loguru import logger
from functools import wraps
import time
from app.schemas.auth_schemas import AuthData

def log_args_and_response(func):
    """
    Logs the arguments and responses in app.log file

    :param func: The function to be decorated
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        This is the wrapper function that logs the arguments and responses of the decorated function
        
        :param args: The arguments passed to the decorated function
        :param kwargs: The keyword arguments passed to the decorated function
        """
        logger.info(f"Function: {func.__name__}, called with args: {args}, kwargs: {kwargs}")
        response = func(*args, **kwargs)
        logger.info(f"Function response: {response}\n")
        return response
    return wrapper

AUTH_SERVICE_URL = "http://localhost:8001/auth/validate" # change "localhost" to "<auth service name>" if use docker

def authenticated(allowed_roles: list[str] | None = None,required_permissions: list[str] | None = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            access_token = kwargs.get("access_token")
            
            if not access_token:
                raise HTTPException(status_code=401, detail="Missing access token")

            async with httpx.AsyncClient() as client:
                try:
                    response = await client.post(
                        AUTH_SERVICE_URL, 
                        params={"access_token": access_token}
                    )
                except httpx.RequestError:
                    raise HTTPException(status_code=503, detail="Auth service unavailable")

            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code, 
                    detail=response.json().get("detail", "Validation failed")
                )
            
            data = response.json()
            auth_obj = AuthData(**data) 
            
            user_roles = auth_obj.roles
            user_perms = auth_obj.permissions

            if "admin" in user_roles:
                pass 
            
            elif required_permissions:
                if not any(perm in user_perms for perm in required_permissions):
                    raise HTTPException(
                        status_code=403, 
                        detail=f"Missing required permission(s): {required_permissions}"
                    )
            
            elif allowed_roles:
                if not any(role in user_roles for role in allowed_roles):
                    raise HTTPException(status_code=403, detail="Role access denied")

            kwargs["auth_info"] = auth_obj 
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator