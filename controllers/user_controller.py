from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from config.database import users_collection
from passlib.context import CryptContext
import jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from bson import ObjectId

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter()
templates = Jinja2Templates(directory="templates")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Route to render login page
@router.get("/")
async def show_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# User Registration
@router.post("/users/register")
async def register_user(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    conf_pass: str = Form(...)
):
    messages = []
    if password != conf_pass:
        messages.append("Passwords do not match!")
    if users_collection.find_one({"email": email}):
        messages.append("Email already registered!")
    
    if messages:
        return templates.TemplateResponse("login.html", {"request": request, "messages": messages})

    hashed_password = pwd_context.hash(password)
    new_user = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": hashed_password
    }
    
    users_collection.insert_one(new_user)

    request.session["user"] = {
    "_id": str(new_user["_id"]),
    "email": new_user["email"],
    "first_name": new_user["first_name"]
    }
    # Redirect user back to the login page instead of dashboard
    return RedirectResponse(url="/welcome", status_code=303)

# User Login
@router.post("/users/login")
async def login_user(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    messages = []
    user = users_collection.find_one({"email": email})
    
    if not user or not pwd_context.verify(password, user["password"]):
        messages.append("Invalid credentials!")
        return templates.TemplateResponse("login.html", {"request": request, "messages": messages})

    # ✅ Save user info to session
    request.session["user"] = {
        "_id": str(user["_id"]),
        "email": user["email"],
        "first_name": user["first_name"]
    }

    access_token = jwt.encode(
        {"sub": user["email"], "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)},
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return RedirectResponse(url="/welcome", status_code=303)



# Logout
@router.get("/users/logout")
async def logout(request: Request):
    request.session.clear()  # This deletes everything from session
    return RedirectResponse(url="/", status_code=303)
