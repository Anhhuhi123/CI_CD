from fastapi import APIRouter
from config.database import get_database
from app.models.users import User
from fastapi import HTTPException, status
db = get_database()
router = APIRouter()


@router.post("/auth/login", status_code=200)
async def login(user: User):
    username = user.username
    password = user.password

    found_user = db.users.find_one({"username": username, "password": password})
    if found_user:
        return {"message": "Login successful", "username": username}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

@router.post("/auth/register", status_code=201)
async def register(user: User):
    username = user.username
    password = user.password

    existing_user = db.users.find_one({"username": username})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )