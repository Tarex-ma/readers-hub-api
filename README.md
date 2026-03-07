# 📚 Readers Hub API

![Django](https://img.shields.io/badge/Django-REST%20Framework-green)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Deployment](https://img.shields.io/badge/Deployment-Render-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

Readers Hub API is a **RESTful backend service** for a book review and recommendation platform.
It allows users to browse books, write reviews, like reviews, manage reading lists, and receive book recommendations.

---

# 🚀 Live Deployment

Base API URL

https://readers-hub-api.onrender.com

Swagger API Documentation

https://readers-hub-api.onrender.com/swagger/

Admin Panel

https://readers-hub-api.onrender.com/admin/

---

# ✨ Features

* JWT authentication
* Browse book catalog
* Write and manage book reviews
* Like reviews
* Personal reading lists
* Book recommendations
* Upload book cover images
* User activity tracking
* Pagination for large datasets

---

# 🛠 Tech Stack

Backend

* Python
* Django
* Django REST Framework

Database

* PostgreSQL

Authentication

* JSON Web Token (JWT)

Deployment

* Render

Documentation

* Swagger / OpenAPI

---

# 📡 API Endpoints

## Books

GET /api/v1/books/
GET /api/v1/books/{id}/

## Reviews

GET /api/v1/books/{book_id}/reviews/
POST /api/v1/books/{book_id}/reviews/

## Review Likes

POST /api/v1/reviews/{id}/like/

## Reading List

GET /api/v1/my-reading-list/
POST /api/v1/my-reading-list/

## User Reviews

GET /api/v1/users/{user_id}/reviews/

## Recommendations

GET /api/v1/recommendations/

---

# 🔐 Authentication

This API uses **JWT Authentication**.

Obtain token:

POST /api/token/

Example request body:

{
"username": "tarex",
"password": "tarex10"
}

Use the token in headers:

Authorization: Bearer your_token_here

---

# 📖 API Documentation

Interactive documentation is available via Swagger UI.

https://readers-hub-api.onrender.com/swagger/

Example Swagger Interface:

![Swagger Screenshot](docs/swagger.png)

---

# 📂 Project Structure

readers-hub-api

books/
users/
activities/
manage.py
requirements.txt
README.md
docs/

---

# ⚙️ Local Development Setup

Clone the repository

git clone https://github.com/Tarex-ma/readers-hub-api.git

Navigate into the project

cd readers-hub-api

Create virtual environment

python -m venv venv

Activate environment

Windows

venv\Scripts\activate

Mac / Linux

source venv/bin/activate

Install dependencies

pip install -r requirements.txt

Run migrations

python manage.py migrate

Create superuser

python manage.py createsuperuser

Start development server

python manage.py runserver

---

# 📊 System Architecture

Client Application (React / Frontend)

↓

Django REST API

↓

PostgreSQL Database

---

# 👨‍💻 Author

Tariku

Backend Developer

GitHub
https://github.com/Tarex-ma
