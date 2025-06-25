from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from .. import models, oauth2
from ..utils import dbAdaptor

router = APIRouter()
db = dbAdaptor.DBAdaptor()

@router.post("/signup", response_model=models.UserOut)
async def sign_up(user: models.UserCreate):
    created = await db.sign_up_user(user.username, user.email, user.password)
    if not created:
        raise HTTPException(status_code=400, detail="Email already registered")
    return created

@router.post("/signin", response_model=models.Token)
async def sign_in(request: OAuth2PasswordRequestForm = Depends()):
    existing = await db.sign_in_user(request.username, request.password)
    if not existing:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = oauth2.create_access_token(data={"sub": existing["email"]})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

"""
@router.get("/user/me", response_model=models.UserOut)
async def get_me(current_user: dict = Depends(oauth2.get_current_user)):
    return {
        "id": str(current_user.id),
        "username": current_user.username,
        "email": current_user.email
    } """