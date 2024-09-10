



# My Recipes API

  

My Recipes API is a FastAPI project designed to manage a collection of recipes, where users can add, update, and retrieve recipes, including details like ingredients, preparation steps, and categories.

# Features

  

* User Management: Allows users to register, with the first user automatically assigned the role of admin.

* Recipe Management:

* Create, update, delete, and retrieve recipes.

* Associate recipes with specific categories (e.g., vegetarian, desserts).

* Categories can be created dynamically.

* Security: Password hashing for user security.

* Validation: Data validation using Pydantic models.

  

# Installation

# Requirements

  

* Python 3.9 or above

* FastAPI

* Uvicorn

* SQLAlchemy

* Pydantic

*  SQLite

  

# Setup

  

1. Clone the repository:

  

	```bash
  

	git clone https://github.com/jp-cortes/my-recipes-api.git


	cd my-recipes-api
	```
  

2. Create a virtual environment:

  

```bash

python -m venv env

source env/bin/activate # On Windows: `env\Scripts\activate` 
```

  

3. Install the dependencies:

  

```bash  

pip install -r requirements.txt
```

  

4. Set up your database:

  

Modify the DATABASE_URL in config.py to match your database connection string.

Run database migrations if applicable.

  

5. Start the server:

  

```bash

uvicorn main:app --reload  

The API will be available at http://127.0.0.1:8000. 
```

  

# Endpoints

## User Endpoints

  

* POST `/register`: Create a new user.

* Admin role is assigned to the first user.

  

# Recipe Endpoints

  

* POST `/recipe/`: Create a new recipe.

* PUT `/recipe/{id}`: Update an existing recipe by ID.

* GET `/recipes/`: Retrieve all recipes.

* GET `/recipes/category/{id}`: Retrieve recipes by category ID.

* GET `/recipe/{id}`: Retrieve a single recipe by ID.

* DELETE `/recipe/{id}`: Delete a recipe by ID.

  

# Example Request (Add Recipe)

  

```json  

{

"title": "Greek Salad",

"images": ["salad_01.png", "salad_02.png", "salad_03.png"],

"ingredients": ["tomato", "cucumber", "feta", "olive oil"],

"preparation": "Mix all ingredients and add olive oil.",

"category_id": 1

}
```

  

# Data Models

## User

  

```json

{

"name": "John Doe",

"email": "johndoe@example.com",

"password": "your-password",

"role": "user" # Auto-assigned as "admin" for the first user

}
```

  

# Recipe

  

```json
 {

"title": "Salad",

"images": ["salad_01.png", "salad_02.png", "salad_03.png"],

"ingredients": ["tomato", "lettuce", "olive oil"],

"preparation": "Chop ingredients, mix, and add olive oil",

"category": "Vegetarian",

"category_id": 1

}
```

  

# Project Structure
  

```bash

my-recipes-api/

├── app/

│ ├── main.py # FastAPI application setup

│ ├── models.py # SQLAlchemy models (User, Recipe, Category)

│ ├── schemas.py # Pydantic models (CreateUser, CreateRecipe)

│ ├── database.py # Database connection and setup

│ ├── middlewares/ # Custom middleware (error handling, etc.)

├── migrations/ # Database migrations

├── tests/ # Unit tests

├── README.md # This file

└── requirements.txt # Python dependencies

```