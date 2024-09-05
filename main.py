from fastapi import FastAPI, Body, Path, Query, status, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token, encode_password
from fastapi.security import HTTPBearer
from config.database import Session, engine, Base
from middlewares.auth import validate_user
from models.recipe import Recipe as RecipeModel
from models.recipe import Category as CategoryModel
from models.user import User as UserModel
from routers.recipe import recipe_router


app = FastAPI()
app.title = "My recipes"
app.version = "0.0.1"

app.include_router(recipe_router)

Base.metadata.create_all(bind=engine)



class Category(BaseModel):
    # id: Optional[int] = 
    title: str = Field(min_length=5)

    class Config:
        json_schema_extra = {
            "example": {
                # "id": 0,
                "title": "Vegetarian"
            }
        }

class User(BaseModel):
    email: str
    password: str




sample_recipes = [
    {"id": 1,
     "title": "bulgarian salad",
     "ingredients": ["Tomato","cucumber","grounded white cheese", "smoked pepper", "olive oil", "apple cider vinnegar", "salt", "black pepper"],
     "preparation":"chop the tomatoe, cucumber and the smoked pepper in dices not bigger than 1cm. In a bowl mix the olive oil, vinnegar, salt and back pepper, to make a vinnagrette. Mix all the ingredients and put the cheese on top.",
     "category_id": 1,
     },

     {"id": 2,
     "title": "tarator",
     "ingredients": ["plane yogurt","cucumber", "dill", "fresh garlic", "chopped nuts", "salt", "black pepper"],
     "preparation":"chop the cucumber, garlic and dill. Mix all the ingredients and mixed with the yougurt. keep in the  fridge for 30 prior to serve on the table",
     "category_id": 1,
     },
]


# endpoint home
@app.get('/', tags = ['home'])
def message():
    return "Welcome to my recipes"

# endpoint to create users
@app.post('/users', tags=['users'], response_model=dict, status_code=201)
def create_user(user: User) -> dict:
    
    db = Session()
    verify_user = db.query(UserModel).filter(UserModel.email == user.email).first()

    if verify_user:
        return JSONResponse(content={"message":"The user already have an account"}, status_code=status.HTTP_404_NOT_FOUND)
    
    hashed_password = encode_password(user.password)
    newUser = UserModel(name= user.name, email= user.email, password=hashed_password)

    db.add(newUser)
    db.commit() 
    db.refresh(newUser)
    
    return JSONResponse(content={"message":"the user has been added"}, status_code=status.HTTP_201_CREATED)


# enpoint to login users
@app.post('/login', tags = ['auth'])
def login(user: User):
    
    db = Session()
       
    auth = validate_user(user, db, UserModel, encode_password)

    if not auth:
        token: str = create_token(user.__dict__)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"token": token})

    return auth


# endpoint to create categories
@app.post('/categories', tags=['categories'], response_model=dict, status_code=201)
def create_category(category: Category) -> dict:
    db = Session()
    newCategory = CategoryModel(**category.model_dump())

    db.add(newCategory)
    db.commit() 
    title = category.title
    # recipes.append(category.model_dump())
    return JSONResponse(content={"message":f"the category {title} has been added"}, status_code=status.HTTP_201_CREATED)




# endpoint to get recipes by category name
'''@app.get('/recipes/', tags=['recipes'], response_model=List[Recipe])
def get_recipes_by_category(category: str = Query(min_length=1)) -> List[Recipe]:
    recipes_by_category = [items for items in sample_recipes if items["category"] == category]
    if not recipes_by_category:
        return JSONResponse(content={"message":f"The category {category} does not exist"}, status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(content=recipes_by_category, status_code=status.HTTP_200_OK)'''
    

