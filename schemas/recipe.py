from pydantic import BaseModel, Field

class Recipe(BaseModel):
    title: str = Field(min_length=5)
    images: list = Field(min_length=1)
    ingredients: list = Field(min_length=3)
    preparation: str = Field(min_length=15)
    category_id: int = Field(ge=1, Le=100)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "bulgarian salad",
                "images": ["salad_01.png", "salad_02.png", "salad_03.png"],
                "ingredients": ["Tomato","cucumber","grounded white cheese", "smoked pepper", "olive oil", "apple cider vinnegar", "salt", "black pepper"],
                "preparation": "chop the tomatoes, cucumber and the smoked pepper in dices not bigger than 1cm. In a bowl mix the olive oil, vinnegar, salt and back pepper, to make a vinnagrette. Mix all the ingredients and put the cheese on top.",
                "category_id": 1
            }
        }