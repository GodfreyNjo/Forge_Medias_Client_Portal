from fastapi import APIRouter, Form, HTTPException
from backend.models.user import User

router = APIRouter(prefix="/api/auth", tags=["authentication"])

# In-memory user storage (replace with database in production)
users_db = {}

@router.post("/register")
async def register_user(
    email: str = Form(...),
    password: str = Form(...),
    name: str = Form(...),
    company: str = Form(None)
):
    if email in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    
    new_user = User.create(email, name, company)
    users_db[email] = new_user
    
    return {
        "user": new_user.dict(),
        "token": "mock-jwt-token",
        "message": "Account created successfully"
    }

@router.post("/login")
async def login_user(email: str = Form(...), password: str = Form(...)):
    if email in users_db:
        return {
            "user": users_db[email].dict(),
            "token": "mock-jwt-token"
        }
    else:
        # Auto-create user for demo
        from backend.routes.auth import register_user
        return await register_user(email, password, email.split('@')[0], "")
