from config.database import Base
from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship

class Recipe(Base):

    __tablename__ = "recipes"

    id = Column(Integer, primary_key= True, autoincrement= True, unique= True, nullable= False)
    title = Column(String, unique= True)
    ingredients = Column(JSON)
    preparation = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"))
    
    category = relationship("Category", back_populates="recipes")


class Category(Base):

    __tablename__ = "categories"

    id = Column(Integer, primary_key= True, autoincrement= True, unique= True, nullable= False)
    title = Column(String, unique= True)

    recipes = relationship("Recipe", back_populates="category")