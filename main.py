from fastapi import FastAPI

recipes = [
    {"id": 1,
     "title": "bulgarian salad",
     "ingredients": ["Tomato","cucumber","grounded white cheese", "smoked pepper", "olive oil", "apple cider vinnegar", "salt", "black pepper"],
     "preparation":"chop the tomatoe, cucumber and the smoked pepper in dices not bigger than 1cm. In a bowl mix the olive oil, vinnegar, salt and back pepper, to make a vinnagrette. Mix all the ingredients and put the cheese on top."
     },

     {"id": 2,
     "title": "bulgarian salad",
     "ingredients": ["Tomato","cucumber","grounded white cheese", "smoked pepper", "olive oil", "apple cider vinnegar", "salt", "black pepper"],
     "preparation":"chop the tomatoe, cucumber and the smoked pepper in dices not bigger than 1cm. In a bowl mix the olive oil, vinnegar, salt and back pepper, to make a vinnagrette. Mix all the ingredients and put the cheese on top."
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

@app.get('/recipe{id}', tags = ['recipe'])
def get_recepies(id: int):
    return id
