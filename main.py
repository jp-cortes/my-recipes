from fastapi import FastAPI
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler

from routers.category import category_router
from routers.recipe import recipe_router
from routers.user import user_router


app = FastAPI()
app.title = "My recipes"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)
app.include_router(recipe_router)
app.include_router(user_router)
app.include_router(category_router)

Base.metadata.create_all(bind=engine)



sample_recipes = [
    {"id": 1,
     "title": "bulgarian salad",
     "ingredients": ["Tomato","cucumber","grounded white cheese", "smoked pepper", "olive oil", "apple cider vinnegar", "salt", "black pepper"],
     "preparation":"chop the tomatoe, cucumber and the smoked pepper in dices not bigger than 1cm. In a bowl mix the olive oil, vinnegar, salt and back pepper, to make a vinnagrette. Mix all the ingredients and put the cheese on top.",
     "category_id": 1,
     },

     {"id": 2,
     "title": "tarator",
     "ingredients": ["plane yogurt","cucumber", "dill", "fresh garlic", "chopped nuts", "salt", "black pepper"],
     "preparation":"chop the cucumber, garlic and dill. Mix all the ingredients and mixed with the yougurt. keep in the  fridge for 30 prior to serve on the table",
     "category_id": 1,
     },
]


# endpoint home
@app.get('/', tags = ['home'])
def message():
    return "Welcome to my recipes"


