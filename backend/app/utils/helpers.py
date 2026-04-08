import httpx
from fastapi import HTTPException
from loguru import logger
from functools import wraps
import time

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

def authenticated(func):
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
        
        return await func(*args, **kwargs)
    return wrapper
