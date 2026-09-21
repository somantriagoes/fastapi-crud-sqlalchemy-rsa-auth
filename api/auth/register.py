from fastapi import APIRouter
from config.db import conn
from models.index import users
from schemas.index import User
import bcrypt

router = APIRouter()


def serialize_users(rows):
    return [dict(row._mapping) for row in rows]

@router.post("/register")
async def create_user(user: User):
    hashed = bcrypt.hashpw(
        user.password.encode(),
        bcrypt.gensalt()
    )
        
    conn.execute(
        users.insert().values(
            name=user.name,
            email=user.email,
            password=hashed,
        )
    )
    conn.commit()
    rows = conn.execute(users.select()).fetchall()
    return {"users": serialize_users(rows), "message": "User registered successfully"}