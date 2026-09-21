from fastapi import APIRouter, Depends
from config.db import conn
from models.index import users
from schemas.index import User
from middleware.auth import auth_required
import bcrypt

user = APIRouter()


def serialize_users(rows):
    return [dict(row._mapping) for row in rows]


@user.get("/users")
async def get_users(user=Depends(auth_required)):
    rows = conn.execute(users.select()).fetchall()
    
    return serialize_users(rows)


@user.get("/user/{id}")
async def get_user(id: int, user=Depends(auth_required)):
    rows = conn.execute(users.select().where(users.c.id == id)).fetchall()
    return serialize_users(rows)


@user.put("/user/{id}")
async def update_user(id: int, updateUser: User, user=Depends(auth_required)):
    hashed = bcrypt.hashpw(
        updateUser.password.encode(),
        bcrypt.gensalt()
    )
    
    conn.execute(
        users.update()
        .where(users.c.id == id)
        .values(
            name=updateUser.name,
            email=updateUser.email,
            password=hashed,
        )
    )
    conn.commit()
    rows = conn.execute(users.select().where(users.c.id == id)).fetchall()
    return serialize_users(rows)


@user.delete("/user/{id}")
async def delete_user(id: int, user=Depends(auth_required)):
    conn.execute(users.delete().where(users.c.id == id))
    conn.commit()
    rows = conn.execute(users.select().where(users.c.id == id)).fetchall()
    return serialize_users(rows)