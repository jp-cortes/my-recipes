from config.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Category(Base):

    __tablename__ = "categories"

    id = Column(Integer, primary_key= True, autoincrement= True, unique= True, nullable= False)
    title = Column(String, unique= True)

    recipes = relationship("Recipe", back_populates="category")
