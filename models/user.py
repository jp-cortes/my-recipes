from config.database import Base
from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key= True, autoincrement= True, unique= True, nullable= False)
    name = Column(String, unique= True)
    email= Column(String, nullable= False, unique= True)
    password = Column(String, nullable= False)

    role = Column(String, nullable=False)
