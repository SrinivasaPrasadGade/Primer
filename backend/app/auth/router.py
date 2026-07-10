from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.auth.security import create_access_token, verify_password
from app.database import get_db

router = APIRouter()


class LoginRequest(BaseModel):
    email: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class UserOut(BaseModel):
    id: str
    email: str
    name: str
    role: str
    designation: str | None = None
    jurisdiction: str | None = None


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


@router.post("/login", response_model=LoginResponse)
async def login(req: LoginRequest, db: AsyncSession = Depends(get_db)):
    row = (
        await db.execute(
            text(
                """
                SELECT id, email, name, role, designation, jurisdiction, password_hash, is_active
                FROM core.users WHERE email = :email
                """
            ),
            {"email": req.email},
        )
    ).mappings().first()

    if row is None or not row["is_active"] or not verify_password(req.password, row["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(
        {
            "sub": str(row["id"]),
            "name": row["name"],
            "role": row["role"],
            "jurisdiction": row["jurisdiction"],
        }
    )
    user = UserOut(
        id=str(row["id"]),
        email=row["email"],
        name=row["name"],
        role=row["role"],
        designation=row["designation"],
        jurisdiction=row["jurisdiction"],
    )
    return LoginResponse(access_token=token, user=user)


@router.get("/me", response_model=UserOut)
async def me(user: dict = Depends(get_current_user)):
    return UserOut(
        id=str(user["id"]),
        email=user["email"],
        name=user["name"],
        role=user["role"],
        designation=user["designation"],
        jurisdiction=user["jurisdiction"],
    )
