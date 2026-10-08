from fastapi import APIRouter, HTTPException

from auth.jwt import create_token


router = APIRouter()


@router.post("/login")
def login(username: str, password: str):

    if username == "admin" and password == "12345":

        token = create_token(username)

        return {
            "message": "Login successful",
            "access_token": token,
            "token_type": "bearer"
        }

    raise HTTPException(
        status_code=401,
        detail="Invalid username or password"
    )