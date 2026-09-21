from fastapi import FastAPI
from api.index import user
from api.auth import register, login, logout
from api import product

app = FastAPI()

app.include_router(register.router, prefix="/api/auth")
app.include_router(login.router, prefix="/api/auth")
app.include_router(logout.router, prefix="/api/auth")

app.include_router(user, prefix="/api")
app.include_router(product.router, prefix="/api")