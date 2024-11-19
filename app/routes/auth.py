from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.firebase import db
from app.schemas import UserCreate
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/", response_model=dict)
async def login_user(user: UserCreate):
    # Check user existence
    users_ref = db.collection("users")
    existing_user = users_ref.where("email", "==", user.email).get()

    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    user_data = existing_user[0].to_dict()

    # Verify password
    if not pwd_context.verify(user.password, user_data["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Successful login
    return {"message": "This is home"}