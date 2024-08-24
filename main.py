from fastapi import FastAPI, Body

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
def get_recipes(id: int):
    recipe = [item for item in recipes if item["id"] == id]
    return recipe

@app.get('/recipes/', tags=['recipes'])
def get_recipes_by_category(category: str):
    recipes_by_category = [items for items in recipes if items["category"] == category]
    return recipes_by_category

@app.post('/recipes', tags=['recipes'])
def create_recipe(id: int = Body(), title: str = Body(), ingredients: list = Body(), preparation: str = Body(), category: str = Body(), category_id: int = Body()):
    recipes.append({
        "id": id,
        "title": title,
        "ingredients": ingredients,
        "preparation": preparation,
        "category": category,
        "category_id": category_id
    })
    return recipes

@app.put('/recipe/{id}', tags = ['recipe'])
def update_recipe(id: int, title: str = Body(), ingredients: list = Body(), preparation: str = Body(), category: str = Body(), category_id: int = Body()):

    # recipe = [item for item in recipes if item["id"] == id]
    # if recipe_keys in recipe[0].keys():
    #     recipe[0].update({recipe_keys:change})

    for item in recipes:
        if item["id"] == id:
            item.update({
            "title": title,
            "ingredients": ingredients,
            "preparation": preparation,
            "category": category,
            "category_id": category_id
            })
        else:
            return "The recipe does not exist"

           
    return recipes

@app.delete('/recipe/{id}', tags = ['recipe'])
def del_recipe(id: int):
    for item in recipes:
        if item["id"] == id:
            deleted = item["title"]
            recipes.remove(item)
    
    return f"the recipe {deleted} has been deleted"