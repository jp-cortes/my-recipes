from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    email: EmailStr = Field(description="A valid email is required")
    password: str= Field(min_length=8, max_length=50, description="The password must be between 8 and 50 characters")
    

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@mail.com",
                "password": "V@lidPassword123!"
            }
        }


class CreateUser(BaseModel):
    name: str = Field(min_length=2, max_length=50, description="The name must be between 2 and 50 characters")
    email: EmailStr = Field(description="A valid email is required")
    password: str= Field(min_length=8, max_length=50, description="The password must be between 8 and 50 characters")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "user@mail.com",
                "password": "V@lidPassword123!"
            }
        }