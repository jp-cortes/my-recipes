from fastapi import APIRouter
from fastapi import status, Depends
from fastapi.responses import JSONResponse
from schemas.user import CreateUser, User
from utils.jwt_manager import create_token, encode_password
# from middlewares.jwt_bearer import JWTBearerAdmin, JWTBearerUser
from config.database import Session
from middlewares.auth import validate_user
from models.user import User as UserModel
from services.user import UserService

user_router = APIRouter()



# endpoint to create users
@user_router.post('/register', tags=['users'], response_model=dict, status_code=201)
def create_user(user: CreateUser) -> dict:
    
    db = Session()
    verify_user = UserService(db).check_user(user)

    if verify_user:
        return JSONResponse(content={"message":"The user already have an account"}, status_code=status.HTTP_409_CONFLICT)
    
    UserService(db).create_user(user, encode_password)
    
    return JSONResponse(content={"message":"the user has been added"}, status_code=status.HTTP_201_CREATED)


# endpoint to login users
@user_router.post('/login', tags = ['users'])
def login(user: User):
    
    db = Session()

    user_role = UserService(db).get_user_role(user)
    
    auth = validate_user(user, db, UserModel, encode_password)
    
    login = { "email": user.email, "password": user.password, "role": user_role}
       

    if not auth:
        token: str = create_token(login)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"token": token})

    return auth


