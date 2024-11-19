from fastapi import FastAPI
from app.routes import auth, user

app = FastAPI()

app.include_router(user.router, prefix="/register", tags=["Register"])
app.include_router(auth.router, prefix="/login", tags=["Login"])
