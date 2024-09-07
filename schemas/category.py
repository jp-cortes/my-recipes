from pydantic import BaseModel, Field


class Category(BaseModel):
    title: str = Field(min_length=5)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Vegetarian"
            }
        }