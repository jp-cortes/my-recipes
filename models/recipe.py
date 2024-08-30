from config.database import Base
from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship

class Recipe(Base):

    __tablename__ = "recipes"

    id = Column(Integer, primary_key= True, autoincrement= True)
    title = Column(str)
    ingredients = Column(String)
    preparation = Column(String)
    category_id = Column(Integer, ForeignKey= "categories.id")
    
    category = relationship("Category", back_populates="belong_to")


class Category(Base):

    __tablename__ = "categories"

    id = Column(Integer, primary_key= True, autoincrement= True)
    title = Column(str)

    belong_to = relationship("Recipe", back_populates="category")