# FastAPI E-Commerce Learning Project

This project is a learning exercise for a web development course, focusing on building a backend for a simplified e-commerce system using **FastAPI** and **SQLAlchemy**.

The application covers many core backend concepts such as:

- Building RESTful APIs with FastAPI  
- Database modeling with SQLAlchemy (SQLite)  
- Authentication & authorization  
- Middleware usage  
- Custom exception handling  
- Modular code structure with routers  
- Role-based access control (e.g. Admin routes)

## 🧪 Features Implemented

- User registration and login with salted + hashed passwords  
- Role-based access (admin/customer)  
- Category creation, modification, deletion  
- Product listing and filtering by category with pagination  
- Cart operations: add, edit, delete, list  
- Placing and managing orders (customer + admin side)  
- Logging HTTP requests with middleware  
- Custom exception handlers for better error responses

## 🛠 Tech Stack

- Python 3.10+  
- FastAPI  
- SQLAlchemy  
- SQLite (for simplicity and learning)  
- Starlette (FastAPI’s underlying ASGI framework)

## 🧠 Learning Topics Covered

- FastAPI core concepts  
- REST principles  
- Relational DB design  
- Dependency injection  
- Exception handling  
- Role-based access control  
- Authentication & tokens  
- MVC-style project organization

## 🚀 Getting Started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

3. Open in browser:
   ```text
   http://127.0.0.1:8000/docs
   ```

## 👨‍🏫 Course Reference

This is part of a broader full stack web development course covering both backend and frontend technologies, using real-world examples to practice common features of modern web applications.

---

**Note:** This backend is educational and not production-grade. Security features and input validations are simplified for learning purposes.
