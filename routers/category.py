from fastapi import APIRouter
from fastapi import status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing import List
from config.database import Session
from models.recipe import Category as CategoryModel
from middlewares.jwt_bearer import JWTBearerUser, JWTBearerAdmin


category_router = APIRouter()

class Category(BaseModel):
    title: str = Field(min_length=5)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Vegetarian"
            }
        }

# endpoint to see all categories
@category_router.get('/categories', tags = ['categories'], response_model=List[Category])
def get_categories() -> List[Category]:
    db = Session()
    all_recipes = db.query(CategoryModel).all()
    return JSONResponse(content=jsonable_encoder(all_recipes), status_code=status.HTTP_200_OK)


# endpoint to create categories
@category_router.post('/categories', tags=['categories'], response_model=dict, dependencies=[Depends(JWTBearerUser())])
def create_category(category: Category) -> dict:
    db = Session()
    verify_category = db.query(CategoryModel).filter(CategoryModel.title == category.title).first()

    if verify_category:
        return JSONResponse(content={"message":"There is already a category under that name"}, status_code=status.HTTP_409_CONFLICT)
    
    newCategory = CategoryModel(**category.model_dump())

    db.add(newCategory)
    db.commit() 
    title = category.title
    
    return JSONResponse(content={"message":f"the category {title} has been added"}, status_code=status.HTTP_201_CREATED)




# endpoint to get recipes by category name
'''@category_router.get('/recipes/', tags=['recipes'], response_model=List[Recipe])
def get_recipes_by_category(category: str = Query(min_length=1)) -> List[Recipe]:
    recipes_by_category = [items for items in sample_recipes if items["category"] == category]
    if not recipes_by_category:
        return JSONResponse(content={"message":f"The category {category} does not exist"}, status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(content=recipes_by_category, status_code=status.HTTP_200_OK)'''
    


#endpoint to update categories
@category_router.put('/category/{id}', tags = ['categories'], response_model=dict, dependencies=[Depends(JWTBearerAdmin())])
def update_category(id: int, update: Category) -> dict:
     
    db = Session()
    category = db.query(CategoryModel).filter(CategoryModel.id == id).first()

    if not category:
        return JSONResponse(content={"message":"The category does not exist"}, status_code=status.HTTP_404_NOT_FOUND)
    
    category.title = update.title
    
    
    db.commit()
    db.refresh(category)
        
    return JSONResponse(content={"message":f"the category {category.title} has been updated"},status_code=status.HTTP_202_ACCEPTED)
        
          