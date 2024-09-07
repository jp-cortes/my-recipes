from fastapi import APIRouter
from fastapi import status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from schemas.category import Category
from typing import List
from config.database import Session
from models.category import Category as CategoryModel
from middlewares.jwt_bearer import JWTBearerUser, JWTBearerAdmin
from services.category import CategoryService


category_router = APIRouter()



# endpoint to see all categories
@category_router.get('/categories', tags = ['categories'], response_model=List[Category])
def get_categories() -> List[Category]:
    db = Session()
    all_recipes = CategoryService(db).get_categories()
    return JSONResponse(content=jsonable_encoder(all_recipes), status_code=status.HTTP_200_OK)


# endpoint to create categories
@category_router.post('/categories', tags=['categories'], response_model=dict, dependencies=[Depends(JWTBearerUser())])
def create_category(category: Category) -> dict:
    db = Session()
    verify_category = CategoryService(db).get_category_by_title(category.title)

    if verify_category:
        return JSONResponse(content={"message":"There is already a category under that name"}, status_code=status.HTTP_409_CONFLICT)
    
    CategoryService(db).create_category(category)
    title = category.title
    
    return JSONResponse(content={"message":f"the category {title} has been added"}, status_code=status.HTTP_201_CREATED)



#endpoint to update categories
@category_router.put('/category/{id}', tags = ['categories'], response_model=dict, dependencies=[Depends(JWTBearerAdmin())])
def update_category(id: int, update: Category) -> dict:
     
    db = Session()
    category = CategoryService(db).get_category_by_id(id)

    if not category:
        return JSONResponse(content={"message":"The category does not exist"}, status_code=status.HTTP_404_NOT_FOUND)
    
    CategoryService(db).update_category(category, update)
    
    return JSONResponse(content={"message":f"the category {update.title} has been updated"},status_code=status.HTTP_202_ACCEPTED)
        
          