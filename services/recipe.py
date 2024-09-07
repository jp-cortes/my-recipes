from models.recipe import Recipe as RecipeModel
from schemas.recipe import Recipe



class RecipeService():
    def __init__(self, db) -> None:
        self.db = db

    def get_recipes(self):
        result = self.db.query(RecipeModel).all()
        return result
    
    def get_one(self, id: int):
        result = self.db.query(RecipeModel).filter(RecipeModel.id == id).first()
        return result
    
    def check_recipe(self, title):
        result = self.db.query(RecipeModel).filter(RecipeModel.title == title).first()
        return result
    
    def get_by_Category_id(self, id: int):
        result = self.db.query(RecipeModel).filter(RecipeModel.category_id == id).all()
        return result
    
    def create_recipe(self, recipe: Recipe):
        newRecipe = RecipeModel(**recipe.model_dump())
        self.db.add(newRecipe)
        self.db.commit() 
        return


    def update_recipe(self, id: int, update: Recipe):
        recipe = self.db.query(RecipeModel).filter(RecipeModel.id == id).first()
        recipe.title = update.title
        recipe.ingredients = update.ingredients
        recipe.preparation = update.preparation
        recipe.category_id = update.category_id
        
        self.db.commit()
        self.db.refresh(recipe)
        return
    
    def delete_recipe(self, recipe):
        self.db.delete(recipe)
        self.db.commit()
        return
    

    '''def get_by_Category_name(self, category):
        result = self.db.query(RecipeModel).filter(RecipeModel.category == category).all()
        return result'''