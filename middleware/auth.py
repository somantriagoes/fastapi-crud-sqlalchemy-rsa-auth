from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from utils.jwt import verify_token

security = HTTPBearer()

def auth_required(credentials=Depends(security)):
    try:
        return verify_token(credentials.credentials)
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )