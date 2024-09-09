from fastapi import APIRouter
from fastapi import Path, status, Depends, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from schemas.recipe import Recipe
from typing import List
from config.database import Session
from middlewares.jwt_bearer import JWTBearerAdmin, JWTBearerUser
from services.recipe import RecipeService


recipe_router = APIRouter()


# endpoint for all recipes
@recipe_router.get('/recipes', tags = ['recipes'], response_model=List[Recipe])
def get_recipes() -> List[Recipe]:
    db = Session()
    all_recipes = RecipeService(db).get_recipes()
    return JSONResponse(content=jsonable_encoder(all_recipes), status_code=status.HTTP_200_OK)


# endpoint to get one recipe
@recipe_router.get('/recipe/{id}', tags = ['recipes'], response_model=Recipe, dependencies=[Depends(JWTBearerUser())])
def get_one(id: int = Path(ge=1, Le=2000)) -> Recipe:
    db = Session()
    recipe = RecipeService(db).get_one(id)

    if not recipe:
        return JSONResponse(content={"message":"The recipe does not exist"}, status_code=status.HTTP_404_NOT_FOUND)

    return JSONResponse(content=jsonable_encoder(recipe), status_code=status.HTTP_200_OK)


# endpoint to get recipes by category id
@recipe_router.get('/recipes/category/{id}', tags=['recipes'], response_model=List[Recipe])
def get_recipes_by_category_id(id: int = Path(ge=1, Le=20)) -> List[Recipe]:
    db = Session()
    recipes_by_category = RecipeService(db).get_by_Category_id(id)
    if not recipes_by_category:
        return JSONResponse(content={"message":f"The category {id} does not exist"}, status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(content=jsonable_encoder(recipes_by_category), status_code=status.HTTP_200_OK)

'''# endpoint to get recipes by category name
@recipe_router.get('/recipes/', tags=['recipes'], response_model=List[Recipe])
def get_recipes_by_category(category: str = Query(min_length=1)) -> List[Recipe]:
    db = Session()
    recipes_by_category = RecipeService(db).get_by_Category_name(category)
    if not recipes_by_category:
        return JSONResponse(content={"message":f"The category {category} does not exist"}, status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(content=recipes_by_category, status_code=status.HTTP_200_OK)
    '''


# endpoint to create recipes
@recipe_router.post('/recipe', tags=['recipes'], response_model=dict, dependencies=[Depends(JWTBearerUser())])
def create_recipe(recipe: Recipe) -> dict:
    db = Session()

    search_recipe = RecipeService(db).check_recipe(recipe.title)
    if search_recipe:
        return JSONResponse(content={"message":f"There is already a recipe with the name {recipe.title}"}, status_code=status.HTTP_403_FORBIDDEN)

    RecipeService(db).create_recipe(recipe)

    title = recipe.title
    
    return JSONResponse(content={"message":f"the recipe {title} has been added"}, status_code=status.HTTP_201_CREATED)


#endpoint to update recipes
@recipe_router.put('/recipe/{id}', tags = ['recipes'], response_model=dict, dependencies=[Depends(JWTBearerAdmin())])
def update_recipe(id: int, update: Recipe) -> dict:
     
    db = Session()
    recipe = RecipeService(db).get_one(id)

    if not recipe:
        return JSONResponse(content={"message":"The recipe does not exist"}, status_code=status.HTTP_404_NOT_FOUND)
    
    RecipeService(db).update_recipe(id, update)
        
    return JSONResponse(content={"message":f"the recipe {update.title} has been updated"},status_code=status.HTTP_202_ACCEPTED)
        
          
# endpoint to delete recipes
@recipe_router.delete('/recipe/{id}', tags = ['recipes'], response_model=dict, dependencies=[Depends(JWTBearerAdmin())])
def del_recipe(id: int = Path(ge=1, Le=2000)) -> dict:
    db = Session()
    recipe = RecipeService(db).get_one(id)
    
    if not recipe:
        return JSONResponse(content={"message":"The recipe does not exist"}, status_code=status.HTTP_404_NOT_FOUND)
    
    title = recipe.title

    RecipeService(db).delete_recipe(recipe)

        
    return JSONResponse(content={"messsage":f"the recipe {title} has been deleted"}, status_code=status.HTTP_202_ACCEPTED)
    