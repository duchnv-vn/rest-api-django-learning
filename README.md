# Recipe API document

## Introduction

1. 19 endpoints:

2. Features:

- User authentication
- Manage: users, recipes, tags, ingredients
- Browserable API (Swagger)
- Browserable admin interface (Django Admin)

3. Technologies:

- Programming language: Python
- Web framework: Django
- REST API: Django REST
- Database: PostpreSQL
- Containerization: Docker
- CI/CD: Github Actions

## Project structure

### App

- `app/` : Django project
- `app/core/` : Codes shared between multiple apps
- `app/user/` : User related codes
- `app/recipe/` : Recipe related codes

### Features:

1. User:

- Create user: POST - /api/user/create
- Get token POST - /api/user/token
- Manage user GET - /api/user/me
- Update user PATCH PUT - /api/user/me

2. Recipe:

- Create recipe: POST - /api/recipes
- List recipe: GET - /api/recipes
- View detail recipe: GET - /api/recipes/:id
- Update recipe: PATCH PUT - /api/recipes/:id
- Delete recipe: DELETE - /api/recipes/:id
