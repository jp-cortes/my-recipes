from fastapi import APIRouter
from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, EmailStr
from jwt_manager import create_token, encode_password
from config.database import Session
from middlewares.auth import validate_user
from models.user import User as UserModel


user_router = APIRouter()

class User(BaseModel):
    email: EmailStr = Field(description="A valid email is required")
    password: str= Field(min_length=8, max_length=50, description="The password must be between 8 and 50 characters")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@mail.com",
                "password": "V@lidPassword123!"
            }
        }


class CreateUser(BaseModel):
    name: str = Field(min_length=2, max_length=50, description="The name must be between 2 and 50 characters")
    email: EmailStr = Field(description="A valid email is required")
    password: str= Field(min_length=8, max_length=50, description="The password must be between 8 and 50 characters")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "user@mail.com",
                "password": "V@lidPassword123!"
            }
        }




# endpoint to create users
@user_router.post('/users', tags=['users'], response_model=dict, status_code=201)
def create_user(user: CreateUser) -> dict:
    
    db = Session()
    verify_user = db.query(UserModel).filter(UserModel.email == user.email).first()

    if verify_user:
        return JSONResponse(content={"message":"The user already have an account"}, status_code=status.HTTP_409_CONFLICT)
    
     # Check if this is the first user in the database
    user_count = db.query(UserModel).count()
    
    # Assign the role based on whether there are any users already
    role = "admin" if user_count == 0 else "user"
    
    hashed_password = encode_password(user.password)
    newUser = UserModel(name= user.name, email= user.email, password=hashed_password, role=role)

    db.add(newUser)
    db.commit() 
    db.refresh(newUser)
    
    return JSONResponse(content={"message":"the user has been added"}, status_code=status.HTTP_201_CREATED)


# enpoint to login users
@user_router.post('/login', tags = ['users'])
def login(user: User):
    
    db = Session()
       
    auth = validate_user(user, db, UserModel, encode_password)

    if not auth:
        token: str = create_token(user.__dict__)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"token": token})

    return auth
