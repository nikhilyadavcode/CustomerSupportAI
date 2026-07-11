from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from database.users import users_collection
from services.auth_service import (
    hash_password,
    verify_password,
    create_access_token
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


# ==========================
# Register
# ==========================
@router.post("/register")
def register(data: RegisterRequest):

    existing_user = users_collection.find_one({"email": data.email})

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists."
        )

    user = {
        "name": data.name,
        "email": data.email,
        "password": hash_password(data.password)
    }

    users_collection.insert_one(user)

    return {
        "message": "User registered successfully."
    }


# ==========================
# Login
# ==========================
@router.post("/login")
def login(data: LoginRequest):

    user = users_collection.find_one({"email": data.email})

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    if not verify_password(
        data.password,
        user["password"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    token = create_access_token(
        {
            "sub": user["email"]
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "name": user["name"],
        "email": user["email"]
    }