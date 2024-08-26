from fastapi import FastAPI, Body, Path, Query
from pydantic import BaseModel, Field, PrivateAttr
from typing import Optional

class Recipe(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5)
    ingredients: list = Field(min_length=5)
    preparation: str = Field(min_length=15)
    category: str = Field(min_length=5)
    category_id: int = Field(ge=1, Le=100)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 0,
                "title": "Salad",
                "ingredients": ["tomato"],
                "preparation": "Cut in brunoise",
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

# endpoint for all recipes
@app.get('/all', tags = ['recipes'])
def get_recepies():
    return recipes

@app.get('/recipe/{id}', tags = ['recipe'])
def get_recipes(id: int = Path(ge=1, Le=2000)):
    recipe = [item for item in recipes if item["id"] == id]
    if recipe:
        return recipe
    else:
        return "The recipe does not exist"

@app.get('/recipes/', tags=['recipes'])
def get_recipes_by_category(category: str = Query(min_length=5)):
    recipes_by_category = [items for items in recipes if items["category"] == category]
    if recipes_by_category:
        return recipes_by_category
    else:
        return f"The category {category} does not exist"

@app.post('/recipes', tags=['recipes'])
def create_recipe(recipe: Recipe):
    recipes.append(recipe)
    return recipes

@app.put('/recipe/{id}', tags = ['recipe'])
def update_recipe(id: int, recipe: Recipe):

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
            return recipes
        else:
            return "The recipe does not exist"
        
    

@app.delete('/recipe/{id}', tags = ['recipe'])
def del_recipe(id: int = Path(ge=1, Le=2000)):
    for item in recipes:
        if item["id"] == id:
            deleted = item["title"]
            recipes.remove(item)
            return f"the recipe {deleted} has been deleted"
        else:
            return "The recipe does not exist"
    