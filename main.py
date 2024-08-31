from fastapi import FastAPI, Body, Path, Query, status, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
from config.database import Session, engine, Base
from models.recipe import Recipe as RecipeModel
from models.recipe import Category as CategoryModel


app = FastAPI()
app.title = "My recipes"
app.version = "0.0.1"

Base.metadata.create_all(bind=engine)

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data["email"] != "user@mail.com":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

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

class Recipe(BaseModel):
    # id: Optional[int] = Field(ge=1)
    title: str = Field(min_length=5)
    ingredients: list = Field(min_length=3)
    preparation: str = Field(min_length=15)
    # category: str = Field(min_length=5)
    category_id: int = Field(ge=1, Le=100)

    class Config:
        json_schema_extra = {
            "example": {
                # "id": 0,
                "title": "Salad",
                "ingredients": ["tomato", "cucumber", "smoked pepper"],
                "preparation": "Cut all the ingredients in brunoise",
                # "category": "Vegetarian",
                "category_id": 1
            }
        }


recipes = [
    {"id": 1,
     "title": "bulgarian salad",
     "ingredients": ["Tomato","cucumber","grounded white cheese", "smoked pepper", "olive oil", "apple cider vinnegar", "salt", "black pepper"],
     "preparation":"chop the tomatoe, cucumber and the smoked pepper in dices not bigger than 1cm. In a bowl mix the olive oil, vinnegar, salt and back pepper, to make a vinnagrette. Mix all the ingredients and put the cheese on top.",
     "category": "vegetarian",
     "category_id": 2,
     },

     {"id": 2,
     "title": "tarator",
     "ingredients": ["plane yogurt","cucumber", "dill", "fresh garlic", "chopped nuts", "salt", "black pepper"],
     "preparation":"chop the cucumber, garlic and dill. Mix all the ingredients and mixed with the yougurt. keep in the  fridge for 30 prior to serve on the table",
     "category": "vegetarian",
     "category_id": 2,
     },
]


# endpoint home
@app.get('/', tags = ['home'])
def message():
    return "Welcome to my recipes"

# enpoint to login user
@app.post('/login', tags = ['auth'])
def login(user: User):
    if user.email == "user@mail.com" and user.password == "12345678":
        token: str = create_token(user.__dict__)
        return JSONResponse(status_code=status.HTTP_200_OK, content=token)
    
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

# endpoint for all recipes
@app.get('/all', tags = ['recipes'], response_model=List[Recipe], dependencies=[Depends(JWTBearer())])
def get_recipes() -> List[Recipe]:
    db = Session()
    all_recipes = db.query(RecipeModel).all()
    return JSONResponse(content=jsonable_encoder(all_recipes), status_code=status.HTTP_200_OK)

# endpoint to get one recipe
@app.get('/recipe/{id}', tags = ['recipe'], response_model=Recipe)
def get_one(id: int = Path(ge=1, Le=2000)) -> Recipe:
    db = Session()
    recipe = db.query(RecipeModel).filter(RecipeModel.id == id).first()

    if not recipe:
        return JSONResponse(content={"message":"The recipe does not exist"}, status_code=status.HTTP_404_NOT_FOUND)

    return JSONResponse(content=jsonable_encoder(recipe), status_code=status.HTTP_200_OK)

# endpoint to get recipes by category
@app.get('/recipes/', tags=['recipes'], response_model=List[Recipe])
def get_recipes_by_category(category: str = Query(min_length=1)) -> List[Recipe]:
    recipes_by_category = [items for items in recipes if items["category"] == category]
    if not recipes_by_category:
        return JSONResponse(content={"message":f"The category {category} does not exist"}, status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(content=recipes_by_category, status_code=status.HTTP_200_OK)
    
# endpoint to get recipes by category id
@app.get('/recipes/category/{id}', tags=['recipes by category'], response_model=List[Recipe])
def get_recipes_by_category_id(id: int = Path(ge=1, Le=20)) -> List[Recipe]:
    db = Session()
    recipes_by_category = db.query(RecipeModel).filter(RecipeModel.category_id == id).all()
    if not recipes_by_category:
        return JSONResponse(content={"message":f"The category {id} does not exist"}, status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(content=jsonable_encoder(recipes_by_category), status_code=status.HTTP_200_OK)

# endpoint to create recipes
@app.post('/recipes', tags=['recipes'], response_model=dict, status_code=201)
def create_recipe(recipe: Recipe) -> dict:
    db = Session()
    newRecipe = RecipeModel(**recipe.model_dump())

    db.add(newRecipe)
    db.commit() 
    title = recipe.title
    # recipes.append(recipe.model_dump())
    return JSONResponse(content={"message":f"the recipe {title} has been added"}, status_code=status.HTTP_201_CREATED)

#endpoint to update recipes
@app.put('/recipe/{id}', tags = ['recipe'], response_model=dict)
def update_recipe(id: int, recipe: Recipe) -> dict:
     
    # db = Session()
    # recipe = db.query(RecipeModel).filter(RecipeModel.id == id).first()

    for item in recipes:
        if item["id"] == id:
            item.update({
            "id": recipe.id,
            "title": recipe.title,
            "ingredients": recipe.ingredients,
            "preparation": recipe.preparation,
            "category_id": recipe.category_id
            })
            return JSONResponse(content={"message":f"the recipe {recipe.title} has been updated"},status_code=status.HTTP_202_ACCEPTED)
        
    return JSONResponse(content={"message":"The recipe does not exist"}, status_code=status.HTTP_404_NOT_FOUND)
        
    
# endpoint to delete recipes
@app.delete('/recipe/{id}', tags = ['recipe'], response_model=dict)
def del_recipe(id: int = Path(ge=1, Le=2000)) -> dict:
    for item in recipes:
        if item["id"] == id:
            deleted = item["title"]
            recipes.remove(item)
            return JSONResponse(content={"messsage":f"the recipe {deleted} has been deleted"}, status_code=status.HTTP_202_ACCEPTED)
        
    return JSONResponse(content={"message":"The recipe does not exist"}, status_code=status.HTTP_404_NOT_FOUND)
    