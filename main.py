from fastapi import FastAPI, Body, Path, Query, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token

class User(BaseModel):
    email: str
    password: str

class Recipe(BaseModel):
    id: Optional[int] = Field(ge=1)
    title: str = Field(min_length=5)
    ingredients: list = Field(min_length=3)
    preparation: str = Field(min_length=15)
    category: str = Field(min_length=5)
    category_id: int = Field(ge=1, Le=100)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 0,
                "title": "Salad",
                "ingredients": ["tomato", "cucumber", "smoked pepper"],
                "preparation": "Cut all the ingredients in brunoise",
                "category": "Vegetarian",
                "category_id": 2
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

app = FastAPI()
app.title = "My recipes"
app.version = "0.0.1"

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

# endpoint for all recipes
@app.get('/all', tags = ['recipes'], response_model=List[Recipe])
def get_recipes() -> List[Recipe]:
    return JSONResponse(content=recipes, status_code=status.HTTP_200_OK)

# endpoint to get one recipe
@app.get('/recipe/{id}', tags = ['recipe'], response_model=Recipe)
def get_one(id: int = Path(ge=1, Le=2000)) -> Recipe:
    recipe = [item for item in recipes if item["id"] == id]
    if recipe:
        return JSONResponse(content=recipe, status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content={"message":"The recipe does not exist"}, status_code=status.HTTP_404_NOT_FOUND)

# endpoint to get recipes by category
@app.get('/recipes/', tags=['recipes'], response_model=List[Recipe])
def get_recipes_by_category(category: str = Query(min_length=5)) -> List[Recipe]:
    recipes_by_category = [items for items in recipes if items["category"] == category]
    if recipes_by_category:
        return JSONResponse(content=recipes_by_category, status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content={"message":f"The category {category} does not exist"}, status_code=status.HTTP_404_NOT_FOUND)

# endpoint to create recipes
@app.post('/recipes', tags=['recipes'], response_model=dict, status_code=201)
def create_recipe(recipe: Recipe) -> dict:
    title = recipe.title
    recipes.append(recipe.model_dump())
    return JSONResponse(content={"message":f"the recipe {title} has been added"}, status_code=status.HTTP_201_CREATED)

#endpoint to update recipes
@app.put('/recipe/{id}', tags = ['recipe'], response_model=dict)
def update_recipe(id: int, recipe: Recipe) -> dict:
     
    for item in recipes:
        if item["id"] == id:
            item.update({
            "id": recipe.id,
            "title": recipe.title,
            "ingredients": recipe.ingredients,
            "preparation": recipe.preparation,
            "category": recipe.category,
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
    