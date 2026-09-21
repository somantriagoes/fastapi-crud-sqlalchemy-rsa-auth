from jose import jwt
import os, time

def sign_token(user):
    payload = {
        "id": user["id"],
        "email": user["email"],
        "exp": time.time() + int(os.getenv("JWT_EXPIRES"))
    }
    return jwt.encode(payload, os.getenv("JWT_SECRET"), algorithm="HS256")

def verify_token(token):
    return jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])