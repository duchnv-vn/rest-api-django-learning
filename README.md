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

### Apps:

- `app/` : Django project
- `app/core/` : Codes shared between multiple apps
- `app/user/` : User related codes
- `app/recipe/` : Recipe related codes
- `app/tag/` : Tag related codes

### APIs:

1. User:

- Create user: POST - /api/user/create
- Get token POST - /api/user/token
- Manage user GET - /api/user/me
- Update user PATCH PUT - /api/user/me

2. Recipe:

- Create recipe: POST - /api/recipe/recipe
- List recipe: GET - /api/recipe/recipe
- View detail recipe: GET - /api/recipe/recipe/:id
- Update recipe: PATCH PUT - /api/recipe/recipe/:id
- Delete recipe: DELETE - /api/recipe/recipe/:id

3. Tag:

- Create a tag: POST - /api/recipe/tags
- Update tags: PUT PATCH - /api/recipe/tags
- Delete a tag: DELETE - /api/recipe/tags
- List available tags: GET - /api/recipe/tags

### Models:

1. User:

- email: varchar255
- password: varchar255
- name: varchar255
- is_active: boolean
- is_staff: boolean

2. Recipe:

- id: int
- user: User
- title: varchar255
- description: text
- time_minutes: int
- price: decimal(5,2)
- link: varchar255

3. Tag

- name: varchar255
- user: User
