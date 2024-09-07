from models.category import Category as CategoryModel
from schemas.category import Category

class CategoryService():
    def __init__(self, db) -> None:
        self.db = db

    def get_categories(self):
        result = self.db.query(CategoryModel).all()
        return result
    
    def get_category_by_title(self, title):
        result = self.db.query(CategoryModel).filter(CategoryModel.title == title).first()
        return result
    
    def get_category_by_id(self, id):
        result = self.db.query(CategoryModel).filter(CategoryModel.id == id).first()
        return result
    
    def create_category(self, category: Category):
        newCategory = CategoryModel(**category.model_dump())
        self.db.add(newCategory)
        self.db.commit()
        return 
    
    def update_category(self, category, update: Category):
        category.title = update.title
        self.db.commit()
        self.db.refresh(category)
        return 