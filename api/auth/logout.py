from fastapi import APIRouter

router = APIRouter()

@router.post("/logout")
def logout():
    return {"message": "Logout handled on client side"}