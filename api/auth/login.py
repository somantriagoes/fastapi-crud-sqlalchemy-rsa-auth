from fastapi import APIRouter, HTTPException
from config.db import conn
from models.index import users
import bcrypt
from utils.rsa import decrypt_password
from utils.jwt import sign_token


router = APIRouter()


def serialize_users(rows):
    return [dict(row._mapping) for row in rows]

def resolve_login_password(raw_password):
    if raw_password is None:
        raise HTTPException(status_code=400, detail="Password is required")

    try:
        return decrypt_password(raw_password)
    except (TypeError, ValueError):
        return str(raw_password)
    
@router.post("/login")
def login(data: dict):
    user = conn.execute(users.select().where(users.c.email == data["email"])).fetchone()
        
    if user:
        user = dict(user._mapping)
        if bcrypt.checkpw(resolve_login_password(data["password"]).encode(), user["password"].encode()):
            return { 
                "user": {
                    "id": user["id"],
                    "name": user["name"],
                    "email": user["email"]
                },
                "access_token": sign_token(user),
                "token_type": "Bearer",
            }
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
    return {"message": "Invalid email or password"}