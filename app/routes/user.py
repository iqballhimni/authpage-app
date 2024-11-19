from fastapi import APIRouter, HTTPException
from app.firebase import db
from app.schemas import UserCreate
from passlib.context import CryptContext
import uuid

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/", response_model=dict)
async def register_user(user: UserCreate):
    # Generate UID
    user_id = str(uuid.uuid4())

    # Check if user already exists
    users_ref = db.collection("users")
    existing_user = users_ref.where("email", "==", user.email).get()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password
    hashed_password = pwd_context.hash(user.password)

    # Save to Firestore
    users_ref.document(user_id).set({
        "email": user.email,
        "password": hashed_password,
        "uid": user_id
    })

    return {"message": "User registered successfully", "uid": user_id}