from fastapi import status, Request, HTTPException
from jwt_manager import validate_token
from fastapi.security import HTTPBearer


class JWTBearerAdmin(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data["role"] != "admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
        
class JWTBearerUser(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        token = validate_token(auth.credentials)
        if not token:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You need to login first")