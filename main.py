from fastapi import FastAPI

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
def get_recepies(id: int):
    recipe = [recipe for recipe in recipes if recipe["id"] == id]
    return recipe

@app.get('/recipes/', tags=['recipes'])
def get_recipes_by_category(category: str):
    recipes_by_category = [recipe for recipe in recipes if recipe["category"] == category]
    return recipes_by_category