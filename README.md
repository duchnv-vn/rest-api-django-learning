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
- `app/ingredient/` : Ingredient related codes

### APIs:

1. `Users`:

- Manage user GET - /api/user/me
- Create user: POST - /api/user/create
- Get token POST - /api/user/token
- Update user PATCH PUT - /api/user/me

2. `Recipes`:

- List recipe: GET - /api/recipe
- View detail recipe: GET - /api/recipe/:id
- Create recipe: POST - /api/recipe
- Update recipe: PATCH PUT - /api/recipe/:id
- Delete recipe: DELETE - /api/recipe/:recipe_id

3. `Tags`:

- List available tags: GET - /api/tags
- Update tags: PUT PATCH - /api/tags/:tag_id
- Delete a tag: DELETE - /api/tags/:tag_id

4. `Ingredients`:

- List available ingredients: GET - /api/ingredients
- Ingredient detail: GET - /api/ingredients/:tag_id
- Update a ingredient: PUT PATCH - /api/ingredients/:tag_id
- Delete a ingredient: DELETE - /api/ingredients/:tag_id

### Models:

1. `Users`:

- email: varchar255
- password: varchar255
- name: varchar255
- is_active: boolean
- is_staff: boolean

2. `Recipes`:

- id: int
- user: User
- title: varchar255
- description: text
- time_minutes: int
- price: decimal(5,2)
- link: varchar255

3. `Tags`

- name: varchar255
- user: User

4. `Ingredients`

- name: varchar255
- user: User
