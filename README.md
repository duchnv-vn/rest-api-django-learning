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
