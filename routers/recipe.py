from fastapi import APIRouter
from fastapi import Path, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing import List
from config.database import Session
from middlewares.jwt_bearer import JWTBearerAdmin, JWTBearerUser
from models.recipe import Recipe as RecipeModel


recipe_router = APIRouter()


class Recipe(BaseModel):
    title: str = Field(min_length=5)
    ingredients: list = Field(min_length=3)
    preparation: str = Field(min_length=15)
    category_id: int = Field(ge=1, Le=100)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "bulgarian salad",
                "ingredients": ["Tomato","cucumber","grounded white cheese", "smoked pepper", "olive oil", "apple cider vinnegar", "salt", "black pepper"],
                "preparation": "chop the tomatoes, cucumber and the smoked pepper in dices not bigger than 1cm. In a bowl mix the olive oil, vinnegar, salt and back pepper, to make a vinnagrette. Mix all the ingredients and put the cheese on top.",
                "category_id": 1
            }
        }


# endpoint for all recipes
@recipe_router.get('/all', tags = ['recipes'], response_model=List[Recipe])
def get_recipes() -> List[Recipe]:
    db = Session()
    all_recipes = db.query(RecipeModel).all()
    return JSONResponse(content=jsonable_encoder(all_recipes), status_code=status.HTTP_200_OK)


# endpoint to get one recipe
@recipe_router.get('/recipe/{id}', tags = ['recipes'], response_model=Recipe, dependencies=[Depends(JWTBearerUser())])
def get_one(id: int = Path(ge=1, Le=2000)) -> Recipe:
    db = Session()
    recipe = db.query(RecipeModel).filter(RecipeModel.id == id).first()

    if not recipe:
        return JSONResponse(content={"message":"The recipe does not exist"}, status_code=status.HTTP_404_NOT_FOUND)

    return JSONResponse(content=jsonable_encoder(recipe), status_code=status.HTTP_200_OK)


# endpoint to get recipes by category id
@recipe_router.get('/recipes/category/{id}', tags=['recipes'], response_model=List[Recipe])
def get_recipes_by_category_id(id: int = Path(ge=1, Le=20)) -> List[Recipe]:
    db = Session()
    recipes_by_category = db.query(RecipeModel).filter(RecipeModel.category_id == id).all()
    if not recipes_by_category:
        return JSONResponse(content={"message":f"The category {id} does not exist"}, status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(content=jsonable_encoder(recipes_by_category), status_code=status.HTTP_200_OK)


# endpoint to create recipes
@recipe_router.post('/recipes', tags=['recipes'], response_model=dict, dependencies=[Depends(JWTBearerUser())])
def create_recipe(recipe: Recipe) -> dict:
    db = Session()
    newRecipe = RecipeModel(**recipe.model_dump())

    db.add(newRecipe)
    db.commit() 
    title = recipe.title
    
    return JSONResponse(content={"message":f"the recipe {title} has been added"}, status_code=status.HTTP_201_CREATED)


#endpoint to update recipes
@recipe_router.put('/recipe/{id}', tags = ['recipes'], response_model=dict, dependencies=[Depends(JWTBearerAdmin())])
def update_recipe(id: int, update: Recipe) -> dict:
     
    db = Session()
    recipe = db.query(RecipeModel).filter(RecipeModel.id == id).first()

    if not recipe:
        return JSONResponse(content={"message":"The recipe does not exist"}, status_code=status.HTTP_404_NOT_FOUND)
    
    recipe.title = update.title
    recipe.ingredients = update.ingredients
    recipe.preparation = update.preparation
    recipe.category_id = update.category_id
    
    
    db.commit()
    db.refresh(recipe)
        
    return JSONResponse(content={"message":f"the recipe {recipe.title} has been updated"},status_code=status.HTTP_202_ACCEPTED)
        
          
# endpoint to delete recipes
@recipe_router.delete('/recipe/{id}', tags = ['recipes'], response_model=dict, dependencies=[Depends(JWTBearerAdmin())])
def del_recipe(id: int = Path(ge=1, Le=2000)) -> dict:
    db = Session()
    recipe = db.query(RecipeModel).filter(RecipeModel.id == id).first()
    
    if not recipe:
        return JSONResponse(content={"message":"The recipe does not exist"}, status_code=status.HTTP_404_NOT_FOUND)
    
    title = recipe.title

    db.delete(recipe)
    db.commit()

        
    return JSONResponse(content={"messsage":f"the recipe {title} has been deleted"}, status_code=status.HTTP_202_ACCEPTED)
    