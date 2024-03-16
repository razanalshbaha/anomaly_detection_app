from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta 
from app.database.database import users_collection
from fastapi.security import OAuth2PasswordRequestForm
from bson import ObjectId
from app.services.router_utils import bcrypt_context, authenticate_user, authenticate_user_email, create_access_token
from app.schemas.schemas import CreateUserRequest, Token, Response

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest):
    existing_user = users_collection.find_one({"email": create_user_request.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already in use."
        )
    if not authenticate_user_email(create_user_request.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email."
        )

    hashed_password = bcrypt_context.hash(create_user_request.password)
    new_user = {
        "id": str(ObjectId()),
        "email": create_user_request.email,
        "hashed_password": hashed_password,
        "is_active": True,
    }
    users_collection.insert_one(new_user)
    return Response(message="Account created successfully")


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
        )
    token = create_access_token(user["email"], str(user["id"]), timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer"}
