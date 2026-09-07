
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from app.auth.security import (
    verify_password,
    create_access_token,
    hash_password,
)
from app.db.database import get_db
from app.db.models import User


router = APIRouter()


# ============================================================
# SIGNUP SCHEMA
# ============================================================

class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


# ============================================================
# SIGNUP
# ============================================================

@router.post("/auth/signup")
def signup(
    signup_data: SignupRequest,
    db: Session = Depends(get_db),
):
    """
    Create a new user account.
    """

    # --------------------------------------------------------
    # CHECK IF EMAIL ALREADY EXISTS
    # --------------------------------------------------------

    existing_user = (
        db.query(User)
        .filter(User.email == signup_data.email)
        .first()
    )

    if existing_user is not None:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # --------------------------------------------------------
    # HASH PASSWORD
    # --------------------------------------------------------

    password_hash = hash_password(signup_data.password)

    # --------------------------------------------------------
    # CREATE USER
    # --------------------------------------------------------

    user = User(
        name=signup_data.name,
        email=signup_data.email,
        password_hash=password_hash,
        role="student",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    # --------------------------------------------------------
    # CREATE JWT
    # --------------------------------------------------------

    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "email": user.email,
            "role": user.role,
        }
    )

    # --------------------------------------------------------
    # RESPONSE
    # --------------------------------------------------------

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "role": user.role,
        }
    }


# ============================================================
# LOGIN
# ============================================================

@router.post("/auth/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Authenticate a user using email and password.
    """

    email = form_data.username
    password = form_data.password

    # --------------------------------------------------------
    # FIND USER IN DATABASE
    # --------------------------------------------------------

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # --------------------------------------------------------
    # VERIFY PASSWORD
    # --------------------------------------------------------

    if not verify_password(
        password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # --------------------------------------------------------
    # CREATE JWT
    # --------------------------------------------------------

    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "email": user.email,
            "role": user.role,
        }
    )

    # --------------------------------------------------------
    # RESPONSE
    # --------------------------------------------------------

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "role": user.role,
        }
    }

